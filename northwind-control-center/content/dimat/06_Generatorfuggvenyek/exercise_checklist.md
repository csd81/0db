# Chapter 06 - Generátorfüggvények - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 06 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 6.0 - Alapfogalmak

- [x] **HF** - Verify: If $G(x) = xF(x)$, then coefficients satisfy $b_n = a_{n-1}$

- [x] **HF** - Compute first 5 terms of geometric series $\frac{1}{1-x}$

- [x] **Study** - Connection to Laplace transform

---

### Section 6.1 - Lineáris rekurziók

#### Fibonacci Example (6.3)

- [x] **HF** - Verify $f_0 = 0$ keeps recurrence valid for $n=2$

- [x] **HF** - Derive $F(x) = \frac{x}{1-x-x^2}$ step by step

- [x] **HF** - Partial fraction decomposition of $\frac{x}{1-x-x^2}$

- [x] **HF** - Verify Binet formula by substitution for $n=1,2,3,4,5$

#### Hanoi Example (6.4)

- [x] **HF** - Verify $h_0 = 0$ keeps recurrence valid

- [x] **HF** - Derive $H(x) = \frac{x}{(1-x)(1-2x)}$

- [x] **HF** - Partial fractions: $\frac{x}{(1-x)(1-2x)} = \frac{1}{1-2x} - \frac{1}{1-x}$

- [x] **HF** - Extract coefficients to get $h_n = 2^n - 1$

#### General Method (6.5)

- [x] **HF** - Apply method to $a_n = 3a_{n-1} - 2a_{n-2}$

- [x] **HF** - Apply method to $a_n = 2a_{n-1} + n$

---

### Section 6.2 - Newton Binomiális Sora

- [x] **HF** - Prove: $(1-x)^{-k} = \sum_{n=0}^{\infty} \binom{n+k-1}{k-1} x^n$

- [x] **HF** - Expand $(1+x)^{-1/2}$ using generalized binomial coefficients

- [x] **HF** - Show: $\binom{-1/2}{n} = (-1)^n \frac{\binom{2n}{n}}{4^n}$

- [x] **Study** - Convergence conditions $|x| < |a|$

---

### Section 6.3 - Nemlineáris rekurziók

#### Catalan Numbers

- [x] **HF** - Derive $C(x) = 1 + xC(x)^2$ from recurrence

- [x] **HF** - Solve quadratic for $C(x)$

- [x] **HF** - Explain why $C(x) = \frac{1-\sqrt{1-4x}}{2x}$ (not plus sign)

- [x] **HF** - Extract coefficients to get $C_n = \frac{1}{n+1}\binom{2n}{n}$

- [x] **HF** - Verify $C_0$ through $C_5$

- [x] **Study** - Applications: bracketings, binary trees, Dyck paths

---

### Section 6.4 - Exponenciális generátorfüggvények

- [x] **HF** - Compute exponential GF for $a_n = 1$ (all n)

- [x] **HF** - Compute exponential GF for $a_n = n$

- [x] **HF** - Relation between ordinary and exponential GF

- [x] **Study** - Applications to permutations

---

## 🔴 Formal Exercises (Section 6.4 - Feladatok)

### 6.1.Feladat - Plane regions via generating functions
- [x] Set up GF equation for $c_{n+1} = c_n + 1 + n$, $c_0 = 1$
- [x] Derive $F(x) = \frac{1-x+x^2}{(1-x)^3}$ and extract $c_n = \frac{n^2+n+2}{2}$

### 6.2.Feladat - Parenthesizations of an n-factor product
- [x] Show recurrence reduces to Catalan: $b_n = C_{n-1}$
- [x] Derive closed form $b_n = \frac{1}{n}\binom{2n-2}{n-1}$

### 6.3.Feladat - Triangulations of a convex (n+2)-gon
- [x] Derive Catalan recurrence from edge-triangle decomposition
- [x] Conclude $c_n = C_n = \frac{1}{n+1}\binom{2n}{n}$

### 6.4.Feladat - Non-crossing chord pairings on 2n points
- [x] Derive Catalan recurrence from point-matching argument
- [x] Conclude $d_n = C_n = \frac{1}{n+1}\binom{2n}{n}$

### 6.5.Feladat - Non-negative solutions of $y_1 + \ldots + y_k = n$
- [x] Apply coin-change GF: $F(x) = (1-x)^{-k}$
- [x] Extract $a_n = \binom{n+k-1}{k-1}$ (combinations with repetition)

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter on generating functions
- [ ] Additional recurrence problems

### From Wilf [W]
- [ ] Generatingfunctionology exercises

### From Sárközy [Sa]
- [ ] Hungarian problem sets

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 20 | 20 | 100% |
| Formal 6.1-6.5 | 5 | 5 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **25** | **25** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** Simple geometric series and first-order recurrences
2. **Master:** Partial fraction decomposition
3. **Understand:** Connection between recurrence and rational functions
4. **Practice:** Coefficient extraction from various series
5. **Key technique:** Recognize standard generating function forms

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 5-6 hours |
| Formal exercises 6.1-6.8 | 6-8 hours |
| External problems | 4-6 hours |
| **Total** | **18-24 hours** |

---

## 📝 Key Formulas to Memorize

```
□ Geometric: 1/(1-x) = Σxⁿ
□ Negative binomial: (1-x)^(-k) = ΣC(n+k-1,k-1)xⁿ
□ Fibonacci GF: x/(1-x-x²)
□ Catalan GF: (1-√(1-4x))/(2x)
□ Binomial: (1+x)^α = ΣC(α,n)xⁿ
```

---

## Common Generating Functions

| Sequence | Ordinary GF | Exponential GF |
|----------|-------------|----------------|
| $1, 1, 1, \ldots$ | $\frac{1}{1-x}$ | $e^x$ |
| $1, r, r^2, \ldots$ | $\frac{1}{1-rx}$ | $e^{rx}$ |
| $1, 2, 3, \ldots$ | $\frac{1}{(1-x)^2}$ | $xe^x$ |
| Fibonacci | $\frac{x}{1-x-x^2}$ | - |
| Catalan | $\frac{1-\sqrt{1-4x}}{2x}$ | - |
| $n!$ | - | $\frac{1}{1-x}$ |

---

*Generated from Chapter 06: Generátorfüggvények*  
*Source: Dr. Szalkai István - Diszkrét Matematika*
