# Chapter 05 - Rekurzív sorozatok - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 05 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 5.0 - Alapfogalmak

- [x] **HF** - Verify that $n!$ satisfies a first-order recurrence
  > $n! = n \cdot (n-1)!$

- [x] **HF** - Write recurrence for compound interest
  > $A_n = A_{n-1}(1 + r)$

- [x] **HF** - Verify Fibonacci values $f_1$ through $f_{10}$

- [x] **Study** - Binet formula verification by induction

---

### Section 5.1 - Iterációs módszer

- [x] **5.3** - Solve Hanoi towers recurrence by iteration
  > $h_{n+1} = 2h_n + 1$, $h_1 = 1$
  > **Answer:** $h_n = 2^n - 1$

- [x] **HF** - Prove by induction: $h_n = 2^{n-1}h_1 + 2^{n-1} + \cdots + 1$

- [x] **5.7** - Solve (from chapter end problems)

- [x] **5.8** - Solve (from chapter end problems)

---

### Section 5.2 - Lineáris rekurziók

#### Algebraic Properties

- [x] **HF** - Prove $S^{\text{Hom}}$ is closed under addition and scalar multiplication

- [x] **HF** - Construct $k$ linearly independent basis sequences for $k$-th order recurrence

- [x] **HF** - Prove: If $(a_n)$ and $(b_n)$ satisfy homogeneous recurrence, so does $(a_n + b_n)$

- [x] **HF** - Prove: Difference of two inhomogeneous solutions satisfies homogeneous equation

- [x] **Study** - Theorem 5.5: Solution space is $k$-dimensional

- [x] **Study** - Theorem 5.7: Inhomogén = Homogén + Partikuláris

---

### Section 5.2.2 - Állandó együtthatójú egyenletek

#### Characteristic Equation Method

- [x] **HF** - Derive characteristic equation for $a_n = d_1 a_{n-1} + \cdots + d_k a_{n-k}$

- [x] **HF** - Verify $a_n = cq^n$ leads to $q^k - d_1 q^{k-1} - \cdots - d_k = 0$

- [x] **HF** - Prove Vandermonde determinant formula (5.9) by induction

- [x] **HF** - Verify linear independence of $(q_i^n)$ for distinct $q_i$

- [x] **Study** - Theorem 5.11: General solution with distinct roots

- [x] **Study** - Theorem 5.12: General solution with multiple roots

---

### Section 5.3 - Klasszikus módszer

#### Second-Order Recurrences

- [x] **HF** - Prove Theorem 5.13 for $k=2$ case (double root)

- [x] **HF** - Verify Fibonacci satisfies $f_n = f_{n-1} + f_{n-2}$

- [x] **HF** - Derive Binet formula coefficients from $f_1 = 1, f_2 = 1$

- [x] **Study** - Connection to generating functions (Chapter 06)

---

## 🔴 Formal Exercises (Section 5.4 - Feladatok)

### 5.1.Feladat - First-order linear recurrence
- [x] Solve: $a_n = r a_{n-1} + b$
- [x] Find explicit formula

### 5.2.Feladat - Sum recurrence
- [x] Solve: $a_n = \sum_{i=0}^{n-1} a_i$
- [x] Find pattern

### 5.3.Feladat - Explicit formulas for named sequences (Lucas, Perrin, Padovan)
- [x] Analyze and solve

### 5.4.Feladat - Fibonacci properties
- [x] Prove: $\sum_{i=1}^n f_i = f_{n+2} - 1$
- [x] Prove: $f_n^2 + f_{n+1}^2 = f_{2n+1}$
- [x] Prove other Fibonacci identities

### 5.5.Feladat - Second-order homogeneous
- [x] Solve given recurrence with constant coefficients

### 5.6.Feladat - Inhomogeneous recurrence
- [x] Find particular solution
- [x] Combine with homogeneous

### 5.7.Feladat - [Problem from chapter]
- [x] Apply iteration method

### 5.8.Feladat - [Problem from chapter]
- [x] Apply classical method

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter on recursive sequences
- [ ] Additional recurrence problems

### From Mickens [M]
- [ ] Journal of Difference Equations problems

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 15 | 15 | 100% |
| Formal 5.1-5.8 | 8 | 8 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **23** | **23** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** First-order recurrences (geometric, arithmetic)
2. **Master:** Iteration method for simple cases
3. **Understand:** Characteristic equation method
4. **Practice:** Finding particular solutions for inhomogeneous cases
5. **Key technique:** Verify solutions by substitution

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 4-5 hours |
| Formal exercises 5.1-5.8 | 5-7 hours |
| External problems | 4-6 hours |
| **Total** | **16-22 hours** |

---

## 📝 Key Formulas to Memorize

```
□ First-order linear: aₙ = r·aₙ₋₁ + b
□ Characteristic equation: q^k - d₁q^(k-1) - ... - dₖ = 0
□ Distinct roots: aₙ = c₁q₁ⁿ + c₂q₂ⁿ + ... + cₖqₖⁿ
□ Multiple roots: aₙ = (c₁ + c₂n + ... + cₘn^(m-1))qⁿ
□ Fibonacci: fₙ = (φⁿ - ψⁿ)/√5
□ Hanoi: hₙ = 2ⁿ - 1
```

---

## Common Recurrence Types

| Type | Form | Solution Method |
|------|------|-----------------|
| First-order linear | $a_n = ra_{n-1} + b$ | Iteration or formula |
| Second-order homogeneous | $a_n = c_1 a_{n-1} + c_2 a_{n-2}$ | Characteristic equation |
| Second-order inhomogeneous | $a_n = c_1 a_{n-1} + c_2 a_{n-2} + f(n)$ | Homogeneous + particular |
| Sum recurrence | $a_n = \sum_{i=0}^{n-1} a_i$ | Transform to difference |
| Divide-and-conquer | $T(n) = aT(n/b) + f(n)$ | Master theorem |

---

*Generated from Chapter 05: Rekurzív sorozatok*  
*Source: Dr. Szalkai István - Diszkrét Matematika*
