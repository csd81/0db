# Chapter 03 - Binomiális együtthatók - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 03 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 3.1 - Binomiális és polinomiális tételek

- [x] **HF** - Prove Newton binomial theorem by induction using Pascal's rule (3.6)
  > $(a+b)^n = \sum_{i=0}^{n} \binom{n}{i} a^i b^{n-i}$

- [x] **HF** - Prove Newton-Leibniz formula (3.2) by induction
  > $(fg)^{(n)} = \sum_{i=0}^{n} \binom{n}{i} f^{(i)} g^{(n-i)}$

- [x] **Study** - Newton binomial series (3.4) for $\alpha = -1$
  > Will be needed for Chapter 06 (Generating Functions)

---

### Section 3.2 - Properties of Binomial Coefficients

- [x] **3.8** - Estimate $\binom{n}{k}$ using Stirling's formula for large n and k

- [x] **HF** - Verify Pascal's triangle properties from (3.6)

- [x] **HF** - Prove Vandermonde convolution (3.11) algebraically using formulas
  > $\sum_{i=0}^{k} \binom{n}{i}\binom{m}{k-i} = \binom{n+m}{k}$

- [x] **HF** - Prove upper summation (3.12) by induction
  > $\sum_{i=k}^{n} \binom{i}{k} = \binom{n+1}{k+1}$

- [x] **HF** - Prove monotonicity (3.13) using $\binom{n}{i+1} = \binom{n}{i} \cdot \frac{n-i}{i+1}$

---

### Section 3.3 - Summation Methods

- [x] **HF** - Prove sum identities (3.14) combinatorially
  > $\sum \binom{n}{i} = 2^n$ and $\sum (-1)^i\binom{n}{i} = 0$

- [x] **HF** - Derive weighted sums (3.15) using derivatives/integrals
  > $\sum i\binom{n}{i} = n2^{n-1}$

- [x] **HF** - Construct $P_k(n)$ polynomials explicitly (from 3.17 proof)
  > Find coefficients $b_j$ in $x^k = \sum b_j \binom{x}{j}$

- [x] **Study** - C Appendix for $P_k(n)$ polynomials and basis transformation

---

## 🔴 Formal Exercises (Section 3.5)

### 3.1.Feladat - Factorial Identity
- [x] Prove:
  $$\frac{1}{0!1![(n-1)!]^2} + \frac{1}{1!2![(n-2)!]^2} + \cdots = \frac{(2n-1)!}{[n!(n-1)!]^2}$$

---

### 3.2.Feladat - Binomial Coefficient Identities

Prove the following (for $m, n, r \in \mathbb{N}$):

