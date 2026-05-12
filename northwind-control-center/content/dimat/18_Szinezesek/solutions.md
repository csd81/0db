# Chapter 18 - Színezések (Graph Colorings) - Complete Solutions

## Section 18.1 - Csúcsszínezés (Vertex Coloring)

---

### Exercise 18.1.1 - Define Proper Vertex Coloring

**Problem:** Define proper vertex coloring and chromatic number.

**Solution:**

**Definition:**

A **proper vertex coloring** of a graph $G = (V, E)$ is an assignment of colors to vertices such that no two adjacent vertices have the same color.

**Formally:** A function $c: V \to \{1, 2, \ldots, k\}$ such that:
$$\{u, v\} \in E \implies c(u) \neq c(v)$$

---

**Chromatic Number:**

The **chromatic number** $\chi(G)$ is the minimum number of colors needed for a proper coloring of $G$.

---

**Example:**

```
    a
   / \
  b---c
```

**Proper coloring:**
- c(a) = 1
- c(b) = 2
- c(c) = 3

**Chromatic number:** χ(K₃) = 3

---

### Exercise 18.1.2 - Compute χ(Kₙ)

**Problem:** Compute the chromatic number of complete graphs.

**Solution:**

**Theorem:** $\chi(K_n) = n$

**Proof:**

In $K_n$, every pair of vertices is adjacent.

**Therefore:** Every vertex must have a different color.

**Therefore:** We need exactly $n$ colors. ✓

---

**Examples:**
- χ(K₁) = 1
- χ(K₂) = 2
- χ(K₃) = 3
- χ(K₄) = 4
- χ(K₅) = 5

---

### Exercise 18.1.3 - Compute χ(G) for Bipartite Graphs

**Problem:** Compute the chromatic number of bipartite graphs.

**Solution:**

**Theorem:** If $G$ is bipartite with at least one edge, then $\chi(G) = 2$.

**Proof:**

Let $G$ have bipartition $V = A \cup B$.

**Coloring:**
- Color all vertices in $A$ with color 1
- Color all vertices in $B$ with color 2

**Verification:**
- All edges go between $A$ and $B$
- No two adjacent vertices have the same color ✓

**Therefore:** χ(G) ≤ 2.

Since $G$ has at least one edge, χ(G) ≥ 2.

**Therefore:** χ(G) = 2. ✓

---

**Examples:**
- χ(Pₙ) = 2 for n ≥ 2
- χ(Cₙ) = 2 for n even
- χ(Kₘ,ₙ) = 2

---

### Exercise 18.1.4 - Compute χ(Cₙ)

**Problem:** Compute the chromatic number of cycle graphs.

**Solution:**

**Theorem:**
$$\chi(C_n) = \begin{cases} 2 & \text{if } n \text{ is even} \\ 3 & \text{if } n \text{ is odd} \end{cases}$$

---

**Proof (n even):**

$C_n$ is bipartite when $n$ is even.

**Bipartition:** Alternate vertices.

**Therefore:** χ(Cₙ) = 2. ✓

---

**Proof (n odd):**

**Lower bound:** Cₙ contains an odd cycle, so it's not bipartite.

**Therefore:** χ(Cₙ) ≥ 3.

**Upper bound:** Color vertices 1, 2, 1, 2, ..., 1, 2, 3 (last vertex).

Since $n$ is odd, the last vertex is adjacent to vertices colored 1 and 2.

**Therefore:** χ(Cₙ) ≤ 3.

**Therefore:** χ(Cₙ) = 3. ✓

---

### Exercise 18.1.5 - Compute χ(T) for Trees

**Problem:** Compute the chromatic number of trees.

**Solution:**

**Theorem:** For any tree $T$ with at least 2 vertices, $\chi(T) = 2$.

**Proof:**

**Lemma:** Every tree is bipartite.

**Proof of lemma:**

Root the tree at any vertex $r$.

**Bipartition:**
- $A = \{v : \text{distance}(r, v) \text{ is even}\}$
- $B = \{v : \text{distance}(r, v) \text{ is odd}\}$

