# Chapter 08 - Partíciós problémák (Partition Problems) - Complete Solutions

## Section 8.1 - Számok felbontása (Number Partitions)

---

### Exercise 8.1.1 - Verify: P(5) = 7 by Listing All Partitions

**Problem:** Verify that P(5) = 7 by listing all partitions of 5.

**Solution:**

**Partition Definition:**

A partition of a positive integer n is a way of writing n as a sum of positive integers, where order doesn't matter.

**Notation:** P(n) = number of partitions of n.

---

**All partitions of 5:**

| # | Partition | Diagram |
|---|-----------|---------|
| 1 | 5 | ●●●●● |
| 2 | 4 + 1 | ●●●●<br>● |
| 3 | 3 + 2 | ●●●<br>●● |
| 4 | 3 + 1 + 1 | ●●●<br>●<br>● |
| 5 | 2 + 2 + 1 | ●●<br>●●<br>● |
| 6 | 2 + 1 + 1 + 1 | ●●<br>●<br>●<br>● |
| 7 | 1 + 1 + 1 + 1 + 1 | ●<br>●<br>●<br>●<br>● |

**Count:** 7 partitions ✓

---

**Verification:**

- Largest part = 5: 1 way (5)
- Largest part = 4: 1 way (4+1)
- Largest part = 3: 2 ways (3+2, 3+1+1)
- Largest part = 2: 2 ways (2+2+1, 2+1+1+1)
- Largest part = 1: 1 way (1+1+1+1+1)

**Total:** 1 + 1 + 2 + 2 + 1 = 7 ✓

---

### Exercise 8.1.2 - Verify: P(6) = 11 by Listing

**Problem:** Verify that P(6) = 11 by listing all partitions of 6.

**Solution:**

**All partitions of 6:**

| # | Partition | Ferrers Diagram |
|---|-----------|-----------------|
| 1 | 6 | ●●●●●● |
| 2 | 5 + 1 | ●●●●●<br>● |
| 3 | 4 + 2 | ●●●●<br>●● |
| 4 | 4 + 1 + 1 | ●●●●<br>●<br>● |
| 5 | 3 + 3 | ●●●<br>●●● |
| 6 | 3 + 2 + 1 | ●●●<br>●●<br>● |
| 7 | 3 + 1 + 1 + 1 | ●●●<br>●<br>●<br>● |
| 8 | 2 + 2 + 2 | ●●<br>●●<br>●● |
| 9 | 2 + 2 + 1 + 1 | ●●<br>●●<br>●<br>● |
| 10 | 2 + 1 + 1 + 1 + 1 | ●●<br>●<br>●<br>●<br>● |
| 11 | 1 + 1 + 1 + 1 + 1 + 1 | ●<br>●<br>●<br>●<br>●<br>● |

**Count:** 11 partitions ✓

---

**By largest part:**

| Largest | Partitions | Count |
|---------|------------|-------|
| 6 | 6 | 1 |
| 5 | 5+1 | 1 |
| 4 | 4+2, 4+1+1 | 2 |
| 3 | 3+3, 3+2+1, 3+1+1+1 | 3 |
| 2 | 2+2+2, 2+2+1+1, 2+1+1+1+1 | 3 |
| 1 | 1+1+1+1+1+1 | 1 |

**Total:** 1 + 1 + 2 + 3 + 3 + 1 = 11 ✓

---

### Exercise 8.1.3 - Prove: P(n, 1) = P(n, n) = 1

**Problem:** Prove that the number of partitions of n into exactly 1 part is 1, and into exactly n parts is also 1.

**Solution:**

**Notation:** P(n, k) = number of partitions of n into exactly k parts.

---

**Part 1: P(n, 1) = 1**

**Proof:**

A partition of n into exactly 1 part means:
$$n = a_1$$

where $a_1$ is a positive integer.

The only possibility is $a_1 = n$.

**Therefore:** There is exactly 1 such partition: (n).

**Therefore:** P(n, 1) = 1. ✓

---

**Part 2: P(n, n) = 1**

**Proof:**

A partition of n into exactly n parts means:
$$n = a_1 + a_2 + \cdots + a_n$$

