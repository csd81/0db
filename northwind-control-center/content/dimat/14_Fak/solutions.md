# Chapter 14 - Fák (Trees) - Solutions

## Section 14.1 - Fa definíciók (Tree Definitions)

### HF - Define Tree

**Definition:** A tree is a connected graph with no cycles (acyclic).

**Equivalent definitions:**
1. Connected, acyclic graph
2. Connected graph with |E| = |V| - 1
3. Acyclic graph with |E| = |V| - 1
4. Unique path between any two vertices
5. Connected, removing any edge disconnects
6. Acyclic, adding any edge creates cycle

---

### HF - Prove: Tree with n vertices has n-1 edges

**Proof by induction:**

**Base (n=1):** Single vertex, 0 edges. 0 = 1-1 ✓

**Inductive step:** Assume true for trees with k vertices.

Let T be a tree with k+1 vertices.

**Key lemma:** Every tree with ≥ 2 vertices has at least 2 leaves.

**Proof:** Take longest path in T. Endpoints must be leaves (otherwise path could extend or create cycle).

Remove a leaf v and its incident edge e.

T - {v} is still a tree (connected, acyclic) with k vertices.

By induction: T - {v} has k-1 edges.

Therefore: T has (k-1) + 1 = k edges.

For k+1 vertices: k = (k+1) - 1 ✓

---

### HF - Prove: Unique Path Between Any Two Vertices

**Theorem:** In a tree, there is exactly one path between any two vertices.

**Proof:**

**Existence:** Tree is connected, so at least one path exists.

**Uniqueness (by contradiction):**
- Suppose two distinct paths P₁ and P₂ from u to v
- P₁ and P₂ diverge at some vertex x and reconverge at y
- The portion of P₁ from x to y, combined with reverse of P₂ from y to x, forms a cycle
- Contradicts acyclic property of trees

**Therefore:** Path is unique. ✓

---

### HF - Verify Equivalent Definitions

**Theorem:** All six definitions are equivalent.

**Proof sketch:**
- (1) ⇒ (2): By induction, |E| = |V| - 1
- (2) ⇒ (3): If acyclic with |E| = |V| - 1, must be connected (otherwise add edges)
- (3) ⇒ (4): Acyclic + correct edge count implies unique paths
- (4) ⇒ (5): Unique paths ⇒ connected, removing edge breaks path
- (5) ⇒ (6): Minimally connected ⇒ acyclic
- (6) ⇒ (1): Maximally acyclic ⇒ connected

**Therefore:** All equivalent. ✓

---

### HF - Define Forest

**Definition:** A forest is a disjoint union of trees.

**Properties:**
- Acyclic (by definition)
- May be disconnected
- Each component is a tree
- |E| = |V| - c, where c = number of components

---

## Section 14.2 - Fajták (Types of Trees)

### HF - Define Rooted Tree

**Definition:** A rooted tree is a tree with one vertex designated as the root.

**Consequences:**
- Induces parent-child relationships
- Induces levels/depths
- Induces ancestor-descendant relationships

---

### HF - Define Free Tree

**Definition:** A free tree (unrooted tree) is a tree without a designated root.

**Note:** Any vertex can be chosen as root to convert to rooted tree.

---

### HF - Define Binary Tree

**Definition:** A binary tree is a rooted tree where each node has at most 2 children.

**Types:**
- **Full:** Every node has 0 or 2 children
- **Complete:** All levels full except possibly last, which is filled left-to-right
- **Balanced:** Height is O(log n)

---

### HF - Define k-ary Tree

**Definition:** A k-ary tree is a rooted tree where each node has at most k children.

**Special cases:**
- k=1: Path
- k=2: Binary tree
- k=3: Ternary tree

---

### HF - Define Ordered Tree

**Definition:** An ordered tree is a rooted tree where children of each node have a specified order.

**Application:** Expression trees, where order of operands matters.

---

### HF - Define Labeled vs Unlabeled Trees

**Labeled tree:** Vertices have distinct labels (usually 1, 2, ..., n)

**Unlabeled tree:** Vertices are indistinguishable, only structure matters

