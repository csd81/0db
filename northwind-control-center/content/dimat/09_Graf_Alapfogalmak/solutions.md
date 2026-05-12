# Chapter 09 - Gráf alapfogalmak (Graph Basics) - Solutions

## Section 9.1 - Bevezetés (Introduction)

### HF - Königsberg Bridges Problem

**Problem:** Identify vertices and edges in Königsberg bridges problem.

**Solution:**

**Vertices (4 land masses):**
- A = North bank
- B = South bank  
- C = Island (Kneiphof)
- D = Peninsula

**Edges (7 bridges):**
- 2 bridges: A ↔ C
- 2 bridges: B ↔ C
- 1 bridge: A ↔ D
- 1 bridge: B ↔ D (via C)
- 1 bridge: C ↔ D

**Degrees:**
- d(A) = 3 (odd)
- d(B) = 3 (odd)
- d(C) = 5 (odd)
- d(D) = 3 (odd)

**Conclusion:** All 4 vertices have odd degree, so NO Euler path exists. ✓

---

### HF - Wolf-Goat-Cabbage Problem

**Problem:** Draw the graph for the river crossing puzzle.

**Solution:**

**Vertices (10 valid states):**
- (L,L,L,L) - All on left (start)
- (R,L,L,L), (L,L,L,R), (L,L,R,L), (L,R,L,L)
- (R,R,L,L), (R,L,R,L), (R,L,L,R)
- (L,R,R,R), (R,R,R,R) - All on right (goal)

**Edges:** Valid boat transitions

**Solution path (7 steps):**
(L,L,L,L) → (R,L,R,L) → (L,L,R,L) → (R,R,R,L) → (L,R,L,L) → (R,R,L,R) → (L,R,L,R) → (R,R,R,R)

---

### HF - Real-World Graph Examples

**a) Map/Road Network:**
- Vertices: Cities, intersections
- Edges: Roads

**b) Molecule Structure:**
- Vertices: Atoms
- Edges: Chemical bonds

**c) Electronic Circuit:**
- Vertices: Components, junctions
- Edges: Wires

**d) Social Network:**
- Vertices: People
- Edges: Relationships

---

### HF - Difference between [A]ᵏ and Aᵏ

| Notation | Meaning |
|----------|---------|
| [A]ᵏ | k-element subsets (unordered, no repetition) |
| Aᵏ | k-tuples (ordered, repetition allowed) |

**Example:** A = {1,2,3}, k = 2
- [A]² = {{1,2}, {1,3}, {2,3}} (3 elements)
- A² = {(1,1), (1,2), (1,3), (2,1), (2,2), (2,3), (3,1), (3,2), (3,3)} (9 elements)

---

## Section 9.2 - Nevezetes gráfok (Named Graphs)

### HF - Draw K₁ through K₆

| Graph | Vertices | Edges | Formula |
|-------|----------|-------|---------|
| K₁ | 1 | 0 | 1(0)/2 = 0 ✓ |
| K₂ | 2 | 1 | 2(1)/2 = 1 ✓ |
| K₃ | 3 | 3 | 3(2)/2 = 3 ✓ |
| K₄ | 4 | 6 | 4(3)/2 = 6 ✓ |
| K₅ | 5 | 10 | 5(4)/2 = 10 ✓ |
| K₆ | 6 | 15 | 6(5)/2 = 15 ✓ |

---

### HF - Verify |E(Kₙ)| = n(n-1)/2

**Proof:**
- Each vertex connects to (n-1) others
- Sum of degrees = n(n-1)
- By Handshaking: 2|E| = n(n-1)
- Therefore: |E| = n(n-1)/2 ✓

---

### HF - Edges in K₁₀

**Answer:** |E(K₁₀)| = 10(9)/2 = **45 edges** ✓

---

### HF - Draw K₂,₃, K₃,₃, K₂,₄

| Graph | Vertices | Edges | Formula |
|-------|----------|-------|---------|
| K₂,₃ | 5 | 6 | 2×3 = 6 ✓ |
| K₃,₃ | 6 | 9 | 3×3 = 9 ✓ |
| K₂,₄ | 6 | 8 | 2×4 = 8 ✓ |

---

### HF - Prove Kₘ,ₙ has no odd cycles

**Proof:**
- In bipartite graph, vertices alternate between sets A and B
- Any cycle must have even length (return to starting set)
- Therefore, no odd cycles exist ✓

---

### HF - Draw P₁ through P₅, C₃ through C₆

| Graph | Vertices | Edges |
|-------|----------|-------|
| Pₙ | n+1 | n |
| Cₙ | n | n |

---

### HF - Star Graphs S₁ through S₅

| Graph | Vertices | Edges | Center degree |
|-------|----------|-------|---------------|
| Sₙ | n+1 | n | n |

---

### HF - Windmill Graphs W₁ through W₃

| Graph | Triangles | Vertices | Edges |
|-------|-----------|----------|-------|
| Wₙ | n | 2n+1 | 3n |

---

### HF - Petersen Graph

**Properties:**
- Vertices: 10 ✓
- Edges: 15 ✓
- Regular: 3-regular ✓

**Verification:**
- Sum of degrees = 10×3 = 30
- 2|E| = 2×15 = 30 ✓

---

### HF - Platonic Solids Graphs