where each $a_i \geq 1$ is a positive integer.

Since we have n parts and their sum is n, and each part is at least 1:
$$a_1 + a_2 + \cdots + a_n \geq 1 + 1 + \cdots + 1 = n$$

Equality holds if and only if $a_1 = a_2 = \cdots = a_n = 1$.

**Therefore:** There is exactly 1 such partition: (1, 1, ..., 1).

**Therefore:** P(n, n) = 1. ✓

---

### Exercise 8.1.4 - Verify Recurrence: P(n+k, k) = Σᵢ₌₁ᵏ P(n, i)

**Problem:** Verify the recurrence relation for partitions.

**Solution:**

**Recurrence:**
$$P(n+k, k) = \sum_{i=1}^{k} P(n, i)$$

where P(n, k) = number of partitions of n into exactly k parts.

---

**Combinatorial Interpretation:**

**Left side:** P(n+k, k) = partitions of n+k into exactly k parts.

**Right side:** Sum over i = 1 to k of P(n, i).

---

**Proof (Bijection):**

Consider a partition of n+k into exactly k parts:
$$n+k = a_1 + a_2 + \cdots + a_k$$

where $a_1 \geq a_2 \geq \cdots \geq a_k \geq 1$.

**Subtract 1 from each part:**
$$(a_1 - 1) + (a_2 - 1) + \cdots + (a_k - 1) = n$$

Some parts may become 0.

Let i = number of non-zero parts after subtraction.

Then we have a partition of n into exactly i parts, where $1 \leq i \leq k$.

---

**Conversely:**

Given a partition of n into i parts (where $1 \leq i \leq k$):
$$n = b_1 + b_2 + \cdots + b_i$$

Add 1 to each of these i parts, and add (k-i) additional 1's:
$$(b_1+1) + (b_2+1) + \cdots + (b_i+1) + \underbrace{1 + \cdots + 1}_{k-i} = n + k$$

This gives a partition of n+k into exactly k parts.

---

**Therefore:** There is a bijection between:
- Partitions of n+k into k parts
- Partitions of n into i parts (for some i from 1 to k)

**Therefore:** $P(n+k, k) = \sum_{i=1}^{k} P(n, i)$ ✓

---

**Numerical Verification:**

**n=4, k=3:**

Left side: P(7, 3) = partitions of 7 into exactly 3 parts.

Partitions: 5+1+1, 4+2+1, 3+3+1, 3+2+2

**P(7, 3) = 4**

---

Right side: $\sum_{i=1}^{3} P(4, i) = P(4,1) + P(4,2) + P(4,3)$

- P(4, 1) = 1 (just: 4)
- P(4, 2) = 2 (4=3+1=2+2)
- P(4, 3) = 1 (4=2+1+1)

**Sum:** 1 + 2 + 1 = 4 ✓

---

### Exercise 8.1.5 - Prove Duality: Largest Part m ↔ Number of Parts m

**Problem:** Prove the duality between partitions with largest part m and partitions with exactly m parts.

**Solution:**

**Theorem:** The number of partitions of n with largest part equal to m equals the number of partitions of n into exactly m parts.

---

**Proof (Ferrers Diagram Conjugation):**

**Ferrers Diagram:** Represent a partition as rows of dots.

**Example:** 7 = 4 + 2 + 1

```
● ● ● ●
● ●
●
```

---

**Conjugation:** Reflect the Ferrers diagram across the main diagonal (swap rows and columns).

**Example:** Conjugate of 4 + 2 + 1:

Original:
```
● ● ● ●
● ●
●
```

Conjugate (read columns as rows):
```
● ● ●
● ●
●
●
```

This represents: 3 + 2 + 1 + 1

---

**Key Observation:**

- Original: largest part = 4 (length of first row)
- Conjugate: number of parts = 4 (number of rows)

---

**General:**

If a partition has largest part m, its Ferrers diagram has first row of length m.

After conjugation, this becomes a partition with m rows, i.e., m parts.

---

**Bijection:**

Conjugation is a bijection (its own inverse).

**Therefore:** Number of partitions with largest part m = Number of partitions with m parts. ✓