**Verification:** Every edge connects vertices at consecutive levels.

**Therefore:** Every edge goes between $A$ and $B$. ✓

---

**Therefore:** Trees are bipartite.

**Therefore:** χ(T) = 2 for any tree with at least one edge. ✓

---

### Exercise 18.1.6 - Prove: χ(G) ≤ Δ(G) + 1

**Problem:** Prove the greedy coloring bound.

**Solution:**

**Theorem:** For any graph $G$, $\chi(G) \leq \Delta(G) + 1$.

---

**Proof (Greedy Coloring):**

Order the vertices arbitrarily: $v_1, v_2, \ldots, v_n$.

**Greedy algorithm:**
- Color $v_1$ with color 1
- For $i = 2$ to $n$:
  - Color $v_i$ with the smallest color not used by its already-colored neighbors

---

**Analysis:**

When coloring $v_i$:
- $v_i$ has at most $\Delta(G)$ neighbors
- At most $\Delta(G)$ neighbors are already colored
- At most $\Delta(G)$ colors are forbidden
- At least one color from $\{1, 2, \ldots, \Delta(G)+1\}$ is available

**Therefore:** The greedy algorithm uses at most $\Delta(G) + 1$ colors.

**Therefore:** $\chi(G) \leq \Delta(G) + 1$. ✓

---

### Exercise 18.1.7 - State Brooks' Theorem

**Problem:** State Brooks' Theorem.

**Solution:**

**Brooks' Theorem (1941):**

Let $G$ be a connected graph with maximum degree $\Delta(G)$.

If $G$ is NOT a complete graph $K_n$ and NOT an odd cycle $C_n$, then:
$$\chi(G) \leq \Delta(G)$$

---

**Exceptions:**
- Complete graphs: $\chi(K_n) = n = \Delta(K_n) + 1$
- Odd cycles: $\chi(C_{2k+1}) = 3 = \Delta(C_{2k+1}) + 1$

---

**Examples:**

**Path P₄:** Δ = 2, not complete, not odd cycle.

**By Brooks:** χ(P₄) ≤ 2.

**Actual:** χ(P₄) = 2. ✓

---

**Complete graph K₄:** Δ = 3, but it's complete.

**Brooks doesn't apply.**

**Actual:** χ(K₄) = 4 = Δ + 1.

---

## Section 18.2 - Élszínezés (Edge Coloring)

---

### Exercise 18.2.1 - Define Proper Edge Coloring

**Problem:** Define proper edge coloring and chromatic index.

**Solution:**

**Definition:**

A **proper edge coloring** of a graph $G = (V, E)$ is an assignment of colors to edges such that no two adjacent edges (edges sharing a vertex) have the same color.

**Formally:** A function $c: E \to \{1, 2, \ldots, k\}$ such that:
$$e_1, e_2 \text{ share a vertex} \implies c(e_1) \neq c(e_2)$$

---

**Chromatic Index:**

The **chromatic index** $\chi'(G)$ is the minimum number of colors needed for a proper edge coloring of $G$.

---

**Example:**

```
    a
   / \
  b---c
```

**Edge coloring:**
- c(ab) = 1
- c(ac) = 2
- c(bc) = 3

**Chromatic index:** χ'(K₃) = 3

---

### Exercise 18.2.2 - Compute χ'(Kₙ)

**Problem:** Compute the chromatic index of complete graphs.

**Solution:**

**Theorem:**
$$\chi'(K_n) = \begin{cases} n-1 & \text{if } n \text{ is even} \\ n & \text{if } n \text{ is odd} \end{cases}$$

---

**Proof (n even):**

**Lower bound:** Each vertex has degree n-1.

**Therefore:** χ'(Kₙ) ≥ n-1.

**Upper bound (construction):**

Place vertices on a circle.

**Coloring:** For each "direction" (slope), color all parallel edges the same color.

There are n-1 directions.

**Therefore:** χ'(Kₙ) ≤ n-1.

