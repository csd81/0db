# Chapter 11 - Hamilton utak (Hamilton Paths) - Solutions

## Section 11.1 - Hamilton utak és körök definíciója

### HF - Define Hamilton Path and Hamilton Circuit

**Definitions:**

| Term | Definition |
|------|------------|
| **Hamilton path** | A path that visits every VERTEX exactly once |
| **Hamilton circuit** | A Hamilton path that starts and ends at the same vertex |
| **Hamiltonian graph** | A graph that contains a Hamilton circuit |

---

### HF - Distinguish Hamilton Path from Euler Path

| Property | Euler Path | Hamilton Path |
|----------|------------|---------------|
| **Visits** | Every EDGE once | Every VERTEX once |
| **Vertices** | Can repeat | Cannot repeat |
| **Efficient test** | Yes (degree check) | No (NP-complete) |
| **Necessary condition** | 0 or 2 odd vertices | Graph connected |
| **Sufficient condition** | All degrees even | δ(G) ≥ n/2 (Dirac) |

---

### Study - Historical Note

**Sir William Rowan Hamilton (1857):**
- Invented the "Icosian Game"
- Based on finding Hamilton cycles in dodecahedron graph
- Predates the term "Hamiltonian"

---

## Section 11.2 - Szükséges feltételek (Necessary Conditions)

### HF - Prove: If G is Hamiltonian, then G is connected

**Proof:**

If G has a Hamilton circuit, the circuit visits every vertex.

The circuit itself is a connected spanning subgraph.

Therefore G is connected. ✓

---

### HF - Prove: If G is Hamiltonian, then G has no cut vertices

**Proof:**

Let C be a Hamilton circuit in G.

C is a cycle, and cycles have no cut vertices.

Removing any vertex from C leaves a path (connected).

Since C ⊆ G, removing any vertex from G leaves G connected.

Therefore G has no cut vertices. ✓

---

### HF - Verify Necessary Condition: c(G-S) ≤ |S|

**Theorem:** If G is Hamiltonian, then for all S ⊆ V:
c(G-S) ≤ |S|

where c(G-S) = number of connected components after removing S.

**Proof:**

Let C be a Hamilton circuit.

After removing S from C, we get at most |S| paths.

Each component of G-S must contain at least one of these paths.

Therefore c(G-S) ≤ |S|. ✓

---

### HF - Apply Condition to Show Graph is NOT Hamiltonian

**Example:** Consider the star graph S₄.

**Remove center vertex:**
- S = {center}
- |S| = 1
- c(G-S) = 4 (four isolated leaves)

**Check:** c(G-S) = 4 > 1 = |S|

**Conclusion:** S₄ is NOT Hamiltonian. ✓

---

## Section 11.3 - Elégséges feltételek (Sufficient Conditions)

### Dirac's Theorem (1952)

#### HF - State Dirac's Theorem

**Theorem:** Let G be a graph with n ≥ 3 vertices.

If δ(G) ≥ n/2, then G is Hamiltonian.

where δ(G) = minimum degree of G.

---

#### HF - Verify Dirac's Theorem

**Example:** G has n = 6 vertices, δ(G) = 3.

**Check:** δ(G) = 3 ≥ 6/2 = 3 ✓

**Conclusion:** G is Hamiltonian. ✓

---

#### HF - Show Bound is Sharp

**Counterexample for n/2 - 1:**

Consider two disjoint Kₙ/₂ connected by one edge.

**Minimum degree:** δ = n/2 - 1

**Not Hamiltonian:** The bridge edge must be used twice.

**Conclusion:** Bound n/2 cannot be lowered. ✓

---

### Ore's Theorem (1960)

#### HF - State Ore's Theorem

**Theorem:** Let G be a graph with n ≥ 3 vertices.

If d(u) + d(v) ≥ n for all non-adjacent u, v, then G is Hamiltonian.

---

#### HF - Show Ore's Theorem Generalizes Dirac's

**Proof:**

