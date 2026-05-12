# Exercise 7.4 - Ray-Chaudhuri-Wilson and Babai-Frankl Theorems

## Problem Statement

Apply the generalized intersection theorems:
- (a) Ray-Chaudhuri-Wilson: $|A_i \cap A_j| \in L, |L| = s \Rightarrow m \leq \binom{n}{s}$
- (b) Babai-Frankl: With gcd condition, $m \leq n$
- (c) Verify with specific examples

---

## Solution

### Part (a): Ray-Chaudhuri-Wilson Theorem (7.12 Tétel, 1975)

**Theorem:** If $|A_i| = k$ (uniform) and $|A_i \cap A_j| \in L = \{r_1, \ldots, r_s\}$ for all $i \neq j$, then:
$$m \leq \binom{n}{s}$$

---

**Example 1: $n = 5, L = \{1\}$ (s = 1)**

This reduces to Fisher's theorem with $t = 1$.

**Bound:** $m \leq \binom{5}{1} = 5$

**Construction:** Can we find 5 sets of uniform size with pairwise intersections = 1?

Try $k = 2$:
- $A_1 = \{1, 2\}$
- $A_2 = \{2, 3\}$
- $A_3 = \{3, 4\}$
- $A_4 = \{4, 5\}$
- $A_5 = \{5, 1\}$

**Verification:**
- All sets have size 2 ✓
- $|A_i \cap A_{i+1}| = 1$ ✓
- But $|A_1 \cap A_3| = |\{1,2\} \cap \{3,4\}| = 0$ ✗

This doesn't work! We need ALL pairs to intersect in exactly 1 element.

**Better construction (star):**
- $A_1 = \{1, 2\}$
- $A_2 = \{1, 3\}$
- $A_3 = \{1, 4\}$
- $A_4 = \{1, 5\}$