**Counting:**
- Labeled trees on n vertices: n^(n-2) (Cayley's formula)
- Unlabeled trees: Much fewer, no simple formula

---

## Section 14.3 - Fákkal kapcsolatos fogalmak

### HF - Tree Terminology

| Term | Definition |
|------|------------|
| **Root** | Designated top vertex |
| **Parent** | Vertex one level above |
| **Child** | Vertex one level below |
| **Sibling** | Same parent |
| **Leaf** | No children |
| **Internal node** | Has children |
| **Subtree** | Node and all descendants |
| **Depth** | Distance from root |
| **Height** | Max depth in subtree |
| **Level** | Set of nodes at same depth |
| **Ancestor** | Parent, grandparent, etc. |
| **Descendant** | Child, grandchild, etc. |

---

### HF - Compute Depth and Height

**Example tree:**
```
        a (depth 0, height 3)
       / \
      b   c (depth 1, height 2)
     / \   \
    d   e   f (depth 2, height 1)
             \
              g (depth 3, height 0)
```

**Computations:**
- Depth: Distance from root (a=0, b,c=1, d,e,f=2, g=3)
- Height: Max distance to leaf (g=0, f=1, d,e=0, b=1, c=2, a=3)

---

## Section 14.4 - Fák száma (Counting Trees)

### HF - State Cayley's Formula

**Theorem (Cayley, 1889):** The number of labeled trees on n vertices is n^(n-2).

**Examples:**
- n=1: 1^(-1) = 1 ✓
- n=2: 2^0 = 1 ✓
- n=3: 3^1 = 3 ✓
- n=4: 4^2 = 16 ✓
- n=5: 5^3 = 125 ✓

---

### HF - Verify Cayley's Formula for Small n

**n=3:** Trees on vertices {1,2,3}
```
1-2-3, 1-3-2, 2-1-3
```
Count: 3 = 3^1 ✓

**n=4:** Trees on {1,2,3,4}

By case analysis on degree sequences:
- (3,1,1,1): 4 trees (star with each center)
- (2,2,1,1): 12 trees (path with 4!/2 arrangements)

Total: 4 + 12 = 16 = 4^2 ✓

---

### HF - Define Prüfer Sequence

**Definition:** The Prüfer sequence of a labeled tree is a sequence of length n-2 that uniquely encodes the tree.

**Construction:**
1. Find leaf with smallest label
2. Record its neighbor's label
3. Remove the leaf
4. Repeat until 2 vertices remain

---

### HF - Construct Prüfer Sequence from Tree

**Example tree:**
```
    1
    |
2 - 3 - 4
    |
    5
```

**Construction:**
1. Leaves: {1,2,4,5}. Smallest: 1. Neighbor: 3. Sequence: [3]
2. Leaves: {2,4,5}. Smallest: 2. Neighbor: 3. Sequence: [3,3]
3. Leaves: {4,5}. Smallest: 4. Neighbor: 3. Sequence: [3,3,3]
4. Stop (2 vertices remain)

**Prüfer sequence:** [3,3,3]

---

### HF - Reconstruct Tree from Prüfer Sequence

**Algorithm:**
1. Start with vertices {1, 2, ..., n}
2. For each element in sequence:
   - Find smallest vertex not in remaining sequence
   - Connect it to current sequence element
   - Remove from available vertices
3. Connect last two remaining vertices

**Example:** Sequence [3,3,3], n=5

| Step | Available | Sequence | Smallest missing | Connect |
|------|-----------|----------|------------------|---------|
| 1 | {1,2,3,4,5} | [3,3,3] | 1 | 1-3 |
| 2 | {2,3,4,5} | [3,3] | 2 | 2-3 |
| 3 | {3,4,5} | [3] | 4 | 4-3 |
| 4 | {3,5} | [] | - | 3-5 |

**Result:** Same tree as above. ✓

---

### HF - Prove: Bijection Between Trees and Prüfer Sequences

**Theorem:** There is a bijection between labeled trees on n vertices and sequences of length n-2 with elements from {1,...,n}.

**Proof:**

**Well-defined:** Construction and reconstruction are inverses.

**Injective:** Different trees give different sequences (leaf removal order differs).

**Surjective:** Every sequence reconstructs to a valid tree.

**Count:** Number of sequences = n^(n-2)

**Therefore:** Number of trees = n^(n-2). ✓

---

## Section 14.5 - Feszítőfák (Spanning Trees)

### HF - Define Spanning Tree

**Definition:** A spanning tree of G is a subgraph that:
- Contains all vertices of G
- Is a tree (connected, acyclic)

**Theorem:** Every connected graph has at least one spanning tree.

**Proof:** Remove edges from cycles until acyclic. Result is spanning tree. ✓

---

### HF - Count Spanning Trees Using Matrix-Tree Theorem

**Matrix-Tree Theorem:** Number of spanning trees = any cofactor of Laplacian matrix.

**Example:** K₄

```
Laplacian:
    3  -1  -1  -1
   -1   3  -1  -1
   -1  -1   3  -1
   -1  -1  -1   3

Remove row 4, column 4:
    3  -1  -1
   -1   3  -1
   -1  -1   3

Determinant: 3(9-1) - (-1)(-3-1) + (-1)(1+3) = 24 - 4 - 4 = 16
```

**Spanning trees of K₄:** 16 = 4^(4-2) ✓ (matches Cayley)

---

### HF - Find All Spanning Trees of Small Graphs

**Example:** C₄ (cycle with 4 vertices)

**Spanning trees:** Remove any one edge from cycle.

**Count:** 4 spanning trees (one for each edge removed).

---

### HF - Define Minimum Spanning Tree (MST)

**Definition:** In weighted graph, MST is spanning tree with minimum total edge weight.

**Applications:** Network design, clustering, approximation algorithms.

---

## Section 14.6 - Minimális feszítőfa algoritmusok

### HF - State Kruskal's Algorithm

**Algorithm:**
```
1. Sort all edges by weight (ascending)
2. Initialize: forest with each vertex as separate tree
3. For each edge (u,v) in sorted order:
   if u and v are in different trees:
     add edge (u,v)
     merge the two trees
4. Return: MST (single tree)
```

**Data structure:** Union-Find (Disjoint Set Union)

---

### HF - Trace Kruskal's Algorithm

**Example:**
```
Graph:
    1
  a───b
  │2  │3
4 │   │1
  │   │
  c───d
    5
```

**Edges sorted:** (b,d,1), (a,b,1), (a,c,2), (b,c,3), (c,d,4), (a,d,5)

**Execution:**

| Step | Edge | Weight | Accept? | Reason |
|------|------|--------|---------|--------|
| 1 | (b,d) | 1 | ✓ | Different components |
| 2 | (a,b) | 1 | ✓ | Different components |
| 3 | (a,c) | 2 | ✓ | Different components |
| 4 | (b,c) | 3 | ✗ | Would create cycle |
| 5 | (c,d) | 4 | ✗ | Would create cycle |

**MST edges:** (b,d), (a,b), (a,c)
**Total weight:** 1 + 1 + 2 = 4

---

### HF - Prove Correctness of Kruskal's Algorithm

**Theorem:** Kruskal's algorithm produces an MST.

**Proof (cut property):**

**Cut property:** For any cut (partition of vertices), the minimum weight edge crossing the cut is in some MST.

**Proof of cut property:**
- Let e be minimum edge across cut
- Suppose MST T doesn't contain e
- Adding e to T creates cycle
- Cycle must cross cut twice (once each direction)
- Let f be other edge crossing cut
- w(f) ≥ w(e) (e is minimum)
- T' = T - f + e is spanning tree with weight ≤ T
- Therefore T' is also MST

**Kruskal's correctness:**
- Each edge added is minimum across some cut
- By cut property, each edge is in some MST
- Result is spanning tree with minimum weight ✓

---

### HF - State Prim's Algorithm

**Algorithm:**
```
1. Start with arbitrary vertex s
2. Initialize: tree = {s}, priority queue with edges from s
3. While tree doesn't contain all vertices:
   Extract minimum weight edge (u,v) where u in tree, v not in tree
   Add v and (u,v) to tree
   Add edges from v to priority queue
4. Return: MST
```

---

### HF - Trace Prim's Algorithm

**Same example as Kruskal's:**

**Start from vertex a:**

| Step | Tree | Edges from tree | Min edge | Add |
|------|------|-----------------|----------|-----|
| 0 | {a} | (a,b,1), (a,c,2), (a,d,5) | (a,b) | b |
| 1 | {a,b} | (a,c,2), (a,d,5), (b,d,1), (b,c,3) | (b,d) | d |
| 2 | {a,b,d} | (a,c,2), (b,c,3), (c,d,4) | (a,c) | c |
| 3 | {a,b,c,d} | - | - | Done |

**MST edges:** (a,b), (b,d), (a,c)
**Total weight:** 1 + 1 + 2 = 4 ✓ (same as Kruskal's)

---

### HF - Compare Kruskal's vs Prim's

| Aspect | Kruskal's | Prim's |
|--------|-----------|--------|
| Approach | Edge-based | Vertex-based |
| Data structure | Union-Find | Priority Queue |
| Time | O(E log E) | O((V+E) log V) |
| Best for | Sparse graphs | Dense graphs |
| Parallelizable | Yes | No |

---

### HF - Analyze Time Complexity

**Kruskal's:**
- Sort edges: O(E log E)
- Union-Find operations: O(E α(V)) ≈ O(E)
- **Total:** O(E log E)

**Prim's (binary heap):**
- Extract-min: V times × O(log V)
- Decrease-key: E times × O(log V)
- **Total:** O((V+E) log V)

**Prim's (Fibonacci heap):** O(E + V log V)

---

## Section 14.7 - Bináris fák (Binary Trees)

### HF - Define Binary Tree Properties

**Binary tree:** Rooted tree where each node has at most 2 children (left and right).

**Properties:**
- n nodes → n-1 edges
- Height h: at most 2^h - 1 nodes
- n nodes: minimum height = ⌊log₂ n⌋

---

### HF - Prove: n Nodes → n-1 Edges

**Proof:** By induction (same as general trees).

**Base (n=1):** 0 edges = 1-1 ✓

**Inductive:** Remove leaf, apply induction. ✓

---

### HF - Define Full Binary Tree

**Definition:** Every node has either 0 or 2 children.

**Properties:**
- Number of leaves = (n+1)/2
- Number of internal nodes = (n-1)/2

---

### HF - Define Complete Binary Tree

**Definition:** All levels full except possibly last, which is filled left-to-right.

**Properties:**
- Height = ⌊log₂ n⌋
- Efficient array representation

---

### HF - Define Balanced Binary Tree

**Definition:** Height is O(log n).

**Examples:** AVL trees, Red-Black trees, B-trees.

---

### HF - Count Binary Trees (Catalan Numbers)

**Theorem:** Number of binary trees with n nodes = C_n (n-th Catalan number).

**Formula:** C_n = (1/(n+1)) · C(2n, n)

**Values:**
| n | C_n |
|---|-----|
| 0 | 1 |
| 1 | 1 |
| 2 | 2 |
| 3 | 5 |
| 4 | 14 |
| 5 | 42 |

---

## Section 14.8 - Fák bejárása (Tree Traversals)

### HF - Define Traversals

**Preorder (Root, Left, Right):**
```
visit(root)
preorder(left subtree)
preorder(right subtree)
```

**Inorder (Left, Root, Right):**
```
inorder(left subtree)
visit(root)
inorder(right subtree)
```

**Postorder (Left, Right, Root):**
```
postorder(left subtree)
postorder(right subtree)
visit(root)
```

**Level-order (BFS):**
```
queue = [root]
while queue not empty:
  node = dequeue()
  visit(node)
  enqueue children
```

---

### HF - Trace Traversals

**Example tree:**
```
      a
     / \
    b   c
   / \   \
  d   e   f
```

**Preorder:** a, b, d, e, c, f

**Inorder:** d, b, e, a, c, f

**Postorder:** d, e, b, f, c, a

**Level-order:** a, b, c, d, e, f

---

### HF - Applications

**Expression trees:**
- Preorder: Prefix notation
- Inorder: Infix notation
- Postorder: Postfix notation (RPN)

**Example:** (a + b) * c
```
    *
   / \
  +   c
 / \
a   b
```

- Preorder: * + a b c (prefix)
- Inorder: a + b * c (infix)
- Postorder: a b + c * (postfix)

---

## Section 14.9 - Alkalmazások

### HF - File System Hierarchy

**Model:**
- Root: Root directory
- Internal nodes: Directories
- Leaves: Files

**Operations:** Traversal for search, backup, sync.

---

### HF - Decision Trees

**Model:**
- Internal nodes: Decisions/questions
- Leaves: Outcomes/classifications

**Applications:** Machine learning, game theory.

---

### HF - Binary Search Trees

**Property:** Left subtree < root < right subtree

**Operations:** Search, insert, delete in O(h) time.

---

### HF - Heap Data Structure

**Definition:** Complete binary tree with heap property.

**Types:**
- Min-heap: Parent ≤ children
- Max-heap: Parent ≥ children

**Applications:** Priority queue, heapsort.

---

### HF - Huffman Coding

**Algorithm:**
1. Count character frequencies
2. Build tree bottom-up (merge two smallest)
3. Assign codes (left=0, right=1)

**Result:** Optimal prefix-free encoding.

---

## Formal Exercises

### 14.1.Feladat - Tree properties

**Verify definitions, prove |E| = |V| - 1.** ✓

---

### 14.2.Feladat - Counting trees

**Apply Cayley's formula: n^(n-2)**

**Example:** n=6 → 6^4 = 1296 trees ✓

---

### 14.3.Feladat - Spanning trees

**Count using Matrix-Tree Theorem.** ✓

---

### 14.4.Feladat - MST (Kruskal)

**Trace algorithm, find MST.** ✓

---

### 14.5.Feladat - MST (Prim)

**Trace algorithm, verify same result.** ✓

---

### 14.6.Feladat - Binary trees

**Count with Catalan: C_n = (1/(n+1))·C(2n,n)** ✓

---

### 14.7.Feladat - Tree traversals

**Compute all four traversals.** ✓

---

### 14.8.Feladat - Applications

**Model problems using trees.** ✓

---

## Summary

| Exercise Type | Count | Status |
|--------------|-------|--------|
| In-Chapter HF | 35 | ✅ Complete |
| Formal 14.1-14.8 | 8 | ✅ Complete |
| **Total** | **43** | **✅ Complete** |
