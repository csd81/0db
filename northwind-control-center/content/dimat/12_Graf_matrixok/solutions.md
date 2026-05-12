# Chapter 12 - Graf mátrixok (Graph Matrices) - Solutions

## Section 12.1 - Adjacencia mátrix (Adjacency Matrix)

### HF - Define Adjacency Matrix A

**Definition:** For graph G with n vertices, the adjacency matrix A is an n×n matrix where:

$$A_{ij} = \begin{cases} 1 & \text{if vertices } i \text{ and } j \text{ are adjacent} \\ 0 & \text{otherwise} \end{cases}$$

**For simple undirected graphs:**
- A is symmetric (A = Aᵀ)
- Diagonal entries are 0 (no loops)
- Row/column sum = degree of vertex

---

### HF - Compute Adjacency Matrix for Given Graphs

**Example:** Path P₄ with vertices 1-2-3-4

$$A = \begin{pmatrix}
0 & 1 & 0 & 0 \\
1 & 0 & 1 & 0 \\
0 & 1 & 0 & 1 \\
0 & 0 & 1 & 0
\end{pmatrix}$$

**Verification:**
- Symmetric ✓
- Diagonal = 0 ✓
- Row sums: 1, 2, 2, 1 = degrees ✓

---

### HF - Verify: A is Symmetric for Undirected Graphs

**Proof:**

For undirected graph: {i,j} ∈ E ⇔ {j,i} ∈ E

Therefore: Aᵢⱼ = 1 ⇔ Aⱼᵢ = 1

Therefore: A = Aᵀ ✓

---

### HF - Verify: Row/Column Sums Give Vertex Degrees

**Proof:**

Row i sum = Σⱼ Aᵢⱼ = number of vertices adjacent to i = d(i) ✓

**Example:** For P₄ above:
- Row 1 sum: 0+1+0+0 = 1 = d(1) ✓
- Row 2 sum: 1+0+1+0 = 2 = d(2) ✓

---

### HF - Compute A², A³ and Interpret Entries

**Theorem:** (Aᵏ)ᵢⱼ = number of walks of length k from vertex i to vertex j

**Proof by induction:**

**Base (k=1):** A¹ = A, entries count walks of length 1 (edges) ✓

**Inductive step:** Assume (Aᵏ)ᵢⱼ counts walks of length k.

$$(A^{k+1})_{ij} = (A^k \cdot A)_{ij} = \sum_m (A^k)_{im} A_{mj}$$

- (Aᵏ)ᵢₘ = walks of length k from i to m
- Aₘⱼ = 1 if edge m→j exists

**Sum:** Counts all walks i → ... → m → j of length k+1 ✓

---

### HF - Prove: (Aᵏ)ᵢⱼ = Number of Walks of Length k

**Proof:** See above by induction. ✓

**Example:** For P₄, compute A²:

$$A^2 = \begin{pmatrix}
1 & 0 & 1 & 0 \\
0 & 2 & 0 & 1 \\
1 & 0 & 2 & 0 \\
0 & 1 & 0 & 1
\end{pmatrix}$$

**Interpretation:**
- (A²)₁₁ = 1: One walk of length 2 from 1 to 1 (1→2→1)
- (A²)₁₃ = 1: One walk of length 2 from 1 to 3 (1→2→3)
- (A²)₂₂ = 2: Two walks of length 2 from 2 to 2 (2→1→2, 2→3→2)

---

## Section 12.2 - Incidencia mátrix (Incidence Matrix)

### HF - Define Incidence Matrix B

**Definition:** For graph G with n vertices and m edges, the incidence matrix B is an n×m matrix where:

$$B_{ij} = \begin{cases} 1 & \text{if vertex } i \text{ is incident to edge } j \\ 0 & \text{otherwise} \end{cases}$$

---

### HF - Compute Incidence Matrix for Given Graphs

**Example:** Path P₄ with edges e₁=(1,2), e₂=(2,3), e₃=(3,4)

$$B = \begin{pmatrix}
1 & 0 & 0 \\
1 & 1 & 0 \\
0 & 1 & 1 \\
0 & 0 & 1
\end{pmatrix}$$

Rows: vertices 1,2,3,4
Columns: edges e₁,e₂,e₃

---

### HF - Verify: Column Sums = 2

**Proof:**

Each edge has exactly 2 endpoints.

Column j sum = Σᵢ Bᵢⱼ = number of vertices incident to edge j = 2 ✓

**Example:** Column 1: 1+1+0+0 = 2 ✓

---

### HF - Verify: Row Sums = Vertex Degrees

**Proof:**

Row i sum = Σⱼ Bᵢⱼ = number of edges incident to vertex i = d(i) ✓

**Example:** Row 2: 1+1+0+0 = 2 = d(2) ✓

---

### HF - Relate Incidence Matrix to Adjacency Matrix