Only $m = 4$ sets (can't get 5 with $k = 2$).

For $k = 3$, by Fisher's theorem, maximum is also $n = 5$.

---

**Example 2: $n = 6, L = \{1, 2\}$ (s = 2)**

**RCW Bound:** $m \leq \binom{6}{2} = 15$

**Construction:** We need sets where any two intersect in either 1 or 2 elements.

Take all 3-element subsets containing element 1:
```
{1,2,3}, {1,2,4}, {1,2,5}, {1,2,6},
{1,3,4}, {1,3,5}, {1,3,6},
{1,4,5}, {1,4,6},
{1,5,6}
```

**Count:** $\binom{5}{2} = 10$ sets

**Intersection sizes:**
- Two sets sharing 2 elements: $|\{1,2,3\} \cap \{1,2,4\}| = 2$ ✓
- Two sets sharing 1 element: $|\{1,2,3\} \cap \{1,4,5\}| = 1$ ✓

So $L = \{1, 2\}$ and $m = 10 \leq 15$ ✓

---

**Example 3: $n = 7, L = \{0, 1\}$ (s = 2)**

**RCW Bound:** $m \leq \binom{7}{2} = 21$

This allows disjoint sets (intersection = 0) and sets intersecting in 1 element.

**Construction:** Take all 2-element subsets:
- Count: $\binom{7}{2} = 21$ sets
- Intersection of two 2-sets: either 0 or 1 element ✓

This achieves the bound! $m = 21 = \binom{7}{2}$ ✓

---

### Part (b): Babai-Frankl Theorem (7.13 Tétel, 1988)

**Theorem:** If the conditions of RCW hold AND $\gcd(r_1, \ldots, r_s) \nmid k$, then:
$$m \leq n$$

This is a much stronger bound!

---

**Example: $n = 7, k = 3, L = \{1, 2\}$**

**Check gcd condition:**
- $\gcd(1, 2) = 1$
- Does $1 \nmid 3$? No, $1 \mid 3$ always.

So the gcd condition is NOT satisfied, and we only get the RCW bound $m \leq \binom{7}{2} = 21$.

---

**Example: $n = 7, k = 3, L = \{2\}$**

**Check gcd condition:**
- $\gcd(2) = 2$
- Does $2 \nmid 3$? Yes! $2 \nmid 3$.

**Babai-Frankl bound:** $m \leq 7$

**RCW bound:** $m \leq \binom{7}{1} = 7$

Both give the same bound in this case.

---

**Example: $n = 9, k = 4, L = \{2, 3\}$**

**Check gcd condition:**
- $\gcd(2, 3) = 1$
- Does $1 \nmid 4$? No.

So only RCW applies: $m \leq \binom{9}{2} = 36$.

---

**Example: $n = 10, k = 5, L = \{2, 4\}$**

**Check gcd condition:**
- $\gcd(2, 4) = 2$
- Does $2 \nmid 5$? Yes!

**Babai-Frankl bound:** $m \leq 10$

**RCW bound:** $m \leq \binom{10}{2} = 45$

Babai-Frankl gives a much stronger bound! ✓

---

### Part (c): Verification with Specific Examples

---

**Example: Fano Plane Revisited**

$n = 7, k = 3, L = \{1\}$

- RCW bound: $m \leq \binom{7}{1} = 7$
- Actual: $m = 7$ ✓

gcd condition: $\gcd(1) = 1$, and $1 \mid 3$, so Babai-Frankl doesn't apply.

---

**Example: Modified Construction**

$n = 6, k = 3, L = \{1, 3\}$

**gcd condition:** $\gcd(1, 3) = 1$, and $1 \mid 3$, so Babai-Frankl doesn't apply.

**RCW bound:** $m \leq \binom{6}{2} = 15$

**Construction:** All 3-sets containing element 1:
- Count: $\binom{5}{2} = 10$ sets
- Intersections: Either 1 or 3 elements (when sets are equal)

But we need $i \neq j$, so intersection is always 1 or 2 (not 3).

Actually, two different 3-sets can intersect in at most 2 elements.

So $L = \{1, 2\}$, not $\{1, 3\}$.

---

## Proof Sketch: Ray-Chaudhuri-Wilson Theorem

**Linear algebra method:**

1. **Characteristic vectors:** $v_i \in \mathbb{R}^n$ for each $A_i$.

2. **Multilinear polynomials:** Define polynomials $f_i(x_1, \ldots, x_n)$ that:
   - Vanish on $v_j$ for $j \neq i$
   - Don't vanish on $v_i$

3. **Linear independence:** Show these polynomials are linearly independent.

4. **Dimension bound:** Space of such polynomials has dimension $\binom{n}{s}$.

5. **Conclusion:** $m \leq \binom{n}{s}$.

---

## Proof Sketch: Babai-Frankl Theorem

**Key insight:** The gcd condition allows a stronger linear independence argument.

1. **Modified inner product:** Use a weighted inner product based on the gcd.

2. **Rank argument:** The Gram matrix has full rank under the gcd condition.

3. **Conclusion:** Vectors are in $\mathbb{R}^n$, so $m \leq n$.

---

## Comparison of Bounds

| $n$ | $k$ | $L$ | $s$ | RCW Bound | BF Bound | Actual Max |
|-----|-----|-----|-----|-----------|----------|------------|
| 7 | 3 | {1} | 1 | 7 | N/A | 7 |
| 7 | 3 | {2} | 1 | 7 | 7 | ? |
| 10 | 5 | {2,4} | 2 | 45 | 10 | ? |
| 6 | 3 | {1,2} | 2 | 15 | N/A | 10 |
| 5 | 2 | {1} | 1 | 5 | N/A | 4 |

**Note:** BF bound applies only when $\gcd(L) \nmid k$.

---

## Applications

### 1. Coding Theory

RCW theorem bounds the size of codes with restricted distances.

### 2. Experimental Design

Fisher's theorem (special case of RCW) is fundamental in BIBD theory.

### 3. Computer Science

Bounds on set systems appear in:
- Data structures
- Complexity theory
- Cryptography

---

## Verification Table

| Theorem | Conditions | Bound | Sharp? |
|---------|------------|-------|--------|
| RCW | $|A_i \cap A_j| \in L, |L| = s$ | $\binom{n}{s}$ | Yes |
| BF | RCW + $\gcd(L) \nmid k$ | $n$ | Sometimes |
| Fisher | $|A_i \cap A_j| = t$ | $n$ | Yes (Fano) |
| EKR | Intersecting, $|A_i| = k$ | $\binom{n-1}{k-1}$ | Yes |

---

*Exercise 7.4 from Chapter 07 - Extremális halmazrendszerek*
