# Chapter 04 - Exercise Solutions Summary

## ✅ Completed Solutions

All formal exercises from Chapter 04 (A logikai szitaformula) have been solved.

---

## Exercise Solutions by Topic

### Inclusion-Exclusion Basics

| # | Problem | Topic | File |
|---|---------|-------|------|
| 4.1 | 67 students, 3 languages | Basic 3-set inclusion-exclusion | [`01_three_languages.md`](./01_three_languages.md) |

**Result:** 6 students speak none of the languages

**Key formula:**
$$|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$$

---

### Derangements (Fixed-Point-Free Permutations)

| # | Problem | Topic | File |
|---|---------|-------|------|
| 4.2 | Exactly 1 fixed point (n=5) | Partial derangements | [`02_derangement_problems.md`](./02_derangement_problems.md) |
| 4.4 | Prove $D_n = n D_{n-1} + (-1)^n$ | Derangement recurrence | [`02_derangement_problems.md`](./02_derangement_problems.md) |

**Key formulas:**
$$D_n = n! \sum_{k=0}^{n} \frac{(-1)^k}{k!} \approx \frac{n!}{e}$$

$$\text{Exactly } k \text{ fixed points: } \binom{n}{k} D_{n-k}$$

---

### Distribution Problems

| # | Problem | Topic | File |
|---|---------|-------|------|
| 4.3 | $r$ objects to $n+p$ people | Constrained distributions | [`02_derangement_problems.md`](./02_derangement_problems.md) |
| 4.6a | 6 toys to 4 children | Surjections $S(6,4)$ | [`03_surjective_functions.md`](./03_surjective_functions.md) |
| 4.6b | 7 tasks to 5 workers | Constrained surjections | [`03_surjective_functions.md`](./03_surjective_functions.md) |

**Key formula:**
$$\text{Distributions} = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n+p-i)^r$$

---

### Surjective Functions

| # | Problem | Topic | File |
|---|---------|-------|------|
| 4.5 | General surjection formula | $S(m,n)$ derivation | [`03_surjective_functions.md`](./03_surjective_functions.md) |
| 4.7 | Special cases | $S(m,1)$, $S(m,2)$, $S(n,n)$, etc. | [`03_surjective_functions.md`](./03_surjective_functions.md) |

**Key formulas:**
$$S(m,n) = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n-i)^m = n! \cdot \stirling{m}{n}$$

| Special Case | Formula |
|--------------|---------|
| $S(m, 1)$ | $1$ |
| $S(m, 2)$ | $2^m - 2$ |
| $S(n, n)$ | $n!$ |
| $S(n+1, n)$ | $\binom{n+1}{2} \cdot n!$ |

---

### Number Theory

| # | Problem | Topic | File |
|---|---------|-------|------|
| 4.8 | Relatively prime numbers | Euler's φ-function | [`04_number_theory_polynomials.md`](./04_number_theory_polynomials.md) |

**Key formulas:**
$$P = \sum_{d | n^\infty} \mu(d) \left\lfloor \frac{M}{d} \right\rfloor$$

$$\phi(n) = n \prod_{p | n} \left(1 - \frac{1}{p}\right)$$

**Example:** $\phi(210) = 48$, count $\leq 10000$ coprime to 210 = 2285

---

### Polynomial Identities

| # | Problem | Topic | File |
|---|---------|-------|------|
| 4.9 | Alternating binomial sum | $\sum (-1)^{n-i} \binom{n}{i} i^k$ | [`04_number_theory_polynomials.md`](./04_number_theory_polynomials.md) |
| 4.10 | Polynomial expansion | $\prod (1-x_i)$ | [`04_number_theory_polynomials.md`](./04_number_theory_polynomials.md) |

**Key results:**
$$\sum_{i=0}^{n} (-1)^{n-i} \binom{n}{i} i^k = \begin{cases} 0 & k < n \\ n! & k = n \end{cases}$$

$$\prod_{i=1}^{r} (1-x_i) = 1 - \sum x_i + \sum x_i x_j - \sum x_i x_j x_k + \cdots$$

---

## Formulas Summary

### Inclusion-Exclusion Principle

$$\left|\bigcup_{i=1}^{m} A_i\right| = \sum_{\emptyset \neq J \subseteq [m]} (-1)^{|J|-1} \left|\bigcap_{j \in J} A_j\right|$$

### Derangements

| Formula | Expression |
|---------|------------|
| Closed form | $D_n = n! \sum_{k=0}^{n} \frac{(-1)^k}{k!}$ |
| Recurrence 1 | $D_n = n D_{n-1} + (-1)^n$ |
| Recurrence 2 | $D_n = (n-1)(D_{n-1} + D_{n-2})$ |
| Asymptotic | $D_n \sim \frac{n!}{e}$ |

### Surjections

$$S(m,n) = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n-i)^m$$

### Euler's φ-function

$$\phi(n) = n \prod_{p|n} \left(1 - \frac{1}{p}\right) = \sum_{d|n} \mu(d) \frac{n}{d}$$

---

## Key Techniques Used

### 1. Inclusion-Exclusion Principle
- Count complement instead of direct count
- Alternate adding and subtracting intersections

### 2. Derangement Applications
- Fixed-point-free permutations
- Hat-check problem
- Letter-envelope matching

### 3. Surjection Counting
- Distribute distinct objects with constraints
- Connect to Stirling numbers of second kind

### 4. Number Theory Applications
- Count coprime numbers
- Möbius inversion

### 5. Polynomial Methods
- Derivative operators for binomial sums
- Product expansions

---

## Files Created

```
04_Logikai_szitaformula/
├── README.md
├── exercise_checklist.md
└── exercises/
    ├── 01_three_languages.md
    ├── 02_derangement_problems.md
    ├── 03_surjective_functions.md
    ├── 04_number_theory_polynomials.md
    └── SOLUTIONS_SUMMARY.md (this file)
```

**Total:** 5 solution files + README + checklist

---

## Progress: Chapter 04 Complete! ✓

All formal exercises from Chapter 04 have been solved with:
- ✅ Complete proofs
- ✅ Verification tables
- ✅ Alternative solutions
- ✅ Connections to other areas

---

## Time Investment

| Task | Estimated Time |
|------|----------------|
| Reading chapter | 2-3 hours |
| In-chapter HF | 2-3 hours |
| Formal exercises 4.1-4.10 | 4-5 hours |
| Writing solutions | 3-4 hours |
| **Total** | **11-15 hours** |

---

## Next Steps

Options for continuing:
1. **Create quiz** for Chapter 04
2. **Continue to Chapter 05** (Rekurzív sorozatok / Recursive Sequences)
3. **Solve external problems** from [SzIs;97] or Lovász [L]

---

*Generated from solutions for Chapter 04: A logikai szitaformula*  
*Source: Dr. Szalkai István - Diszkrét Matematika*
