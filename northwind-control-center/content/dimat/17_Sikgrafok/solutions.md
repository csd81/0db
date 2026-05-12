# Chapter 17 - Síkgráfok (Planar Graphs) - Complete Solutions

## Section 17.1 - Síkgráf definíció (Planar Graph Definition)

---

### Exercise 17.1.1 - Define Planar Graph

**Problem:** Define what a planar graph is.

**Solution:**

**Definition:**

A graph $G = (V, E)$ is **planar** if it can be drawn in the plane without any edges crossing.

---

**Terminology:**

- **Planar graph:** A graph that CAN be drawn without crossings (abstract property)
- **Plane graph:** A graph that IS drawn without crossings (includes the embedding)
- **Planar embedding:** A drawing of a planar graph without edge crossings
- **Face:** A region of the plane bounded by edges (including the outer/unbounded region)

---

**Examples:**

**Planar graphs:**
- $K_1, K_2, K_3, K_4$ (all complete graphs up to 4 vertices)
- Paths $P_n$
- Cycles $C_n$
- Trees (all trees are planar)

**Non-planar graphs:**
- $K_5$ (complete graph on 5 vertices)
- $K_{3,3}$ (complete bipartite graph with 3+3 vertices)

---

### Exercise 17.1.2 - Verify: K₁, K₂, K₃, K₄ are Planar

**Problem:** Verify that complete graphs up to $K_4$ are planar.

**Solution:**

**$K_1$:** Single vertex, no edges. Trivially planar. ✓

```
●
```

---

**$K_2$:** Two vertices, one edge. Planar. ✓

```
●-----●
```

---

**$K_3$:** Triangle. Planar. ✓

```
  ●
 / \
●---●
```

---

**$K_4$:** Complete graph on 4 vertices. Planar. ✓

```
  ●
 /|\
●-●-●
 \|/
  ●
```

Or without crossings:
```
  ●
 / \
●---●
 \ /
  ●
```

**Verification:** 4 vertices, 6 edges, drawn without crossings. ✓

---

### Exercise 17.1.3 - Verify: K₅ is NOT Planar

**Problem:** Verify that $K_5$ is not planar.

**Solution:**

**$K_5$:** Complete graph on 5 vertices.

**Attempt to draw:**

```
    ●
   /|\
  / | \
 ●--●--●
  \ | /
   \|/
    ●
```

Any attempt to draw $K_5$ results in at least one crossing!

---

**Proof using Euler's formula (will be proved later):**

For a simple planar graph with $V \geq 3$:
$$E \leq 3V - 6$$

For $K_5$: $V = 5$, $E = 10$.

Check: $10 \leq 3(5) - 6 = 9$? 

**NO!** $10 > 9$.

**Therefore:** $K_5$ is NOT planar. ✓

---

### Exercise 17.1.4 - Define Faces of a Plane Graph

**Problem:** Define what faces are in a plane graph.

**Solution:**

**Definition:**

A **face** of a plane graph is a connected region of the plane bounded by edges.

---

**Types of faces:**

1. **Bounded faces (inner faces):** Finite regions
2. **Unbounded face (outer face):** The infinite region outside the graph

---

**Example:**

```
    a
   / \
  b---c
```

**Faces:**
1. Triangle abc (bounded)
2. Outside region (unbounded/outer face)

**Total:** 2 faces

---

**Example (cube graph):**

```
  a-----b
 /|    /|
d-----c |
| e---|-f
|/    |/
h-----g
```

**Faces:** 6 faces (corresponding to the 6 faces of a cube)

---

## Section 17.2 - Euler-formula (Euler's Formula)

---

### Exercise 17.2.1 - State Euler's Formula

**Problem:** State Euler's formula for planar graphs.

**Solution:**

**Euler's Formula (1750):**

For any connected plane graph:
$$V - E + F = 2$$

where:
- $V$ = number of vertices
- $E$ = number of edges
- $F$ = number of faces (including the outer face)

---

**Example Verification:**

**Triangle ($K_3$):**
- $V = 3$
- $E = 3$
- $F = 2$ (1 bounded + 1 outer)

Check: $3 - 3 + 2 = 2$ ✓

---

**Square with diagonal:**
```
  a-----b
  | \   |
  |  \  |
  |   \ |
  d-----c
```
- $V = 4$
- $E = 5$
- $F = 3$ (2 triangles + 1 outer)

Check: $4 - 5 + 3 = 2$ ✓

---

