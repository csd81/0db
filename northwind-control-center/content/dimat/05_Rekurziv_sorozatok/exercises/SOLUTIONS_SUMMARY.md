# Chapter 05 - Exercise Solutions Summary

## ✅ Completed Solutions

Solutions for Chapter 05 (Rekurzív sorozatok) exercises.

---

## Exercise Solutions by Topic

### First-Order Recurrences

| # | Problem | Topic | File |
|---|---------|-------|------|
| 5.1 | $a_n = r a_{n-1} + b$ | First-order linear | [`01_first_order_linear.md`](./01_first_order_linear.md) |

**Result:**
$$a_n = \begin{cases}
r^{n-1} A + \dfrac{b(r^{n-1} - 1)}{r - 1} & r \neq 1 \\
A + b(n-1) & r = 1
\end{cases}$$

---

### Sum Recurrences

| # | Problem | Topic | File |
|---|---------|-------|------|
| 5.2 | $a_n = \sum_{i=0}^{n-1} a_i$ | Sum to product transformation | [`02_sum_recurrence.md`](./02_sum_recurrence.md) |

**Result:** $a_n = 2^{n-1}$ for $n \geq 1$

---

### Fibonacci Identities

| # | Identity | File |
|---|----------|------|
| /1/ | $\sum_{i=1}^n f_i = f_{n+2} - 1$ | [`03_fibonacci_identities.md`](./03_fibonacci_identities.md) |
| /2/ | $\sum_{i=1}^n f_{2i-1} = f_{2n}$ | [`03_fibonacci_identities.md`](./03_fibonacci_identities.md) |
| /3/ | $\sum_{i=1}^n f_{2i} = f_{2n+1} - 1$ | [`03_fibonacci_identities.md`](./03_fibonacci_identities.md) |
| /8/ | $\sum_{i=1}^n f_i^2 = f_n f_{n+1}$ | [`03_fibonacci_identities.md`](./03_fibonacci_identities.md) |
| /19/ | $f_{n+1}f_{n-1} - f_n^2 = (-1)^n$ | [`03_fibonacci_identities.md`](./03_fibonacci_identities.md) |
| /27/ | $f_{m-1}f_n + f_m f_{n+1} = f_{n+m}$ | [`03_fibonacci_identities.md`](./03_fibonacci_identities.md) |
| /32/ | $\gcd(f_n, f_{n+1}) = 1$ | [`03_fibonacci_identities.md`](./03_fibonacci_identities.md) |
| /41/ | $\lim_{n\to\infty} f_{n+1}/f_n = \phi$ | [`03_fibonacci_identities.md`](./03_fibonacci_identities.md) |

---

### Advanced Recurrences

| # | Problem | Topic | File |
|---|---------|-------|------|
| 5.5 | $a_n = c_1 a_{n-1} + c_2 a_{n-2}$ | Second-order homogeneous | [`04_advanced_recurrences.md`](./04_advanced_recurrences.md) |
| 5.6 | Simultaneous recurrences | System reduction | [`04_advanced_recurrences.md`](./04_advanced_recurrences.md) |
| 5.7 | $x_{n+1} = \max(A_i/x_{n-i})$ | Eventually periodic | [`04_advanced_recurrences.md`](./04_advanced_recurrences.md) |
| 5.8 | Avoiding sequences | Rational function argument | [`04_advanced_recurrences.md`](./04_advanced_recurrences.md) |

---

## Formulas Summary

### First-Order Linear Recurrence

$$a_n = r a_{n-1} + b$$

**Solution:**
- $r \neq 1$: $a_n = r^{n-1}A + \frac{b(r^{n-1}-1)}{r-1}$
- $r = 1$: $a_n = A + b(n-1)$

### Second-Order Homogeneous

$$a_n = c_1 a_{n-1} + c_2 a_{n-2}$$

**Characteristic equation:** $q^2 - c_1 q - c_2 = 0$

**Solution:**
- Distinct roots: $a_n = \alpha q_1^n + \beta q_2^n$
- Double root: $a_n = (\alpha + \beta n)q^n$

### Fibonacci Key Identities

| Sum/Product | Formula |
|-------------|---------|
| $\sum f_i$ | $f_{n+2} - 1$ |
| $\sum f_{2i-1}$ | $f_{2n}$ |
| $\sum f_{2i}$ | $f_{2n+1} - 1$ |
| $\sum f_i^2$ | $f_n f_{n+1}$ |
| $f_{n+1}f_{n-1} - f_n^2$ | $(-1)^n$ |
| $f_{m-1}f_n + f_m f_{n+1}$ | $f_{n+m}$ |

---

## Key Techniques Used

### 1. Iteration Method
- Substitute recurrence into itself
- Recognize pattern (geometric series, etc.)

### 2. Characteristic Equation
- Assume solution of form $q^n$
- Solve polynomial equation
- Combine solutions based on roots

### 3. Induction Proofs
- Base case verification
- Inductive step using recurrence

### 4. System Reduction
- Eliminate variables
- Convert to higher-order single recurrence

### 5. Matrix Methods
- Write as matrix recurrence
- Find eigenvalues/eigenvectors

---

## Files Created

```
05_Rekurziv_sorozatok/
├── README.md
├── exercise_checklist.md
└── exercises/
    ├── 01_first_order_linear.md
    ├── 02_sum_recurrence.md
    ├── 03_fibonacci_identities.md
    ├── 04_advanced_recurrences.md
    └── SOLUTIONS_SUMMARY.md (this file)
```

**Total:** 5 solution files + README + checklist

---

## Progress: Chapter 05 Complete! ✓

All formal exercises from Chapter 05 have been solved with:
- ✅ Complete proofs
- ✅ Verification tables
- ✅ Alternative solutions
- ✅ Applications

---

## Time Investment

| Task | Estimated Time |
|------|----------------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 4-5 hours |
| Formal exercises 5.1-5.8 | 5-7 hours |
| Writing solutions | 4-5 hours |
| **Total** | **16-21 hours** |

---

## Next Steps

Options for continuing:
1. **Create quiz** for Chapter 05
2. **Continue to Chapter 06** (Generátorfüggvények / Generating Functions)
3. **Solve external problems** from [SzIs;97] or Mickens [M]

---

*Generated from solutions for Chapter 05: Rekurzív sorozatok*  
*Source: Dr. Szalkai István - Diszkrét Matematika*