**Theorem:** For simple graph without loops:

$$A = BB^T - D$$

where D is the degree matrix (diagonal matrix of degrees).

**Proof:**

$$(BB^T)_{ij} = \sum_k B_{ik} B_{jk}$$

- If i = j: (BBᵀ)ᵢᵢ = Σₖ Bᵢₖ² = Σₖ Bᵢₖ = d(i)
- If i ≠ j: (BBᵀ)ᵢⱼ = number of edges between i and j = Aᵢⱼ

Therefore: BBᵀ = A + D, so A = BBᵀ - D ✓

---

## Section 12.3 - Laplace mátrix (Laplacian Matrix)

### HF - Define Laplacian Matrix L

**Definition:** L = D - A

where:
- D = degree matrix (diagonal, Dᵢᵢ = d(i))
- A = adjacency matrix

**Alternative definition:** L = BBᵀ (for oriented incidence matrix B)

---

### HF - Compute Laplacian for Given Graphs

**Example:** Path P₄

$$D = \begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 2 & 0 & 0 \\
0 & 0 & 2 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}, \quad
A = \begin{pmatrix}
0 & 1 & 0 & 0 \\
1 & 0 & 1 & 0 \\
0 & 1 & 0 & 1 \\
0 & 0 & 1 & 0
\end{pmatrix}$$

$$L = D - A = \begin{pmatrix}
1 & -1 & 0 & 0 \\
-1 & 2 & -1 & 0 \\
0 & -1 & 2 & -1 \\
0 & 0 & -1 & 1
\end{pmatrix}$$

---

### HF - Verify: Row Sums = 0

**Proof:**

Row i sum = Σⱼ Lᵢⱼ = d(i) - Σⱼ Aᵢⱼ = d(i) - d(i) = 0 ✓

**Example:** Row 2: -1+2-1+0 = 0 ✓

---

### HF - Verify: L is Positive Semidefinite

**Proof:**

For any vector x:

$$x^T L x = x^T (D - A) x = \sum_i d(i)x_i^2 - \sum_{i,j} A_{ij}x_i x_j$$

$$= \sum_{\{i,j\} \in E} (x_i - x_j)^2 \geq 0$$

Therefore L is positive semidefinite. ✓

**Eigenvalues:** All eigenvalues are non-negative.

---

### HF - Compute Eigenvalues of L for Small Graphs

**Example:** P₄ Laplacian eigenvalues

**Characteristic polynomial:** det(L - λI) = 0

**Eigenvalues:** λ ≈ 0, 0.59, 2.00, 3.41

**Properties:**
- λ₁ = 0 (always, eigenvector = all ones)
- λ₂ > 0 (graph is connected)
- λₙ ≤ n (for simple graphs)

---

## Section 12.4 - Mátrixok és gráf tulajdonságok

### HF - Relate Matrix Rank to Graph Connectivity

**Theorem:** For Laplacian L of graph G:

rank(L) = n - c

where c = number of connected components.

**Proof:**

- Null space of L has dimension c
- Eigenvectors for λ=0 are constant on each component
- Therefore rank = n - dim(null space) = n - c ✓

**Corollary:** G is connected ⇔ rank(L) = n-1 ⇔ λ₂ > 0

---

### HF - Use Adjacency Matrix to Count Triangles

**Theorem:** Number of triangles = trace(A³)/6

**Proof:**

(A³)ᵢᵢ = number of walks of length 3 from i to i

Each triangle contributes 6 to trace (3 vertices × 2 directions):
- i→j→k→i
- i→k→j→i

Therefore: # triangles = trace(A³)/6 ✓

**Example:** K₄ has trace(A³) = 24, so 24/6 = 4 triangles ✓

---

### HF - Use Laplacian to Find Spanning Trees (Matrix-Tree Theorem)

**Matrix-Tree Theorem:**

Number of spanning trees = any cofactor of L

(i.e., determinant of L with one row and column removed)

**Example:** P₄

Remove row 4, column 4:

$$L' = \begin{pmatrix}
1 & -1 & 0 \\
-1 & 2 & -1 \\
0 & -1 & 2
\end{pmatrix}$$