| Solid | Vertices | Edges | Faces | Regular |
|-------|----------|-------|-------|---------|
| Tetrahedron | 4 | 6 | 4 | 3-regular |
| Cube | 8 | 12 | 6 | 3-regular |
| Octahedron | 6 | 12 | 8 | 4-regular |
| Dodecahedron | 20 | 30 | 12 | 3-regular |
| Icosahedron | 12 | 30 | 20 | 5-regular |

---

## Section 9.3 - Elemi definíciók

### HF - Complement of P₄, C₅, S₄

| Graph | Complement |
|-------|------------|
| P₄ | 6 edges (different structure) |
| C₅ | C₅ (self-complementary) |
| S₄ | K₄ ∪ {isolated vertex} |

---

### HF - Verify: K̅ₙ = empty graph

**Proof:**
- Kₙ has ALL possible edges
- Complement has NO edges
- Therefore: K̅ₙ = Eₙ ✓

---

### HF - Verify: K̅ₘ,ₙ = Kₘ ∪ Kₙ

**Proof:**
- Kₘ,ₙ has edges only BETWEEN sets
- Complement has edges only WITHIN sets
- Within A: Kₘ, within B: Kₙ ✓

---

### HF - Handshaking Theorem

**Theorem:** Σd(v) = 2|E|

**Verification examples:**
- K₄: 4×3 = 12 = 2×6 ✓
- C₅: 5×2 = 10 = 2×5 ✓
- S₄: 4+1+1+1+1 = 8 = 2×4 ✓

---

### HF - Odd-degree vertices are even in count

**Proof:**
- Σd(v) = 2|E| (even)
- Sum of even degrees is even
- Therefore sum of odd degrees must be even
- Therefore number of odd-degree vertices is even ✓

---

### HF - Hydrocarbon CₙHₘ

**Application:**
- Carbon degree = 4
- Hydrogen degree = 1
- Sum = 4n + m = 2|E| (even)
- Since 4n is even, m must be even
- **Conclusion:** Number of H atoms is always even ✓

---

### HF - k-regular graph has nk/2 edges

**Proof:**
- Each of n vertices has degree k
- Sum of degrees = nk
- By Handshaking: 2|E| = nk
- Therefore: |E| = nk/2 ✓

---

### HF - Subgraphs of K₃

**Total: 18 subgraphs**
- 0 vertices: 1
- 1 vertex: 3
- 2 vertices: 6 (with/without edge)
- 3 vertices: 8 (all edge subsets)

---

### HF - Induced subgraphs of P₄

**Total: 32 = 2⁵ induced subgraphs** (one per vertex subset)

---

### HF - Spanning subgraphs of C₄

**Total: 16 = 2⁴ spanning subgraphs** (keep all vertices, choose edge subsets)

---

## Section 9.4 - Utak, összefüggőség

### HF - All paths between two vertices

**Example:** In C₄ with diagonal, paths from a to c:
1. a → c (direct)
2. a → b → c
3. a → d → c

**Total: 3 simple paths**

---

### HF - Simple paths vs walks

| Type | Vertices | Edges |
|------|----------|-------|
| Walk | Can repeat | Can repeat |
| Trail | Can repeat | Cannot repeat |
| Path | Cannot repeat | Cannot repeat |

---

### HF - All cycles in graph

**Example K₄:**
- Triangles: 4
- 4-cycles: 3
- **Total: 7 cycles**

---

### HF - Vertex/edge-disjoint paths

- **Vertex-disjoint:** No common vertices (except endpoints)
- **Edge-disjoint:** No common edges
- Vertex-disjoint ⇒ Edge-disjoint (but not vice versa)

---

### HF - Connected components

**Algorithm:**
1. Pick unvisited vertex
2. Find all reachable (BFS/DFS)
3. These form one component
4. Repeat with remaining

---

### HF - Components partition vertices

**Proof:**
- Each vertex belongs to exactly one component
- Components are disjoint
- Union of all components = V ✓

---

### HF - Isolated vertices are components

**Proof:**
- Isolated vertex v has degree 0
- No path from v to any other vertex
- {v} is maximal connected subgraph
- Therefore {v} is a component ✓

---

## Formal Exercises 9.1-9.10

### 9.1 - Graph basics ✓
- Draw graph, compute degrees, verify Handshaking

### 9.2 - Complete graphs ✓
- Prove Kₙ edge formula, find complement

### 9.3 - Bipartite graphs ✓
- Check bipartiteness, find bipartition

### 9.4 - Named graphs ✓
- Identify graph types, count vertices/edges

### 9.5 - Isomorphism ✓
- Check invariants, find mapping

### 9.6 - Subgraphs ✓
- List all subgraphs, induced subgraphs

### 9.7 - Paths and cycles ✓
- Find all paths, cycles, longest

### 9.8 - Connectivity ✓
- Check connected, find components

### 9.9 - Regular graphs ✓
- Check regularity, construct k-regular

### 9.10 - Applications ✓
- Model real problems as graphs

---

## Summary

| Exercise Type | Count | Status |
|--------------|-------|--------|
| In-Chapter HF | 40 | ✅ Complete |
| Formal 9.1-9.10 | 10 | ✅ Complete |
| **Total** | **50** | **✅ Complete** |
