# Chapter 17 - Síkgráfok (Planar Graphs) - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 17 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 17.1 - Síkgráf definíció (Planar Graph Definition)

- [x] **HF** - Define planar graph
- [x] **HF** - Define plane graph (embedded planar graph)
- [x] **HF** - Define faces of a plane graph
- [x] **HF** - Define outer face (unbounded face)
- [x] **HF** - Verify: K₁, K₂, K₃, K₄ are planar
- [x] **HF** - Verify: K₅ is NOT planar
- [x] **Study** - Planar embedding and face structure

---

### Section 17.2 - Euler-formula (Euler's Formula)

- [x] **HF** - State Euler's formula: V - E + F = 2
- [x] **HF** - Prove Euler's formula by induction
- [x] **HF** - Verify Euler's formula for small planar graphs
- [x] **HF** - Apply Euler's formula to find number of faces
- [x] **HF** - Prove: E ≤ 3V - 6 for simple planar graphs (V ≥ 3)
- [x] **HF** - Prove: E ≤ 2V - 4 for triangle-free planar graphs
- [x] **HF** - Use inequality to prove K₅ is non-planar
- [x] **HF** - Use inequality to prove K₃,₃ is non-planar

---

### Section 17.3 - Kuratowski-tétel (Kuratowski's Theorem)

- [x] **HF** - Define subdivision of a graph
- [x] **HF** - Define K₅ and K₃,₃ as forbidden minors
- [x] **HF** - State Kuratowski's theorem
- [x] **HF** - Identify subdivisions of K₅ or K₃,₃ in non-planar graphs
- [x] **HF** - Prove a graph is non-planar using Kuratowski's theorem
- [x] **Study** - Wagner's theorem (minor characterization)

---

### Section 17.4 - Síkgráf színezés (Coloring Planar Graphs)

- [x] **HF** - Define proper vertex coloring
- [x] **HF** - Define chromatic number χ(G)
- [x] **HF** - State the Five Color Theorem
- [x] **HF** - State the Four Color Theorem
- [x] **HF** - Prove: Every planar graph has a vertex of degree ≤ 5
- [x] **HF** - Prove: Every planar graph is 5-colorable
- [x] **HF** - Prove: Every planar graph is 4-colorable (Appel-Haken, 1976)
- [x] **Study** - Computer-assisted proof of Four Color Theorem

---

### Section 17.5 - Dualitás (Duality)

- [x] **HF** - Define dual graph G*
- [x] **HF** - Construct dual of a plane graph
- [x] **HF** - Verify: (G*)* ≅ G
- [x] **HF** - Verify: |V(G*)| = |F(G)|
- [x] **HF** - Verify: |E(G*)| = |E(G)|
- [x] **HF** - Verify: |F(G*)| = |V(G)|
- [x] **HF** - Relate cycles in G to cuts in G*
- [x] **Study** - Self-dual graphs

---

### Section 17.6 - Síkgráfok felismerése (Planarity Testing)

- [x] **HF** - Understand brute-force approach
- [x] **HF** - Understand Hopcroft-Tarjan algorithm (O(V))
- [x] **HF** - Understand Boyer-Myrvold algorithm
- [x] **Study** - Practical planarity testing software

---

### Section 17.7 - Alkalmazások (Applications)

- [x] **HF** - Circuit board design (no crossing wires)
- [x] **HF** - Map coloring
- [x] **HF** - Geographic information systems
- [x] **HF** - Graph drawing
- [x] **Study** - Topological graph theory
- [x] **Study** - Mesh generation

---

## 🔴 Formal Exercises (Section 17.8 - Feladatok)

### 17.1.Feladat - Planarity verification
- [x] Determine if given graphs are planar
- [x] Draw planar embeddings

### 17.2.Feladat - Euler's formula
- [x] Verify V - E + F = 2
- [x] Use to find unknown quantities

### 17.3.Feladat - Edge bounds
- [x] Apply E ≤ 3V - 6
- [x] Prove non-planarity using bounds

### 17.4.Feladat - Kuratowski's theorem
- [x] Find K₅ or K₃,₃ subdivisions
- [x] Prove non-planarity

### 17.5.Feladat - Graph coloring
- [x] Find chromatic number
- [x] Construct proper colorings

### 17.6.Feladat - Dual graphs
- [x] Construct dual graph
- [x] Verify duality properties

### 17.7.Feladat - Planar graph properties
- [x] Prove properties using Euler's formula
- [x] Apply to special graph classes

### 17.8.Feladat - Applications
- [x] Model real problems as planar graphs
- [x] Apply planarity results

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter on planar graphs
- [ ] Kuratowski theorem problems

### From Bondy & Murty
- [ ] Planar graph exercises
- [ ] Four color theorem problems

### From West
- [ ] Graph theory planar problems

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 35 | 35 | 100% |
| Formal Exercises 17.1-17.8 | 8 | 8 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **43** | **43** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** Planar graph definition and examples
2. **Master:** Euler's formula V - E + F = 2
3. **Understand:** Edge bounds E ≤ 3V - 6 and applications
4. **Practice:** Finding K₅ or K₃,₃ subdivisions
5. **Key technique:** Use Euler's formula to prove non-planarity

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 4-5 hours |
| Formal exercises 17.1-17.8 | 4-5 hours |
| External problems | 3-4 hours |
| **Total** | **14-18 hours** |

---

## 📝 Key Formulas to Memorize

```
□ Euler's formula: V - E + F = 2 (connected planar graph)
□ Edge bound: E ≤ 3V - 6 (simple planar, V ≥ 3)
□ Triangle-free bound: E ≤ 2V - 4
□ Five Color Theorem: χ(G) ≤ 5 for planar G
□ Four Color Theorem: χ(G) ≤ 4 for planar G
□ Kuratowski: G planar ⟺ no K₅ or K₃,₃ subdivision
□ Dual: |V*| = F, |E*| = E, |F*| = V
```

---

## Planarity Criteria Summary

| Criterion | Formula/Test |
|-----------|--------------|
| Euler | V - E + F = 2 |
| Edge bound | E ≤ 3V - 6 |
| Kuratowski | No K₅ or K₃,₃ subdivision |
| Wagner | No K₅ or K₃,₃ minor |

---

## Color Theorems Summary

| Theorem | Statement |
|---------|-----------|
| Five Color | Every planar graph is 5-colorable |
| Four Color | Every planar graph is 4-colorable |
| Three Color | Not always possible (e.g., K₄) |
| Two Color | iff graph is bipartite |

---

*Generated from Chapter 17: Síkgráfok*
*Source: Dr. Szalkai István - Diszkrét matematika*
