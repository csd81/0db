// Chapter 13 – Neo4j: Advanced Cypher queries
// Aggregations, variable-length paths, and Northwind product graph patterns

// ── Aggregations ──────────────────────────────────────────────────────────────

// 1. Count friends per person
MATCH (p:Person)-[:FRIEND_OF]->(friend:Person)
RETURN p.name AS person, count(friend) AS friend_count
ORDER BY friend_count DESC;

// 2. Average rating per restaurant
MATCH (p:Person)-[l:LIKES]->(r:Restaurant)
RETURN r.name AS restaurant, avg(l.rating) AS avg_rating, count(p) AS fans
ORDER BY fans DESC;

// 3. Restaurants per city with fan count
MATCH (r:Restaurant)-[:LOCATED_IN]->(c:City)
OPTIONAL MATCH (p:Person)-[:LIKES]->(r)
RETURN c.name AS city, r.name AS restaurant, count(p) AS fans
ORDER BY city, fans DESC;

// ── Variable-length paths ─────────────────────────────────────────────────────

// 4. All persons reachable from john within 2 hops
MATCH (:Person {name: 'john'})-[:FRIEND_OF*1..2]->(p:Person)
RETURN DISTINCT p.name AS reachable;

// 5. All paths between john and alice (up to 4 hops)
MATCH path = (:Person {name: 'john'})-[:FRIEND_OF*1..4]->(:Person {name: 'alice'})
RETURN [n IN nodes(path) | n.name] AS route, length(path) AS hops
ORDER BY hops;

// 6. Diameter of the social network (longest shortest path)
MATCH (a:Person), (b:Person)
WHERE a.id < b.id
MATCH path = shortestPath((a)-[:FRIEND_OF*]-(b))
RETURN a.name, b.name, length(path) AS distance
ORDER BY distance DESC
LIMIT 5;

// ── Northwind product graph ────────────────────────────────────────────────────

// 7. Products in an order with total line value
MATCH (o:Order)-[c:CONTAINS]->(p:Product)
RETURN o.id AS order_id, p.name AS product,
       c.quantity AS qty, p.price AS unit_price,
       round(c.quantity * p.price * (1 - coalesce(c.discount, 0.0)), 2) AS line_total
ORDER BY order_id;

// 8. Products ordered together (co-occurrence)
MATCH (o:Order)-[:CONTAINS]->(p1:Product),
      (o)-[:CONTAINS]->(p2:Product)
WHERE p1.id < p2.id
RETURN p1.name AS product_a, p2.name AS product_b, count(o) AS shared_orders
ORDER BY shared_orders DESC;

// 9. Revenue by category
MATCH (o:Order)-[c:CONTAINS]->(p:Product)
RETURN p.category AS category,
       round(sum(c.quantity * p.price * (1 - coalesce(c.discount, 0.0))), 2) AS revenue
ORDER BY revenue DESC;

// ── Graph algorithms (requires APOC or GDS plugin) ────────────────────────────

// 10. PageRank-style centrality (manual approximation — friend count as proxy)
MATCH (p:Person)
OPTIONAL MATCH (other:Person)-[:FRIEND_OF]->(p)
RETURN p.name AS person, count(other) AS in_degree
ORDER BY in_degree DESC;
