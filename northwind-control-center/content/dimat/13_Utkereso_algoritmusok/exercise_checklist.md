# Chapter 13 - Útkereső algoritmusok (Pathfinding Algorithms) - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 13 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 13.1 - Legrövidebb út problémák (Shortest Path Problems)

- [x] **HF** - Define shortest path problem
- [x] **HF** - Distinguish single-source vs all-pairs problems
- [x] **HF** - Understand negative weight edges
- [x] **Study** - Applications: routing, navigation, networks

---

### Section 13.2 - Dijkstra algoritmusa

- [x] **HF** - State Dijkstra's algorithm prerequisites
- [x] **HF** - Trace Dijkstra's algorithm on example graphs
- [x] **HF** - Prove correctness of Dijkstra's algorithm
- [x] **HF** - Analyze time complexity: O((V+E) log V)
- [x] **HF** - Implement with priority queue
- [x] **HF** - Verify: Works only with non-negative weights

---

### Section 13.3 - Bellman-Ford algoritmus

- [x] **HF** - State Bellman-Ford algorithm
- [x] **HF** - Trace algorithm on example graphs
- [x] **HF** - Prove: Handles negative weights correctly
- [x] **HF** - Detect negative cycles
- [x] **HF** - Analyze time complexity: O(VE)
- [x] **HF** - Compare with Dijkstra's algorithm

---

### Section 13.4 - Floyd-Warshall algoritmus

- [x] **HF** - State Floyd-Warshall algorithm for all-pairs shortest paths
- [x] **HF** - Trace algorithm on example graphs
- [x] **HF** - Prove correctness using dynamic programming
- [x] **HF** - Analyze time complexity: O(V³)
- [x] **HF** - Analyze space complexity: O(V²)
- [x] **HF** - Reconstruct paths from predecessor matrix

---

### Section 13.5 - Szélességi keresés (BFS)

- [x] **HF** - State BFS algorithm for unweighted graphs
- [x] **HF** - Trace BFS on example graphs
- [x] **HF** - Prove: BFS finds shortest paths in unweighted graphs
- [x] **HF** - Analyze time complexity: O(V+E)
- [x] **HF** - Applications: connectivity, bipartiteness

---

### Section 13.6 - Mélységi keresés (DFS)

- [x] **HF** - State DFS algorithm
- [x] **HF** - Trace DFS on example graphs
- [x] **HF** - Classify edges (tree, back, forward, cross)
- [x] **HF** - Analyze time complexity: O(V+E)
- [x] **HF** - Applications: topological sort, SCC

---

### Section 13.7 - A* algoritmus (A-Star)

- [x] **HF** - State A* algorithm with heuristic
- [x] **HF** - Define admissible heuristic
- [x] **HF** - Prove: A* is optimal with admissible heuristic
- [x] **HF** - Compare with Dijkstra's algorithm
- [x] **Study** - Common heuristics: Manhattan, Euclidean

---

### Section 13.8 - Alkalmazások (Applications)

- [x] **HF** - GPS navigation systems
- [x] **HF** - Network routing protocols
- [x] **HF** - Game AI pathfinding
- [x] **HF** - Social network analysis
- [x] **Study** - Real-world implementations

---

## 🔴 Formal Exercises (Section 13.9 - Feladatok)

### 13.1.Feladat - Dijkstra's algorithm
- [x] Trace algorithm on given graph
- [x] Find shortest path from source to all vertices
- [x] Compute total distance

### 13.2.Feladat - Bellman-Ford
- [x] Handle negative weight edges
- [x] Detect negative cycles if present

### 13.3.Feladat - Floyd-Warshall
- [x] Compute all-pairs shortest paths
- [x] Build distance and predecessor matrices

### 13.4.Feladat - BFS
- [x] Find shortest path in unweighted graph
- [x] Compute distances from source

### 13.5.Feladat - DFS
- [x] Classify edges
- [x] Find connected components

### 13.6.Feladat - A* algorithm
- [x] Apply with given heuristic
- [x] Compare with Dijkstra

### 13.7.Feladat - Algorithm comparison
- [x] Choose appropriate algorithm for given problem
- [x] Justify choice based on graph properties

### 13.8.Feladat - Applications
- [x] Model real problem as shortest path
- [x] Solve using appropriate algorithm

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter on pathfinding algorithms
- [ ] Shortest path variations

### From Cormen et al. (CLRS)
- [ ] Chapter 24: Single-Source Shortest Paths
- [ ] Chapter 25: All-Pairs Shortest Paths

### From Sedgewick
- [ ] Graph algorithms exercises

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 30 | 30 | 100% |
| Formal Exercises 13.1-13.8 | 8 | 8 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **38** | **38** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** BFS (simplest, unweighted graphs)
2. **Master:** Dijkstra's algorithm (most common)
3. **Understand:** When to use each algorithm
4. **Practice:** Trace algorithms by hand
5. **Key technique:** Relaxation operation

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 4-5 hours |
| Formal exercises 13.1-13.8 | 4-5 hours |
| External problems | 3-4 hours |
| **Total** | **14-18 hours** |

---

## 📝 Key Formulas to Memorize

```
□ Dijkstra: O((V+E) log V) - non-negative weights only
□ Bellman-Ford: O(VE) - handles negative weights
□ Floyd-Warshall: O(V³) - all-pairs shortest paths
□ BFS: O(V+E) - unweighted graphs
□ DFS: O(V+E) - traversal, not shortest path
□ A*: O(b^d) - with admissible heuristic
□ Relaxation: if d[u] + w(u,v) < d[v], update d[v]
```

---

## Algorithm Comparison

| Algorithm | Time | Space | Negative Weights? | Use Case |
|-----------|------|-------|-------------------|----------|
| BFS | O(V+E) | O(V) | N/A | Unweighted |
| Dijkstra | O((V+E) log V) | O(V) | ✗ No | Single-source |
| Bellman-Ford | O(VE) | O(V) | ✓ Yes | Detect negative cycles |
| Floyd-Warshall | O(V³) | O(V²) | ✓ Yes | All-pairs |
| A* | O(b^d) | O(b^d) | Depends | Heuristic search |

---

*Generated from Chapter 13: Útkereső algoritmusok*
*Source: Dr. Szalkai István - Diszkrét matematika*
