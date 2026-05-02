"""
02_migrate_from_sql.py
ETL: reads the c8 social network graph from SQL Server and loads it into Neo4j.

Requirements:
    pip install pyodbc neo4j

Usage:
    python 02_migrate_from_sql.py
"""

import pyodbc
from neo4j import GraphDatabase

# ── Configuration ─────────────────────────────────────────────────────────────
SQL_CONN_STR = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=<your-server>,1433;"
    "DATABASE=northwind;"
    "UID=<user>;PWD=<password>;"
    "Encrypt=yes;TrustServerCertificate=yes;"
)

NEO4J_URI      = "bolt://localhost:7687"
NEO4J_USER     = "neo4j"
NEO4J_PASSWORD = "your-neo4j-password"


def main():
    sql = pyodbc.connect(SQL_CONN_STR)
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as neo:
        # Clear previous demo data
        neo.run("MATCH (n) DETACH DELETE n")

        # ── Nodes ──────────────────────────────────────────────────────────────
        for table, label in [('person', 'Person'), ('restaurant', 'Restaurant'), ('city', 'City')]:
            rows = sql.execute(f"SELECT id, name FROM {table}").fetchall()
            for row in rows:
                neo.run(f"CREATE (:{label} {{id: $id, name: $name}})",
                        id=row[0], name=row[1])
            print(f"Loaded {len(rows)} {label} nodes")

        # statename for City
        rows = sql.execute("SELECT id, statename FROM city").fetchall()
        for row in rows:
            neo.run("MATCH (c:City {id:$id}) SET c.state = $state", id=row[0], state=row[1])

        # ── LIKES edges ────────────────────────────────────────────────────────
        likes = sql.execute("""
            SELECT p.id AS person_id, r.id AS rest_id, l.rating
            FROM likes l
            JOIN person p ON p.$node_id = l.$from_id
            JOIN restaurant r ON r.$node_id = l.$to_id
        """).fetchall()
        for row in likes:
            neo.run(
                "MATCH (p:Person {id:$pid}), (r:Restaurant {id:$rid}) "
                "CREATE (p)-[:LIKES {rating:$rating}]->(r)",
                pid=row[0], rid=row[1], rating=row[2],
            )
        print(f"Loaded {len(likes)} LIKES edges")

        # ── LIVES_IN edges ─────────────────────────────────────────────────────
        livesin = sql.execute("""
            SELECT p.id, c.id
            FROM livesin l
            JOIN person p ON p.$node_id = l.$from_id
            JOIN city c ON c.$node_id = l.$to_id
        """).fetchall()
        for row in livesin:
            neo.run(
                "MATCH (p:Person {id:$pid}), (c:City {id:$cid}) "
                "CREATE (p)-[:LIVES_IN]->(c)",
                pid=row[0], cid=row[1],
            )
        print(f"Loaded {len(livesin)} LIVES_IN edges")

        # ── LOCATED_IN edges ───────────────────────────────────────────────────
        locatedin = sql.execute("""
            SELECT r.id, c.id
            FROM locatedin l
            JOIN restaurant r ON r.$node_id = l.$from_id
            JOIN city c ON c.$node_id = l.$to_id
        """).fetchall()
        for row in locatedin:
            neo.run(
                "MATCH (r:Restaurant {id:$rid}), (c:City {id:$cid}) "
                "CREATE (r)-[:LOCATED_IN]->(c)",
                rid=row[0], cid=row[1],
            )
        print(f"Loaded {len(locatedin)} LOCATED_IN edges")

        # ── FRIEND_OF edges ────────────────────────────────────────────────────
        friendof = sql.execute("""
            SELECT p1.id, p2.id
            FROM friendof f
            JOIN person p1 ON p1.$node_id = f.$from_id
            JOIN person p2 ON p2.$node_id = f.$to_id
        """).fetchall()
        for row in friendof:
            neo.run(
                "MATCH (p1:Person {id:$id1}), (p2:Person {id:$id2}) "
                "CREATE (p1)-[:FRIEND_OF]->(p2)",
                id1=row[0], id2=row[1],
            )
        print(f"Loaded {len(friendof)} FRIEND_OF edges")

    print("Migration complete.")
    sql.close()
    driver.close()


if __name__ == '__main__':
    main()