### Exercise 17.2.2 - Prove Euler's Formula by Induction

**Problem:** Prove Euler's formula $V - E + F = 2$ by induction.

**Solution:**

**Theorem:** For any connected plane graph, $V - E + F = 2$.

---

**Proof by Induction on E (number of edges):**

---

**Base case (E = 0):**

A connected graph with 0 edges has $V = 1$ vertex and $F = 1$ face (the outer face).

Check: $1 - 0 + 1 = 2$ ✓

---

**Base case (E = 1):**

A connected graph with 1 edge has $V = 2$ vertices and $F = 1$ face.

Check: $2 - 1 + 1 = 2$ ✓

---

**Inductive hypothesis:** Assume Euler's formula holds for all connected plane graphs with $k$ edges.

---

**Inductive step (E = k+1):**

Let $G$ be a connected plane graph with $k+1$ edges.

**Case 1: G has no cycles (G is a tree).**

For a tree: $E = V - 1$ and $F = 1$ (only the outer face).

Check: $V - (V-1) + 1 = V - V + 1 + 1 = 2$ ✓

---

**Case 2: G has a cycle.**

Let $e$ be an edge on a cycle.

Remove $e$ to get $G' = G - e$.

**Properties of $G'$:**
- $V' = V$ (same vertices)
- $E' = E - 1$ (one less edge)
- $F' = F - 1$ (removing an edge from a cycle merges two faces)
- $G'$ is still connected (edge was on a cycle)

By inductive hypothesis:
$$V' - E' + F' = 2$$

Substitute:
$$V - (E-1) + (F-1) = 2$$
$$V - E + 1 + F - 1 = 2$$
$$V - E + F = 2$$ ✓

---

**By induction:** Euler's formula holds for all connected plane graphs. ∎

---

### Exercise 17.2.3 - Prove: E ≤ 3V - 6 for Simple Planar Graphs

**Problem:** Prove the edge bound for simple planar graphs.

**Solution:**

**Theorem:** For any simple planar graph with $V \geq 3$:
$$E \leq 3V - 6$$

---

**Proof:**

Let $G$ be a simple planar graph with $V \geq 3$.

Assume $G$ is connected (if not, add edges to make it connected; this only increases $E$).

---

**Step 1: Count edge-face incidences.**

Each face is bounded by at least 3 edges (since $G$ is simple, no loops or multiple edges).

Let $f_i$ = number of edges bounding face $i$.

Then: $\sum_{i=1}^{F} f_i \geq 3F$

---

**Step 2: Each edge bounds exactly 2 faces.**

Therefore: $\sum_{i=1}^{F} f_i = 2E$

---

**Step 3: Combine.**

$$2E \geq 3F$$
$$F \leq \frac{2E}{3}$$

---

**Step 4: Apply Euler's formula.**

$$V - E + F = 2$$
$$V - E + \frac{2E}{3} \geq 2$$
$$V - \frac{E}{3} \geq 2$$
$$V - 2 \geq \frac{E}{3}$$
$$3V - 6 \geq E$$

**Therefore:** $E \leq 3V - 6$. ∎

---

### Exercise 17.2.4 - Use Bound to Prove K₅ is Non-Planar

**Problem:** Use the edge bound to prove $K_5$ is not planar.

**Solution:**

**For $K_5$:**
- $V = 5$
- $E = \binom{5}{2} = 10$

**Edge bound:** $E \leq 3V - 6$

**Check:** $10 \leq 3(5) - 6 = 9$?

**NO!** $10 > 9$.

**Therefore:** $K_5$ violates the edge bound.

**Therefore:** $K_5$ is NOT planar. ✓

---

### Exercise 17.2.5 - Prove: E ≤ 2V - 4 for Triangle-Free Planar Graphs

**Problem:** Prove the edge bound for triangle-free planar graphs.

**Solution:**

**Theorem:** For any triangle-free planar graph with $V \geq 3$:
$$E \leq 2V - 4$$

---

**Proof:**

Since $G$ is triangle-free, every face is bounded by at least 4 edges.

**Count edge-face incidences:**

$$\sum_{i=1}^{F} f_i \geq 4F$$

Since each edge bounds 2 faces:

$$2E \geq 4F$$
$$F \leq \frac{E}{2}$$

---

**Apply Euler's formula:**

$$V - E + F = 2$$
$$V - E + \frac{E}{2} \geq 2$$
$$V - \frac{E}{2} \geq 2$$
$$V - 2 \geq \frac{E}{2}$$
$$2V - 4 \geq E$$

