# Chapter 07 - Extremális halmazrendszerek - Exercise Checklist

## 📋 Complete Exercise List

Use this checklist to track your progress through Chapter 07 exercises.

---

## 🔵 In-Chapter Exercises (HF = Házi Feladat)

### Section 7.1 - Sperner tétele

- [ ] **HF** - Verify: For $n=4$, maximum Sperner family has $\binom{4}{2} = 6$ sets

- [ ] **HF** - Verify: For $n=5$, maximum is $\binom{5}{2} = 10$ sets

- [ ] **HF** - Prove Lubell's inequality: $\sum_{i=1}^m \frac{1}{\binom{n}{|A_i|}} \leq 1$

- [ ] **HF** - Prove: Maximum binomial coefficient is at middle: $\binom{n}{\lfloor n/2 \rfloor}$

- [ ] **Study** - Chain counting argument in Sperner's proof

- [ ] **Study** - Connection to posets and Dilworth's theorem

---

### Section 7.2 - Erdős-DeBruijn, Ryser és Fisher tételei

#### Erdős-DeBruijn Theorem

- [ ] **HF** - Verify: For $n=3$, maximum $m=3$ with $|A_i \cap A_j| = 1$

- [ ] **HF** - Construct the three equality cases (a), (b), (c)

- [ ] **Study** - Finite geometry axioms

#### Gallai's Theorem

- [ ] **HF** - Prove dual of Gallai's theorem (points ↔ lines)

- [ ] **HF** - Verify with example: 4 points not on one line determine ≥ 4 lines

#### Ryser's Theorem

- [ ] **HF** - Prove Lemma 7.8: Linear independence criterion

- [ ] **HF** - Complete the vector space proof of Ryser's theorem

- [ ] **HF** - Verify: If exactly one $|A_{i_0}| = t$, then $m \leq n-t$

#### Fisher's Theorem

- [ ] **HF** - Explain connection to experimental design (BIBD)

- [ ] **Study** - Block designs and incidence matrices

---

### Section 7.3 - Erdős-Ko-Rado tétele

- [ ] **HF** - Verify EKR bound for $n=5, k=2$: $m \leq \binom{4}{1} = 4$

- [ ] **HF** - Construct the sharp example: all $k$-sets containing fixed $x_0$

- [ ] **HF** - Compare: $\binom{n-1}{k-1}$ vs $\binom{n}{k}$ (total $k$-sets)

- [ ] **HF** - Prove: For $k > n/2$, any two $k$-sets intersect

- [ ] **Study** - Why condition $k \leq n/2$ is necessary

---

### Section 7.4 - Egyéb eredmények

#### Ray-Chaudhuri-Wilson Theorem

- [ ] **HF** - Verify: If $|A_i \cap A_j| \in \{1, 2\}$, then $m \leq \binom{n}{2}$

- [ ] **Study** - Proof using linear algebra method

#### Babai-Frankl Theorem

- [ ] **HF** - Explain gcd condition: $\gcd(r_1, \ldots, r_s) \nmid k$

- [ ] **Study** - Why this gives stronger bound $m \leq n$

#### Róka Sándor's Theorems

- [ ] **HF** - 7.14: Symmetric difference version

- [ ] **HF** - 7.15: Triple intersection bound $m \leq \frac{1}{3}n(n-1)$

- [ ] **HF** - 7.17: Independent intersection systems $c_1 \log_2 n \leq m \leq c_2 n^2$

#### Tuza's Theorem

- [ ] **HF** - Compare conditions (a), (b), (c) in 7.18

---

### Section 7.5 - Szimplexek

- [ ] **HF** - Define: Chemical reaction as linear combination = 0

- [ ] **HF** - Explain: Minimal reaction = simplex

- [ ] **HF** - Find all minimal reactions for given compounds

- [ ] **Study** - Connection to null space of composition matrix

---

## 🔴 Formal Exercises (Section 7.6 - Feladatok)

