# Chapter 16 - Izomorfia (Graph Isomorphism) - Complete Solutions

## Section 16.1 - Izomorfia definíció (Isomorphism Definition)

---

### Exercise 16.1.1 - Define Graph Isomorphism

**Problem:** Define what it means for two graphs to be isomorphic.

**Solution:**

**Definition:**

Two graphs $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$ are **isomorphic**, written $G_1 \cong G_2$, if there exists a bijection $f: V_1 \to V_2$ such that:

$$\{u, v\} \in E_1 \iff \{f(u), f(v)\} \in E_2$$

for all $u, v \in V_1$.

---

**In words:**

- $f$ is a one-to-one correspondence between vertices
- Adjacency is preserved: adjacent vertices map to adjacent vertices
- Non-adjacency is preserved: non-adjacent vertices map to non-adjacent vertices

---

**Example:**

```
G₁:           G₂:
  a             1
 / \           / \
b---c         3---2
```

**Isomorphism:** $f(a) = 2, f(b) = 1, f(c) = 3$

**Verification:**
- Edges in G₁: {a,b}, {a,c}, {b,c}
- Edges in G₂: {2,1}, {2,3}, {1,3}
- $f$ preserves all adjacencies ✓

---

### Exercise 16.1.2 - Verify Isomorphism is an Equivalence Relation

**Problem:** Prove that graph isomorphism is an equivalence relation.

**Solution:**

**Theorem:** Graph isomorphism is an equivalence relation.

**Proof:**

We need to verify three properties: reflexivity, symmetry, and transitivity.

---

**1. Reflexivity:** $G \cong G$ for all graphs $G$.

**Proof:** The identity map $id: V \to V$ defined by $id(v) = v$ is a bijection that preserves adjacency. ✓

---

**2. Symmetry:** If $G_1 \cong G_2$, then $G_2 \cong G_1$.

**Proof:** If $f: V_1 \to V_2$ is an isomorphism, then $f^{-1}: V_2 \to V_1$ is also a bijection.

For any $x, y \in V_2$:
- $\{x, y\} \in E_2 \iff \{f^{-1}(x), f^{-1}(y)\} \in E_1$ (since $f$ preserves adjacency)

Therefore $f^{-1}$ is an isomorphism from $G_2$ to $G_1$. ✓

---

**3. Transitivity:** If $G_1 \cong G_2$ and $G_2 \cong G_3$, then $G_1 \cong G_3$.

**Proof:** Let $f: V_1 \to V_2$ and $g: V_2 \to V_3$ be isomorphisms.

Consider $h = g \circ f: V_1 \to V_3$.

**h is a bijection:** Composition of bijections is a bijection.

**h preserves adjacency:**
$$\{u, v\} \in E_1 \iff \{f(u), f(v)\} \in E_2 \iff \{g(f(u)), g(f(v))\} \in E_3$$

Therefore $h$ is an isomorphism from $G_1$ to $G_3$. ✓

---

**Conclusion:** Isomorphism is an equivalence relation. ∎

---

### Exercise 16.1.3 - Prove: Isomorphic Graphs Have Same Number of Vertices

**Problem:** Prove that if $G_1 \cong G_2$, then $|V(G_1)| = |V(G_2)|$.

**Solution:**

**Theorem:** If $G_1 \cong G_2$, then $|V_1| = |V_2|$.

**Proof:**

By definition of isomorphism, there exists a bijection $f: V_1 \to V_2$.

A bijection exists between two finite sets if and only if they have the same cardinality.

**Therefore:** $|V_1| = |V_2|$. ∎

---

### Exercise 16.1.4 - Prove: Isomorphic Graphs Have Same Number of Edges

**Problem:** Prove that if $G_1 \cong G_2$, then $|E(G_1)| = |E(G_2)|$.

**Solution:**

**Theorem:** If $G_1 \cong G_2$, then $|E_1| = |E_2|$.