**Therefore:** $E \leq 2V - 4$. ∎

---

### Exercise 17.2.6 - Use Bound to Prove K₃,₃ is Non-Planar

**Problem:** Use the triangle-free bound to prove $K_{3,3}$ is not planar.

**Solution:**

**For $K_{3,3}$:**
- $V = 6$
- $E = 3 \times 3 = 9$
- $K_{3,3}$ is triangle-free (bipartite graphs have no odd cycles)

**Triangle-free bound:** $E \leq 2V - 4$

**Check:** $9 \leq 2(6) - 4 = 8$?

**NO!** $9 > 8$.

**Therefore:** $K_{3,3}$ violates the bound.

**Therefore:** $K_{3,3}$ is NOT planar. ✓

---

## Section 17.3 - Kuratowski-tétel (Kuratowski's Theorem)

---

### Exercise 17.3.1 - Define Subdivision of a Graph

**Problem:** Define what a subdivision of a graph is.

**Solution:**

**Definition:**

A **subdivision** of a graph $G$ is obtained by replacing edges with paths.

**Formally:** To subdivide an edge $\{u, v\}$:
1. Remove edge $\{u, v\}$
2. Add a new vertex $w$
3. Add edges $\{u, w\}$ and $\{w, v\}$

---

**Example:**

```
Original G:       Subdivision:
  a-----b           a--x--b
  |     |           |     |
  c-----d           c-----d
```

Edge $\{a,b\}$ was subdivided by adding vertex $x$.

---

**Key property:** Subdivision preserves planarity.

- If $G$ is planar, any subdivision of $G$ is planar.
- If a subdivision of $G$ is planar, then $G$ is planar.

---

### Exercise 17.3.2 - State Kuratowski's Theorem

**Problem:** State Kuratowski's theorem.

**Solution:**

**Kuratowski's Theorem (1930):**

A graph $G$ is planar **if and only if** $G$ does not contain a subdivision of $K_5$ or $K_{3,3}$.

---

**Equivalent formulation:**

$G$ is non-planar **if and only if** $G$ contains a subdivision of $K_5$ or $K_{3,3}$.

---

**Forbidden subdivisions:**
- $K_5$ (complete graph on 5 vertices)
- $K_{3,3}$ (complete bipartite graph with 3+3 vertices)

These are the "minimal" non-planar graphs.

---

### Exercise 17.3.3 - Identify K₅ or K₃,₃ Subdivisions

**Problem:** Find subdivisions of $K_5$ or $K_{3,3}$ in non-planar graphs.

**Solution:**

**Example 1: Utility Graph**

```
  1   2   3    (houses)
  | \ | / |
  |  \|/  |
  |  / \  |
  | / | \ |
  A   B   C    (utilities)
```

This IS $K_{3,3}$ (3 houses connected to 3 utilities).

**Therefore:** Non-planar by Kuratowski's theorem. ✓

---

**Example 2: Petersen Graph**

The Petersen graph contains a subdivision of $K_{3,3}$.

**Therefore:** Non-planar. ✓

---

### Exercise 17.3.4 - Prove Non-Planarity Using Kuratowski's Theorem

**Problem:** Use Kuratowski's theorem to prove a graph is non-planar.

**Solution:**

**Example:** Prove the Petersen graph is non-planar.

**Petersen Graph:**
```
      ●
     / \
    /   \
   ●-----●
   | \ / |
   |  ●  |
   | / \ |
   ●-----●
    \   /
     \ /
      ●
```

**Proof:**

Find a $K_{3,3}$ subdivision:

**Partition vertices:**
- Part A: {outer vertices at positions 1, 3, 5}
- Part B: {inner vertices at positions 2, 4, 5}

**Verify:** Each vertex in A connects to each vertex in B via paths.

**Therefore:** Petersen graph contains a $K_{3,3}$ subdivision.

**Therefore:** Petersen graph is non-planar. ✓

---

## Section 17.4 - Síkgráf Színezés (Coloring Planar Graphs)

---

### Exercise 17.4.1 - Define Proper Vertex Coloring

**Problem:** Define proper vertex coloring and chromatic number.

**Solution:**

**Definition:**

A **proper vertex coloring** of a graph $G = (V, E)$ is an assignment of colors to vertices such that no two adjacent vertices have the same color.

**Formally:** A function $c: V \to \{1, 2, \ldots, k\}$ such that:
$$\{u, v\} \in E \implies c(u) \neq c(v)$$