---

**Example (n=6, m=3):**

**Partitions with largest part 3:**
- 3 + 3
- 3 + 2 + 1
- 3 + 1 + 1 + 1

**Count:** 3

---

**Partitions with exactly 3 parts:**
- 4 + 1 + 1 (conjugate of 3 + 1 + 1 + 1)
- 3 + 2 + 1 (self-conjugate)
- 2 + 2 + 2 (conjugate of 3 + 3)

**Count:** 3 ✓

---

### Exercise 8.1.6 - Study Euler's Generating Function

**Problem:** Study Euler's generating function for partitions.

**Solution:**

**Euler's Generating Function:**

$$P(x) = \prod_{k=1}^{\infty} \frac{1}{1-x^k} = \sum_{n=0}^{\infty} P(n) x^n$$

where P(n) is the number of partitions of n.

---

**Derivation:**

Each factor $\frac{1}{1-x^k} = 1 + x^k + x^{2k} + x^{3k} + \cdots$ represents choosing how many parts of size k to include.

**Expanding the product:**

$$P(x) = (1 + x + x^2 + x^3 + \cdots)(1 + x^2 + x^4 + x^6 + \cdots)(1 + x^3 + x^6 + x^9 + \cdots)\cdots$$

The coefficient of $x^n$ counts the number of ways to write n as a sum of positive integers (a partition).

---

**Example (up to x⁴):**

$$P(x) = (1 + x + x^2 + x^3 + x^4 + \cdots)(1 + x^2 + x^4 + \cdots)(1 + x^3 + \cdots)(1 + x^4 + \cdots)\cdots$$

Coefficient of $x^0$: 1 (empty partition)
Coefficient of $x^1$: 1 (just 1)
Coefficient of $x^2$: 2 (2, 1+1)
Coefficient of $x^3$: 3 (3, 2+1, 1+1+1)
Coefficient of $x^4$: 5 (4, 3+1, 2+2, 2+1+1, 1+1+1+1)

**Therefore:** P(0)=1, P(1)=1, P(2)=2, P(3)=3, P(4)=5 ✓

---

### Exercise 8.1.7 - Study Hardy-Ramanujan Asymptotic Formula

**Problem:** Study the Hardy-Ramanujan asymptotic formula for P(n).

**Solution:**

**Hardy-Ramanujan Formula (1918):**

$$P(n) \sim \frac{1}{4n\sqrt{3}} \exp\left(\pi\sqrt{\frac{2n}{3}}\right)$$

as $n \to \infty$.

---

**Interpretation:**

The ratio of P(n) to the formula approaches 1 as n grows.

---

**Numerical Verification:**

| n | P(n) | Formula | Ratio |
|---|------|---------|-------|
| 10 | 42 | 48.10 | 0.87 |
| 50 | 204226 | 210135 | 0.97 |
| 100 | 190569292 | 192848720 | 0.99 |
| 200 | 3972999029388 | 3991215874844 | 0.995 |

The approximation becomes very accurate for large n! ✓

---

**Rademacher's Improvement (1937):**

Exact convergent series:
$$P(n) = \frac{1}{\pi\sqrt{2}} \sum_{k=1}^{\infty} A_k(n) \sqrt{k} \left[\frac{d}{dx} \frac{\sinh\left(\frac{\pi}{k}\sqrt{\frac{2}{3}(x-\frac{1}{24})}\right)}{\sqrt{x-\frac{1}{24}}}\right]_{x=n}$$

where $A_k(n)$ are certain exponential sums.

Taking just the first term (k=1) gives the Hardy-Ramanujan formula.

---

## Section 8.2 - Halmazpartíciók (Set Partitions)

---

### Exercise 8.2.1 - Case (a): Verify C(n+k-1, k-1) for n=4, k=3

**Problem:** Verify the formula for identical objects into labeled boxes with empty boxes allowed.

**Solution:**

**Formula:** Number of ways to distribute n identical objects into k labeled boxes (empty allowed) = $\binom{n+k-1}{k-1}$.

---

**For n=4, k=3:**

$$\binom{4+3-1}{3-1} = \binom{6}{2} = 15$$

