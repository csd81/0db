"""
pgvector_service.py — Semantic similarity search demo using pgvector + TF-IDF embeddings.
Requires: PostgreSQL with pgvector extension; pip install pgvector scikit-learn numpy
"""
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
import meta_db
import db_adapter

VECTOR_DIM = 64

# Module-level model cache (fitted during import_products)
_vectorizer: TfidfVectorizer | None = None
_svd: TruncatedSVD | None = None
_fitted_texts: list[str] = []


def ensure_pgvector(conn_id: int) -> str | None:
    """
    Enable the pgvector extension on the target PostgreSQL database.
    Returns None on success, or an error string on failure.
    """
    try:
        conn = db_adapter.get_adapter_connection(conn_id)
        rec = meta_db.get_connection_by_id(conn_id)
        if not rec or rec['db_type'] != 'postgresql':
            return "Connection is not a PostgreSQL connection."
        # psycopg2 connections from get_adapter_connection already have autocommit=True
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        return None
    except Exception as e:
        return str(e)


def setup_embeddings_table(conn_id: int) -> str | None:
    """
    Create the product_embeddings table (vector(64)) if it does not exist.
    Returns None on success, or an error string on failure.
    """
    try:
        conn = db_adapter.get_adapter_connection(conn_id)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS product_embeddings (
                    product_id   INT  PRIMARY KEY,
                    product_name TEXT,
                    category     TEXT,
                    unit_price   REAL,
                    embedding    vector(64)
                )
            """)
        return None
    except Exception as e:
        return str(e)


def _make_texts(names, categories, descriptions) -> list[str]:
    """Combine name + category + description into a single searchable string."""
    return [f"{n} {c} {d}" for n, c, d in zip(names, categories, descriptions)]


def _fit_and_embed(texts: list[str]) -> np.ndarray:
    """
    Fit TF-IDF + TruncatedSVD on *texts*, update module-level model cache,
    and return a (n, VECTOR_DIM) array of L2-normalised vectors.
    """
    global _vectorizer, _svd, _fitted_texts

    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(texts)

    # n_components must be < n_features
    n_components = min(VECTOR_DIM, tfidf_matrix.shape[1] - 1)
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    reduced = svd.fit_transform(tfidf_matrix)

    # Zero-pad to VECTOR_DIM if SVD produced fewer components
    # (SVD output is limited by min(n_samples, n_features, n_components))
    actual_dims = reduced.shape[1]
    if actual_dims < VECTOR_DIM:
        padding = np.zeros((reduced.shape[0], VECTOR_DIM - actual_dims))
        reduced = np.hstack([reduced, padding])

    normed = normalize(reduced, norm="l2")

    _vectorizer = vectorizer
    _svd = svd
    _fitted_texts = list(texts)

    return normed  # shape (n, VECTOR_DIM)


def _embed_query(text: str) -> np.ndarray | None:
    """
    Embed a single query string using the fitted vectorizer + SVD.
    Returns a (VECTOR_DIM,) ndarray, or None if the model is not yet fitted.
    """
    if _vectorizer is None or _svd is None:
        return None

    tfidf_vec = _vectorizer.transform([text])
    reduced = _svd.transform(tfidf_vec)

    # Zero-pad if necessary
    if reduced.shape[1] < VECTOR_DIM:
        padding = np.zeros((1, VECTOR_DIM - reduced.shape[1]))
        reduced = np.hstack([reduced, padding])

    normed = normalize(reduced, norm="l2")
    return normed[0]  # shape (VECTOR_DIM,)


def import_products(conn_id: int, source_conn_id: int) -> tuple[int, str | None]:
    """
    Read Products + Categories from *source_conn_id*, generate 64-dim TF-IDF
    embeddings, and upsert them into product_embeddings on *conn_id*.

    Tries MSSQL/MySQL column capitalisation first; falls back to PostgreSQL lowercase.
    Returns (count, None) on success or (0, error_string) on failure.
    """
    try:
        src_rec = meta_db.get_connection_by_id(source_conn_id)
        src_type = src_rec['db_type'] if src_rec else ''

        columns, rows = [], []
        last_err = None

        # Try PostgreSQL lowercase schema first if source is postgresql, else MSSQL style
        if src_type == 'postgresql':
            queries = [
                # lowercase (standard Northwind on Postgres)
                "SELECT p.product_id, p.product_name, c.category_name,"
                " COALESCE(c.description, '') AS desc, p.unit_price"
                " FROM products p"
                " JOIN categories c ON p.category_id = c.category_id",
                # quoted capitalised variant (some Postgres Northwind imports)
                'SELECT p."ProductID", p."ProductName", c."CategoryName",'
                ' COALESCE(c."Description", \'\') AS "Desc", p."UnitPrice"'
                ' FROM "Products" p'
                ' JOIN "Categories" c ON p."CategoryID" = c."CategoryID"',
            ]
        else:
            queries = [
                # MSSQL / MySQL capitalised
                """SELECT p.ProductID, p.ProductName, c.CategoryName,
                          ISNULL(c.Description,'') AS Desc, p.UnitPrice
                   FROM Products p
                   JOIN Categories c ON p.CategoryID = c.CategoryID""",
            ]

        for sql in queries:
            try:
                columns, rows = db_adapter.adapter_select(source_conn_id, sql)
                if rows:
                    break
            except Exception as e:
                last_err = str(e)

        if not rows:
            return 0, last_err or "No products found in source connection."

        col_lower = [c.lower() for c in columns]

        def _idx(candidates):
            for name in candidates:
                if name in col_lower:
                    return col_lower.index(name)
            raise ValueError(f"Column not found: {candidates}")

        idx_id    = _idx(['productid', 'product_id'])
        idx_name  = _idx(['productname', 'product_name'])
        idx_cat   = _idx(['categoryname', 'category_name'])
        idx_desc  = _idx(['desc', 'description'])
        idx_price = _idx(['unitprice', 'unit_price'])

        product_ids   = [r[idx_id]    for r in rows]
        product_names = [r[idx_name]  for r in rows]
        categories    = [r[idx_cat]   for r in rows]
        descriptions  = [r[idx_desc] or '' for r in rows]
        unit_prices   = [r[idx_price] for r in rows]

        texts = _make_texts(product_names, categories, descriptions)
        embeddings = _fit_and_embed(texts)  # shape (n, VECTOR_DIM)

        conn = db_adapter.get_adapter_connection(conn_id)
        records = [
            (
                int(product_ids[i]),
                str(product_names[i]),
                str(categories[i]),
                float(unit_prices[i]) if unit_prices[i] is not None else None,
                str(embeddings[i].tolist()),   # "[0.1, 0.2, ...]"
            )
            for i in range(len(rows))
        ]

        with conn.cursor() as cur:
            cur.executemany(
                """INSERT INTO product_embeddings
                       (product_id, product_name, category, unit_price, embedding)
                   VALUES (%s, %s, %s, %s, %s::vector)
                   ON CONFLICT (product_id) DO UPDATE
                       SET embedding     = EXCLUDED.embedding,
                           product_name  = EXCLUDED.product_name,
                           category      = EXCLUDED.category,
                           unit_price    = EXCLUDED.unit_price""",
                records,
            )

        return len(records), None

    except Exception as e:
        return 0, str(e)


def similarity_search(
    conn_id: int, query_text: str, k: int = 10
) -> tuple[list, list, str | None]:
    """
    Embed *query_text* with the fitted model and return the *k* nearest products.
    Returns (columns, rows_as_lists, error).
    """
    query_vec = _embed_query(query_text)
    if query_vec is None:
        return [], [], "Import products first to fit the embedding model."

    try:
        conn = db_adapter.get_adapter_connection(conn_id)
        query_vec_str = str(query_vec.tolist())

        with conn.cursor() as cur:
            cur.execute(
                """SELECT product_id,
                          product_name,
                          category,
                          unit_price,
                          ROUND((1 - (embedding <=> %s::vector))::numeric, 4) AS similarity
                   FROM product_embeddings
                   ORDER BY embedding <=> %s::vector
                   LIMIT %s""",
                (query_vec_str, query_vec_str, k),
            )
            columns = [d[0] for d in cur.description]
            rows    = [list(r) for r in cur.fetchall()]

        return columns, rows, None

    except Exception as e:
        return [], [], str(e)


def sql_like_search(
    conn_id: int, source_conn_id: int, query_text: str
) -> tuple[list, list, str | None]:
    """
    Perform a SQL LIKE / ILIKE search on the source connection's Products table.
    Returns (columns, rows, error).
    """
    try:
        src_rec = meta_db.get_connection_by_id(source_conn_id)
        src_type = src_rec['db_type'] if src_rec else ''

        safe = query_text.replace("'", "''")

        if src_type == 'postgresql':
            sql = f"""
                SELECT p."ProductID", p."ProductName", c."CategoryName", p."UnitPrice"
                FROM "Products" p
                JOIN "Categories" c ON p."CategoryID" = c."CategoryID"
                WHERE p."ProductName" ILIKE '%{safe}%'
                   OR c."CategoryName" ILIKE '%{safe}%'
                ORDER BY p."ProductName"
            """
        else:
            sql = f"""
                SELECT p.ProductID, p.ProductName, c.CategoryName, p.UnitPrice
                FROM Products p
                JOIN Categories c ON p.CategoryID = c.CategoryID
                WHERE p.ProductName LIKE '%{safe}%'
                   OR c.CategoryName LIKE '%{safe}%'
                ORDER BY p.ProductName
            """

        # For PostgreSQL source with lowercase schema, fall back gracefully
        try:
            columns, rows = db_adapter.adapter_select(source_conn_id, sql)
        except Exception:
            if src_type == 'postgresql':
                sql_lc = f"""
                    SELECT p.product_id, p.product_name, c.category_name, p.unit_price
                    FROM products p
                    JOIN categories c ON p.category_id = c.category_id
                    WHERE p.product_name ILIKE '%{safe}%'
                       OR c.category_name ILIKE '%{safe}%'
                    ORDER BY p.product_name
                """
                columns, rows = db_adapter.adapter_select(source_conn_id, sql_lc)
            else:
                raise

        return columns, rows, None

    except Exception as e:
        return [], [], str(e)


def get_stats(conn_id: int) -> dict:
    """
    Return a stats dict: {'count': int, 'has_extension': bool, 'model_fitted': bool, 'error': str|None}
    """
    try:
        conn = db_adapter.get_adapter_connection(conn_id)
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
            has_ext = cur.fetchone() is not None

            count = 0
            try:
                cur.execute("SELECT COUNT(*) FROM product_embeddings")
                row = cur.fetchone()
                count = int(row[0]) if row else 0
            except Exception:
                pass

        return {
            'count':       count,
            'has_extension': has_ext,
            'model_fitted':  _vectorizer is not None and _svd is not None,
            'error':       None,
        }
    except Exception as e:
        return {
            'count':       0,
            'has_extension': False,
            'model_fitted':  _vectorizer is not None and _svd is not None,
            'error':       str(e),
        }
