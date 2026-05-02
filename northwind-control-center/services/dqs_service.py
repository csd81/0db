"""
dqs_service.py — Python Data Quality Services.

Three checks:
  1. Levenshtein duplicate detection (python-Levenshtein)
  2. Heuristic 3NF transitive-dependency detection
  3. Null statistics per column
"""

import Levenshtein
import db_adapter


def get_null_stats(conn_id: int, table: str) -> list[dict]:
    cols, rows = db_adapter.adapter_select(conn_id, f"SELECT * FROM [{table}] LIMIT 5000")
    if not rows:
        return []
    total = len(rows)
    result = []
    for i, col in enumerate(cols):
        null_count = sum(1 for r in rows if r[i] is None or r[i] == '')
        result.append({
            'col': col,
            'null_count': null_count,
            'total': total,
            'null_pct': round(null_count / total * 100, 1) if total else 0,
        })
    return result


def scan_duplicates_levenshtein(conn_id: int, table: str,
                                col: str, threshold: int = 2) -> tuple[list[dict], str | None]:
    """
    Pairwise Levenshtein scan on a text column.
    Returns (pairs, warning) — warning is set if row count > 5000 (sample used).
    """
    try:
        _, count_rows = db_adapter.adapter_select(
            conn_id, f"SELECT COUNT(*) FROM [{table}]"
        )
        total = count_rows[0][0] if count_rows else 0
    except Exception as e:
        return [], str(e)

    warning = None
    limit = 5000
    if total > limit:
        warning = f"Table has {total} rows; scan limited to first {limit} for performance."

    try:
        cols, rows = db_adapter.adapter_select(
            conn_id, f"SELECT rowid, [{col}] FROM [{table}] LIMIT {limit}"
        )
    except Exception as e:
        return [], str(e)

    pairs = []
    data = [(r[0], str(r[1])) for r in rows if r[1] is not None]
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            dist = Levenshtein.distance(data[i][1], data[j][1])
            if 0 < dist <= threshold:
                pairs.append({
                    'row_id_a': data[i][0],
                    'val_a': data[i][1],
                    'row_id_b': data[j][0],
                    'val_b': data[j][1],
                    'distance': dist,
                })
    pairs.sort(key=lambda x: x['distance'])
    return pairs, warning


def check_3nf_violations(conn_id: int, table: str) -> list[dict]:
    """
    Heuristic: for each ordered pair of non-PK columns (A, B), if every distinct
    value of A maps to exactly one value of B, flag as a possible transitive dependency.
    """
    try:
        cols, rows = db_adapter.adapter_select(
            conn_id, f"SELECT * FROM [{table}] LIMIT 3000"
        )
    except Exception as e:
        return []

    if not rows or len(cols) < 2:
        return []

    violations = []
    for i, col_a in enumerate(cols):
        for j, col_b in enumerate(cols):
            if i == j:
                continue
            mapping: dict = {}
            consistent = True
            for row in rows:
                va, vb = row[i], row[j]
                if va is None:
                    continue
                if va not in mapping:
                    mapping[va] = vb
                elif mapping[va] != vb:
                    consistent = False
                    break
            if consistent and len(mapping) > 1:
                example = list(mapping.items())[:3]
                violations.append({
                    'col_a': col_a,
                    'col_b': col_b,
                    'distinct_a': len(mapping),
                    'confidence': 1.0,
                    'examples': [{'a': k, 'b': v} for k, v in example],
                })
    return violations


def run_full_dqs_report(conn_id: int, table: str,
                        text_col: str | None = None,
                        levenshtein_threshold: int = 2) -> dict:
    null_stats = get_null_stats(conn_id, table)
    violations = check_3nf_violations(conn_id, table)
    duplicates, dup_warning = [], None
    if text_col:
        duplicates, dup_warning = scan_duplicates_levenshtein(
            conn_id, table, text_col, levenshtein_threshold
        )
    return {
        'table': table,
        'null_stats': null_stats,
        'violations': violations,
        'duplicates': duplicates,
        'dup_warning': dup_warning,
        'text_col': text_col,
    }
