// Chapter 13 – Neo4j: Create the social network graph from c8
// Run in Neo4j Browser or cypher-shell

// Clear existing demo data
MATCH (n) DETACH DELETE n;

// ── Persons ──────────────────────────────────────────────────────────────────
CREATE (:Person {id: 1, name: 'john'});
CREATE (:Person {id: 2, name: 'mary'});
CREATE (:Person {id: 3, name: 'alice'});
CREATE (:Person {id: 4, name: 'jacob'});
CREATE (:Person {id: 5, name: 'julie'});
CREATE (:Person {id: 6, name: 'tom'});

// ── Restaurants ──────────────────────────────────────────────────────────────
CREATE (:Restaurant {id: 1, name: 'taco dell'});
CREATE (:Restaurant {id: 2, name: 'ginger and spice'});
CREATE (:Restaurant {id: 3, name: 'noodle land'});

// ── Cities ───────────────────────────────────────────────────────────────────
CREATE (:City {id: 1, name: 'bellevue',  state: 'wa'});
CREATE (:City {id: 2, name: 'seattle',   state: 'wa'});
CREATE (:City {id: 3, name: 'redmond',   state: 'wa'});

// ── LIKES edges ──────────────────────────────────────────────────────────────
MATCH (p:Person {id:1}), (r:Restaurant {id:1}) CREATE (p)-[:LIKES {rating:9}]->(r);
MATCH (p:Person {id:2}), (r:Restaurant {id:2}) CREATE (p)-[:LIKES {rating:9}]->(r);
MATCH (p:Person {id:3}), (r:Restaurant {id:3}) CREATE (p)-[:LIKES {rating:9}]->(r);
MATCH (p:Person {id:4}), (r:Restaurant {id:3}) CREATE (p)-[:LIKES {rating:9}]->(r);
MATCH (p:Person {id:5}), (r:Restaurant {id:3}) CREATE (p)-[:LIKES {rating:9}]->(r);

// ── LIVES_IN edges ────────────────────────────────────────────────────────────
MATCH (p:Person {id:1}), (c:City {id:1}) CREATE (p)-[:LIVES_IN]->(c);
MATCH (p:Person {id:2}), (c:City {id:2}) CREATE (p)-[:LIVES_IN]->(c);
MATCH (p:Person {id:3}), (c:City {id:3}) CREATE (p)-[:LIVES_IN]->(c);
MATCH (p:Person {id:4}), (c:City {id:3}) CREATE (p)-[:LIVES_IN]->(c);
MATCH (p:Person {id:5}), (c:City {id:1}) CREATE (p)-[:LIVES_IN]->(c);

// ── LOCATED_IN edges ──────────────────────────────────────────────────────────
MATCH (r:Restaurant {id:1}), (c:City {id:1}) CREATE (r)-[:LOCATED_IN]->(c);
MATCH (r:Restaurant {id:2}), (c:City {id:2}) CREATE (r)-[:LOCATED_IN]->(c);
MATCH (r:Restaurant {id:3}), (c:City {id:3}) CREATE (r)-[:LOCATED_IN]->(c);

// ── FRIEND_OF edges (directed, use both directions for undirected semantics) ──
MATCH (p1:Person {id:1}), (p2:Person {id:2}) CREATE (p1)-[:FRIEND_OF]->(p2);
MATCH (p1:Person {id:1}), (p2:Person {id:5}) CREATE (p1)-[:FRIEND_OF]->(p2);
MATCH (p1:Person {id:2}), (p2:Person {id:3}) CREATE (p1)-[:FRIEND_OF]->(p2);
MATCH (p1:Person {id:3}), (p2:Person {id:2}) CREATE (p1)-[:FRIEND_OF]->(p2);
MATCH (p1:Person {id:3}), (p2:Person {id:5}) CREATE (p1)-[:FRIEND_OF]->(p2);
MATCH (p1:Person {id:3}), (p2:Person {id:6}) CREATE (p1)-[:FRIEND_OF]->(p2);
MATCH (p1:Person {id:4}), (p2:Person {id:2}) CREATE (p1)-[:FRIEND_OF]->(p2);
MATCH (p1:Person {id:5}), (p2:Person {id:4}) CREATE (p1)-[:FRIEND_OF]->(p2);

// ── Northwind product/order sample ───────────────────────────────────────────
CREATE (:Product {id: 1,  name: 'Chai',          price: 18.00, category: 'Beverages'});
CREATE (:Product {id: 2,  name: 'Chang',         price: 19.00, category: 'Beverages'});
CREATE (:Product {id: 11, name: 'Queso Cabrales', price: 21.00, category: 'Dairy Products'});
CREATE (:Product {id: 72, name: 'Mozzarella di Giovanni', price: 34.80, category: 'Dairy Products'});

CREATE (:Order {id: 10248, date: '1996-07-04'});
CREATE (:Order {id: 10249, date: '1996-07-05'});

MATCH (o:Order {id:10248}), (p:Product {id:11})  CREATE (o)-[:CONTAINS {quantity:12, discount:0.0}]->(p);
MATCH (o:Order {id:10248}), (p:Product {id:72})  CREATE (o)-[:CONTAINS {quantity:10, discount:0.0}]->(p);
MATCH (o:Order {id:10249}), (p:Product {id:1})   CREATE (o)-[:CONTAINS {quantity:9,  discount:0.0}]->(p);
MATCH (o:Order {id:10249}), (p:Product {id:2})   CREATE (o)-[:CONTAINS {quantity:40, discount:0.0}]->(p);
