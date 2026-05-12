# Exercise 7.2 - Erdős-Ko-Rado Theorem Applications

## Problem Statement

Apply the EKR theorem to find the maximum size of an intersecting family:
- (a) $n = 6, k = 3$
- (b) $n = 7, k = 3$
- (c) Construct the maximum family for $n = 5, k = 2$

---

## Solution

### EKR Theorem Statement (7.10 Tétel)

If $\mathcal{F} = \{A_1, \ldots, A_m\}$ is an **intersecting family** ($A_i \cap A_j \neq \emptyset$ for all $i \neq j$) with $|A_i| \leq k \leq n/2$, then:
$$m \leq \binom{n-1}{k-1}$$

**Sharp construction:** All $k$-sets containing a fixed element $x_0$.

---

### Part (a): $n = 6, k = 3$

**Check condition:** $k = 3 \leq n/2 = 3$ ✓

**EKR bound:**
$$m \leq \binom{6-1}{3-1} = \binom{5}{2} = 10$$

**Maximum construction:** Fix element 1, take all 3-sets containing 1:
```
{1,2,3}, {1,2,4}, {1,2,5}, {1,2,6},
{1,3,4}, {1,3,5}, {1,3,6},
{1,4,5}, {1,4,6},
{1,5,6}
```

**Count:** 10 sets ✓

**Verification:** Every pair intersects (they all contain 1) ✓

---

### Part (b): $n = 7, k = 3$

**Check condition:** $k = 3 \leq n/2 = 3.5$ ✓

**EKR bound:**
$$m \leq \binom{7-1}{3-1} = \binom{6}{2} = 15$$

**Maximum construction:** Fix element 1, take all 3-sets containing 1:

**Count:** $\binom{6}{2} = 15$ sets ✓

**List:**
```
{1,2,3}, {1,2,4}, {1,2,5}, {1,2,6}, {1,2,7},
{1,3,4}, {1,3,5}, {1,3,6}, {1,3,7},
{1,4,5}, {1,4,6}, {1,4,7},
{1,5,6}, {1,5,7},
{1,6,7}
```

---

### Part (c): $n = 5, k = 2$

**Check condition:** $k = 2 \leq n/2 = 2.5$ ✓

**EKR bound:**
$$m \leq \binom{5-1}{2-1} = \binom{4}{1} = 4$$

**Maximum construction:** Fix element 1, take all 2-sets containing 1:
```
{1,2}, {1,3}, {1,4}, {1,5}
```

**Verification:**
- All sets intersect (contain 1) ✓
- Size = 4 ✓
- Cannot add any more 2-sets:
  - {2,3} doesn't intersect {1,4} or {1,5} ✗
  - {2,4} doesn't intersect {1,3} or {1,5} ✗
  - etc.

---

## Why $k \leq n/2$ is Necessary

**Counterexample for $k > n/2$:**

Let $n = 5, k = 3$.

**All 3-sets:** $\binom{5}{3} = 10$ sets

**Key observation:** Any two 3-sets from a 5-element set MUST intersect!

**Proof:** If $|A| = |B| = 3$ and $A \cap B = \emptyset$, then $|A \cup B| = 6 > 5$. Contradiction!

So for $k > n/2$, **all** $\binom{n}{k}$ sets form an intersecting family!

**For $n = 5, k = 3$:**
- EKR would give: $\binom{4}{2} = 6$
- Actual maximum: $\binom{5}{3} = 10$

This is why the condition $k \leq n/2$ is essential!

---

## Comparison: All $k$-sets vs. EKR Maximum

| $n$ | $k$ | All $k$-sets $\binom{n}{k}$ | EKR bound $\binom{n-1}{k-1}$ | Ratio |
|-----|-----|----------------------------|------------------------------|-------|
| 5 | 2 | 10 | 4 | 40% |
| 6 | 3 | 20 | 10 | 50% |
| 7 | 3 | 35 | 15 | 43% |
| 8 | 4 | 70 | 35 | 50% |
| 9 | 4 | 126 | 56 | 44% |

**Observation:** The intersecting condition reduces the maximum by about 50-60%!

---

## Proof of EKR Theorem (Sketch)

**Method 1: Shifting**

Define a "shifting" operation that:
1. Preserves the intersecting property
2. Doesn't decrease family size
3. Eventually produces a "shifted" family

For shifted families, the maximum is achieved by taking all $k$-sets containing element 1.

**Method 2: Katona's cycle method**

Arrange elements on a circle and count "arcs" (consecutive $k$-sets).

**Method 3: Linear algebra**

Use characteristic vectors and eigenvalue methods.

---

## Generalization: $t$-Intersecting Families

**Definition:** $\mathcal{F}$ is **$t$-intersecting** if $|A_i \cap A_j| \geq t$ for all $i \neq j$.

**Erdős-Ko-Rado for $t$-intersections:**

For $n \geq (t+1)(k-t+1)$:
$$m \leq \binom{n-t}{k-t}$$

**Construction:** All $k$-sets containing a fixed $t$-set.

---

## Application: Committee Selection

**Problem:** Select committees of size $k$ from $n$ people such that any two committees share at least one member.

**Solution:** By EKR, maximum number of committees is $\binom{n-1}{k-1}$.

**Optimal strategy:** Fix one person (the "chair"), and form all committees containing that person.

---

## Verification Table

| $n$ | $k$ | EKR Bound | Construction | Intersecting? |
|-----|-----|-----------|--------------|---------------|
| 4 | 2 | $\binom{3}{1} = 3$ | {1,2}, {1,3}, {1,4} | ✓ |
| 5 | 2 | $\binom{4}{1} = 4$ | {1,2}, {1,3}, {1,4}, {1,5} | ✓ |
| 6 | 2 | $\binom{5}{1} = 5$ | All 2-sets with 1 | ✓ |
| 6 | 3 | $\binom{5}{2} = 10$ | All 3-sets with 1 | ✓ |
| 7 | 3 | $\binom{6}{2} = 15$ | All 3-sets with 1 | ✓ |
| 8 | 3 | $\binom{7}{2} = 21$ | All 3-sets with 1 | ✓ |
| 8 | 4 | $\binom{7}{3} = 35$ | All 4-sets with 1 | ✓ |

---

*Exercise 7.2 from Chapter 07 - Extremális halmazrendszerek*
