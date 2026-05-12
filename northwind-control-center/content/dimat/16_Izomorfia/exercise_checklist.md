# Chapter 16 - Izomorfia (Graph Isomorphism) - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 16 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 16.1 - Izomorfia definíció (Isomorphism Definition)

- [x] **HF** - Define graph isomorphism
- [x] **HF** - Define isomorphism as bijection preserving adjacency
- [x] **HF** - Verify isomorphism is an equivalence relation
- [x] **HF** - Prove: Isomorphic graphs have same number of vertices
- [x] **HF** - Prove: Isomorphic graphs have same number of edges
- [x] **HF** - Prove: Isomorphic graphs have same degree sequence
- [x] **Study** - Graph isomorphism as equivalence relation

---

### Section 16.2 - Izomorfia invariánsok (Isomorphism Invariants)

- [x] **HF** - List graph invariants (properties preserved by isomorphism)
- [x] **HF** - Verify: Number of vertices is invariant
- [x] **HF** - Verify: Number of edges is invariant
- [x] **HF** - Verify: Degree sequence is invariant
- [x] **HF** - Verify: Connectivity is invariant
- [x] **HF** - Verify: Diameter is invariant
- [x] **HF** - Verify: Girth is invariant
- [x] **HF** - Verify: Chromatic number is invariant
- [x] **HF** - Verify: Presence of cycles is invariant
- [x] **HF** - Verify: Bipartiteness is invariant
- [x] **Study** - Properties NOT preserved by isomorphism

---

### Section 16.3 - Izomorfia tesztelése (Testing Isomorphism)

- [x] **HF** - Use invariants to show graphs are NOT isomorphic
- [x] **HF** - Construct explicit isomorphism to show graphs ARE isomorphic
- [x] **HF** - Use adjacency matrices to test isomorphism
- [x] **HF** - Use degree sequences as first test
- [x] **HF** - Use canonical labeling approach
- [x] **Study** - Graph isomorphism problem complexity

---

### Section 16.4 - Automorfizmus (Automorphism)

- [x] **HF** - Define automorphism (isomorphism from G to itself)
- [x] **HF** - Verify: Identity map is always an automorphism
- [x] **HF** - Prove: Automorphisms form a group (Aut(G))
- [x] **HF** - Find automorphism group of Kₙ (symmetric group Sₙ)
- [x] **HF** - Find automorphism group of Pₙ
- [x] **HF** - Find automorphism group of Cₙ (dihedral group Dₙ)
- [x] **HF** - Find automorphism group of complete bipartite Kₘ,ₙ
- [x] **Study** - Symmetric graphs and vertex-transitivity

---

### Section 16.5 - Speciális gráfok izomorfia (Isomorphism of Special Graphs)

- [x] **HF** - Prove: All Kₙ with same n are isomorphic
- [x] **HF** - Prove: All Pₙ with same n are isomorphic
- [x] **HF** - Prove: All Cₙ with same n are isomorphic
- [x] **HF** - Prove: All Kₘ,ₙ with same m,n are isomorphic
- [x] **HF** - Determine when two trees are isomorphic
- [x] **Study** - Canonical forms for special graph classes

---

### Section 16.6 - Izomorfia algoritmusok (Isomorphism Algorithms)

- [x] **HF** - Understand brute-force approach (n! permutations)
- [x] **HF** - Understand vertex refinement / Weisfeiler-Lehman algorithm
- [x] **HF** - Understand complexity: GI is in NP, not known NP-complete
- [x] **Study** - Babai's quasipolynomial algorithm (2015)
- [x] **Study** - Practical isomorphism testing software (nauty, bliss)

---

### Section 16.7 - Alkalmazások (Applications)

- [x] **HF** - Chemical structure identification
- [x] **HF** - Pattern recognition
- [x] **HF** - Network analysis
- [x] **HF** - Code equivalence
- [x] **Study** - Graph database queries
- [x] **Study** - Social network comparison

---

## 🔴 Formal Exercises (Section 16.8 - Feladatok)

### 16.1.Feladat - Isomorphism definition
- [x] Verify isomorphism between given graphs
- [x] Construct explicit bijection

### 16.2.Feladat - Invariants
- [x] Compute graph invariants
- [x] Use invariants to distinguish non-isomorphic graphs

### 16.3.Feladat - Non-isomorphism proof
- [x] Prove two graphs are NOT isomorphic
- [x] Find distinguishing invariant

### 16.4.Feladat - Isomorphism proof
- [x] Prove two graphs ARE isomorphic
- [x] Give explicit isomorphism mapping

### 16.5.Feladat - Automorphism group
- [x] Find all automorphisms of given graph
- [x] Determine automorphism group structure

### 16.6.Feladat - Adjacency matrix method
- [x] Use adjacency matrices to test isomorphism
- [x] Find permutation matrix

### 16.7.Feladat - Special graphs
- [x] Classify special graphs up to isomorphism
- [x] Count non-isomorphic graphs

### 16.8.Feladat - Applications
- [x] Apply isomorphism to real problems
- [x] Model and solve

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter on graph isomorphism
- [ ] Isomorphism testing problems

### From Bondy & Murty
- [ ] Graph isomorphism exercises
- [ ] Automorphism group problems

### From computational sources
- [ ] Graph isomorphism algorithm implementations

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 35 | 35 | 100% |
| Formal Exercises 16.1-16.8 | 8 | 8 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **43** | **43** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** Definition of isomorphism (bijection preserving adjacency)
2. **Master:** Using invariants to prove NON-isomorphism
3. **Understand:** Constructing explicit isomorphism to prove ISOMORPHISM
4. **Practice:** Computing automorphism groups
5. **Key technique:** Degree sequence is necessary but not sufficient

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 4-5 hours |
| Formal exercises 16.1-16.8 | 4-5 hours |
| External problems | 3-4 hours |
| **Total** | **14-18 hours** |

---

## 📝 Key Formulas to Memorize

```
□ Isomorphism: bijection f: V(G) → V(H) preserving adjacency
□ Invariants: |V|, |E|, degree sequence, connectivity, etc.
□ Aut(Kₙ) = Sₙ (symmetric group, size n!)
□ Aut(Pₙ) = ℤ₂ (size 2, for n ≥ 3)
□ Aut(Cₙ) = Dₙ (dihedral group, size 2n)
□ GI ∈ NP, not known to be NP-complete
□ Babai (2015): Quasipolynomial time algorithm
```

---

## Isomorphism Testing Strategy

| Step | Action | Purpose |
|------|--------|---------|
| 1 | Compare |V| | Quick rejection |
| 2 | Compare |E| | Quick rejection |
| 3 | Compare degree sequences | Quick rejection |
| 4 | Compare other invariants | Further filtering |
| 5 | Try to construct isomorphism | Positive proof |
| 6 | Use canonical labeling | Computational approach |

---

## Automorphism Groups Summary

| Graph | Aut(G) | Size |
|-------|--------|------|
| Kₙ | Sₙ (symmetric group) | n! |
| Pₙ (n ≥ 3) | ℤ₂ | 2 |
| Cₙ | Dₙ (dihedral group) | 2n |
| Kₘ,ₙ (m ≠ n) | Sₘ × Sₙ | m! · n! |
| Kₙ,ₙ | Sₙ ≀ ℤ₂ | 2 · (n!)² |

---

*Generated from Chapter 16: Izomorfia*
*Source: Dr. Szalkai István - Diszkrét matematika*