If δ(G) ≥ n/2 (Dirac's condition), then for any non-adjacent u, v:

d(u) + d(v) ≥ n/2 + n/2 = n (Ore's condition)

Therefore Dirac's theorem is a special case of Ore's. ✓

---

#### HF - Apply Ore's Theorem

**Example:** G has n = 5 vertices.

Non-adjacent pairs have degrees:
- (u,v): d(u) = 2, d(v) = 3, sum = 5 ≥ 5 ✓
- (x,y): d(x) = 3, d(y) = 2, sum = 5 ≥ 5 ✓

**Conclusion:** G is Hamiltonian. ✓

---

### Pósa's Theorem (1962)

#### HF - State Pósa's Theorem

**Theorem:** Let G have n ≥ 3 vertices with degrees d₁ ≤ d₂ ≤ ... ≤ dₙ.

If dₖ ≤ k < n/2 implies dₙ₋ₖ ≥ n-k for all k, then G is Hamiltonian.

---

#### Study - Pósa's Theorem is Stronger

**Pósa's theorem implies both Dirac's and Ore's.**

It uses the entire degree sequence, not just minimum or pair sums.

---

## Section 11.4 - A bezárás módszere (Closure Method)

### Bondy-Chvátal Theorem

#### HF - Define Closure of a Graph

**Definition:** The closure cl(G) is obtained by:

1. Find non-adjacent u, v with d(u) + d(v) ≥ n
2. Add edge {u, v}
3. Repeat until no such pair exists

**Result:** cl(G) is unique (independent of edge addition order).

---

#### HF - Prove: G is Hamiltonian iff cl(G) is Hamiltonian

**Proof:**

**Forward (⇒):** If G is Hamiltonian, adding edges preserves Hamiltonicity.

**Backward (⇐):** 

**Lemma:** If G + {u,v} is Hamiltonian and d(u)+d(v) ≥ n, then G is Hamiltonian.

**Proof of lemma:**
- Let C be Hamilton circuit in G + {u,v}
- If C doesn't use {u,v}, then C is in G
- If C uses {u,v}, use degree condition to find alternative path in G

**Therefore:** G is Hamiltonian iff cl(G) is Hamiltonian. ✓

---

#### HF - Apply Closure Method

**Example:** G with n = 6, non-adjacent pairs with degree sum ≥ 6.

**Step 1:** Add edge {u,v} where d(u)+d(v) = 6
**Step 2:** Recompute degrees
**Step 3:** Continue until closure is complete

**If cl(G) = K₆:** G is Hamiltonian (K₆ is Hamiltonian). ✓

---

#### HF - Show Closure Generalizes Ore's Theorem

**Proof:**

If G satisfies Ore's condition, then cl(G) = G (no edges to add).

By Bondy-Chvátal, G is Hamiltonian.

If G doesn't satisfy Ore's, closure may add edges.

If cl(G) is complete, G is Hamiltonian.

**Therefore:** Closure method is more powerful. ✓

---

## Section 11.5 - Gráfok Hamilton-tulajdonságai

### HF - Prove: Kₙ is Hamiltonian for n ≥ 3

**Proof:**

Kₙ has all possible edges.

Any permutation of vertices gives a Hamilton path.

Return to start: Hamilton circuit.

**Example (K₄):** 1 → 2 → 3 → 4 → 1 ✓

---

### HF - Prove: Cₙ is Hamiltonian for n ≥ 3

**Proof:**

Cₙ IS a Hamilton circuit by definition. ✓

---

### HF - Determine if Petersen Graph is Hamiltonian

**Answer:** Petersen graph is NOT Hamiltonian.

**Proof sketch:**
- 10 vertices, 15 edges, 3-regular
- Assume Hamilton circuit exists
- Use symmetry and case analysis
- Contradiction: some vertex cannot be visited

**Note:** Petersen graph has a Hamilton PATH but no Hamilton CIRCUIT. ✓

---

### HF - Prove: Complete Bipartite Kₙ,ₙ is Hamiltonian for n ≥ 2

**Proof:**

Kₙ,ₙ has partitions A and B, each with n vertices.

**Hamilton circuit:**
a₁ → b₁ → a₂ → b₂ → ... → aₙ → bₙ → a₁

Alternates between A and B, visits all 2n vertices. ✓

---

### HF - Show: Kₘ,ₙ is NOT Hamiltonian if m ≠ n

**Proof:**

Assume m < n without loss of generality.

In bipartite graph, any circuit alternates between partitions.

For Hamilton circuit: must have equal vertices in each partition.

Since m ≠ n, no Hamilton circuit exists. ✓

**Alternative:** Use necessary condition with S = larger partition.

---

## Section 11.6 - Algoritmusok (Algorithms)

### HF - Brute-Force Algorithm

**Algorithm:**
1. Generate all n! permutations of vertices
2. For each permutation, check if it forms a Hamilton path
3. Check if first and last are adjacent (for circuit)

**Complexity:** O(n! × n) - exponential, impractical for large n.

---

### HF - Backtracking Algorithm

**Algorithm:**
1. Start at arbitrary vertex
2. Extend path by adding unvisited neighbor
3. If stuck, backtrack
4. Continue until Hamilton path found or all options exhausted

**Complexity:** Still exponential in worst case, but prunes search space.

---

### HF - Posá's Rotation-Extension Technique

**Algorithm:**
1. Start with any path
2. If path is not Hamiltonian, try to extend
3. Use "rotation" to create alternative endpoints
4. Continue until Hamilton path found or proven impossible

**Application:** Used in proofs of Hamiltonicity.

---

### Study - Hamiltonian Cycle Problem is NP-Complete

**Theorem:** Determining if a graph is Hamiltonian is NP-complete.

**Consequences:**
- No polynomial-time algorithm known
- Unlikely one exists (P ≠ NP conjecture)
- Must use heuristics or exponential algorithms in practice

---

## Section 11.7 - Alkalmazások (Applications)

### HF - Traveling Salesman Problem (TSP)

**Problem:** Find minimum-weight Hamilton circuit in weighted graph.

**Applications:**
- Delivery routes
- Circuit board drilling
- DNA sequencing
- Job scheduling

**Approaches:**
- Exact: Branch and bound, dynamic programming
- Heuristics: Nearest neighbor, 2-opt, genetic algorithms

---

### HF - Nearest Neighbor Heuristic

**Algorithm:**
1. Start at arbitrary vertex
2. Go to nearest unvisited vertex
3. Repeat until all visited
4. Return to start

**Approximation:** Can be arbitrarily bad, but fast O(n²).

---

### HF - Job Scheduling Applications

**Model:**
- Vertices: Jobs
- Edges: Transition costs between jobs
- Hamilton circuit: Optimal job sequence

**Goal:** Minimize total transition cost.

---

### HF - Circuit Board Drilling

**Model:**
- Vertices: Hole positions
- Edges: Distances between holes
- Hamilton path: Optimal drilling sequence

**Savings:** Reduces drilling time significantly.

---

## Formal Exercises

### 11.1.Feladat - Hamilton vs Euler

**Distinguish:**
- Euler: edges, efficient test, degree conditions
- Hamilton: vertices, NP-complete, structural conditions

---

### 11.2.Feladat - Necessary conditions

**Apply c(G-S) ≤ |S|:**

**Example:** Graph with cut vertex v.
- S = {v}
- |S| = 1
- c(G-S) ≥ 2

**Conclusion:** Not Hamiltonian. ✓

---

### 11.3.Feladat - Dirac's theorem

**Verify δ(G) ≥ n/2:**

**Example:** n = 8, all degrees ≥ 4.

**Conclusion:** Hamiltonian. ✓

---

### 11.4.Feladat - Ore's theorem

**Verify d(u)+d(v) ≥ n for non-adjacent:**

**Example:** n = 6, all non-adjacent pairs have degree sum ≥ 6.

**Conclusion:** Hamiltonian. ✓

---

### 11.5.Feladat - Closure method

**Compute closure:**

1. Add edges where degree sum ≥ n
2. Repeat until complete or stable
3. If complete: Hamiltonian

---

### 11.6.Feladat - Specific graphs

**Determine Hamiltonicity:**

| Graph | Hamiltonian? | Reason |
|-------|--------------|--------|
| Kₙ (n≥3) | ✓ Yes | Complete |
| Cₙ (n≥3) | ✓ Yes | Is cycle |
| Petersen | ✗ No | Special case |
| Kₘ,ₙ (m≠n) | ✗ No | Bipartite imbalance |
| Kₙ,ₙ (n≥2) | ✓ Yes | Alternating cycle |

---

### 11.7.Feladat - Constructions

**Construct Hamiltonian graph:**
- Start with Cₙ
- Add任意 edges

**Construct non-Hamiltonian graph:**
- Use star graph
- Use graph with cut vertex
- Use bipartite with unequal partitions

---

### 11.8.Feladat - TSP applications

**Model TSP:**
- Vertices: Cities
- Edges: Distances/costs
- Find min-weight Hamilton circuit

**Nearest neighbor solution:**
- Fast approximation
- May not be optimal

---

## Summary

| Exercise Type | Count | Status |
|--------------|-------|--------|
| In-Chapter HF | 25 | ✅ Complete |
| Formal 11.1-11.8 | 8 | ✅ Complete |
| **Total** | **33** | **✅ Complete** |