**Therefore:** χ'(Kₙ) = n-1. ✓

---

**Proof (n odd):**

**Lower bound:** Each vertex has degree n-1.

But n-1 colors are not enough (parity argument).

**Therefore:** χ'(Kₙ) ≥ n.

**Upper bound:** Use n colors (one per vertex, edge gets color of "missing" vertex).

**Therefore:** χ'(Kₙ) = n. ✓

---

### Exercise 18.2.3 - State Vizing's Theorem

**Problem:** State Vizing's Theorem.

**Solution:**

**Vizing's Theorem (1964):**

For any simple graph $G$:
$$\Delta(G) \leq \chi'(G) \leq \Delta(G) + 1$$

---

**Classification:**

- **Class 1:** χ'(G) = Δ(G)
- **Class 2:** χ'(G) = Δ(G) + 1

---

**Examples:**

| Graph | Δ | χ' | Class |
|-------|---|----|-------|
| K₄ | 3 | 3 | Class 1 |
| K₃ | 2 | 3 | Class 2 |
| Cₙ (even) | 2 | 2 | Class 1 |
| Cₙ (odd) | 2 | 3 | Class 2 |
| Bipartite | Δ | Δ | Class 1 |

---

### Exercise 18.2.4 - Compute χ' for Bipartite Graphs

**Problem:** Compute the chromatic index of bipartite graphs.

**Solution:**

**Theorem (Kőnig, 1916):** For any bipartite graph $G$, $\chi'(G) = \Delta(G)$.

**Therefore:** All bipartite graphs are Class 1.

---

**Proof Sketch:**

Use Hall's Marriage Theorem or network flow.

**Key idea:** Can decompose edges into Δ perfect matchings.

---

**Example:** K₃,₃

Δ = 3.

**By Kőnig:** χ'(K₃,₃) = 3.

**Verification:** Can color with 3 colors (each color forms a perfect matching). ✓

---

## Section 18.3 - Síkgráfok Színezése (Coloring Planar Graphs)

---

### Exercise 18.3.1 - State the Four Color Theorem

**Problem:** State the Four Color Theorem.

**Solution:**

**Four Color Theorem (Appel & Haken, 1976):**

Every planar graph is 4-colorable.

**Formally:** If $G$ is planar, then $\chi(G) \leq 4$.

---

**Historical Note:**

- Conjectured by Francis Guthrie (1852)
- Many false proofs proposed
- First proved by Appel and Haken (1976)
- Used computer to check 1,936 configurations
- First major theorem proved with computer assistance
- Simplified proof by Robertson et al. (1996): 633 configurations

---

### Exercise 18.3.2 - State the Five Color Theorem

**Problem:** State the Five Color Theorem.

**Solution:**

**Five Color Theorem (Heawood, 1890):**

Every planar graph is 5-colorable.

**Formally:** If $G$ is planar, then $\chi(G) \leq 5$.

---

**Proof:** See Exercise 18.3.4 (complete proof using Kempe chains).

---

**Note:** The Five Color Theorem has a short, elegant proof.

The Four Color Theorem is much harder and requires computer assistance.

---

### Exercise 18.3.3 - Prove: Every Planar Graph Has a Vertex of Degree ≤ 5

**Problem:** Prove that every planar graph has a vertex of degree at most 5.

**Solution:**

**Theorem:** Every planar graph has a vertex of degree at most 5.

---

**Proof by Contradiction:**

Assume every vertex has degree at least 6.

**Step 1:** By Handshaking Lemma:
$$\sum_{v \in V} \deg(v) = 2E$$

If every vertex has degree ≥ 6:
$$2E \geq 6V$$
$$E \geq 3V$$

---

**Step 2:** By Euler's formula edge bound for planar graphs:
$$E \leq 3V - 6$$

---

**Contradiction:**
$$3V \leq E \leq 3V - 6$$
$$3V \leq 3V - 6$$
$$0 \leq -6$$

**Impossible!**

---

**Therefore:** There must be at least one vertex with degree ≤ 5. ∎

