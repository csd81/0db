"""
neo4j_service.py — Cypher query execution and schema introspection for Neo4j connections.
"""

import meta_db
import db_adapter

_BUILT_IN_QUERIES = [
    {
        'key': 'friends_of_john',
        'label': "John's friends",
        'description': 'Direct friends of john (one hop)',
        'cypher': (
            "MATCH (p1:Person {name: 'john'})-[:FRIEND_OF]->(p2:Person) "
            "RETURN p2.name AS friend"
        ),
    },
    {
        'key': 'john_likes',
        'label': "Restaurants john likes",
        'description': 'Restaurants that john has rated',
        'cypher': (
            "MATCH (:Person {name: 'john'})-[l:LIKES]->(r:Restaurant) "
            "RETURN r.name AS restaurant, l.rating AS rating"
        ),
    },
    {
        'key': 'friends_liked_restaurants',
        'label': "Restaurants liked by john's friends",
        'description': "Two-hop: john → friend → restaurant",
        'cypher': (
            "MATCH (:Person {name: 'john'})-[:FRIEND_OF]->(p2:Person)-[l:LIKES]->(r:Restaurant) "
            "RETURN p2.name AS friend, r.name AS restaurant, l.rating AS rating"
        ),
    },
    {
        'key': 'locals_like_local',
        'label': 'People who like a local restaurant',
        'description': 'Persons who like a restaurant located in the same city they live in',
        'cypher': (
            "MATCH (p:Person)-[:LIKES]->(r:Restaurant)-[:LOCATED_IN]->(c:City), "
            "(p)-[:LIVES_IN]->(c) "
            "RETURN p.name AS person, r.name AS restaurant, c.name AS city"
        ),
    },
    {
        'key': 'friends_local_taste',
        'label': "Friends with local taste",
        'description': "Persons whose friend likes a restaurant in the friend's own city",
        'cypher': (
            "MATCH (p1:Person)-[:FRIEND_OF]->(p2:Person)-[:LIKES]->(r:Restaurant)"
            "-[:LOCATED_IN]->(c:City), (p2)-[:LIVES_IN]->(c) "
            "RETURN DISTINCT p1.name AS person, p2.name AS friend, "
            "r.name AS restaurant, c.name AS city"
        ),
    },
    {
        'key': 'common_friends',
        'label': 'Common friends',
        'description': 'Pairs of people who share a mutual friend',
        'cypher': (
            "MATCH (p1:Person)-[:FRIEND_OF]->(p0:Person)<-[:FRIEND_OF]-(p2:Person) "
            "WHERE p1.id <> p2.id AND p1.name < p2.name "
            "RETURN p0.name AS mutual_friend, p1.name AS person1, p2.name AS person2"
        ),
    },
    {
        'key': 'shortest_path_from_john',
        'label': 'Shortest paths from john',
        'description': 'All shortest friendship paths starting at john',
        'cypher': (
            "MATCH path = shortestPath((:Person {name:'john'})-[:FRIEND_OF*]->(p2:Person)) "
            "WHERE p2.name <> 'john' "
            "RETURN p2.name AS reaches, length(path) AS hops, "
            "[n IN nodes(path) | n.name] AS route"
        ),
    },
]


def built_in_queries() -> list[dict]:
    return _BUILT_IN_QUERIES


def run_cypher(conn_id: int, cypher: str, params: dict | None = None) -> tuple[list, list, str | None]:
    """Execute a Cypher query. Returns (columns, rows, error)."""
    try:
        driver = db_adapter.get_neo4j_driver(conn_id)
        with driver.session() as session:
            result = session.run(cypher, params or {})
            records = result.data()
            if not records:
                return [], [], None
            columns = list(records[0].keys())
            rows = [list(r.values()) for r in records]
            return columns, rows, None
    except Exception as e:
        return [], [], str(e)


def get_schema(conn_id: int) -> dict:
    """Return node labels and relationship types present in the database."""
    try:
        driver = db_adapter.get_neo4j_driver(conn_id)
        with driver.session() as session:
            labels = [r['label'] for r in session.run("CALL db.labels() YIELD label").data()]
            rel_types = [r['relationshipType'] for r in
                         session.run("CALL db.relationshipTypes() YIELD relationshipType").data()]
        return {'labels': labels, 'rel_types': rel_types, 'error': None}
    except Exception as e:
        return {'labels': [], 'rel_types': [], 'error': str(e)}
