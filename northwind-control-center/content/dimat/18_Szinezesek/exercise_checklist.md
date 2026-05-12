# Chapter 18 - Színezések (Graph Colorings) - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 18 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 18.1 - Csúcsszínezés (Vertex Coloring)

- [x] **HF** - Define proper vertex coloring
- [x] **HF** - Define chromatic number χ(G)
- [x] **HF** - Compute χ(G) for complete graphs Kₙ
- [x] **HF** - Compute χ(G) for bipartite graphs
- [x] **HF** - Compute χ(G) for cycles Cₙ
- [x] **HF** - Compute χ(G) for trees
- [x] **HF** - Prove: χ(G) ≤ Δ(G) + 1 (Brooks' Theorem bound)
- [x] **HF** - State Brooks' Theorem: χ(G) ≤ Δ(G) except for Kₙ and Cₙ (n odd)
- [x] **Study** - Greedy coloring algorithm

---

### Section 18.2 - Élszínezés (Edge Coloring)

- [x] **HF** - Define proper edge coloring
- [x] **HF** - Define chromatic index χ'(G)
- [x] **HF** - Compute χ'(G) for complete graphs
- [x] **HF** - Compute χ'(G) for bipartite graphs
- [x] **HF** - State Vizing's Theorem: Δ(G) ≤ χ'(G) ≤ Δ(G) + 1
- [x] **HF** - Classify graphs as Class 1 or Class 2
- [x] **Study** - Edge coloring applications

---

### Section 18.3 - Síkgráfok színezése (Coloring Planar Graphs)

- [x] **HF** - State the Four Color Theorem
- [x] **HF** - State the Five Color Theorem
- [x] **HF** - Prove: Every planar graph has a vertex of degree ≤ 5
- [x] **HF** - Prove the Five Color Theorem
- [x] **HF** - Understand the Four Color Theorem proof (computer-assisted)
- [x] **Study** - Historical development of color theorems

---

### Section 18.4 - Kritikus gráfok (Critical Graphs)

- [x] **HF** - Define k-critical graph
- [x] **HF** - Prove: Kₖ is k-critical
- [x] **HF** - Prove: Cₙ (n odd) is 3-critical
- [x] **HF** - Prove properties of critical graphs
- [x] **HF** - Prove: δ(G) ≥ χ(G) - 1 for critical graphs
- [x] **Study** - Structure of critical graphs

---

### Section 18.5 - Színezési algoritmusok (Coloring Algorithms)

- [x] **HF** - Understand greedy coloring
- [x] **HF** - Understand Welsh-Powell algorithm
- [x] **HF** - Understand DSatur algorithm
- [x] **HF** - Analyze approximation quality
- [x] **Study** - Exact algorithms (exponential time)
- [x] **Study** - Heuristic approaches

---

### Section 18.6 - Alkalmazások (Applications)

- [x] **HF** - Scheduling problems
- [x] **HF** - Register allocation
- [x] **HF** - Frequency assignment
- [x] **HF** - Sudoku as coloring
- [x] **Study** - Timetabling problems
- [x] **Study** - Pattern matching

---

## 🔴 Formal Exercises (Section 18.7 - Feladatok)

### 18.1.Feladat - Vertex coloring basics
- [x] Compute chromatic number of given graphs
- [x] Construct proper colorings

### 18.2.Feladat - Edge coloring
- [x] Compute chromatic index
- [x] Apply Vizing's theorem

### 18.3.Feladat - Planar graph coloring
- [x] Apply Four/Five Color Theorem
- [x] Construct 5-colorings

### 18.4.Feladat - Critical graphs
- [x] Identify critical graphs
- [x] Prove criticality

### 18.5.Feladat - Brooks' Theorem
- [x] Apply Brooks' Theorem
- [x] Identify exceptions

### 18.6.Feladat - Coloring algorithms
- [x] Apply greedy coloring
- [x] Compare algorithms

### 18.7.Feladat - Bounds and inequalities
- [x] Prove coloring bounds
- [x] Apply to specific graphs

### 18.8.Feladat - Applications
- [x] Model scheduling as coloring
- [x] Solve real problems

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter on graph coloring
- [ ] Chromatic number problems

### From Bondy & Murty
- [ ] Coloring exercises
- [ ] Critical graph problems

### From West
- [ ] Graph coloring problems

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 30 | 30 | 100% |
| Formal Exercises 18.1-18.8 | 8 | 8 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **38** | **38** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** Vertex coloring definition and chromatic number
2. **Master:** Computing χ(G) for standard graph families
3. **Understand:** Brooks' Theorem and its exceptions
4. **Practice:** Edge coloring and Vizing's Theorem
5. **Key technique:** Greedy coloring with different orderings

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 4-5 hours |
| Formal exercises 18.1-18.8 | 4-5 hours |
| External problems | 3-4 hours |
| **Total** | **14-18 hours** |

---

## 📝 Key Formulas to Memorize

```
□ Chromatic number: χ(G) = minimum colors for vertex coloring
□ Chromatic index: χ'(G) = minimum colors for edge coloring
□ Brooks' Theorem: χ(G) ≤ Δ(G) except Kₙ and odd Cₙ
□ Vizing's Theorem: Δ(G) ≤ χ'(G) ≤ Δ(G) + 1
□ Four Color Theorem: χ(G) ≤ 4 for planar G
□ Five Color Theorem: χ(G) ≤ 5 for planar G
□ Critical graph: χ(G-v) < χ(G) for all v
□ Greedy bound: χ(G) ≤ Δ(G) + 1
```

---

## Chromatic Numbers of Common Graphs

| Graph | χ(G) | χ'(G) |
|-------|------|-------|
| Kₙ | n | n-1 (n even), n (n odd) |
| Cₙ (n even) | 2 | 2 |
| Cₙ (n odd) | 3 | 3 |
| Pₙ | 2 | Δ |
| Tree | 2 | Δ |
| Kₘ,ₙ | 2 | max(m,n) |
| Planar | ≤ 4 | Δ or Δ+1 |

---

## Coloring Algorithm Comparison

| Algorithm | Time | Quality | Use Case |
|-----------|------|---------|----------|
| Greedy | O(V+E) | Poor | Quick estimate |
| Welsh-Powell | O(V log V + E) | Better | General purpose |
| DSatur | O(V²) | Good | Better quality |
| Exact | Exponential | Optimal | Small graphs |

---

*Generated from Chapter 18: Színezések*
*Source: Dr. Szalkai István - Diszkrét matematika*