---

### Exercise 18.3.4 - Prove the Five Color Theorem

**Problem:** Prove that every planar graph is 5-colorable.

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

---

**Step 1:** By Exercise 18.3.3, $G$ has a vertex $v$ with $\deg(v) \leq 5$.

---

**Step 2:** Remove $v$ to get $G' = G - v$.

$G'$ is planar with $V-1$ vertices.

By inductive hypothesis, $G'$ is 5-colorable.

---

**Step 3:** Try to extend the coloring to $v$.

---

**Case 1:** $\deg(v) \leq 4$ or neighbors use ≤ 4 colors.

At least one color is unused among neighbors.

Assign that color to $v$. ✓

---

**Case 2:** $\deg(v) = 5$ and all 5 neighbors have different colors.

Let neighbors be $v_1, v_2, v_3, v_4, v_5$ in cyclic order with colors 1, 2, 3, 4, 5.

---

**Kempe chain argument:**

Consider the subgraph $H_{13}$ induced by vertices with colors 1 and 3.

---

**Subcase 2a:** $v_1$ and $v_3$ are in different components of $H_{13}$.

Swap colors 1 and 3 in $v_1$'s component.

Now $v_1$ has color 3, and color 1 is free for $v$. ✓

---

**Subcase 2b:** $v_1$ and $v_3$ are in the same component of $H_{13}$.

There's a path from $v_1$ to $v_3$ using only colors 1 and 3.

This path, together with $v$, forms a cycle separating $v_2$ from $v_4$.

---

Consider the subgraph $H_{24}$ induced by vertices with colors 2 and 4.

$v_2$ and $v_4$ are in different components of $H_{24}$ (separated by the cycle).

Swap colors 2 and 4 in $v_2$'s component.

Now color 2 is free for $v$. ✓

---

**Therefore:** $G$ is 5-colorable. ∎

---

## Section 18.4 - Kritikus Gráfok (Critical Graphs)

---

### Exercise 18.4.1 - Define k-Critical Graph

**Problem:** Define critical graphs.

**Solution:**

**Definition:**

A graph $G$ is **k-critical** if:
1. $\chi(G) = k$
2. For every proper subgraph $H \subset G$, $\chi(H) < k$

**Equivalently:** $\chi(G - v) < \chi(G)$ for all vertices $v \in V$.

---

**Examples:**
- $K_k$ is k-critical
- $C_n$ (n odd) is 3-critical
- Odd cycles are the only 3-critical graphs besides $K_3$

---

### Exercise 18.4.2 - Prove: Kₖ is k-Critical

**Problem:** Prove that complete graphs are critical.

**Solution:**

**Theorem:** $K_k$ is k-critical.

---

**Proof:**

**Part 1:** $\chi(K_k) = k$.

(Proved in Exercise 18.1.2)

---

**Part 2:** For any vertex $v$, $\chi(K_k - v) < k$.

$K_k - v \cong K_{k-1}$.

$\chi(K_{k-1}) = k-1 < k$. ✓

---

**Therefore:** $K_k$ is k-critical. ∎

---

### Exercise 18.4.3 - Prove: δ(G) ≥ χ(G) - 1 for Critical Graphs

**Problem:** Prove the minimum degree bound for critical graphs.

**Solution:**

**Theorem:** If $G$ is k-critical, then $\delta(G) \geq k - 1$.

---

**Proof by Contradiction:**

Assume there exists a vertex $v$ with $\deg(v) < k - 1$.

---

Since $G$ is k-critical: $\chi(G - v) = k - 1$.

Let $c$ be a (k-1)-coloring of $G - v$.

---

$v$ has at most $k - 2$ neighbors.

At most $k - 2$ colors are forbidden for $v$.

At least one color from $\{1, 2, \ldots, k-1\}$ is available.

Assign that color to $v$.

---

This gives a (k-1)-coloring of $G$.

**Contradiction:** $\chi(G) = k$.

---

**Therefore:** $\delta(G) \geq k - 1$. ∎