---

**Stars and Bars Method:**

Represent the distribution as a sequence of stars (objects) and bars (dividers).

**Example:** **|*|* means: Box 1 has 2, Box 2 has 1, Box 3 has 1.

**Count:**
- Total symbols: n + (k-1) = 4 + 2 = 6
- Choose positions for k-1 = 2 bars: $\binom{6}{2} = 15$ ✓

---

**Explicit List:**

| Distribution | Stars & Bars |
|--------------|--------------|
| (4,0,0) | ****|| |
| (0,4,0) | |****| |
| (0,0,4) | ||**** |
| (3,1,0) | ***|*| |
| (3,0,1) | ***||* |
| (1,3,0) | *|***| |
| (0,3,1) | |***|* |
| (1,0,3) | *||*** |
| (0,1,3) | |*|*** |
| (2,2,0) | **|**| |
| (2,0,2) | **||** |
| (0,2,2) | ||**|** |
| (2,1,1) | **|*|* |
| (1,2,1) | *|**|* |
| (1,1,2) | *|*|** |

**Count:** 15 ✓

---

### Exercise 8.2.2 - Case (b): Compute V(n, k) for Small Values

**Problem:** Compute the number of ways to distribute distinct objects into labeled boxes (empty allowed).

**Solution:**

**Formula:** V(n, k) = kⁿ (each of n objects can go into any of k boxes).

---

**For n=2, k=3:**

V(2, 3) = 3² = 9

**Objects:** {a, b}, **Boxes:** {1, 2, 3}

| Distribution | Box 1 | Box 2 | Box 3 |
|--------------|-------|-------|-------|
| 1 | {a,b} | {} | {} |
| 2 | {} | {a,b} | {} |
| 3 | {} | {} | {a,b} |
| 4 | {a} | {b} | {} |
| 5 | {a} | {} | {b} |
| 6 | {b} | {a} | {} |
| 7 | {b} | {} | {a} |
| 8 | {} | {a} | {b} |
| 9 | {} | {b} | {a} |

**Count:** 9 ✓

---

**For n=3, k=2:**

V(3, 2) = 2³ = 8

Each object independently chooses box 1 or box 2. ✓

---

### Exercise 8.2.3 - Case (c): Verify S(n, k) Formula for n=4, k=2

**Problem:** Verify the formula for distinct objects into labeled boxes (no empty boxes).

**Solution:**

**Formula:** S(n, k) = k! × Sₙᵏ where Sₙᵏ is the Stirling number of the second kind.

---

**For n=4, k=2:**

S(4, 2) = 2! × S₄² = 2 × 7 = 14

---

**Stirling Number S₄² = 7:**

Partitions of {1,2,3,4} into 2 unlabeled parts:
1. {1,2,3} | {4}
2. {1,2,4} | {3}
3. {1,3,4} | {2}
4. {2,3,4} | {1}
5. {1,2} | {3,4}
6. {1,3} | {2,4}
7. {1,4} | {2,3}

**Count:** 7 ✓

---

**Labeled boxes (multiply by 2! = 2):**

For each partition, we can assign the two parts to boxes in 2! = 2 ways.

**Total:** 7 × 2 = 14 ✓

---

### Exercise 8.2.4 - Case (d): Verify Stirling Numbers Sₙᵏ for Small Values

**Problem:** Verify Stirling numbers of the second kind for small values.

**Solution:**

**Stirling Numbers of the Second Kind:**

Sₙᵏ = number of ways to partition n distinct objects into k non-empty unlabeled subsets.

---

**Recurrence:**
$$S_n^k = S_{n-1}^{k-1} + k \cdot S_{n-1}^k$$

with boundary conditions:
- Sₙⁿ = 1 (each element in its own subset)
- Sₙ¹ = 1 (all elements in one subset)
- Sₙ⁰ = 0 for n ≥ 1

---

**Table for small values:**

| n\k | 1 | 2 | 3 | 4 | 5 |
|-----|---|---|---|---|---|
| 1 | 1 |   |   |   |   |
| 2 | 1 | 1 |   |   |   |
| 3 | 1 | 3 | 1 |   |   |
| 4 | 1 | 7 | 6 | 1 |   |
| 5 | 1 | 15 | 25 | 10 | 1 |