### 7.1.Feladat - Sperner families
- [ ] Find maximum Sperner family for $n=6$
- [ ] Verify: $\binom{6}{3} = 20$

### 7.2.Feladat - Intersecting families
- [ ] Apply EKR theorem to specific case
- [ ] Construct maximum intersecting family

### 7.3.Feladat - Constant intersection
- [ ] Apply Fisher's theorem
- [ ] Find maximum $m$ for given parameters

### 7.4.Feladat - Projective plane
- [ ] Verify Fano plane satisfies Erdős-DeBruijn conditions
- [ ] Count points and lines

### 7.5.Feladat - Block designs
- [ ] Verify BIBD parameters
- [ ] Apply Fisher's inequality

### 7.6.Feladat - Linear algebra method
- [ ] Construct characteristic vectors
- [ ] Prove linear independence

### 7.7.Feladat - Chemical reactions
- [ ] Find all minimal reactions
- [ ] Verify simplex structure

### 7.8.Feladat - [Additional problem from chapter]
- [ ] Analyze and solve

---

## 📚 Referenced External Exercises

### From Szalkai [SzIs;97] Problem Collection
- [ ] Chapter on extremal set theory
- [ ] Additional Sperner-type problems

### From Babai-Frankl [BF]
- [ ] Linear algebra methods in combinatorics

### From Vilenkin [ViN]
- [ ] Combinatorial problems on sets

---

## 📊 Progress Tracker

| Category | Total | Completed | Percentage |
|----------|-------|-----------|------------|
| In-Chapter HF | 25 | 25 | 100% |
| Formal 7.1-7.8 | 8 | 8 | 100% |
| External Problems | 0 | 0 | 0% |
| **TOTAL** | **33** | **33** | **100%** |

---

## 🎯 Study Tips

1. **Start with:** Sperner's theorem - foundational result
2. **Master:** Chain counting argument (Lubell's proof)
3. **Understand:** Linear algebra method for intersection theorems
4. **Practice:** EKR theorem applications
5. **Key technique:** Characteristic vectors → linear independence

---

## ⏱️ Estimated Time

| Task | Time |
|------|------|
| Reading chapter | 3-4 hours |
| In-chapter HF | 5-6 hours |
| Formal exercises 7.1-7.8 | 5-7 hours |
| External problems | 4-6 hours |
| **Total** | **17-23 hours** |

---

## 📝 Key Formulas to Memorize

```
□ Sperner: m ≤ C(n, ⌊n/2⌋)
□ Lubell: Σ 1/C(n,|Aᵢ|) ≤ 1
□ Erdős-DeBruijn: |Aᵢ∩Aⱼ| = 1 ⇒ m ≤ n
□ Ryser: |Aᵢ∩Aⱼ| = t ⇒ m ≤ n
□ EKR: Intersecting, |Aᵢ| ≤ k ⇒ m ≤ C(n-1,k-1)
□ Ray-Chaudhuri-Wilson: |Aᵢ∩Aⱼ| ∈ L, |L| = s ⇒ m ≤ C(n,s)
```

---

## Important Theorems Summary

| Theorem | Condition | Bound | Sharp? |
|---------|-----------|-------|--------|
| Sperner | $A_i \not\subseteq A_j$ | $\binom{n}{\lfloor n/2 \rfloor}$ | Yes |
| Erdős-DeBruijn | $|A_i \cap A_j| = 1$ | $n$ | Yes |
| Ryser | $|A_i \cap A_j| = t$ | $n$ | ? |
| Fisher | $|A_i| = k, |A_i \cap A_j| = t$ | $n$ | ? |
| EKR | Intersecting, $k \leq n/2$ | $\binom{n-1}{k-1}$ | Yes |
| R-C-W | $|A_i \cap A_j| \in L$ | $\binom{n}{s}$ | Yes |

---

*Generated from Chapter 07: Extremális halmazrendszerek*  
*Source: Dr. Szalkai István - Diszkrét Matematika*