- [x] **/1/** $\binom{n}{1} + 6\binom{n}{2} + 6\binom{n}{3} = n^3$

- [x] **/2/** $1 + 7\binom{n}{1} + 12\binom{n}{2} + 6\binom{n}{3} = (n+1)^3$

- [x] **/3/** $1 + 14\binom{n}{1} + 36\binom{n}{2} + 24\binom{n}{3} = (n+1)^4 - n^4$

- [x] **/4/** $\binom{n}{1} + 14\binom{n}{2} + 36\binom{n}{3} + 24\binom{n}{4} = n^4$

- [x] **/5/** $\frac{[\binom{n+1}{r+1} - \binom{n}{r}] \cdot \binom{n-1}{r-1}}{\binom{n}{r}^2 - \binom{n+1}{r+1} \cdot \binom{n-1}{r-1}} = r$

- [x] **/6/** $\binom{m}{1} + \binom{m+1}{2} + \cdots + \binom{m+n-1}{n} = \binom{n}{1} + \binom{n+1}{2} + \cdots + \binom{n+m-1}{m}$

- [x] **/7/** $\sum_{i=1}^{n} i\binom{n}{i} = n \cdot 2^{n-1}$

- [x] **/8/** $\sum_{i=0}^{n}(i+1)\binom{n}{i} = (n+2) \cdot 2^{n-1}$

- [x] **/9/** $1\binom{n}{2} + 2\binom{n}{3} + \cdots + (n-1)\binom{n}{n} = (n-2) \cdot 2^{n-1} + 1$

- [x] **/10/** $\sum_{i=0}^{n}(2i+1)\binom{n}{i} = (n+1) \cdot 2^n$

- [x] **/11/** $\sum_{i=0}^{n}(-1)^i(i+1)\binom{n}{i} = 0$ (for $n \geq 2$)

- [x] **/12/** $3\binom{n}{1} + 7\binom{n}{2} + \cdots + (4n-1)\binom{n}{n} = (2n-1) \cdot 2^n + 1$

- [x] **/13/** $\sum_{i=1}^{n}(-1)^{i-1} i\binom{n}{i} = 0$ (for $n \geq 2$)

- [x] **/14/** $\frac{1}{1}\binom{n}{0} + \frac{1}{2}\binom{n}{1} + \cdots + \frac{1}{n+1}\binom{n}{n} = \frac{2^{n+1}-1}{n+1}$

- [x] **/15/** $\frac{1}{2}\binom{n}{0} + \frac{1}{3}\binom{n}{1} + \cdots + \frac{1}{n+2}\binom{n}{n} = \frac{n \cdot 2^{n+1}+1}{(n+1)(n+2)}$

- [x] **/16/** $\frac{1}{1}\binom{n}{0} - \frac{1}{2}\binom{n}{1} + \cdots + \frac{(-1)^n}{n+1}\binom{n}{n} = \frac{1}{n+1}$

- [x] **/17/** $\sum_{i=0}^{n}(-1)^i\binom{n}{i}^2 = \begin{cases} 0 & \text{if } n \text{ odd} \\ (-1)^{n/2}\binom{n}{n/2} & \text{if } n \text{ even} \end{cases}$

- [x] **/18/** $\sum_{i=1}^{n}i\binom{n}{i}^2 = \frac{(2n-1)!}{[(n-1)!]^2}$

- [x] **/19/** $\sum_{k=0}^{n}\frac{\binom{n}{k}\binom{n}{r}}{\binom{2n}{k+r}} = \frac{2n+1}{n+1}$

- [x] **/20/** $\sum_{k=1}^{n}\frac{\binom{n-1}{k-1}}{\binom{2n-1}{k}} = \frac{2}{n+1}$

- [x] **/21/** $\sum_{k=1}^{n}\frac{\binom{n-1}{k-1}}{\binom{n+r}{k}} = \frac{n+r+1}{(r+1)(r+2)}$

- [x] **/22/** $\sum_{k=1}^{n}\frac{\binom{n-2}{k-2}}{\binom{n+r}{k}} = \frac{2(n+r+1)}{(r+1)(r+2)(r+3)}$

- [x] **/23/** $\sum_{i \geq 0}(-3)^i\binom{n}{2i} = (-2)^n\cos\frac{2n\pi}{3}$

- [x] **/24/** $\sum_{i \geq 0}(-3)^i\binom{n}{2i+1} = \frac{2^n}{\sqrt{3}}\sin\frac{n\pi}{3}$

- [x] **/25/** $\sum_{i \geq 0}\binom{n}{3i} = \frac{1}{3}(2^n + 2\cos\frac{n\pi}{3})$

- [x] **/26/** $\sum_{i \geq 0}\binom{n}{3i+1} = \frac{1}{3}(2^n + 2\cos\frac{(n-2)\pi}{3})$

- [x] **/27/** $\sum_{i \geq 0}\binom{n}{3i+2} = \frac{1}{3}(2^n + 2\cos\frac{(n+2)\pi}{3})$

- [x] **/28/** $\sum_{i \geq 0}\binom{n}{4i} = \frac{1}{2}(2^{n-1} + 2^{n/2}\cos\frac{n\pi}{4})$

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Page 7 notes on power sums
- [ ] Various binomial coefficient problems

### From Vilenkin [ViN;87]
- [ ] End-of-chapter combinatorial problems

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 11 | 11 | 100% |
| Formal 3.1 | 1 | 1 | 100% |
| Formal 3.2 | 28 | 28 | 100% |
| External Problems | 3 | 0 | 0% |
| **TOTAL** | **43** | **40** | **93%** |

---

*Generated from Chapter 03: Binomiális és polinomiális együtthatók*
*Source: Dr. Szalkai István - Diszkrét Matematika*