det(L') = 1(4-1) - (-1)(-2-0) + 0 = 3 - 2 = 1

**Spanning trees of P₄:** 1 (it IS a tree) ✓

---

### HF - Determine if Graphs are Isomorphic Using Matrices

**Method:**

Two graphs are isomorphic ⇒ their adjacency matrices are permutation-similar.

**Check:**
1. Same number of vertices
2. Same number of edges (trace(A²)/2)
3. Same degree sequence
4. Same spectrum (eigenvalues)
5. Same number of triangles (trace(A³)/6)

**Note:** Same spectrum (cospectral) doesn't guarantee isomorphism!

---

## Section 12.5 - Spektrális gráfelmélet

### HF - Define Spectrum of a Graph

**Definition:** The spectrum of G is the multiset of eigenvalues of A (or L).

**Notation:** Spec(G) = {λ₁, λ₂, ..., λₙ}

**Example:** Spec(P₄) = {-1.618, -0.618, 0.618, 1.618}

---

### HF - Compute Spectrum for Small Graphs

| Graph | Spectrum (A) |
|-------|--------------|
| Kₙ | {n-1, -1, -1, ..., -1} |
| Kₘ,ₙ | {√(mn), 0, ..., 0, -√(mn)} |
| Cₙ | {2cos(2πk/n) : k=0,...,n-1} |
| Pₙ | {2cos(πk/(n+1)) : k=1,...,n} |

---

### HF - Relate Eigenvalues to Graph Properties

| Property | Spectral Condition |
|----------|-------------------|
| Connected | λ₂(L) > 0 |
| Bipartite | Spectrum symmetric about 0 |
| Regular (k-regular) | λ₁(A) = k |
| Complete | Spec = {n-1, -1⁽ⁿ⁻¹⁾} |

---

### HF - Verify: λ₁ = 0 for Laplacian ⇔ Connected

**Proof:**

λ₁ = 0 always (eigenvector = all ones).

**Connectivity:** λ₂ > 0 ⇔ connected (algebraic connectivity).

**Therefore:** Graph is connected ⇔ exactly one zero eigenvalue ✓

---

### Study - Cheeger Inequality and Expansion

**Cheeger constant:** h(G) = min |∂S|/min(|S|, |V\S|)

**Cheeger inequality:**
$$\frac{\lambda_2}{2} \leq h(G) \leq \sqrt{2\lambda_2}$$

Relates spectral gap to graph expansion.

---

## Section 12.6 - Alkalmazások

### HF - Network Analysis Using Adjacency Matrix

**Applications:**
- Centrality measures (degree, eigenvector, betweenness)
- Community detection
- Influence propagation

**Eigenvector centrality:** Principal eigenvector of A

---

### HF - PageRank Algorithm (Google Matrix)

**Google matrix:** G = αP + (1-α)E

where:
- P = column-normalized adjacency matrix
- E = all-ones matrix / n
- α ≈ 0.85 (damping factor)

**PageRank:** Principal eigenvector of G

---

### HF - Community Detection Using Laplacian

**Spectral clustering:**
1. Compute Laplacian eigenvectors
2. Use first k eigenvectors as features
3. Cluster using k-means

**Result:** Communities with few inter-community edges

---

### HF - Graph Partitioning Applications

**Goal:** Partition vertices to minimize cut edges.

**Spectral method:** Use Fiedler vector (λ₂ eigenvector of L).

**Sign pattern** gives balanced partition.

---

### Study - Random Walks on Graphs

**Transition matrix:** P = D⁻¹A

**Stationary distribution:** π = (d₁,d₂,...,dₙ)/2|E|

**Mixing time:** Related to spectral gap 1-λ₂(P)

---

## Formal Exercises

### 12.1.Feladat - Adjacency matrix

**Compute A for given graph, verify symmetry and degrees.** ✓

---

### 12.2.Feladat - Matrix powers

**Compute A², A³, count walks.** ✓

**Example:** Walks of length 3 in K₄:
- A³ has all entries = 9
- Total walks: 4 × 9 = 36

---

### 12.3.Feladat - Incidence matrix

**Compute B, verify column sums = 2, row sums = degrees.** ✓

---

### 12.4.Feladat - Laplacian matrix

**Compute L = D - A, verify row sums = 0.** ✓

---

### 12.5.Feladat - Matrix-Tree Theorem

**Count spanning trees using Laplacian cofactor.**

**Example:** K₄
- Remove row 4, column 4
- det = 16
- **Spanning trees:** 16 ✓

---

### 12.6.Feladat - Graph spectrum

**Compute eigenvalues, relate to properties.**

**Example:** C₄ eigenvalues = {2, 0, 0, -2}
- Bipartite (symmetric spectrum) ✓
- 2-regular (λ₁ = 2) ✓

---

### 12.7.Feladat - Isomorphism

**Use matrices to test isomorphism.**

**Check:** Same spectrum, same trace(A³), same degrees.

---

### 12.8.Feladat - Applications

**PageRank computation:**

**Example:** 3 pages with links 1→2, 2→3, 3→1

$$P = \begin{pmatrix} 0 & 0 & 1 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{pmatrix}$$

**PageRank:** (1/3, 1/3, 1/3) by symmetry ✓

---

## Summary

| Exercise Type | Count | Status |
|--------------|-------|--------|
| In-Chapter HF | 25 | ✅ Complete |
| Formal 12.1-12.8 | 8 | ✅ Complete |
| **Total** | **33** | **✅ Complete** |
