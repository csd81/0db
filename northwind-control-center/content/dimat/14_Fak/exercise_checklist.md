# Chapter 14 - Fák (Trees) - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 14 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 14.1 - Fa definíciók (Tree Definitions)

- [x] **HF** - Define tree (connected, acyclic graph)
- [x] **HF** - Prove: Tree with n vertices has n-1 edges
- [x] **HF** - Prove: Any two vertices in tree connected by unique path
- [x] **HF** - Verify equivalent definitions of trees
- [x] **HF** - Define forest (disjoint union of trees)
- [x] **Study** - Tree properties and characterizations

---

### Section 14.2 - Fajták (Types of Trees)

- [x] **HF** - Define rooted tree
- [x] **HF** - Define free tree (unrooted)
- [x] **HF** - Define binary tree
- [x] **HF** - Define k-ary tree
- [x] **HF** - Define ordered tree
- [x] **HF** - Define labeled vs unlabeled trees
- [x] **Study** - Tree isomorphism

---

### Section 14.3 - Fákkal kapcsolatos fogalmak (Tree Terminology)

- [x] **HF** - Define: root, parent, child, sibling
- [x] **HF** - Define: leaf, internal node
- [x] **HF** - Define: subtree
- [x] **HF** - Define: depth, height, level
- [x] **HF** - Define: ancestor, descendant
- [x] **HF** - Compute depth and height for given trees

---

### Section 14.4 - Fák száma (Counting Trees)

- [x] **HF** - State Cayley's formula: n^(n-2) labeled trees
- [x] **HF** - Verify Cayley's formula for small n
- [x] **HF** - Define Prüfer sequence
- [x] **HF** - Construct Prüfer sequence from tree
- [x] **HF** - Reconstruct tree from Prüfer sequence
- [x] **HF** - Prove: Bijection between trees and Prüfer sequences

---

### Section 14.5 - Feszítőfák (Spanning Trees)

- [x] **HF** - Define spanning tree
- [x] **HF** - Prove: Every connected graph has spanning tree
- [x] **HF** - Count spanning trees using Matrix-Tree Theorem
- [x] **HF** - Find all spanning trees of small graphs
- [x] **HF** - Define minimum spanning tree (MST)

---

### Section 14.6 - Minimális feszítőfa algoritmusok (MST Algorithms)

- [x] **HF** - State Kruskal's algorithm
- [x] **HF** - Trace Kruskal's algorithm on examples
- [x] **HF** - Prove correctness of Kruskal's algorithm
- [x] **HF** - State Prim's algorithm
- [x] **HF** - Trace Prim's algorithm on examples
- [x] **HF** - Compare Kruskal's vs Prim's
- [x] **HF** - Analyze time complexity of both algorithms

---

### Section 14.7 - Bináris fák (Binary Trees)

- [x] **HF** - Define binary tree properties
- [x] **HF** - Prove: n nodes → n-1 edges in binary tree
- [x] **HF** - Define full binary tree
- [x] **HF** - Define complete binary tree
- [x] **HF** - Define balanced binary tree
- [x] **HF** - Count binary trees with n nodes (Catalan numbers)

---

### Section 14.8 - Fák bejárása (Tree Traversals)

- [x] **HF** - Define preorder traversal
- [x] **HF** - Define inorder traversal
- [x] **HF** - Define postorder traversal
- [x] **HF** - Define level-order (BFS) traversal
- [x] **HF** - Trace traversals on example trees
- [x] **HF** - Applications: expression trees, syntax trees

---

### Section 14.9 - Alkalmazások (Applications)

- [x] **HF** - File system hierarchy
- [x] **HF** - Decision trees
- [x] **HF** - Binary search trees
- [x] **HF** - Heap data structure
- [x] **HF** - Huffman coding
- [x] **Study** - Phylogenetic trees

---

## 🔴 Formal Exercises (Section 14.10 - Feladatok)

### 14.1.Feladat - Tree properties
- [x] Verify tree definitions
- [x] Prove basic properties

### 14.2.Feladat - Counting trees
- [x] Apply Cayley's formula
- [x] Construct Prüfer sequences

### 14.3.Feladat - Spanning trees
- [x] Find all spanning trees
- [x] Count using Matrix-Tree Theorem

### 14.4.Feladat - MST (Kruskal)
- [x] Trace Kruskal's algorithm
- [x] Find minimum weight spanning tree

### 14.5.Feladat - MST (Prim)
- [x] Trace Prim's algorithm
- [x] Compare with Kruskal's result

### 14.6.Feladat - Binary trees
- [x] Construct binary trees
- [x] Count using Catalan numbers

### 14.7.Feladat - Tree traversals
- [x] Compute preorder, inorder, postorder
- [x] Reconstruct tree from traversals

### 14.8.Feladat - Applications
- [x] Model problems using trees
- [x] Apply tree algorithms

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter on trees
- [ ] Counting tree problems

### From Cayley
- [ ] Original tree counting papers

### From CLRS
- [ ] Chapter on MST algorithms
- [ ] Chapter on binary trees

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 35 | 35 | 100% |
| Formal Exercises 14.1-14.8 | 8 | 8 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **43** | **43** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** Basic tree definitions and properties
2. **Master:** Cayley's formula and Prüfer sequences
3. **Understand:** MST algorithms (Kruskal, Prim)
4. **Practice:** Tree traversals (preorder, inorder, postorder)
5. **Key technique:** Induction on number of vertices

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 4-5 hours |
| Formal exercises 14.1-14.8 | 4-5 hours |
| External problems | 3-4 hours |
| **Total** | **14-18 hours** |

---

## 📝 Key Formulas to Memorize

```
□ Tree: connected, acyclic graph
□ Tree edges: |E| = |V| - 1
□ Cayley: n^(n-2) labeled trees on n vertices
□ Prüfer sequence: length n-2, uniquely identifies tree
□ Kruskal: Sort edges, add if no cycle
□ Prim: Grow tree from arbitrary start
□ Catalan: C_n = (1/(n+1))·C(2n,n) binary trees
□ Preorder: Root, Left, Right
□ Inorder: Left, Root, Right
□ Postorder: Left, Right, Root
```

---

## Tree Properties Summary

| Property | Formula/Description |
|----------|---------------------|
| Edges | \|E\| = \|V\| - 1 |
| Labeled trees | n^(n-2) (Cayley) |
| Binary trees | C_n (Catalan) |
| Spanning trees | Cofactor of Laplacian |
| MST weight | Sum of selected edge weights |

---

## MST Algorithm Comparison

| Algorithm | Time | Space | Best For |
|-----------|------|-------|----------|
| Kruskal | O(E log E) | O(V) | Sparse graphs |
| Prim | O((V+E) log V) | O(V) | Dense graphs |
| Prim (Fibonacci) | O(E + V log V) | O(V) | Very large graphs |

---

*Generated from Chapter 14: Fák*
*Source: Dr. Szalkai István - Diszkrét matematika*
