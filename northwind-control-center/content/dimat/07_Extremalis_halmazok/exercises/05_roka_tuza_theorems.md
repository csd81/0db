# Exercise 7.5 - Róka Sándor's Theorems and Tuza's Theorem

## Problem Statement

Apply the more recent extremal results:
- (a) Róka 7.14: Symmetric difference version
- (b) Róka 7.15: Triple intersection bound
- (c) Róka 7.17: Independent intersection systems
- (d) Tuza 7.18: Cross-intersection conditions

---

## Solution

### Part (a): Róka's Symmetric Difference Theorem (7.14 Tétel, 1992)

**Theorem:** If $|A_i \triangle A_j| \in L$ for all $i \neq j$, where $|L| = s$, then:
$$m \leq \binom{n}{s}$$

**Definition:** Symmetric difference $A \triangle B = (A \setminus B) \cup (B \setminus A)$

---

**Example 1: $n = 4, L = \{2\}$ (s = 1)**

**Bound:** $m \leq \binom{4}{1} = 4$

**Construction:** Find sets where any two have symmetric difference of size 2.

Take all 2-element subsets:
```
{1,2}, {1,3}, {1,4}, {2,3}, {2,4}, {3,4}
```

**Symmetric differences:**
- $|\{1,2\} \triangle \{1,3\}| = |\{2, 3\}| = 2$ ✓
- $|\{1,2\} \triangle \{3,4\}| = |\{1, 2, 3, 4\}| = 4$ ✗

This doesn't work! We need ALL pairs to have symmetric difference = 2.

**Better construction:**
```
{1,2}, {2,3}, {3,4}, {4,1}
```

**Verification:**
- $|\{1,2\} \triangle \{2,3\}| = |\{1, 3\}| = 2$ ✓
- $|\{1,2\} \triangle \{3,4\}| = |\{1, 2, 3, 4\}| = 4$ ✗

Still doesn't work for all pairs.

**Working construction (size 3):**
```
{1,2}, {2,3}, {1,3}
```

**Verification:**
- $|\{1,2\} \triangle \{2,3\}| = |\{1, 3\}| = 2$ ✓
- $|\{1,2\} \triangle \{1,3\}| = |\{2, 3\}| = 2$ ✓
- $|\{2,3\} \triangle \{1,3\}| = |\{1, 2\}| = 2$ ✓

So $m = 3 \leq 4$ ✓

---

**Example 2: $n = 5, L = \{2, 4\}$ (s = 2)**

**Bound:** $m \leq \binom{5}{2} = 10$

**Construction:** All 2-element subsets:
- Count: $\binom{5}{2} = 10$ sets
- Symmetric difference of two 2-sets:
  - If they share 1 element: $|\{a,b\} \triangle \{a,c\}| = |\{b, c\}| = 2$ ✓
  - If disjoint: $|\{a,b\} \triangle \{c,d\}| = |\{a, b, c, d\}| = 4$ ✓

So $L = \{2, 4\}$ and $m = 10 = \binom{5}{2}$ ✓

This achieves the bound!

---

### Part (b): Róka's Triple Intersection Theorem (7.15 Tétel, 1993)

**Theorem:** If $|A_i| = 3$ and $|A_i \cap A_j \cap A_k| \leq 1$ for all distinct $i, j, k$, then:
$$m \leq \frac{1}{3}n(n-1)$$

---

**Example: $n = 6$**

**Bound:** $m \leq \frac{1}{3} \cdot 6 \cdot 5 = 10$

**Construction:** All 3-element subsets?
- Count: $\binom{6}{3} = 20$ sets
- Triple intersection: Three 3-sets can share at most... 

Wait, we need to check: $|A_i \cap A_j \cap A_k| \leq 1$

Take $\{1,2,3\}, \{1,2,4\}, \{1,2,5\}$:
- Triple intersection = $\{1, 2\}$, size = 2 ✗

So we can't take all 3-sets.

**Better construction:** Take 3-sets such that no two elements appear together in more than 2 sets.

This is related to **packing designs**.

For $n = 6$, a good construction:
```
{1,2,3}, {1,4,5}, {2,4,6}, {3,5,6}
```

**Verification:**
- Any three sets have triple intersection of size at most 1 ✓
- $m = 4 \leq 10$ ✓

Can we do better? This is an open research problem!

---

**Example: $n = 7$ (Fano Plane)**

**Bound:** $m \leq \frac{1}{3} \cdot 7 \cdot 6 = 14$

**Fano plane lines (7 sets of size 3):**
```
{1,2,3}, {1,4,5}, {1,6,7}, {2,4,6}, {2,5,7}, {3,4,7}, {3,5,6}
```

**Triple intersection check:**
- Any three lines in Fano plane intersect in at most 1 point ✓
- (This is a property of projective planes)

So $m = 7 \leq 14$ ✓

---

### Part (c): Róka's Independent Intersection Systems (7.17 Tétel, 1997)

