# SQL Server Graph vs Neo4j Cypher — Side-by-Side Comparison

## Data Model

| Concept | SQL Server Graph | Neo4j / Cypher |
|---|---|---|
| Node table | `CREATE TABLE person (...) AS NODE` | Implicit — just create nodes with labels |
| Edge table | `CREATE TABLE likes (...) AS EDGE` | Implicit — relationships created inline |
| Node identity | `$node_id` (internal JSON) | Internal node id, accessed via `id(n)` |
| Edge identity | `$edge_id` (internal JSON) | Internal rel id, accessed via `id(r)` |
| Node properties | Regular columns | Key-value properties on the node |
| Edge properties | Regular columns | Key-value properties on the relationship |
| Labels / types | Table name is the node type | `:Person`, `:Restaurant` — multiple allowed |
| Relationship types | Edge table name | `:LIKES`, `:FRIEND_OF` — exactly one per rel |

## DDL

| Operation | SQL Server | Cypher |
|---|---|---|
| Create node type | `CREATE TABLE person (id INT PRIMARY KEY, name VARCHAR(100)) AS NODE` | _(no DDL needed — just CREATE)_ |
| Create edge type | `CREATE TABLE likes (rating INT) AS EDGE` | _(no DDL needed)_ |
| Add edge constraint | `ALTER TABLE friendof ADD CONSTRAINT ec_1 CONNECTION (person TO person)` | No direct equivalent (application logic or APOC constraints) |
| Create index | `CREATE INDEX ON person(name)` | `CREATE INDEX FOR (p:Person) ON (p.name)` |

## DML

| Operation | SQL Server | Cypher |
|---|---|---|
| Insert node | `INSERT INTO person VALUES (1, 'john')` | `CREATE (:Person {id:1, name:'john'})` |
| Insert edge | `INSERT INTO likes VALUES ((SELECT $node_id FROM person WHERE id=1), (SELECT $node_id FROM restaurant WHERE id=1), 9)` | `MATCH (p:Person {id:1}), (r:Restaurant {id:1}) CREATE (p)-[:LIKES {rating:9}]->(r)` |
| Update node | `UPDATE person SET name='johnny' WHERE id=1` | `MATCH (p:Person {id:1}) SET p.name='johnny'` |
| Delete node+edges | `DELETE FROM person WHERE id=1` _(must delete edges first)_ | `MATCH (p:Person {id:1}) DETACH DELETE p` |

## Pattern Matching

| Query | SQL Server (T-SQL MATCH) | Cypher |
|---|---|---|
| Direct friends | `SELECT p2.name FROM person p1, person p2, friendof WHERE MATCH(p1-(friendof)->p2) AND p1.name='john'` | `MATCH (:Person {name:'john'})-[:FRIEND_OF]->(p2:Person) RETURN p2.name` |
| Liked restaurants | `SELECT r.name FROM person, likes, restaurant WHERE MATCH(person-(likes)->restaurant) AND person.name='john'` | `MATCH (:Person {name:'john'})-[:LIKES]->(r:Restaurant) RETURN r.name` |
| Two-hop path | `SELECT restaurant.name FROM person p1, person p2, likes, friendof, restaurant WHERE MATCH(p1-(friendof)->p2-(likes)->restaurant) AND p1.name='john'` | `MATCH (:Person {name:'john'})-[:FRIEND_OF]->()-[:LIKES]->(r:Restaurant) RETURN r.name` |
| AND pattern | `MATCH(person-(likes)->restaurant-(locatedin)->city AND person-(livesin)->city)` | `MATCH (p)-[:LIKES]->(r)-[:LOCATED_IN]->(c), (p)-[:LIVES_IN]->(c)` |
| Shortest path | `MATCH(SHORTEST_PATH(p1(-(friend)->p2)+)) WHERE p1.name='john'` | `MATCH path=shortestPath((:Person {name:'john'})-[:FRIEND_OF*]->(dest:Person))` |
| Variable length | `SHORTEST_PATH(p1(-(friend)->p2){1,2})` | `MATCH (p1)-[:FRIEND_OF*1..2]->(p2)` |

## Key Differences

| Aspect | SQL Server Graph | Neo4j |
|---|---|---|
| **Storage** | Relational tables with hidden graph columns | Native property graph store |
| **Query language** | T-SQL + MATCH extension | Cypher (declarative, pattern-first) |
| **Multi-label nodes** | Not supported (one table = one type) | Supported (`:Person:Employee`) |
| **Schema enforcement** | Via table definitions and FK constraints | Optional (schema-optional by default; constraints via `CREATE CONSTRAINT`) |
| **Graph algorithms** | Limited (SHORTEST_PATH only) | Rich via GDS plugin (PageRank, Louvain, BFS, etc.) |
| **Visualization** | Requires external tools | Built-in Neo4j Browser |
| **Horizontal scale** | SQL Server clustering | Neo4j Fabric / Aura |
| **Transactions** | Full ACID (same as SQL Server) | Full ACID (MVCC) |
| **Best for** | Graphs embedded in an existing relational schema | Large, deeply connected graphs with complex traversals |