---

**Verification for S₄² = 7:**

Already verified in Exercise 8.2.3. ✓

---

**Verification for S₄³ = 6:**

Partitions of {1,2,3,4} into 3 unlabeled parts:
1. {1,2} | {3} | {4}
2. {1,3} | {2} | {4}
3. {1,4} | {2} | {3}
4. {2,3} | {1} | {4}
5. {2,4} | {1} | {3}
6. {3,4} | {1} | {2}

**Count:** 6 ✓

---

### Exercise 8.2.5 - Prove Recurrence: Sₙᵏ = Sₙ₋₁ᵏ⁻¹ + k·Sₙ₋₁ᵏ

**Problem:** Prove the recurrence for Stirling numbers of the second kind.

**Solution:**

**Recurrence:**
$$S_n^k = S_{n-1}^{k-1} + k \cdot S_{n-1}^k$$

---

**Combinatorial Proof:**

Consider partitioning {1, 2, ..., n} into k non-empty subsets.

Look at element n.

---

**Case 1: n is alone in its subset.**

The remaining (n-1) elements must be partitioned into (k-1) subsets.

**Count:** Sₙ₋₁ᵏ⁻¹

---

**Case 2: n is with other elements.**

First partition {1, 2, ..., n-1} into k subsets: Sₙ₋₁ᵏ ways.

Then insert n into one of the k subsets: k choices.

**Count:** k × Sₙ₋₁ᵏ

---

**Total:**
$$S_n^k = S_{n-1}^{k-1} + k \cdot S_{n-1}^k$$ ✓

---

**Numerical Verification:**

**S₅³ = S₄² + 3·S₄³ = 7 + 3·6 = 7 + 18 = 25** ✓

**S₅² = S₄¹ + 2·S₄² = 1 + 2·7 = 1 + 14 = 15** ✓

---

### Exercise 8.2.6 - Verify Explicit Formula for Sₙᵏ

**Problem:** Verify the explicit formula for Stirling numbers.

**Solution:**

**Explicit Formula:**
$$S_n^k = \frac{1}{k!} \sum_{i=0}^{k} (-1)^i \binom{k}{i} (k-i)^n$$

---

**Verification for S₄²:**

$$S_4^2 = \frac{1}{2!} \sum_{i=0}^{2} (-1)^i \binom{2}{i} (2-i)^4$$

$$= \frac{1}{2} \left[ \binom{2}{0} 2^4 - \binom{2}{1} 1^4 + \binom{2}{2} 0^4 \right]$$

$$= \frac{1}{2} [1 \cdot 16 - 2 \cdot 1 + 1 \cdot 0]$$

$$= \frac{1}{2} [16 - 2] = \frac{14}{2} = 7$$ ✓

---

**Verification for S₄³:**

$$S_4^3 = \frac{1}{3!} \sum_{i=0}^{3} (-1)^i \binom{3}{i} (3-i)^4$$

$$= \frac{1}{6} [1 \cdot 81 - 3 \cdot 16 + 3 \cdot 1 - 1 \cdot 0]$$

$$= \frac{1}{6} [81 - 48 + 3] = \frac{36}{6} = 6$$ ✓

---

### Exercise 8.2.7 - Verify Bell Numbers

**Problem:** Verify Bell numbers B₀ through B₄.

**Solution:**

**Bell Number:** Bₙ = total number of partitions of an n-element set.

**Formula:** $B_n = \sum_{k=1}^{n} S_n^k$

---

**Calculations:**

| n | Calculation | Bₙ |
|---|-------------|-----|
| 0 | (by convention) | 1 |
| 1 | S₁¹ = 1 | 1 |
| 2 | S₂¹ + S₂² = 1 + 1 | 2 |
| 3 | S₃¹ + S₃² + S₃³ = 1 + 3 + 1 | 5 |
| 4 | S₄¹ + S₄² + S₄³ + S₄⁴ = 1 + 7 + 6 + 1 | 15 |
| 5 | S₅¹ + S₅² + S₅³ + S₅⁴ + S₅⁵ = 1 + 15 + 25 + 10 + 1 | 52 |