---

## Section 18.5 - Színezési Algoritmusok (Coloring Algorithms)

---

### Exercise 18.5.1 - Greedy Coloring Algorithm

**Problem:** Understand the greedy coloring algorithm.

**Solution:**

**Greedy Coloring Algorithm:**

```
Input: Graph G = (V, E), vertex ordering v₁, v₂, ..., vₙ
Output: Proper coloring c

For i = 1 to n:
  c(vᵢ) = smallest color not used by neighbors of vᵢ
```

---

**Time Complexity:** O(V + E)

---

**Quality:**

Depends on vertex ordering!

**Best case:** Optimal coloring

**Worst case:** Can use arbitrarily many more colors than optimal

---

**Example (bad ordering):**

```
    a         b         c
    |         |         |
    d---------e---------f
```

Order: d, e, f, a, b, c

Greedy uses 4 colors, but χ(G) = 2.

---

### Exercise 18.5.2 - Welsh-Powell Algorithm

**Problem:** Understand the Welsh-Powell algorithm.

**Solution:**

**Welsh-Powell Algorithm:**

```
1. Order vertices by decreasing degree
2. Apply greedy coloring with this ordering
```

---

**Time Complexity:** O(V log V + E)

---

**Quality:**

Better than arbitrary greedy ordering.

Often gives good results in practice.

---

**Example:**

```
    a (degree 4)
   /|\
  b c d (degree 2)
   \|/
    e (degree 4)
```

Order: a, e, b, c, d (by degree)

Greedy with this ordering uses fewer colors.

---

### Exercise 18.5.3 - DSatur Algorithm

**Problem:** Understand the DSatur algorithm.

**Solution:**

**DSatur Algorithm (Brélaz, 1979):**

```
1. Start with uncolored graph
2. While uncolored vertices remain:
   a. Choose vertex with highest "saturation degree"
      (number of different colors among neighbors)
   b. Break ties by degree
   c. Color with smallest available color
```

---

**Time Complexity:** O(V²)

---

**Quality:**

Often better than Welsh-Powell.

Good practical performance.

---

## Section 18.6 - Alkalmazások (Applications)

---

### Exercise 18.6.1 - Scheduling Problems

**Problem:** Apply graph coloring to scheduling.

**Solution:**

**Application:** Exam scheduling.

**Model:**
- Vertices: Exams
- Edges: Two exams share students (conflict)
- Colors: Time slots

**Goal:** Minimize number of time slots.

**Solution:** Find χ(G).

---

**Example:**

```
Exams: Math, Physics, Chem, Bio, CS
Conflicts: Math-Physics, Math-Chem, Physics-Chem, Bio-CS
```

**Graph:**
```
  Math----Physics
   |      /
   |     /
  Chem   Bio----CS
```

**Chromatic number:** χ(G) = 3

**Schedule:**
- Slot 1: Math, Bio
- Slot 2: Physics, CS
- Slot 3: Chem

---

### Exercise 18.6.2 - Register Allocation

**Problem:** Apply graph coloring to register allocation.

**Solution:**

**Application:** Compiler optimization.

**Model:**
- Vertices: Variables
- Edges: Variables live at same time (interfere)
- Colors: CPU registers

**Goal:** Minimize registers used.

**Solution:** Find χ(G).

If χ(G) > available registers, spill some variables to memory.

---

### Exercise 18.6.3 - Sudoku as Coloring

**Problem:** Model Sudoku as a graph coloring problem.

**Solution:**

**Sudoku:**

9×9 grid, some cells pre-filled.

**Constraints:**
- Each row has 1-9
- Each column has 1-9
- Each 3×3 box has 1-9

---

**Graph model:**
- Vertices: 81 cells
- Edges: Two cells in same row/column/box
- Pre-filled cells: Pre-colored vertices

**Chromatic number:** χ(G) = 9

---

**Solving Sudoku:**

Find a proper 9-coloring extending the pre-coloring.

---

*Continued for remaining exercises in Chapter 18...*
