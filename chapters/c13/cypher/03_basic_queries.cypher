// Chapter 13 – Neo4j: Basic Cypher queries
// Direct translations of the 7 SQL Server MATCH queries from c8/sql/02_graph_queries.sql

// 1. John's direct friends (one hop)
//    SQL: SELECT p2.name FROM person p1, person p2, friendof
//         WHERE match(p1-(friendof)->p2) AND p1.name = 'john'
MATCH (:Person {name: 'john'})-[:FRIEND_OF]->(friend:Person)
RETURN friend.name AS friend;

// ─────────────────────────────────────────────────────────────────────────────

// 2. Restaurants that john likes
//    SQL: SELECT restaurant.name FROM person, likes, restaurant
//         WHERE match(person-(likes)->restaurant) AND person.name = 'john'
MATCH (:Person {name: 'john'})-[l:LIKES]->(r:Restaurant)
RETURN r.name AS restaurant, l.rating AS rating;

// ─────────────────────────────────────────────────────────────────────────────

// 3. Restaurants liked by john's friends (two hops)
//    SQL: SELECT restaurant.name FROM person p1, person p2, likes, friendof, restaurant
//         WHERE match(p1-(friendof)->p2-(likes)->restaurant) AND p1.name = 'john'
MATCH (:Person {name: 'john'})-[:FRIEND_OF]->(p2:Person)-[:LIKES]->(r:Restaurant)
RETURN p2.name AS friend, r.name AS restaurant;

// ─────────────────────────────────────────────────────────────────────────────

// 4. People who like a restaurant in the same city they live in
//    SQL: SELECT person.id, person.name FROM person, likes, restaurant, livesin, city, locatedin
//         WHERE match(person-(likes)->restaurant-(locatedin)->city AND person-(livesin)->city)
MATCH (p:Person)-[:LIKES]->(r:Restaurant)-[:LOCATED_IN]->(c:City),
      (p)-[:LIVES_IN]->(c)
RETURN p.name AS person, r.name AS restaurant, c.name AS city;

// ─────────────────────────────────────────────────────────────────────────────

// 5. People whose friend likes a restaurant in the friend's own city
//    SQL: SELECT DISTINCT p1.id, p1.name FROM person p1, person p2, friendof, likes,
//         restaurant, livesin, city, locatedin
//         WHERE match(p1-(friendof)->p2 AND p2-(likes)->restaurant-(locatedin)->city AND p2-(livesin)->city)
MATCH (p1:Person)-[:FRIEND_OF]->(p2:Person)-[:LIKES]->(r:Restaurant)-[:LOCATED_IN]->(c:City),
      (p2)-[:LIVES_IN]->(c)
RETURN DISTINCT p1.name AS person, p2.name AS friend, r.name AS restaurant, c.name AS city;

// ─────────────────────────────────────────────────────────────────────────────

// 6. Pairs of people who share a mutual friend
//    SQL: SELECT p0.name person, p1.name Friend1, p2.name Friend2
//         FROM person p1, friendof f1, person p2, friendof f2, person p0
//         WHERE match(p1-(f1)->p0 AND p2-(f2)->p0) AND p1.id <> p2.id
MATCH (p1:Person)-[:FRIEND_OF]->(p0:Person)<-[:FRIEND_OF]-(p2:Person)
WHERE p1.id <> p2.id AND p1.name < p2.name
RETURN p0.name AS mutual_friend, p1.name AS person1, p2.name AS person2;

// ─────────────────────────────────────────────────────────────────────────────

// 7a. Shortest paths from john to all reachable persons
//     SQL: MATCH (shortest_path(p1(-(friend)->p2)+)) WHERE p1.name='john'
MATCH path = shortestPath((:Person {name: 'john'})-[:FRIEND_OF*]->(dest:Person))
WHERE dest.name <> 'john'
RETURN dest.name AS reaches,
       length(path) AS hops,
       [n IN nodes(path) | n.name] AS route
ORDER BY hops;

// 7b. Shortest path from john to jacob specifically
MATCH path = shortestPath(
    (:Person {name: 'john'})-[:FRIEND_OF*]->(:Person {name: 'jacob'})
)
RETURN length(path) AS hops, [n IN nodes(path) | n.name] AS route;
