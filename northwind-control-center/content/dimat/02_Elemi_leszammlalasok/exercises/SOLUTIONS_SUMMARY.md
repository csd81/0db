# Chapter 02 - Exercise Solutions Summary

## ✅ Completed Solutions

All solutions for Chapter 02 (Elemi leszámlálások) exercises have been solved and documented.

---

## Exercise 2.1 - Induction Proofs (10 problems)

| # | Problem | Topic | File |
|---|---------|-------|------|
| 1 | $\sum i^3 = [n(n+1)/2]^2$ | Sum of cubes | [`01_sum_of_cubes.md`](./01_sum_of_cubes.md) |
| 2 | $H_{2^n} \geq n/2$ | Harmonic inequality | [`02_harmonic_inequality.md`](./02_harmonic_inequality.md) |
| 3 | $\sum k! \cdot k = (n+1)! - 1$ | Factorial sum | [`03_factorial_sum.md`](./03_factorial_sum.md) |
| 4 | $\sum (-1)^k k^2 = (-1)^n \cdot n(n+1)/2$ | Alternating squares | [`04_alternating_square_sum.md`](./04_alternating_square_sum.md) |
| 5 | If $a + 1/a \in \mathbb{Z}$, then $a^n + 1/a^n \in \mathbb{Z}$ | Algebraic integers | [`05_algebraic_integers.md`](./05_algebraic_integers.md) |
| 6 | $n$ lines divide plane into $(n^2+n+2)/2$ regions | Plane division | [`06_plane_division.md`](./06_plane_division.md) |
| 7 | Equal sum partition of $\{1,...,2n\}$ | Partition (even n only) | [`07_equal_sum_partition.md`](./07_equal_sum_partition.md) |
| 8 | $\sum (2i-1) = n^2$ | Sum of odd numbers | [`08_sum_of_odds.md`](./08_sum_of_odds.md) |
| 9 | $\sum i(i+1) = n(n+1)(n+2)/3$ | Product sum | [`09_product_sum.md`](./09_product_sum.md) |
| 10 | $H_{2^n} \geq 1 + n/2$ | Harmonic numbers | [`10_harmonic_numbers.md`](./10_harmonic_numbers.md) |

---

## Exercises 2.2 & 2.3 - Combinatorial Problems

| # | Problem | Answer | File |
|---|---------|--------|------|
| 2.2 | Solutions to $x_1 + ... + x_k = n$ | $\binom{n+k-1}{k-1}$ | [`11_miscellaneous_problems.md`](./11_miscellaneous_problems.md) |
| 2.3 | Max diagonal intersections in n-gon | $\binom{n}{4}$ | [`11_miscellaneous_problems.md`](./11_miscellaneous_problems.md) |

---

## Key Techniques Used

### 1. Mathematical Induction
- Base case verification
- Inductive hypothesis
- Inductive step proof

### 2. Strong Induction
- Using multiple previous cases (Exercise 5)

### 3. Combinatorial Arguments
- Stars and bars (Exercise 2.2)
- Bijection counting (Exercise 2.3)
- Geometric reasoning (Exercise 6)

### 4. Algebraic Manipulation
- Factoring
- Common denominators
- Telescoping sums

### 5. Known Identities
- Sum of first n numbers: $n(n+1)/2$
- Sum of squares: $n(n+1)(2n+1)/6$
- Hockey-stick identity
- Binomial coefficient properties

---

## Formulas Proven

### Summation Formulas

| Sum | Closed Form | Exercise |
|-----|-------------|----------|
| $\sum_{i=1}^n i^3$ | $\left[\frac{n(n+1)}{2}\right]^2$ | 2.1/1 |
| $\sum_{i=1}^n i! \cdot i$ | $(n+1)! - 1$ | 2.1/3 |
| $\sum_{i=1}^n (-1)^i i^2$ | $(-1)^n \cdot \frac{n(n+1)}{2}$ | 2.1/4 |
| $\sum_{i=1}^n (2i-1)$ | $n^2$ | 2.1/8 |
| $\sum_{i=1}^n i(i+1)$ | $\frac{n(n+1)(n+2)}{3}$ | 2.1/9 |

### Inequalities

| Inequality | Exercise |
|------------|----------|
| $H_{2^n} \geq \frac{n}{2}$ | 2.1/2 |
| $H_{2^n} \geq 1 + \frac{n}{2}$ | 2.1/10 |

### Combinatorial Formulas

| Problem | Formula | Exercise |
|---------|---------|----------|
| Plane division by n lines | $\frac{n^2+n+2}{2}$ | 2.1/6 |
| Combinations with repetition | $\binom{n+k-1}{k-1}$ | 2.2 |
| Polygon diagonal intersections | $\binom{n}{4}$ | 2.3 |

---

## Interesting Discoveries

### Exercise 2.1/5 - Recurrence Relation
Discovered the recurrence:
$$S_{n+1} = S_1 \cdot S_n - S_{n-1}$$
where $S_n = a^n + \frac{1}{a^n}$

This connects to **Chebyshev polynomials**!

### Exercise 2.1/6 - Lazy Caterer's Sequence
The plane division formula is known as the **Lazy Caterer's Sequence**:
$$1, 2, 4, 7, 11, 16, 22, 29, ...$$

### Exercise 2.1/7 - Parity Constraint
Discovered the partition is **only possible for even n** because the total sum $n(2n+1)$ must be even.

### Exercise 2.1/3 - Telescoping Alternative
Found a non-inductive proof using telescoping:
$$k! \cdot k = (k+1)! - k!$$

---

## Time Investment

| Task | Estimated Time |
|------|----------------|
| Reading chapter | 2-3 hours |
| Solving 2.1 (10 problems) | 4-5 hours |
| Solving 2.2 & 2.3 | 1 hour |
| Writing solutions | 3-4 hours |
| **Total** | **10-13 hours** |

---

## Files Created

```
02_Elemi_leszammlalasok/
├── README.md
├── exercise_checklist.md
└── exercises/
    ├── 01_sum_of_cubes.md
    ├── 02_harmonic_inequality.md
    ├── 03_factorial_sum.md
    ├── 04_alternating_square_sum.md
    ├── 05_algebraic_integers.md
    ├── 06_plane_division.md
    ├── 07_equal_sum_partition.md
    ├── 08_sum_of_odds.md
    ├── 09_product_sum.md
    ├── 10_harmonic_numbers.md
    └── 11_miscellaneous_problems.md
```

**Total:** 12 solution files + README + checklist

---

## Progress: Chapter 02 Complete! ✓

All formal exercises from Chapter 02 have been solved with:
- ✅ Complete proofs
- ✅ Verification tables
- ✅ Alternative solutions
- ✅ Historical context
- ✅ Related formulas

---

## Next Steps

Options for continuing:
1. **Chapter 03** - Binomiális együtthatók (Binomial Coefficients)
2. **Create quiz** for Chapter 02
3. **Solve external problems** from [SzIs;97] referenced in the chapter

---

*Generated from solutions for Chapter 02: Elemi leszámlálások*  
*Source: Dr. Szalkai István - Diszkrét Matematika*