**Proof:**

Let $f: V_1 \to V_2$ be an isomorphism.

Define $F: E_1 \to E_2$ by $F(\{u, v\}) = \{f(u), f(v)\}$.

**F is well-defined:** Since $f$ preserves adjacency, $\{u, v\} \in E_1 \implies \{f(u), f(v)\} \in E_2$.

**F is injective:** If $F(\{u, v\}) = F(\{x, y\})$, then $\{f(u), f(v)\} = \{f(x), f(y)\}$.

Since $f$ is injective, $\{u, v\} = \{x, y\}$.

**F is surjective:** For any $\{a, b\} \in E_2$, since $f$ is surjective, there exist $u, v \in V_1$ with $f(u) = a, f(v) = b$.

Since $f^{-1}$ preserves adjacency, $\{u, v\} \in E_1$ and $F(\{u, v\}) = \{a, b\}$.

**Therefore:** $F$ is a bijection between $E_1$ and $E_2$.

**Therefore:** $|E_1| = |E_2|$. ∎

---

### Exercise 16.1.5 - Prove: Isomorphic Graphs Have Same Degree Sequence

**Problem:** Prove that isomorphic graphs have the same degree sequence.

**Solution:**

**Theorem:** If $G_1 \cong G_2$, then they have the same degree sequence.

**Proof:**

Let $f: V_1 \to V_2$ be an isomorphism.

**Claim:** For any $v \in V_1$, $\deg_{G_1}(v) = \deg_{G_2}(f(v))$.

**Proof of claim:**

Let $N_1(v) = \{u \in V_1 : \{u, v\} \in E_1\}$ be the neighbors of $v$ in $G_1$.

Let $N_2(f(v)) = \{w \in V_2 : \{w, f(v)\} \in E_2\}$ be the neighbors of $f(v)$ in $G_2$.

**Claim:** $f$ restricts to a bijection $N_1(v) \to N_2(f(v))$.

- If $u \in N_1(v)$, then $\{u, v\} \in E_1$, so $\{f(u), f(v)\} \in E_2$, so $f(u) \in N_2(f(v))$.
- If $w \in N_2(f(v))$, then $\{w, f(v)\} \in E_2$, so $\{f^{-1}(w), v\} \in E_1$, so $f^{-1}(w) \in N_1(v)$.

**Therefore:** $|N_1(v)| = |N_2(f(v))|$.

**Therefore:** $\deg_{G_1}(v) = \deg_{G_2}(f(v))$. ✓

---

**Degree sequence:**

List the degrees in non-increasing order.

Since $f$ is a bijection that preserves degrees, the multisets of degrees are identical.

**Therefore:** The degree sequences are the same. ∎

---

### Exercise 16.1.6 - Find All Isomorphisms Between Two Graphs

**Problem:** Find all isomorphisms between two given isomorphic graphs.

**Solution:**

**Example:** $G_1$ and $G_2$ are both $K_3$ (triangles).

```
G₁:           G₂:
  a             1
 / \           / \
b---c         3---2
```

**All isomorphisms:**

Since both are $K_3$, any bijection is an isomorphism (all vertices are adjacent to all others).

**Number of isomorphisms:** $3! = 6$

**List:**
1. $f_1(a)=1, f_1(b)=2, f_1(c)=3$
2. $f_2(a)=1, f_2(b)=3, f_2(c)=2$
3. $f_3(a)=2, f_3(b)=1, f_3(c)=3$
4. $f_4(a)=2, f_4(b)=3, f_4(c)=1$
5. $f_5(a)=3, f_5(b)=1, f_5(c)=2$
6. $f_6(a)=3, f_6(b)=2, f_6(c)=1$

---

## Section 16.2 - Izomorfia Invariánsok (Isomorphism Invariants)

---

### Exercise 16.2.1 - List Graph Invariants

**Problem:** List properties that are preserved by isomorphism.

**Solution:**

