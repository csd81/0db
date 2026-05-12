# Chapter 04 - A logikai szitaformula - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 04 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 4.1 - A formula

- [x] **HF** - Prove inclusion-exclusion formula by induction using Pascal's rule
  > Verify: $\sum_{k=1}^{r} (-1)^{k-1} \binom{r}{k} = 1$

- [x] **HF** - Prove using characteristic functions
  > $\chi_{A \cup B} = \chi_A + \chi_B - \chi_{A \cap B}$

- [x] **Study** - Complexity: $O(2^m)$ terms in full formula

---

### Section 4.2 - Elcserélt levelek (Derangements)

- [x] **4.8** - Verify derangement values in table (D₁ through D₁₂)

- [x] **HF** - Prove recurrence: $D_n = n D_{n-1} + (-1)^n$ (from 4.6 formula)

- [x] **HF** - Prove: $D_n = (n-1)(D_{n-1} + D_{n-2})$

- [x] **HF** - Prove limit: $\lim_{n \to \infty} \frac{D_n}{n!} = \frac{1}{e}$

- [x] **HF** - Prove: $D_n = \left\lfloor \frac{n!}{e} + \frac{1}{2} \right\rfloor$

- [x] **Study** - Joó István's generalization (4.12 Theorem)

---

### Section 4.3 - Additív halmazfüggvények

- [x] **HF** - Verify $\mathcal{A}$ is a set algebra in example (h) (number-theoretic density)

- [x] **HF** - Prove $\mu$ is a measure on $\mathcal{A}$ in example (h)

- [x] **HF** - Prove: $0 \leq d(A) \leq 1$ for all measurable $A \subseteq \mathbb{N}$

- [x] **HF** - Prove 4.16 properties (i)-(iv) for general measures

- [x] **HF** - Extend inclusion-exclusion to general measures (4.18, 4.19)

- [x] **HF** - Express measurable sets using minterms $m_\epsilon$ (from 1.3 section)

- [x] **Study** - Quantity-independent sets: $\mu(A \cap B) = \mu(A)\mu(B)$

---

## 🔴 Formal Exercises (Section 4.4)

### 4.1.Feladat - Three languages
- [x] 67 students, 47 English, 35 German, 23 both, 20 French, 12 English+French, 11 German+French, 5 all three
- [x] **Find:** Students who speak none of the languages
- [x] **Answer:** 6

---

### 4.2.Feladat - Exactly one fixed point
- [x] 5 letters, exactly 1 person gets their own letter
- [x] **Find:** Number of ways
- [x] **Answer:** $5 \cdot D_4 = 45$

---

### 4.3.Feladat - At least one object
- [x] Distribute $r$ distinct objects to $n+p$ people
- [x] **Constraint:** First $n$ people each get at least 1 object
- [x] **Find:** Number of distributions
- [x] **Answer:** $\sum_{i=0}^{n} (-1)^i \binom{n}{i} (n+p-i)^r$

---

### 4.4.Feladat - Derangement recurrence
- [x] **Prove:** $D_n = n D_{n-1} + (-1)^n$ for $n \geq 2$

---

### 4.5.Feladat - Surjective functions
- [x] **Find:** Number of surjections $B \to A$ where $|B| = m, |A| = n$
- [x] **Formula:** $S(m,n) = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n-i)^m$

---

### 4.6.Feladat - Distributing toys

**a)**
- [x] 6 toys to 4 children, each gets at least 1
- [x] **Answer:** $S(6,4) = 1560$

**b)**
- [x] 7 tasks to 5 workers, each gets at least 1, hardest task to best worker
- [x] **Answer:** $S(6,5) + S(6,4) = 3360$

---

### 4.7.Feladat - Special cases of surjections
- [x] $S(m, 1) = 1$
- [x] $S(m, 2) = 2^m - 2$
- [x] $S(n+1, n) = \frac{n+1}{2} \cdot n!$
- [x] $S(n, n) = n!$
- [x] $S(n+2, n) = n! \left[\frac{n+2}{3} + \binom{n+2}{2} - \frac{n}{2}\right]$

---

### 4.8.Feladat - Relatively prime numbers
- [x] Count numbers $\leq M$ that are coprime to $n$
- [x] **Formula:** $P = M - \sum \left\lfloor \frac{M}{p_i} \right\rfloor + \sum \left\lfloor \frac{M}{p_i p_j} \right\rfloor - \cdots$
- [x] **Euler's φ:** $\phi(n) = n \prod_{p|n} \left(1 - \frac{1}{p}\right)$
- [x] **Example:** $n = 210, M = 10000 \Rightarrow P = 2285$

---

### 4.9.Feladat - Alternating binomial sum
- [x] **Evaluate:** $\sum_{i=0}^{n} (-1)^{n-i} \binom{n}{i} i^k$
- [x] **Answer:** $\begin{cases} 0 & \text{if } k < n \\ n! & \text{if } k = n \end{cases}$

---

### 4.10.Feladat - Polynomial expansion
- [x] **Expand:** $\prod_{i=1}^{r} (1 - x_i)$
- [x] **Answer:** $1 - \sum x_i + \sum x_i x_j - \sum x_i x_j x_k + \cdots + (-1)^r x_1 x_2 \cdots x_r$

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter 4 problems with detailed solutions
- [ ] Additional derangement variations

### From Vilenkin [ViN;87]
- [ ] Inclusion-exclusion combinatorial problems

### From Lovász [L]
- [ ] Combinatorial Problems and Exercises
- [ ] Graph coloring applications

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 12 | 12 | 100% |
| Formal 4.1-4.10 | 10 | 10 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **22** | **22** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** Basic inclusion-exclusion (4.1) - two and three sets
2. **Master:** Derangements - classic application, appears frequently
3. **Understand:** General measure formulation - applies to probability, number theory
4. **Practice:** Surjective functions - connects to Stirling numbers
5. **Key technique:** Identify what to count directly vs. via complement

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Read chapter | 2-3 hours |
| In-chapter HF | 3-4 hours |
| Formal exercises 4.1-4.10 | 4-6 hours |
| External problems | 3-5 hours |
| **Total** | **12-18 hours** |

---

## 📝 Key Formulas to Memorize

```
□ Inclusion-Exclusion: |∪Aᵢ| = Σ|Aᵢ| - Σ|Aᵢ∩Aⱼ| + Σ|Aᵢ∩Aⱼ∩Aₖ| - ...
□ Derangement: Dₙ = n! Σ(-1)ᵏ/k! ≈ n!/e
□ Derangement recurrence: Dₙ = (n-1)(Dₙ₋₁ + Dₙ₋₂)
□ Surjections: S(m,n) = Σ(-1)ⁱC(n,i)(n-i)ᵐ
□ Euler φ: φ(n) = n Π(1-1/p)
```

---

*Generated from Chapter 04: A logikai szitaformula*  
*Source: Dr. Szalkai István - Diszkrét Matematika*
