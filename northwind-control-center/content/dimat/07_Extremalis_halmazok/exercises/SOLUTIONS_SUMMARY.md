# Chapter 07 - Exercise Solutions Summary

## ✅ Completed Solutions

Solutions for Chapter 07 (Extremális halmazrendszerek) exercises.

---

## Exercise Solutions by Topic

### Sperner's Theorem

| # | Problem | Topic | File |
|---|---------|-------|------|
| 7.1 | Maximum Sperner families | Sperner applications | [`01_sperner_applications.md`](./01_sperner_applications.md) |

**Results:**
- $n = 6$: Maximum = $\binom{6}{3} = 20$ sets
- $n = 7$: Maximum = $\binom{7}{3} = 35$ sets
- Lubell's inequality: $\sum \frac{1}{\binom{n}{|A_i|}} \leq 1$

**Key technique:** Chain counting argument

---

### Erdős-Ko-Rado Theorem

| # | Problem | Topic | File |
|---|---------|-------|------|
| 7.2 | Intersecting families | EKR applications | [`02_ekr_applications.md`](./02_ekr_applications.md) |

**Results:**
- $n = 6, k = 3$: Maximum = $\binom{5}{2} = 10$ intersecting sets
- $n = 7, k = 3$: Maximum = $\binom{6}{2} = 15$ intersecting sets
- Why $k \leq n/2$ is necessary

**Key construction:** All $k$-sets containing a fixed element

---

### Erdős-DeBruijn & Fisher Theorems

| # | Problem | Topic | File |
|---|---------|-------|------|
| 7.3 | Constant intersection | Intersection theorems | [`03_erdos_debruijn_fisher.md`](./03_erdos_debruijn_fisher.md) |

**Results:**
- $|A_i \cap A_j| = 1 \Rightarrow m \leq n$
- Fano plane: $n = 7, k = 3, t = 1$, achieves $m = n = 7$
- Connection to block designs and projective planes

**Key technique:** Linear algebra method (characteristic vectors)

---

### Ray-Chaudhuri-Wilson & Babai-Frankl

| # | Problem | Topic | File |
|---|---------|-------|------|
| 7.4 | Restricted intersections | Generalized theorems | [`04_ray_chaudhuri_wilson.md`](./04_ray_chaudhuri_wilson.md) |

**Results:**
- RCW: $|A_i \cap A_j| \in L, |L| = s \Rightarrow m \leq \binom{n}{s}$
- BF: With $\gcd(L) \nmid k \Rightarrow m \leq n$ (stronger!)
- Examples with various $L$ sets

**Key insight:** gcd condition gives much stronger bound

---

### Róka Sándor's & Tuza's Theorems

| # | Problem | Topic | File |
|---|---------|-------|------|
| 7.5 | Recent results | Modern extremal theory | [`05_roka_tuza_theorems.md`](./05_roka_tuza_theorems.md) |

**Results:**
- Symmetric difference: $|A_i \triangle A_j| \in L \Rightarrow m \leq \binom{n}{s}$
- Triple intersection: $|A_i \cap A_j \cap A_k| \leq 1 \Rightarrow m \leq \frac{1}{3}n(n-1)$
- Independent systems: $c_1 \log n \leq m \leq c_2 n^2$
- Tuza's cross-intersection inequalities

**Applications:** Coding theory, data structures

---

### Simplices & Chemical Applications

| # | Problem | Topic | File |
|---|---------|-------|------|
| 7.6 | Minimal reactions | Chemical applications | [`06_simplices_chemical.md`](./06_simplices_chemical.md) |

**Results:**
- Water formation: $\{H_2, O_2, H_2O\}$ is a simplex
- Methane combustion: $\{CH_4, O_2, CO_2, H_2O\}$ is a simplex
- Algorithm for finding all minimal reactions

**Connection:** Minimal reactions = simplices in vector space

---

## Formulas Summary

### Main Theorems

| Theorem | Condition | Bound |
|---------|-----------|-------|
| **Sperner** | $A_i \not\subseteq A_j$ | $\binom{n}{\lfloor n/2 \rfloor}$ |
| **Lubell** | Sperner family | $\sum \frac{1}{\binom{n}{|A_i|}} \leq 1$ |
| **EKR** | Intersecting, $k \leq n/2$ | $\binom{n-1}{k-1}$ |
| **Erdős-DeBruijn** | $|A_i \cap A_j| = 1$ | $n$ |
| **Fisher** | $|A_i| = k, |A_i \cap A_j| = t$ | $n$ |
| **RCW** | $|A_i \cap A_j| \in L, |L| = s$ | $\binom{n}{s}$ |
| **Babai-Frankl** | RCW + $\gcd(L) \nmid k$ | $n$ |
| **Róka 7.15** | $|A_i \cap A_j \cap A_k| \leq 1$ | $\frac{1}{3}n(n-1)$ |
| **Róka 7.17** | Independent intersection system | $\Theta(\log n)$ to $\Theta(n^2)$ |

---

## Key Techniques Used

### 1. Chain Counting (Sperner/Lubell)
- Count maximal chains in Boolean lattice
- Each set appears in $k!(n-k)!$ chains
- Sum over all sets ≤ total chains

### 2. Linear Algebra Method
- Characteristic vectors in $\mathbb{R}^n$
- Show linear independence
- Dimension bound gives $m \leq n$

### 3. Polynomial Method (RCW)
- Construct polynomials vanishing on vectors
- Linear independence of polynomials
- Dimension of polynomial space

### 4. Shifting (EKR)
- Transform family while preserving properties
- Eventually get "canonical" form
- Bound the canonical family

### 5. Geometric Constructions
- Projective planes
- Block designs
- Achieve bounds in special cases

---

## Files Created

```
07_Extremalis_halmazok/
├── README.md
├── exercise_checklist.md
└── exercises/
    ├── 01_sperner_applications.md
    ├── 02_ekr_applications.md
    ├── 03_erdos_debruijn_fisher.md
    ├── 04_ray_chaudhuri_wilson.md
    ├── 05_roka_tuza_theorems.md
    ├── 06_simplices_chemical.md
    └── SOLUTIONS_SUMMARY.md (this file)
```

**Total:** 7 solution files + README + checklist

---

## Progress: Chapter 07 Complete! ✓

All major exercises from Chapter 07 have been solved with:
- ✅ Complete proofs and verifications
- ✅ Explicit constructions
- ✅ Connections between theorems
- ✅ Applications (chemistry, coding theory)

---

## Time Investment

| Task | Estimated Time |
|------|----------------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 5-6 hours |
| Formal exercises 7.1-7.6 | 6-8 hours |
| Writing solutions | 4-5 hours |
| **Total** | **18-23 hours** |

---

## Comparison of Extremal Bounds

For $n = 10$:

| Condition | Maximum $m$ |
|-----------|-------------|
| No condition | $2^{10} = 1024$ |
| Sperner | $\binom{10}{5} = 252$ |
| Intersecting (k=5) | $\binom{9}{4} = 126$ |
| $|A_i \cap A_j| = 1$ | $10$ |
| $|A_i \cap A_j| \in \{1,2\}$ | $\binom{10}{2} = 45$ |

**Observation:** Stronger conditions → exponentially smaller maximum!

---

## Next Steps

Options for continuing:
1. **Create quiz** for Chapter 07
2. **Continue to Chapter 08** (Partíciós problémák)
3. **Solve external problems** from Babai-Frankl [BF]

---

*Generated from solutions for Chapter 07: Extremális halmazrendszerek*  
*Source: Dr. Szalkai István - Diszkrét Matematika*
