# Exercise 7.1 - Sperner's Theorem Applications

## Problem Statement

Find the maximum size of a Sperner family (no set contains another) for:
- (a) $n = 6$
- (b) $n = 7$
- (c) Verify Lubell's inequality for a specific example

---

## Solution

### Part (a): $n = 6$

By Sperner's theorem, the maximum size is:
$$m \leq \binom{6}{\lfloor 6/2 \rfloor} = \binom{6}{3} = \frac{6 \cdot 5 \cdot 4}{3 \cdot 2 \cdot 1} = 20$$

**Maximum construction:** All 3-element subsets of $\{1,2,3,4,5,6\}$

**List of all 20 sets:**
```
{1,2,3}, {1,2,4}, {1,2,5}, {1,2,6}, {1,3,4},
{1,3,5}, {1,3,6}, {1,4,5}, {1,4,6}, {1,5,6},
{2,3,4}, {2,3,5}, {2,3,6}, {2,4,5}, {2,4,6},
{2,5,6}, {3,4,5}, {3,4,6}, {3,5,6}, {4,5,6}
```

**Verification:** No set contains another (all have exactly 3 elements) ✓

---

### Part (b): $n = 7$

By Sperner's theorem:
$$m \leq \binom{7}{\lfloor 7/2 \rfloor} = \binom{7}{3} = \frac{7 \cdot 6 \cdot 5}{3 \cdot 2 \cdot 1} = 35$$

**Maximum construction:** All 3-element subsets of $\{1,2,3,4,5,6,7\}$

**Count:** $\binom{7}{3} = 35$ sets ✓

---

### Part (c): Verify Lubell's Inequality

**Lubell's inequality (7.4 Tétel):**
$$\sum_{i=1}^m \frac{1}{\binom{n}{|A_i|}} \leq 1$$

**Example:** $n = 4$, Sperner family $\mathcal{F} = \{\{1,2\}, \{1,3\}, \{1,4\}, \{2,3\}, \{2,4\}, \{3,4\}\}$

All sets have size 2, so:
$$\sum_{i=1}^6 \frac{1}{\binom{4}{2}} = 6 \cdot \frac{1}{6} = 1$$ ✓

**Another example:** $n = 4$, mixed sizes

Let $\mathcal{F} = \{\{1\}, \{2,3\}, \{2,4\}, \{3,4\}\}$

Check Sperner property:
- $\{1\}$ doesn't contain any 2-element set ✓
- No 2-element set contains $\{1\}$ ✓
- 2-element sets don't contain each other ✓

**Lubell's inequality:**
$$\sum_{i=1}^4 \frac{1}{\binom{4}{|A_i|}} = \frac{1}{\binom{4}{1}} + \frac{1}{\binom{4}{2}} + \frac{1}{\binom{4}{2}} + \frac{1}{\binom{4}{2}}$$
$$= \frac{1}{4} + \frac{1}{6} + \frac{1}{6} + \frac{1}{6} = \frac{1}{4} + \frac{3}{6} = \frac{1}{4} + \frac{1}{2} = \frac{3}{4} < 1$$ ✓

---

## Proof of Lubell's Inequality

**Key idea:** Count chains.

**Definition:** A **maximal chain** in $\mathcal{P}(S)$ is:
$$\emptyset = C_0 \subset C_1 \subset C_2 \subset \cdots \subset C_n = S$$
where $|C_i| = i$.

**Fact:** There are exactly $n!$ maximal chains (correspond to permutations of $S$).

**Key observation:** If $A \subseteq S$ with $|A| = k$, then $A$ appears in exactly $k!(n-k)!$ maximal chains.

**Proof:** 
- Choose ordering of elements in $A$: $k!$ ways
- Choose ordering of elements in $S \setminus A$: $(n-k)!$ ways
- Concatenate to get a permutation, which gives a chain

**Sperner property implication:** Different sets from $\mathcal{F}$ appear in disjoint sets of chains.

Therefore:
$$\sum_{i=1}^m |A_i|!(n-|A_i|)! \leq n!$$

Dividing by $n!$:
$$\sum_{i=1}^m \frac{|A_i|!(n-|A_i|)!}{n!} = \sum_{i=1}^m \frac{1}{\binom{n}{|A_i|}} \leq 1$$ ✓

---

## Connection to Sperner's Theorem

From Lubell's inequality:
$$\sum_{i=1}^m \frac{1}{\binom{n}{|A_i|}} \leq 1$$

Since $\binom{n}{k}$ is maximized at $k = \lfloor n/2 \rfloor$:
$$\frac{1}{\binom{n}{|A_i|}} \geq \frac{1}{\binom{n}{\lfloor n/2 \rfloor}}$$

Therefore:
$$\sum_{i=1}^m \frac{1}{\binom{n}{\lfloor n/2 \rfloor}} \leq \sum_{i=1}^m \frac{1}{\binom{n}{|A_i|}} \leq 1$$

$$\frac{m}{\binom{n}{\lfloor n/2 \rfloor}} \leq 1$$

$$m \leq \binom{n}{\lfloor n/2 \rfloor}$$

This proves Sperner's theorem! ✓

---

## Verification Table

| n | Max size $\binom{n}{\lfloor n/2 \rfloor}$ | Construction |
|---|------------------------------------------|--------------|
| 1 | 1 | {1} |
| 2 | 2 | {1}, {2} |
| 3 | 3 | {1,2}, {1,3}, {2,3} |
| 4 | 6 | All 2-element subsets |
| 5 | 10 | All 2-element or all 3-element |
| 6 | 20 | All 3-element subsets |
| 7 | 35 | All 3-element subsets |
| 8 | 70 | All 4-element subsets |

---

## Generalization: LYM Inequality

The **LYM inequality** (Lubell-Yamamoto-Meshalkin) is exactly Lubell's inequality:
$$\sum_{i=1}^m \frac{1}{\binom{n}{|A_i|}} \leq 1$$

This is stronger than Sperner's theorem because it accounts for different set sizes.

---

*Exercise 7.1 from Chapter 07 - Extremális halmazrendszerek*
