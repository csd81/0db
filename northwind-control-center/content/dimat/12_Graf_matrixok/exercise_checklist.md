# Chapter 12 - Graf mátrixok (Graph Matrices) - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 12 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 12.1 - Adjacencia mátrix (Adjacency Matrix)

- [x] **HF** - Define adjacency matrix A for graph G
- [x] **HF** - Compute adjacency matrix for given graphs
- [x] **HF** - Verify: A is symmetric for undirected graphs
- [x] **HF** - Verify: Row/column sums give vertex degrees
- [x] **HF** - Compute A², A³ and interpret entries
- [x] **HF** - Prove: (Aᵏ)ᵢⱼ = number of walks of length k from i to j

---

### Section 12.2 - Incidencia mátrix (Incidence Matrix)

- [x] **HF** - Define incidence matrix B for graph G
- [x] **HF** - Compute incidence matrix for given graphs
- [x] **HF** - Verify: Column sums = 2 (each edge has 2 endpoints)
- [x] **HF** - Verify: Row sums = vertex degrees
- [x] **HF** - Relate incidence matrix to adjacency matrix

---

### Section 12.3 - Laplace mátrix (Laplacian Matrix)

- [x] **HF** - Define Laplacian matrix L = D - A
- [x] **HF** - Compute Laplacian for given graphs
- [x] **HF** - Verify: Row sums = 0
- [x] **HF** - Verify: L is positive semidefinite
- [x] **HF** - Compute eigenvalues of L for small graphs

---

### Section 12.4 - Mátrixok és gráf tulajdonságok

- [x] **HF** - Relate matrix rank to graph connectivity
- [x] **HF** - Use adjacency matrix to count triangles
- [x] **HF** - Use Laplacian to find spanning trees (Matrix-Tree Theorem)
- [x] **HF** - Determine if graphs are isomorphic using matrices

---

### Section 12.5 - Spektrális gráfelmélet (Spectral Graph Theory)

- [x] **HF** - Define spectrum of a graph
- [x] **HF** - Compute spectrum for small graphs
- [x] **HF** - Relate eigenvalues to graph properties
- [x] **HF** - Verify: λ₁ = 0 for Laplacian ⇔ connected
- [x] **Study** - Cheeger inequality and expansion

---

### Section 12.6 - Alkalmazások (Applications)

- [x] **HF** - Network analysis using adjacency matrix
- [x] **HF** - PageRank algorithm (Google matrix)
- [x] **HF** - Community detection using Laplacian
- [x] **HF** - Graph partitioning applications
- [x] **Study** - Random walks on graphs

---

## 🔴 Formal Exercises (Section 12.7 - Feladatok)

### 12.1.Feladat - Adjacency matrix
- [x] Compute A for given graph
- [x] Verify properties (symmetry, degrees)

### 12.2.Feladat - Matrix powers
- [x] Compute A², A³
- [x] Count walks of given length

### 12.3.Feladat - Incidence matrix
- [x] Compute B for given graph
- [x] Verify column/row sums

### 12.4.Feladat - Laplacian matrix
- [x] Compute L = D - A
- [x] Verify row sums = 0

### 12.5.Feladat - Matrix-Tree Theorem
- [x] Count spanning trees using Laplacian
- [x] Verify with direct counting

### 12.6.Feladat - Graph spectrum
- [x] Compute eigenvalues
- [x] Relate to graph properties

### 12.7.Feladat - Isomorphism
- [x] Use matrices to test isomorphism
- [x] Find isomorphism mapping

### 12.8.Feladat - Applications
- [x] Apply to network problems
- [x] PageRank computation

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter on graph matrices
- [ ] Spectral graph theory problems

### From Brouwer & Haemers
- [ ] Spectra of Graphs exercises

### From Chung [Ch]
- [ ] Spectral Graph Theory problems

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 25 | 25 | 100% |
| Formal Exercises 12.1-12.8 | 8 | 8 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **33** | **33** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** Adjacency matrix definition and examples
2. **Master:** Matrix powers count walks
3. **Understand:** Laplacian and Matrix-Tree Theorem
4. **Practice:** Computing eigenvalues for small graphs
5. **Key technique:** Use trace(A³)/6 to count triangles

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Reading chapter | 2-3 hours |
| In-chapter HF | 3-4 hours |
| Formal exercises 12.1-12.8 | 3-4 hours |
| External problems | 2-3 hours |
| **Total** | **10-14 hours** |

---

## 📝 Key Formulas to Memorize

```
□ Adjacency: A[i][j] = 1 if adjacent, 0 otherwise
□ (A^k)[i][j] = # walks of length k from i to j
□ Incidence: B[i][j] = 1 if vertex i incident to edge j
□ Laplacian: L = D - A (D = degree matrix)
□ Matrix-Tree: # spanning trees = any cofactor of L
□ Spectrum: eigenvalues of A or L
□ trace(A^3) = 6 × (# triangles)
```

---

## Matrix Types Summary

| Matrix | Size | Entries | Properties |
|--------|------|---------|------------|
| Adjacency A | n×n | 0,1 | Symmetric (undirected) |
| Incidence B | n×m | 0,1 | Column sum = 2 |
| Degree D | n×n | degrees | Diagonal |
| Laplacian L | n×n | varies | Row sum = 0, PSD |

---

*Generated from Chapter 12: Graf mátrixok*
*Source: Dr. Szalkai István - Diszkrét matematika*