**Graph Invariants** (properties preserved by isomorphism):

| Invariant | Definition |
|-----------|------------|
| **|V|** | Number of vertices |
| **|E|** | Number of edges |
| **Degree sequence** | List of vertex degrees (sorted) |
| **Connectivity** | Whether graph is connected |
| **Number of components** | Number of connected components |
| **Diameter** | Maximum distance between any two vertices |
| **Radius** | Minimum eccentricity |
| **Girth** | Length of shortest cycle (∞ if acyclic) |
| **Chromatic number χ(G)** | Minimum colors for proper coloring |
| **Clique number ω(G)** | Size of largest complete subgraph |
| **Independence number α(G)** | Size of largest independent set |
| **Presence of cycles** | Whether graph contains a cycle |
| **Bipartiteness** | Whether graph is bipartite |
| **Planarity** | Whether graph can be drawn without crossings |
| **Eulerian** | Whether graph has Euler circuit |
| **Hamiltonian** | Whether graph has Hamilton circuit |
| **Genus** | Minimum genus of surface for embedding |
| **Automorphism group** | Group structure of Aut(G) |
| **Spectrum** | Eigenvalues of adjacency matrix |

---

### Exercise 16.2.2 - Verify: Diameter is Invariant

**Problem:** Prove that diameter is preserved by isomorphism.

**Solution:**

**Theorem:** If $G_1 \cong G_2$, then $\text{diam}(G_1) = \text{diam}(G_2)$.

**Proof:**

Let $f: V_1 \to V_2$ be an isomorphism.

**Claim:** For any $u, v \in V_1$, the distance $d_{G_1}(u, v) = d_{G_2}(f(u), f(v))$.

**Proof of claim:**

A path $u = v_0, v_1, \ldots, v_k = v$ in $G_1$ maps to a path $f(u) = f(v_0), f(v_1), \ldots, f(v_k) = f(v)$ in $G_2$.

Conversely, any path in $G_2$ maps back to a path in $G_1$ via $f^{-1}$.

**Therefore:** Shortest paths correspond.

**Therefore:** Distances are preserved. ✓

---

**Diameter:**

$$\text{diam}(G) = \max_{u,v \in V} d(u, v)$$

Since distances are preserved, the maximum is also preserved.

**Therefore:** $\text{diam}(G_1) = \text{diam}(G_2)$. ∎

---

### Exercise 16.2.3 - Verify: Chromatic Number is Invariant

**Problem:** Prove that chromatic number is preserved by isomorphism.

**Solution:**

**Theorem:** If $G_1 \cong G_2$, then $\chi(G_1) = \chi(G_2)$.

**Proof:**

Let $f: V_1 \to V_2$ be an isomorphism.

**Claim:** There is a bijection between proper k-colorings of $G_1$ and proper k-colorings of $G_2$.

**Proof:**

Given a proper k-coloring $c_1: V_1 \to \{1, \ldots, k\}$ of $G_1$.

Define $c_2: V_2 \to \{1, \ldots, k\}$ by $c_2(v) = c_1(f^{-1}(v))$.

**c₂ is proper:** If $\{u, v\} \in E_2$, then $\{f^{-1}(u), f^{-1}(v)\} \in E_1$.

Since $c_1$ is proper: $c_1(f^{-1}(u)) \neq c_1(f^{-1}(v))$.

**Therefore:** $c_2(u) \neq c_2(v)$. ✓

---

**Therefore:** $G_1$ has a proper k-coloring if and only if $G_2$ has a proper k-coloring.

**Therefore:** The minimum k is the same.

**Therefore:** $\chi(G_1) = \chi(G_2)$. ∎

---

### Exercise 16.2.4 - Verify: Bipartiteness is Invariant

**Problem:** Prove that bipartiteness is preserved by isomorphism.

**Solution:**

**Theorem:** If $G_1 \cong G_2$ and $G_1$ is bipartite, then $G_2$ is bipartite.