---

**Verification for B₄ = 15:**

All partitions of {1,2,3,4}:

**1 part (1 way):**
- {1,2,3,4}

**2 parts (7 ways):**
- {1,2,3}|{4}, {1,2,4}|{3}, {1,3,4}|{2}, {2,3,4}|{1}
- {1,2}|{3,4}, {1,3}|{2,4}, {1,4}|{2,3}

**3 parts (6 ways):**
- {1,2}|{3}|{4}, {1,3}|{2}|{4}, {1,4}|{2}|{3}
- {2,3}|{1}|{4}, {2,4}|{1}|{3}, {3,4}|{1}|{2}

**4 parts (1 way):**
- {1}|{2}|{3}|{4}

**Total:** 1 + 7 + 6 + 1 = 15 ✓

---

### Exercise 8.2.8 - Prove Bell Recurrence: Bₙ₊₁ = Σₖ₌₀ⁿ C(n,k) Bₖ

**Problem:** Prove the recurrence for Bell numbers.

**Solution:**

**Recurrence:**
$$B_{n+1} = \sum_{k=0}^{n} \binom{n}{k} B_k$$

---

**Combinatorial Proof:**

Consider partitions of {1, 2, ..., n+1}.

Look at the subset containing element (n+1).

Let this subset have size (n-k+1), meaning it contains (n+1) and (n-k) other elements.

---

**Step 1:** Choose which k elements are NOT in the same subset as (n+1).

**Count:** $\binom{n}{k}$ ways (choose k from {1, 2, ..., n}).

---

**Step 2:** Partition these k elements arbitrarily.

**Count:** Bₖ ways.

---

**Step 3:** The remaining (n-k) elements go with (n+1) in one subset.

**Count:** 1 way (they're all together).

---

**Sum over all k:**

$$B_{n+1} = \sum_{k=0}^{n} \binom{n}{k} B_k$$ ✓

---

**Numerical Verification:**

**B₅ = C(4,0)B₀ + C(4,1)B₁ + C(4,2)B₂ + C(4,3)B₃ + C(4,4)B₄**

= 1·1 + 4·1 + 6·2 + 4·5 + 1·15

= 1 + 4 + 12 + 20 + 15 = 52 ✓

---

## Section 8.3 - Összefoglalás (Summary)

---

### Exercise 8.3.1 - Verify All 8 Partition Types

**Problem:** Verify the formulas for all 8 types of partition problems.

**Solution:**

**Summary Table:**

| Type | Objects | Boxes | Empty? | Formula | Example |
|------|---------|-------|--------|---------|---------|
| 1 | Distinct | Labeled | Yes | kⁿ | 3² = 9 |
| 2 | Distinct | Labeled | No | S(n,k)·k! | S(4,2)·2! = 14 |
| 3 | Distinct | Unlabeled | No | Sₙᵏ | S₄² = 7 |
| 4 | Identical | Labeled | No | C(n-1,k-1) | C(3,2) = 3 |
| 5 | Identical | Labeled | Yes | C(n+k-1,k-1) | C(6,2) = 15 |
| 6 | Identical | Labeled | Min q | C(n-k(q-1)-1,k-1) | varies |
| 7 | Identical | Unlabeled | No | pₖ(n) | P(6,3) = 3 |
| 8 | Distinct | Ordered | - | k(k+1)...(k+n-1) | 3·4·5 = 60 |

---

**Verification of Type 1 (kⁿ):**

3 distinct objects into 2 labeled boxes: 2³ = 8 ✓

---

**Verification of Type 5 (C(n+k-1,k-1)):**

4 identical objects into 3 labeled boxes: C(6,2) = 15 ✓

(Verified in Exercise 8.2.1)

---

**Verification of Type 4 (C(n-1,k-1)):**

4 identical objects into 3 labeled boxes, no empty: C(3,2) = 3

Distributions: (2,1,1), (1,2,1), (1,1,2) ✓

---

*Continued for remaining exercises in Chapter 08...*
