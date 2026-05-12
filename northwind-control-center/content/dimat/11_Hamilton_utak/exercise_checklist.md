# Chapter 11 - Hamilton utak (Hamilton Paths) - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 11 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 11.1 - Hamilton utak és körök definíciója

- [x] **HF** - Define Hamilton path and Hamilton circuit
- [x] **HF** - Distinguish Hamilton path from Euler path
- [x] **HF** - Define Hamiltonian graph
- [x] **Study** - Historical note: Sir William Rowan Hamilton, 1857

---

### Section 11.2 - Szükséges feltételek (Necessary Conditions)

- [x] **HF** - Prove: If G is Hamiltonian, then G is connected
- [x] **HF** - Prove: If G is Hamiltonian, then G has no cut vertices
- [x] **HF** - Verify necessary condition: c(G-S) ≤ |S| for all S ⊆ V
- [x] **HF** - Apply condition to show graph is NOT Hamiltonian

---

### Section 11.3 - Elégséges feltételek (Sufficient Conditions)

#### Dirac's Theorem

- [x] **HF** - State Dirac's theorem (1952)
- [x] **HF** - Verify: If δ(G) ≥ n/2, then G is Hamiltonian
- [x] **HF** - Apply Dirac's theorem to specific graphs
- [x] **HF** - Show bound is sharp (construct counterexample for n/2 - 1)

---

#### Ore's Theorem

- [x] **HF** - State Ore's theorem (1960)
- [x] **HF** - Verify: If d(u)+d(v) ≥ n for all non-adjacent u,v, then G is Hamiltonian
- [x] **HF** - Show Ore's theorem generalizes Dirac's theorem
- [x] **HF** - Apply Ore's theorem to specific graphs

---

#### Pósa's Theorem

- [x] **HF** - State Pósa's theorem (1962)
- [x] **HF** - Verify degree sequence condition
- [x] **Study** - Pósa's theorem is stronger than Dirac's

---

### Section 11.4 - A bezárás módszere (Closure Method)

#### Bondy-Chvátal Theorem

- [x] **HF** - Define closure of a graph
- [x] **HF** - Prove: G is Hamiltonian iff closure(G) is Hamiltonian
- [x] **HF** - Apply closure method to specific graphs
- [x] **HF** - Show closure generalizes Ore's theorem

---

### Section 11.5 - Gráfok Hamilton-tulajdonságai

- [x] **HF** - Prove: Kₙ is Hamiltonian for n ≥ 3
- [x] **HF** - Prove: Cₙ is Hamiltonian for n ≥ 3
- [x] **HF** - Determine if Petersen graph is Hamiltonian
- [x] **HF** - Prove: Complete bipartite Kₙ,ₙ is Hamiltonian for n ≥ 2
- [x] **HF** - Show: Kₘ,ₙ is NOT Hamiltonian if m ≠ n

---

### Section 11.6 - Algoritmusok (Algorithms)

- [x] **HF** - Understand brute-force algorithm (n! permutations)
- [x] **HF** - Study backtracking algorithm
- [x] **HF** - Understand Posá's rotation-extension technique
- [x] **Study** - Hamiltonian cycle problem is NP-complete

---

### Section 11.7 - Alkalmazások (Applications)

- [x] **HF** - Traveling Salesman Problem (TSP)
- [x] **HF** - Job scheduling applications
- [x] **HF** - Circuit board drilling
- [x] **Study** - Approximation algorithms for TSP

---

## 🔴 Formal Exercises (Section 11.8 - Feladatok)

### 11.1.Feladat - Hamilton vs Euler
- [x] Distinguish Hamilton from Euler problems
- [x] Compare necessary and sufficient conditions

### 11.2.Feladat - Necessary conditions
- [x] Apply c(G-S) ≤ |S| condition
- [x] Show graph is NOT Hamiltonian

### 11.3.Feladat - Dirac's theorem
- [x] Verify minimum degree condition
- [x] Apply to specific graphs

### 11.4.Feladat - Ore's theorem
- [x] Verify degree sum condition
- [x] Compare with Dirac's theorem

### 11.5.Feladat - Closure method
- [x] Compute closure of graph
- [x] Determine Hamiltonicity from closure

### 11.6.Feladat - Specific graphs
- [x] Determine if given graphs are Hamiltonian
- [x] Find Hamilton cycle if exists

### 11.7.Feladat - Constructions
- [x] Construct Hamiltonian graphs with given properties
- [x] Construct non-Hamiltonian graphs

### 11.8.Feladat - TSP applications
- [x] Model TSP as graph problem
- [x] Apply nearest neighbor heuristic

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter on Hamilton paths
- [ ] TSP variations

### From Bondy & Murty
- [ ] Graph Theory exercises
- [ ] Hamiltonian graph problems

### From Rosen [RoKe]
- [ ] Discrete mathematics graph problems

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 25 | 25 | 100% |
| Formal Exercises 11.1-11.8 | 8 | 8 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **33** | **33** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** Definitions (Hamilton vs Euler)
2. **Master:** Dirac's and Ore's theorems
3. **Understand:** Closure method (Bondy-Chvátal)
4. **Practice:** Applying sufficient conditions
5. **Key technique:** Use degree conditions to prove Hamiltonicity

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Reading chapter | 2-3 hours |
| In-chapter HF | 3-4 hours |
| Formal exercises 11.1-11.8 | 3-4 hours |
| External problems | 2-3 hours |
| **Total** | **10-14 hours** |

---

## 📝 Key Formulas to Memorize

```
□ Hamilton path: visits every VERTEX exactly once
□ Hamilton circuit: Hamilton path that returns to start
□ Dirac: δ(G) ≥ n/2 ⇒ Hamiltonian (n ≥ 3)
□ Ore: d(u)+d(v) ≥ n for non-adjacent ⇒ Hamiltonian
□ Closure: G Hamiltonian ⇔ cl(G) Hamiltonian
□ Necessary: c(G-S) ≤ |S| for all S ⊆ V
```

---

## Hamilton vs Euler Comparison

| Property | Euler | Hamilton |
|----------|-------|----------|
| Visits | Every EDGE once | Every VERTEX once |
| Efficient test | Yes (degree check) | No (NP-complete) |
| Necessary condition | All degrees even | c(G-S) ≤ |S| |
| Sufficient condition | All degrees even | δ(G) ≥ n/2 (Dirac) |

---

*Generated from Chapter 11: Hamilton utak*
*Source: Dr. Szalkai István - Diszkrét matematika*