**Proof:**

$G_1$ is bipartite means $V_1 = A \cup B$ with $A \cap B = \emptyset$ and all edges between $A$ and $B$.

Define $A' = f(A)$ and $B' = f(B)$.

Since $f$ is a bijection: $A' \cap B' = \emptyset$ and $A' \cup B' = V_2$.

**Claim:** All edges of $G_2$ are between $A'$ and $B'$.

Let $\{u, v\} \in E_2$. Then $\{f^{-1}(u), f^{-1}(v)\} \in E_1$.

Since $G_1$ is bipartite, one of $f^{-1}(u), f^{-1}(v)$ is in $A$ and the other is in $B$.

**Therefore:** One of $u, v$ is in $A'$ and the other is in $B'$. ✓

**Therefore:** $G_2$ is bipartite. ∎

---

### Exercise 16.2.5 - Use Invariants to Distinguish Non-Isomorphic Graphs

**Problem:** Use invariants to show two graphs are NOT isomorphic.

**Solution:**

**Example 1:**

```
G₁:           G₂:
  a             1
 /|\           / \
b c d         2---3
```

**Invariants:**
- |V|: Both have 4 ✓
- |E|: G₁ has 3, G₂ has 1 ✗

**Conclusion:** G₁ ≇ G₂ (different number of edges).

---

**Example 2:**

```
G₁:           G₂:
  a           a
 / \         / \
b---c       b   c
```

**Invariants:**
- |V|: Both have 3 ✓
- |E|: Both have 3 ✓
- Degree sequence: G₁ = (2,2,2), G₂ = (1,1,2) ✗

**Conclusion:** G₁ ≇ G₂ (different degree sequences).

---

**Example 3:**

```
G₁:           G₂:
  a           a
 / \         / \
b   c       b---c
|   |       |   |
d---e       d   e
```

**Invariants:**
- |V|: Both have 5 ✓
- |E|: Both have 5 ✓
- Degree sequence: Both (2,2,2,2,2) ✓
- Girth: G₁ has 4-cycle, G₂ has no cycle ✗