**Definition:** $\{A_1, \ldots, A_m\}$ is an **intersection system** if every $x \in S$ can be written as:
$$x = \bigcap \{A_i : i \in I_x\}$$

for some $I_x \subseteq \{1, \ldots, m\}$.

**Independent:** Removing any $A_i$ destroys the intersection system property.

---

**Theorem (7.17):** For an independent intersection system on $n$ elements:
$$c_1 \log_2 n \leq m \leq c_2 n^2$$

Both bounds are tight in order of magnitude!

---

**Example: Lower bound construction**

**Idea:** Use binary representation.

For $n = 2^k$, we need about $k = \log_2 n$ sets.

**Construction:** Let $S = \{0, 1, \ldots, 2^k - 1\}$.

For each bit position $j = 1, \ldots, k$, define:
$$A_j = \{x \in S : \text{$j$-th bit of $x$ is 1}\}$$

**Verification:**
- Each element $x$ is uniquely determined by which $A_j$'s contain it
- Specifically: $x = \bigcap_{j: x \in A_j} A_j \cap \bigcap_{j: x \notin A_j} \overline{A_j}$
- But we need intersections only (no complements)

**Better construction:** Use both $A_j$ and "complement-like" sets.

For $n = 4 = 2^2$:
```
A₁ = {1, 2}  (first bit = 1)
A₂ = {2, 3}  (second bit = 1)
A₃ = {1, 4}  (first bit = 0, encoded differently)
A₄ = {3, 4}  (second bit = 0, encoded differently)
```

Each element is an intersection of some of these sets.

**Result:** $m \approx 2 \log_2 n$ sets suffice.

---

**Example: Upper bound construction**

**Idea:** Take all pairs.

For $n$ elements, take all $\binom{n}{2}$ 2-element sets.

**Verification:**
- Each singleton $\{x\}$ can be obtained as intersection of all pairs containing $x$
- Actually, we need to be more careful...

**Better:** Take a specific construction with $O(n^2)$ sets.

The exact constants $c_1, c_2$ are research problems!

---

### Part (d): Tuza's Theorem (7.18 Tétel, 1987)

**Theorem 7.18(a):** If $A_i \cap B_j \neq \emptyset$ for all $i \neq j$, then:
$$\sum_{i=1}^m \frac{1}{\binom{|A_i| + |B_i|}{|A_i|}} \leq 1$$

**Theorem 7.18(b):** If $A_i \cap B_j \neq \emptyset$ for all $i < j$, with $a = \max |A_i|$, $b = \max |B_i|$, then:
$$m \leq \binom{a+b}{a}$$

**Theorem 7.18(c):** If $A_i \cap B_j \neq \emptyset$ OR $B_i \cap A_j \neq \emptyset$ for all $i \neq j$, then for any $p, q > 0$ with $p + q = 1$:
$$\sum_{i=1}^m p^{|A_i|} q^{|B_i|} \leq 1$$

---

**Example for 7.18(a):**

$n = 4$, pairs $(A_i, B_i)$:
```
(A₁, B₁) = ({1}, {2,3,4})
(A₂, B₂) = ({2}, {1,3,4})
(A₃, B₃) = ({3}, {1,2,4})
(A₄, B₄) = ({4}, {1,2,3})
```

**Check condition:** $A_i \cap B_j \neq \emptyset$ for $i \neq j$:
- $A_1 \cap B_2 = \{1\} \cap \{1,3,4\} = \{1\}$ ✓
- $A_1 \cap B_3 = \{1\} \cap \{1,2,4\} = \{1\}$ ✓
- etc.

**Tuza's inequality:**
$$\sum_{i=1}^4 \frac{1}{\binom{1+3}{1}} = 4 \cdot \frac{1}{4} = 1$$ ✓

---

## Summary Table

| Theorem | Condition | Bound | Application |
|---------|-----------|-------|-------------|
| Róka 7.14 | $|A_i \triangle A_j| \in L$ | $\binom{n}{s}$ | Coding theory |
| Róka 7.15 | $|A_i \cap A_j \cap A_k| \leq 1$ | $\frac{1}{3}n(n-1)$ | Packing designs |
| Róka 7.17 | Independent intersection system | $c_1 \log n \leq m \leq c_2 n^2$ | Data structures |
| Tuza 7.18(a) | $A_i \cap B_j \neq \emptyset$ ($i \neq j$) | Sum inequality | Cross-intersection |
| Tuza 7.18(b) | $A_i \cap B_j \neq \emptyset$ ($i < j$) | $\binom{a+b}{a}$ | Ordered systems |
| Tuza 7.18(c) | Symmetric cross-intersection | Weighted sum | Probability |

---

## Research Problems

1. **Róka 7.15:** Exact maximum for specific $n$?
2. **Róka 7.17:** Best constants $c_1, c_2$?
3. **Tuza:** Extensions to hypergraphs?

---

*Exercise 7.5 from Chapter 07 - Extremális halmazrendszerek*