---

**Chromatic Number:**

The **chromatic number** $\chi(G)$ is the minimum number of colors needed for a proper coloring.

---

**Examples:**

| Graph | χ(G) |
|-------|------|
| $K_n$ | n |
| $C_n$ (n odd) | 3 |
| $C_n$ (n even) | 2 |
| Bipartite | 2 |
| Tree | 2 |

---

### Exercise 17.4.2 - State the Five Color Theorem

**Problem:** State the Five Color Theorem.

**Solution:**

**Five Color Theorem (Heawood, 1890):**

Every planar graph is 5-colorable.

**Formally:** If $G$ is planar, then $\chi(G) \leq 5$.

---

**Proof:** (Will be proved in Exercise 17.4.5)

---

### Exercise 17.4.3 - State the Four Color Theorem

**Problem:** State the Four Color Theorem.

**Solution:**

**Four Color Theorem (Appel & Haken, 1976):**

Every planar graph is 4-colorable.

**Formally:** If $G$ is planar, then $\chi(G) \leq 4$.

---

**Historical Note:**

- Conjectured by Francis Guthrie (1852)
- Many false proofs were proposed
- First proved by Appel and Haken (1976)
- First major theorem proved using computer assistance
- Proof checked 1,936 configurations

---

### Exercise 17.4.4 - Prove: Every Planar Graph Has a Vertex of Degree ≤ 5

**Problem:** Prove that every planar graph has a vertex of degree at most 5.

**Solution:**

**Theorem:** Every planar graph has a vertex of degree at most 5.

---

**Proof by Contradiction:**

Assume every vertex has degree at least 6.

**Step 1: Count edge-vertex incidences.**

$$\sum_{v \in V} \deg(v) = 2E$$ (Handshaking lemma)

If every vertex has degree ≥ 6:
$$2E \geq 6V$$
$$E \geq 3V$$

---

**Step 2: Apply edge bound.**

For planar graphs: $E \leq 3V - 6$

**Contradiction:**
$$3V \leq E \leq 3V - 6$$
$$3V \leq 3V - 6$$
$$0 \leq -6$$

**Contradiction!**

---

**Therefore:** There must be at least one vertex with degree ≤ 5. ∎

---

### Exercise 17.4.5 - Prove: Every Planar Graph is 5-Colorable

**Problem:** Prove the Five Color Theorem.

**Solution:**

**Theorem:** Every planar graph is 5-colorable.

---

**Proof by Induction on V:**

---

**Base case (V ≤ 5):**

Color each vertex with a different color. ✓

---

**Inductive hypothesis:** Assume every planar graph with $V-1$ vertices is 5-colorable.

---

**Inductive step:**

Let $G$ be a planar graph with $V$ vertices.

**Step 1:** By Exercise 17.4.4, $G$ has a vertex $v$ with $\deg(v) \leq 5$.

---

**Step 2:** Remove $v$ to get $G' = G - v$.

$G'$ is planar with $V-1$ vertices.

By inductive hypothesis, $G'$ is 5-colorable.

---

**Step 3:** Try to extend the coloring to $v$.

**Case 1:** $\deg(v) \leq 4$ or neighbors use ≤ 4 colors.

At least one color is unused among neighbors.

Assign that color to $v$. ✓

---

**Case 2:** $\deg(v) = 5$ and all 5 neighbors have different colors.

Let neighbors be $v_1, v_2, v_3, v_4, v_5$ in cyclic order with colors $1, 2, 3, 4, 5$.

**Kempe chain argument:**

Consider the subgraph induced by colors 1 and 3.

**Subcase 2a:** $v_1$ and $v_3$ are in different components.

Swap colors 1 and 3 in $v_1$'s component.

Now $v_1$ has color 3, and color 1 is free for $v$. ✓

**Subcase 2b:** $v_1$ and $v_3$ are in the same component.

There's a path from $v_1$ to $v_3$ using only colors 1 and 3.

This path, together with $v$, forms a cycle separating $v_2$ from $v_4$.

Consider colors 2 and 4.

$v_2$ and $v_4$ are in different components (separated by the cycle).

Swap colors 2 and 4 in $v_2$'s component.

Now color 2 is free for $v$. ✓

---

**Therefore:** $G$ is 5-colorable. ∎

---

## Section 17.5 - Dualitás (Duality)

---

### Exercise 17.5.1 - Define Dual Graph

**Problem:** Define the dual graph $G^*$.

**Solution:**

**Definition:**