**Conclusion:** G₁ ≇ G₂ (G₁ has a cycle, G₂ doesn't).

---

## Section 16.3 - Izomorfia Tesztelése (Testing Isomorphism)

---

### Exercise 16.3.1 - Construct Explicit Isomorphism

**Problem:** Show that two graphs ARE isomorphic by constructing an explicit isomorphism.

**Solution:**

**Example:**

```
G₁:           G₂:
  a           4
 / \         / \
b---c       3---5
|   |       |   |
d---e       2---1
```

**Step 1: Check invariants**
- |V| = 5 ✓
- |E| = 5 ✓
- Degree sequence = (2,2,2,2,2) ✓
- Both are 5-cycles ✓

**Step 2: Find isomorphism**

Trace the cycle in G₁: a-b-d-e-c-a

Trace the cycle in G₂: 4-3-2-1-5-4

**Isomorphism:**
- f(a) = 4
- f(b) = 3
- f(d) = 2
- f(e) = 1
- f(c) = 5

**Verification:**
- Edges in G₁: {a,b}, {b,d}, {d,e}, {e,c}, {c,a}
- Edges in G₂: {4,3}, {3,2}, {2,1}, {1,5}, {5,4}
- All edges preserved ✓

**Therefore:** G₁ ≅ G₂. ∎

---

### Exercise 16.3.2 - Use Adjacency Matrices to Test Isomorphism

**Problem:** Use adjacency matrices to test if two graphs are isomorphic.

**Solution:**

**Theorem:** $G_1 \cong G_2$ if and only if their adjacency matrices $A_1$ and $A_2$ satisfy:

$$A_2 = P^T A_1 P$$

for some permutation matrix $P$.

---

**Example:**

```
G₁:           G₂:
  a           1
 / \         / \
b---c       3---2
```

**Adjacency matrix of G₁** (order: a,b,c):
$$A_1 = \begin{pmatrix}
0 & 1 & 1 \\
1 & 0 & 1 \\
1 & 1 & 0
\end{pmatrix}$$

**Adjacency matrix of G₂** (order: 1,2,3):
$$A_2 = \begin{pmatrix}
0 & 1 & 1 \\
1 & 0 & 1 \\
1 & 1 & 0
\end{pmatrix}$$

**A₁ = A₂**, so the identity permutation works.

**Therefore:** G₁ ≅ G₂. ✓

---

**Different ordering:**

If G₂ is ordered as (2,1,3):
$$A_2' = \begin{pmatrix}
0 & 1 & 1 \\
1 & 0 & 1 \\
1 & 1 & 0
\end{pmatrix}$$

Still the same! (All orderings give the same matrix for K₃)

---

**Non-isomorphic example:**

```
G₁:           G₂:
  a           a
 / \         / \
b   c       b---c
```

$$A_1 = \begin{pmatrix}
0 & 1 & 1 \\
1 & 0 & 0 \\
1 & 0 & 0
\end{pmatrix}, \quad
A_2 = \begin{pmatrix}
0 & 1 & 1 \\
1 & 0 & 1 \\
1 & 1 & 0
\end{pmatrix}$$

No permutation can transform A₁ into A₂ (different eigenvalues).

**Therefore:** G₁ ≇ G₂. ✓

---

### Exercise 16.3.3 - Graph Isomorphism Problem Complexity

**Problem:** Understand the complexity of the graph isomorphism problem.

**Solution:**

**Graph Isomorphism Problem (GI):**

**Input:** Two graphs G₁ and G₂.

**Question:** Is G₁ ≅ G₂?

---

**Complexity Status:**

- **GI ∈ NP:** A certificate (isomorphism) can be verified in polynomial time.

- **GI is not known to be in P:** No polynomial-time algorithm is known.

- **GI is not known to be NP-complete:** Strong evidence suggests it's not NP-complete.

- **GI is in NP ∩ coAM:** Has interactive proof systems.

---

**Babai's Theorem (2015):**

**Theorem:** Graph isomorphism can be solved in quasipolynomial time.

**Time complexity:** $\exp(O((\log n)^c))$ for some constant $c$.

This is much faster than exponential but slower than polynomial.

---

**Practical Algorithms:**

- **nauty** (McKay): Very efficient for most graphs
- **bliss**: Efficient for large sparse graphs
- **Traces**: State-of-the-art implementation

These work well in practice despite no proven polynomial bound.

---

## Section 16.4 - Automorfizmus (Automorphism)

---

### Exercise 16.4.1 - Define Automorphism

**Problem:** Define what an automorphism is.

**Solution:**

**Definition:**

An **automorphism** of a graph $G = (V, E)$ is an isomorphism from $G$ to itself.

That is, a bijection $f: V \to V$ such that:

$$\{u, v\} \in E \iff \{f(u), f(v)\} \in E$$

---

**Example:**

```
G:
  a
 / \
b---c
```

**Automorphisms:**
1. Identity: id(a)=a, id(b)=b, id(c)=c
2. Swap b,c: f(a)=a, f(b)=c, f(c)=b

**Non-example:** g(a)=b, g(b)=a, g(c)=c is NOT an automorphism (doesn't preserve adjacency: {a,c} ∈ E but {g(a),g(c)} = {b,c} ∈ E, but {a,b} ∈ E and {g(a),g(b)} = {b,a} ∈ E... actually this IS an automorphism for K₃!)

For K₃, ALL 6 permutations are automorphisms.

---

### Exercise 16.4.2 - Prove: Automorphisms Form a Group

**Problem:** Prove that the automorphisms of a graph form a group under composition.

**Solution:**

**Theorem:** The set of automorphisms of a graph $G$, denoted $\text{Aut}(G)$, forms a group under composition.

**Proof:**

We verify the group axioms:

---

**1. Closure:**

If $f, g \in \text{Aut}(G)$, then $f \circ g \in \text{Aut}(G)$.

**Proof:** Composition of bijections is a bijection.

For any $u, v \in V$:
$$\{u, v\} \in E \iff \{g(u), g(v)\} \in E \iff \{f(g(u)), f(g(v))\} \in E$$

**Therefore:** $f \circ g$ preserves adjacency. ✓

---

**2. Associativity:**

Function composition is always associative. ✓

---

**3. Identity:**

The identity map $id: V \to V$ is an automorphism.

**Proof:** id is a bijection and preserves all adjacencies. ✓

---

**4. Inverses:**

If $f \in \text{Aut}(G)$, then $f^{-1} \in \text{Aut}(G)$.

**Proof:** $f^{-1}$ is a bijection.

For any $x, y \in V$:
$$\{x, y\} \in E \iff \{f(f^{-1}(x)), f(f^{-1}(y))\} \in E \iff \{f^{-1}(x), f^{-1}(y)\} \in E$$

**Therefore:** $f^{-1}$ preserves adjacency. ✓

---

**Conclusion:** $\text{Aut}(G)$ is a group. ∎

---

### Exercise 16.4.3 - Find Aut(Kₙ)

**Problem:** Find the automorphism group of the complete graph Kₙ.

**Solution:**

**Theorem:** $\text{Aut}(K_n) \cong S_n$ (the symmetric group on n elements).

**Proof:**

In $K_n$, every pair of vertices is adjacent.

**Therefore:** ANY bijection $f: V \to V$ preserves adjacency (all pairs are adjacent, all pairs map to adjacent pairs).

**Therefore:** Every permutation of vertices is an automorphism.

**Therefore:** $\text{Aut}(K_n) = S_n$.

**Size:** $|\text{Aut}(K_n)| = n!$ ✓

---

### Exercise 16.4.4 - Find Aut(Pₙ)

**Problem:** Find the automorphism group of the path graph Pₙ.

**Solution:**

**Theorem:** For $n \geq 3$, $\text{Aut}(P_n) \cong \mathbb{Z}_2$ (the group of order 2).

**Proof:**

```
Pₙ: v₁---v₂---v₃---...---vₙ₋₁---vₙ
```

**Degree analysis:**
- v₁ and vₙ have degree 1 (endpoints)
- v₂, ..., vₙ₋₁ have degree 2 (internal vertices)

**Automorphisms must preserve degrees:**
- Endpoints must map to endpoints
- Internal vertices must map to internal vertices

**Two possibilities:**
1. Identity: vᵢ ↦ vᵢ for all i
2. Reflection: vᵢ ↦ vₙ₋ᵢ₊₁ for all i (flip the path)

**Therefore:** $|\text{Aut}(P_n)| = 2$ for $n \geq 3$.

**Group structure:** $\mathbb{Z}_2$ (cyclic group of order 2). ✓

---

**Special cases:**
- P₁: Aut(P₁) = {id}, size 1
- P₂: Aut(P₂) = S₂, size 2 (can swap the two vertices)

---

### Exercise 16.4.5 - Find Aut(Cₙ)

**Problem:** Find the automorphism group of the cycle graph Cₙ.

**Solution:**

**Theorem:** $\text{Aut}(C_n) \cong D_n$ (the dihedral group of order 2n).

**Proof:**

```
C₅:
      v₁
     /  \
   v₅    v₂
   |      |
   v₄----v₃
```

**Automorphisms:**

1. **Rotations (n of them):**
   - Rotate by 0: vᵢ ↦ vᵢ
   - Rotate by 1: vᵢ ↦ vᵢ₊₁ (mod n)
   - ...
   - Rotate by n-1: vᵢ ↦ vᵢ₊ₙ₋₁ (mod n)

2. **Reflections (n of them):**
   - Reflect across axis through v₁
   - Reflect across axis through v₂
   - ...
   - (n different axes)

**Total:** n + n = 2n automorphisms.

**Group structure:** $D_n$ (dihedral group). ✓

---

**Size:** $|\text{Aut}(C_n)| = 2n$

---

### Exercise 16.4.6 - Find Aut(Kₘ,ₙ)

**Problem:** Find the automorphism group of the complete bipartite graph Kₘ,ₙ.

**Solution:**

**Case 1: m ≠ n**

**Theorem:** $\text{Aut}(K_{m,n}) \cong S_m \times S_n$ for $m \neq n$.

**Proof:**

```
K₂,₃:
  a₁    a₂      (part A, size m=2)
   | \  / |
   |  \/  |
   |  /\  |
   | /  \ |
  b₁ b₂  b₃    (part B, size n=3)
```

**Degree analysis:**
- All vertices in A have degree n
- All vertices in B have degree m
- Since m ≠ n, vertices in A cannot map to vertices in B

**Therefore:** Automorphisms must map A to A and B to B.

**Within A:** Any permutation works (all vertices in A have same neighbors: all of B).

**Within B:** Any permutation works.

**Therefore:** $\text{Aut}(K_{m,n}) \cong S_m \times S_n$.

**Size:** $m! \cdot n!$ ✓

---

**Case 2: m = n**

**Theorem:** $\text{Aut}(K_{n,n}) \cong S_n \wr \mathbb{Z}_2$ (wreath product), with size $2 \cdot (n!)^2$.

**Proof:**

When m = n, we can also swap the two parts.

**Automorphisms:**
1. Permute within A: n! ways
2. Permute within B: n! ways
3. Optionally swap A and B: 2 ways

**Total:** $2 \cdot (n!)^2$ ✓

---

## Section 16.5 - Speciális Gráfok Izomorfia

---

### Exercise 16.5.1 - Prove: All Kₙ with Same n are Isomorphic

**Problem:** Prove that all complete graphs with n vertices are isomorphic.

**Solution:**

**Theorem:** If G₁ and G₂ are both complete graphs on n vertices, then G₁ ≅ G₂.

**Proof:**

Let $V_1 = \{u_1, \ldots, u_n\}$ and $V_2 = \{v_1, \ldots, v_n\}$.

Define $f: V_1 \to V_2$ by $f(u_i) = v_i$.

**f is a bijection:** Clear by construction.

**f preserves adjacency:**

In a complete graph, EVERY pair of vertices is adjacent.

For any $u_i, u_j \in V_1$: $\{u_i, u_j\} \in E_1$ (complete).

And $\{f(u_i), f(u_j)\} = \{v_i, v_j\} \in E_2$ (complete).

**Therefore:** f is an isomorphism. ✓

---

**Conclusion:** There is exactly one complete graph on n vertices (up to isomorphism). ∎

---

### Exercise 16.5.2 - Prove: All Pₙ with Same n are Isomorphic

**Problem:** Prove that all path graphs with n vertices are isomorphic.

**Solution:**

**Theorem:** If G₁ and G₂ are both paths on n vertices, then G₁ ≅ G₂.

**Proof:**

Let $G_1: u_1 - u_2 - \cdots - u_n$

Let $G_2: v_1 - v_2 - \cdots - v_n$

Define $f: V_1 \to V_2$ by $f(u_i) = v_i$.

**f is a bijection:** Clear.

**f preserves adjacency:**

$\{u_i, u_j\} \in E_1 \iff |i - j| = 1 \iff \{v_i, v_j\} \in E_2$. ✓

**Therefore:** f is an isomorphism. ∎

---

### Exercise 16.5.3 - Prove: All Cₙ with Same n are Isomorphic

**Problem:** Prove that all cycle graphs with n vertices are isomorphic.

**Solution:**

**Theorem:** If G₁ and G₂ are both cycles on n vertices, then G₁ ≅ G₂.

**Proof:**

Similar to the path case.

Let $G_1: u_1 - u_2 - \cdots - u_n - u_1$

Let $G_2: v_1 - v_2 - \cdots - v_n - v_1$

Define $f(u_i) = v_i$.

**Adjacency preserved:**

$\{u_i, u_j\} \in E_1 \iff |i - j| \equiv 1 \pmod{n} \iff \{v_i, v_j\} \in E_2$. ✓

**Therefore:** G₁ ≅ G₂. ∎

---

## Section 16.6 - Izomorfia Algoritmusok

---

### Exercise 16.6.1 - Brute-Force Approach

**Problem:** Understand the brute-force approach to graph isomorphism.

**Solution:**

**Brute-Force Algorithm:**

```
Input: Graphs G₁ = (V₁, E₁), G₂ = (V₂, E₂) with |V₁| = |V₂| = n

1. For each permutation π of {1, ..., n}:
   a. Define f: V₁ → V₂ by f(vᵢ) = v_{π(i)}
   b. Check if f preserves all adjacencies
   c. If yes, return "Isomorphic"

2. Return "Not isomorphic"
```

---

**Time Complexity:**

- Number of permutations: n!
- Checking each permutation: O(n²)

**Total:** O(n! · n²)

---

**Example:**

For n = 10: 10! × 100 ≈ 3.6 × 10⁸ operations (feasible)

For n = 20: 20! × 400 ≈ 10²⁰ operations (infeasible)

---

**Optimization:**

- First check invariants (|V|, |E|, degree sequence)
- Only try permutations that preserve degrees
- Use backtracking with pruning

---

### Exercise 16.6.2 - Weisfeiler-Lehman Algorithm

**Problem:** Understand the Weisfeiler-Lehman (WL) algorithm for isomorphism testing.

**Solution:**

**1-dimensional WL (Color Refinement):**

```
1. Initialize: All vertices have the same color

2. Repeat until stable:
   For each vertex v:
     New color of v = (old color of v, multiset of colors of neighbors)

3. Compare color distributions of G₁ and G₂
```

---

**Example:**

```
G₁:           G₂:
  a           1
 / \         / \
b---c       2---3
```

**Iteration 0:** All vertices color 0.

**Iteration 1:**
- a: (0, {0,0}) → color 1
- b: (0, {0,0}) → color 1
- c: (0, {0,0}) → color 1

All same color (not helpful for K₃).

---

**Limitations:**

WL cannot distinguish all non-isomorphic graphs.

**Counterexample:** Certain strongly regular graphs.

But WL works for most practical cases!

---

## Section 16.7 - Alkalmazások (Applications)

---

### Exercise 16.7.1 - Chemical Structure Identification

**Problem:** Apply graph isomorphism to chemical structure identification.

**Solution:**

**Application:**

Molecules can be represented as graphs:
- Vertices = atoms
- Edges = bonds

**Problem:** Given two molecular graphs, are they the same molecule?

**Solution:** Test graph isomorphism!

---

**Example:**

```
Ethanol:        Dimethyl ether:
    H               H
    |               |
H - C - C - O - H   C - O - C
    |   |           |   |
    H   H           H   H
```

These are NOT isomorphic (different connectivity).

**Therefore:** Different molecules (isomers).

---

### Exercise 16.7.2 - Pattern Recognition

**Problem:** Apply graph isomorphism to pattern recognition.

**Solution:**

**Application:**

Objects can be represented as graphs:
- Vertices = features
- Edges = relationships

**Problem:** Does an image contain a specific pattern?

**Solution:** Test if pattern graph is isomorphic to a subgraph of image graph.

---

**Example:**

- Pattern: Letter "A" as a graph
- Image: Document with text
- Test: Does image graph contain "A" subgraph?

---

*Continued for remaining exercises in Chapter 16...*
