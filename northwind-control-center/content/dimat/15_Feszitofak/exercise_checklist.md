# Chapter 15 - Feszítőfák (Spanning Trees) - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 15 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 15.1 - Feszítőfa definíció (Spanning Tree Definition)

- [x] **HF** - Define spanning tree
- [x] **HF** - Prove: Every connected graph has a spanning tree
- [x] **HF** - Prove: All spanning trees of a graph have the same number of edges
- [x] **HF** - Verify: A spanning tree of G with n vertices has n-1 edges
- [x] **HF** - Find all spanning trees of small graphs (K₃, K₄, C₄)
- [x] **Study** - Relationship between spanning trees and connectivity

---

### Section 15.2 - Minimális feszítőfa (Minimum Spanning Tree)

- [x] **HF** - Define minimum spanning tree (MST)
- [x] **HF** - Prove: MST is unique when edge weights are distinct
- [x] **HF** - Verify cut property for MST
- [x] **HF** - Verify cycle property for MST
- [x] **HF** - Apply cut property to find MST edges
- [x] **HF** - Apply cycle property to eliminate non-MST edges

---

### Section 15.3 - Kruskal algoritmus (Kruskal's Algorithm)

- [x] **HF** - State Kruskal's algorithm
- [x] **HF** - Trace Kruskal's algorithm on weighted graphs
- [x] **HF** - Prove correctness of Kruskal's algorithm
- [x] **HF** - Analyze time complexity: O(E log E)
- [x] **HF** - Implement using Union-Find data structure
- [x] **HF** - Verify MST weight on example graphs

---

### Section 15.4 - Prim algoritmus (Prim's Algorithm)

- [x] **HF** - State Prim's algorithm
- [x] **HF** - Trace Prim's algorithm on weighted graphs
- [x] **HF** - Prove correctness of Prim's algorithm
- [x] **HF** - Analyze time complexity: O((V+E) log V)
- [x] **HF** - Compare with Kruskal's algorithm
- [x] **HF** - Verify same MST as Kruskal's

---

### Section 15.5 - Fák száma (Counting Spanning Trees)

- [x] **HF** - State Matrix-Tree Theorem
- [x] **HF** - Compute Laplacian matrix of graphs
- [x] **HF** - Count spanning trees using cofactors
- [x] **HF** - Verify: Kₙ has n^(n-2) spanning trees (Cayley's formula)
- [x] **HF** - Count spanning trees of K₃, K₄, K₅
- [x] **HF** - Count spanning trees of Cₙ, Pₙ, Kₘ,ₙ

---

### Section 15.6 - Feszítőfák alkalmazásai (Applications)

- [x] **HF** - Network design applications
- [x] **HF** - Clustering applications
- [x] **HF** - Approximation algorithms (TSP)
- [x] **HF** - Image segmentation
- [x] **Study** - Phylogenetic trees
- [x] **Study** - Circuit design

---

## 🔴 Formal Exercises (Section 15.7 - Feladatok)

### 15.1.Feladat - Spanning tree basics
- [x] Find all spanning trees of given graph
- [x] Count spanning trees
- [x] Verify n-1 edges property

### 15.2.Feladat - MST properties
- [x] Verify cut property
- [x] Verify cycle property
- [x] Prove uniqueness for distinct weights

### 15.3.Feladat - Kruskal's algorithm
- [x] Trace algorithm step by step
- [x] Compute MST weight
- [x] Verify optimality

### 15.4.Feladat - Prim's algorithm
- [x] Trace algorithm from different starting vertices
- [x] Compare with Kruskal's result
- [x] Analyze running time

### 15.5.Feladat - Matrix-Tree Theorem
- [x] Compute Laplacian matrix
- [x] Find cofactors
- [x] Count spanning trees

### 15.6.Feladat - Cayley's formula
- [x] Verify n^(n-2) for small n
- [x] Count labeled trees
- [x] Apply to complete graphs

### 15.7.Feladat - Algorithm comparison
- [x] Compare Kruskal vs Prim
- [x] Choose appropriate algorithm
- [x] Justify choice

### 15.8.Feladat - Applications
- [x] Model network design problem
- [x] Find optimal network
- [x] Compute cost savings

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter on spanning trees
- [ ] MST variations

### From CLRS
- [ ] Chapter on MST algorithms
- [ ] Union-Find data structure

### From West
- [ ] Graph theory spanning tree problems

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 30 | 30 | 100% |
| Formal Exercises 15.1-15.8 | 8 | 8 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **38** | **38** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** Spanning tree definition and basic properties
2. **Master:** Kruskal's and Prim's algorithms (trace by hand)
3. **Understand:** Cut and cycle properties for MST
4. **Practice:** Matrix-Tree Theorem calculations
5. **Key technique:** Union-Find for efficient implementation

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 4-5 hours |
| Formal exercises 15.1-15.8 | 4-5 hours |
| External problems | 3-4 hours |
| **Total** | **14-18 hours** |

---

## 📝 Key Formulas to Memorize

```
□ Spanning tree: n vertices → n-1 edges
□ Cayley's formula: Kₙ has n^(n-2) spanning trees
□ Matrix-Tree: # trees = any cofactor of Laplacian
□ Kruskal: Sort edges, add if no cycle
□ Prim: Grow tree from arbitrary start
□ Cut property: Min weight edge across cut is in MST
□ Cycle property: Max weight edge in cycle is not in MST
```

---

## MST Algorithm Comparison

| Algorithm | Time | Space | Best For |
|-----------|------|-------|----------|
| Kruskal | O(E log E) | O(V) | Sparse graphs |
| Prim | O((V+E) log V) | O(V) | Dense graphs |
| Prim (Fibonacci) | O(E + V log V) | O(V) | Very large graphs |

---

*Generated from Chapter 15: Feszítőfák*
*Source: Dr. Szalkai István - Diszkrét matematika*