Let $G$ be a plane graph (embedded planar graph).

The **dual graph** $G^*$ is constructed as follows:

1. Place one vertex in each face of $G$ (including the outer face)
2. For each edge $e$ of $G$, draw an edge $e^*$ in $G^*$ that crosses $e$
3. Connect the vertices in the faces on either side of $e$

---

**Properties:**
- $|V(G^*)| = |F(G)|$
- $|E(G^*)| = |E(G)|$
- $|F(G^*)| = |V(G)|$
- $(G^*)^* \cong G$

---

### Exercise 17.5.2 - Construct Dual of a Plane Graph

**Problem:** Construct the dual of a given plane graph.

**Solution:**

**Example:** Triangle with a vertex inside

```
    a
   / \
  b---c
   \ /
    d (inside)
```

**Faces:** 3 (triangle abc is split into abd, acd, bcd by d)

Wait, let me reconsider. If d is inside triangle abc and connected to all three vertices:

**Faces:** 3 bounded faces (abd, bcd, cad) + 1 outer face = 4 faces

**Dual graph:**
- 4 vertices (one per face)
- Edges cross the original edges

The dual is also a triangle with a central vertex (self-dual structure).

---

### Exercise 17.5.3 - Verify: |V(G*)| = F(G)

**Problem:** Verify the relationship between vertices of dual and faces of original.

**Solution:**

**By construction:**

Each face of $G$ (including the outer face) contains exactly one vertex of $G^*$.

**Therefore:** $|V(G^*)| = |F(G)|$. ✓

---

### Exercise 17.5.4 - Verify: (G*)* ≅ G

**Problem:** Verify that the dual of the dual is isomorphic to the original graph.

**Solution:**

**Theorem:** $(G^*)^* \cong G$.

---

**Proof:**

**Step 1:** $G^*$ has one vertex per face of $G$.

**Step 2:** $(G^*)^*$ has one vertex per face of $G^*$.

**Step 3:** Faces of $G^*$ correspond to vertices of $G$.

(Each vertex of $G$ is surrounded by a face in $G^*$)

**Therefore:** $(G^*)^*$ has one vertex per vertex of $G$.

**Step 4:** Edges correspond similarly.

**Therefore:** $(G^*)^* \cong G$. ✓

---

## Section 17.6 - Síkgráfok Felismerése (Planarity Testing)

---

### Exercise 17.6.1 - Hopcroft-Tarjan Algorithm

**Problem:** Understand the Hopcroft-Tarjan planarity testing algorithm.

**Solution:**

**Hopcroft-Tarjan Algorithm (1974):**

**Time complexity:** $O(V)$ (linear time)

**Approach:**
1. Use DFS to find a spanning tree
2. Process edges in post-order
3. Maintain embedding constraints
4. Detect conflicts that imply non-planarity

---

**Key insight:** A graph is planar iff it can be embedded incrementally without conflicts.

---

### Exercise 17.6.2 - Graph Isomorphism Complexity

**Problem:** Understand the complexity of planarity testing.

**Solution:**

**Complexity:**

- **Planarity testing:** $O(V)$ (Hopcroft-Tarjan, Boyer-Myrvold)
- **Finding embedding:** $O(V)$
- **Finding Kuratowski subdivision:** $O(V)$ (if non-planar)

---

**Practical software:**
- **nauty:** Graph isomorphism and planarity
- **LEDA:** Graph algorithms library
- **NetworkX:** Python library with planarity testing

---

## Section 17.7 - Alkalmazások (Applications)

---

### Exercise 17.7.1 - Circuit Board Design

**Problem:** Apply planar graphs to circuit board design.

**Solution:**

**Application:**

In printed circuit boards (PCBs), wires (traces) cannot cross on the same layer.

**Model:**
- Vertices: Components/pins
- Edges: Connections (wires)

**Problem:** Can all connections be made on one layer?

**Solution:** Test if the connection graph is planar!

If non-planar, need multiple layers or vias.

---

### Exercise 17.7.2 - Map Coloring

**Problem:** Apply the Four Color Theorem to map coloring.

**Solution:**

**Application:**

Color a map so that no two adjacent regions (countries, states) have the same color.

**Model:**
- Vertices: Regions
- Edges: Adjacency (shared border)

**Result:** Dual graph is planar.

**By Four Color Theorem:** 4 colors suffice.

---

**Example:** US States can be colored with 4 colors. ✓

---

*Continued for remaining exercises in Chapter 17...*
