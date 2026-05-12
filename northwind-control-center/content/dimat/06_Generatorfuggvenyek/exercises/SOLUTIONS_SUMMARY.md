# Chapter 06 - Exercise Solutions Summary

## ✅ Completed Solutions

Solutions for Chapter 06 (Generátorfüggvények) exercises.

---

## Exercise Solutions by Topic

### Basic Generating Functions

| # | Problem | Topic | File |
|---|---------|-------|------|
| 6.1 | $a_n = r a_{n-1} + b$ | First-order linear via GF | [`01_first_order_gf.md`](./01_first_order_gf.md) |

**Result:**
$$a_n = \begin{cases}
A r^n + \dfrac{b(r^n - 1)}{r - 1} & r \neq 1 \\
A + bn & r = 1
\end{cases}$$

**Key technique:** Partial fraction decomposition of $\frac{A}{1-rx} + \frac{bx}{(1-x)(1-rx)}$

---

### Fibonacci Numbers

| # | Problem | Topic | File |
|---|---------|-------|------|
| 6.2 | $f_n = f_{n-1} + f_{n-2}$ | Second-order via GF | [`02_fibonacci_gf.md`](./02_fibonacci_gf.md) |

**Result (Binet's Formula):**
$$f_n = \frac{\phi^n - \psi^n}{\sqrt{5}}, \quad \phi = \frac{1+\sqrt{5}}{2}, \psi = \frac{1-\sqrt{5}}{2}$$

**Generating Function:**
$$F(x) = \frac{x}{1-x-x^2}$$

**Key steps:**
1. Derive $F(x) = \frac{x}{1-x-x^2}$
2. Factor denominator: $(1-\phi x)(1-\psi x)$
3. Partial fractions: $\frac{1}{\sqrt{5}}\left(\frac{1}{1-\phi x} - \frac{1}{1-\psi x}\right)$
4. Extract coefficients

---

### Catalan Numbers

| # | Problem | Topic | File |
|---|---------|-------|------|
| 6.3 | $C_{n+1} = \sum_{i=0}^n C_i C_{n-i}$ | Nonlinear recurrence | [`03_catalan_numbers.md`](./03_catalan_numbers.md) |

**Result:**
$$C_n = \frac{1}{n+1}\binom{2n}{n}$$

**Generating Function:**
$$C(x) = \frac{1-\sqrt{1-4x}}{2x}$$

**Key insight:** Convolution $\sum C_i C_{n-i}$ corresponds to $C(x)^2$

**Values:** 1, 1, 2, 5, 14, 42, 132, 429, 1430, ...

---

## Formulas Summary

### Method Summary

| Step | Action |
|------|--------|
| 1 | Define $F(x) = \sum a_n x^n$ |
| 2 | Multiply recurrence by $x^n$, sum over valid $n$ |
| 3 | Express sums in terms of $F(x)$ |
| 4 | Solve algebraic equation for $F(x)$ |
| 5 | Partial fraction decomposition |
| 6 | Expand as power series |
| 7 | Extract coefficient $[x^n]F(x) = a_n$ |

### Common Generating Functions

| Sequence | Generating Function | Explicit Formula |
|----------|---------------------|------------------|
| Constant $(1)$ | $\frac{1}{1-x}$ | $1$ |
| Geometric $(r^n)$ | $\frac{1}{1-rx}$ | $r^n$ |
| Arithmetic $(n)$ | $\frac{x}{(1-x)^2}$ | $n$ |
| First-order linear | $\frac{A}{1-rx} + \frac{bx}{(1-x)(1-rx)}$ | See above |
| Fibonacci | $\frac{x}{1-x-x^2}$ | $\frac{\phi^n - \psi^n}{\sqrt{5}}$ |
| Catalan | $\frac{1-\sqrt{1-4x}}{2x}$ | $\frac{1}{n+1}\binom{2n}{n}$ |

### Useful Series Expansions

| Function | Expansion |
|----------|-----------|
| $\frac{1}{1-x}$ | $\sum_{n=0}^{\infty} x^n$ |
| $\frac{1}{1-rx}$ | $\sum_{n=0}^{\infty} r^n x^n$ |
| $\frac{1}{(1-x)^k}$ | $\sum_{n=0}^{\infty} \binom{n+k-1}{k-1} x^n$ |
| $(1-x)^{1/2}$ | $1 - \sum_{n=1}^{\infty} \frac{2}{n}\binom{2n-2}{n-1} x^n$ |
| $(1-4x)^{-1/2}$ | $\sum_{n=0}^{\infty} \binom{2n}{n} x^n$ |

---

## Key Techniques Used

### 1. Generating Function Setup
- Multiply recurrence by $x^n$
- Sum over appropriate range
- Shift indices to match $F(x)$

### 2. Algebraic Manipulation
- Solve linear/quadratic equations for $F(x)$
- Handle initial conditions automatically

### 3. Partial Fraction Decomposition
- Factor denominator
- Find coefficients A, B, ...
- Express as sum of simpler fractions

### 4. Series Expansion
- Geometric series: $\frac{1}{1-ax} = \sum a^n x^n$
- Newton binomial: $(1+x)^\alpha = \sum \binom{\alpha}{n} x^n$
- Extract $[x^n]$ coefficient

### 5. Convolution Recognition
- $\sum_{i=0}^n a_i b_{n-i} = [x^n] A(x)B(x)$
- Catalan: $C_{n+1} = \sum C_i C_{n-i} \Rightarrow C(x) = 1 + xC(x)^2$

---

## Files Created

```
06_Generatorfuggvenyek/
├── README.md
├── exercise_checklist.md
└── exercises/
    ├── 01_first_order_gf.md
    ├── 02_fibonacci_gf.md
    ├── 03_catalan_numbers.md
    └── SOLUTIONS_SUMMARY.md (this file)
```

**Total:** 4 solution files + README + checklist

---

## Progress: Chapter 06 Complete! ✓

All formal exercises from Chapter 06 have been solved with:
- ✅ Complete derivations
- ✅ Verification tables
- ✅ Alternative methods
- ✅ Applications

---

## Time Investment

| Task | Estimated Time |
|------|----------------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 5-6 hours |
| Formal exercises 6.1-6.3 | 4-5 hours |
| Writing solutions | 3-4 hours |
| **Total** | **15-19 hours** |

---

## Comparison: Generating Functions vs. Classical Method

| Aspect | Classical (Ch. 5) | Generating Functions (Ch. 6) |
|--------|-------------------|------------------------------|
| Approach | Characteristic equation | Algebraic equation for F(x) |
| Initial conditions | Determine constants at end | Built into derivation |
| Inhomogeneous | Need particular solution | Handled automatically |
| Nonlinear | Limited applicability | Works for some (e.g., Catalan) |
| Complexity | Medium | Medium-High |

---

## Next Steps

Options for continuing:
1. **Create quiz** for Chapter 06
2. **Continue to Chapter 07** (Extremális halmazok)
3. **Solve external problems** from Wilf [W] or Sárközy [Sa]

---

*Generated from solutions for Chapter 06: Generátorfüggvények*  
*Source: Dr. Szalkai István - Diszkrét Matematika*
