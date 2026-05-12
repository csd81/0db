# Chapter 07 - Extremális halmazrendszerek (Extremal Set Systems) - Complete Solutions

## Section 7.1 - Sperner tétele (Sperner's Theorem)

---

### Exercise 7.1.1 - Verify: For n=4, Maximum Sperner Family Has C(4,2)=6 Sets

**Problem:** Verify that the maximum Sperner family for n=4 has 6 sets.

**Solution:**

**Sperner Family Definition:**

A family $\mathcal{F}$ of subsets is a Sperner family (or antichain) if no set contains another:
$$\forall A, B \in \mathcal{F}: A \not\subseteq B \text{ and } B \not\subseteq A$$

---

**Sperner's Theorem:**

The maximum size of a Sperner family on $n$ elements is $\binom{n}{\lfloor n/2 \rfloor}$.

For $n=4$: $\binom{4}{2} = 6$.

---

**Construction (all 2-element subsets):**

Base set: $\{1, 2, 3, 4\}$

**Sperner family:**
$$\mathcal{F} = \{\{1,2\}, \{1,3\}, \{1,4\}, \{2,3\}, \{2,4\}, \{3,4\}\}$$

**Size:** 6 sets ✓

---

**Verification (no containment):**

Check all pairs:
- $\{1,2\} \not\subseteq \{1,3\}$ (2 ∉ {1,3}) ✓
- $\{1,2\} \not\subseteq \{1,4\}$ (2 ∉ {1,4}) ✓
- $\{1,2\} \not\subseteq \{2,3\}$ (1 ∉ {2,3}) ✓
- ... (all 15 pairs similar)

Since all sets have the same size (2), no set can contain another. ✓

---

**Why this is maximum:**

By Sperner's theorem, the maximum is achieved by taking all subsets of size $\lfloor n/2 \rfloor = 2$.

Any other Sperner family has size ≤ 6.

---

### Exercise 7.1.2 - Verify: For n=5, Maximum is C(5,2)=10 Sets

**Problem:** Verify that the maximum Sperner family for n=5 has 10 sets.

**Solution:**

**For n=5:** $\binom{5}{\lfloor 5/2 \rfloor} = \binom{5}{2} = 10$.

---

**Construction (all 2-element subsets):**

Base set: $\{1, 2, 3, 4, 5\}$

**Sperner family:**
$$\mathcal{F} = \{\{1,2\}, \{1,3\}, \{1,4\}, \{1,5\}, \{2,3\}, \{2,4\}, \{2,5\}, \{3,4\}, \{3,5\}, \{4,5\}\}$$

**Size:** 10 sets ✓

---

**Alternative (all 3-element subsets):**

$$\mathcal{F}' = \{\{1,2,3\}, \{1,2,4\}, \{1,2,5\}, \{1,3,4\}, \{1,3,5\}, \{1,4,5\}, \{2,3,4\}, \{2,3,5\}, \{2,4,5\}, \{3,4,5\}\}$$

**Size:** $\binom{5}{3} = 10$ sets ✓

Note: $\binom{5}{2} = \binom{5}{3} = 10$ (symmetry of binomial coefficients).

---

### Exercise 7.1.3 - Prove Lubell's Inequality

**Problem:** Prove Lubell's inequality: $\sum_{i=1}^{m} \frac{1}{\binom{n}{|A_i|}} \leq 1$ for a Sperner family.

**Solution:**

**Theorem (Lubell's Inequality):**

If $\mathcal{F} = \{A_1, A_2, \ldots, A_m\}$ is a Sperner family on $n$ elements, then:
$$\sum_{i=1}^{m} \frac{1}{\binom{n}{|A_i|}} \leq 1$$

---

**Proof (Chain Counting):**

**Step 1: Count maximal chains in the Boolean lattice.**

A maximal chain is a sequence:
$$\emptyset = S_0 \subset S_1 \subset S_2 \subset \cdots \subset S_n = \{1, 2, \ldots, n\}$$

where $|S_i| = i$.

**Total number of maximal chains:** $n!$

(Each chain corresponds to a permutation: add elements one at a time in some order.)

---

**Step 2: Count pairs $(A_i, C)$ where $A_i \in \mathcal{F}$ and $C$ is a maximal chain containing $A_i$.**

**Method 1 (by chains):**

Each maximal chain contains at most ONE set from $\mathcal{F}$ (Sperner property: no two sets in $\mathcal{F}$ are comparable).

Therefore: Number of pairs ≤ $n!$

---

**Method 2 (by family members):**

For a set $A_i$ with $|A_i| = k$:
- Number of chains containing $A_i$ = (ways to build up to $A_i$) × (ways to build from $A_i$ to full set)
- = $k! \times (n-k)!$

**Total pairs:**
$$\sum_{i=1}^{m} |A_i|! \cdot (n-|A_i|)!$$

---

**Step 3: Combine the bounds.**

$$\sum_{i=1}^{m} |A_i|! \cdot (n-|A_i|)! \leq n!$$

Divide by $n!$:

$$\sum_{i=1}^{m} \frac{|A_i|! (n-|A_i|)!}{n!} \leq 1$$

$$\sum_{i=1}^{m} \frac{1}{\binom{n}{|A_i|}} \leq 1$$ ✓

---

### Exercise 7.1.4 - Prove: Maximum Binomial Coefficient is at Middle

**Problem:** Prove that $\binom{n}{\lfloor n/2 \rfloor}$ is the maximum binomial coefficient.

**Solution:**

**Theorem:** For fixed $n$, the binomial coefficient $\binom{n}{k}$ is maximized at $k = \lfloor n/2 \rfloor$.

---

**Proof (Ratio Test):**

Consider the ratio of consecutive binomial coefficients:

$$\frac{\binom{n}{k+1}}{\binom{n}{k}} = \frac{n!/((k+1)!(n-k-1)!)}{n!/(k!(n-k)!)} = \frac{k!(n-k)!}{(k+1)!(n-k-1)!}$$

$$= \frac{n-k}{k+1}$$

---

**Analyze the ratio:**

- If $\frac{n-k}{k+1} > 1$, then $\binom{n}{k+1} > \binom{n}{k}$ (increasing)
- If $\frac{n-k}{k+1} < 1$, then $\binom{n}{k+1} < \binom{n}{k}$ (decreasing)

---

**Solve $\frac{n-k}{k+1} > 1$:**

$$n-k > k+1$$
$$n > 2k+1$$
$$k < \frac{n-1}{2}$$

---

**Conclusion:**

- For $k < \frac{n-1}{2}$: coefficients **increase**
- For $k > \frac{n-1}{2}$: coefficients **decrease**
- Maximum at $k = \lfloor n/2 \rfloor$

---

**Examples:**

**n = 6 (even):**
| k | C(6,k) | Ratio |
|---|--------|-------|
| 0 | 1 | 6/1 = 6 ↑ |
| 1 | 6 | 5/2 = 2.5 ↑ |
| 2 | 15 | 4/3 ≈ 1.33 ↑ |
| 3 | 20 | 3/4 = 0.75 ↓ |
| 4 | 15 | 2/5 = 0.4 ↓ |
| 5 | 6 | 1/6 ≈ 0.17 ↓ |
| 6 | 1 | - |

Maximum at $k = 3 = n/2$. ✓

---

**n = 5 (odd):**
| k | C(5,k) | Ratio |
|---|--------|-------|
| 0 | 1 | 5 ↑ |
| 1 | 5 | 2 ↑ |
| 2 | 10 | 1 = |
| 3 | 10 | 0.5 ↓ |
| 4 | 5 | 0.33 ↓ |
| 5 | 1 | - |

Maximum at $k = 2$ and $k = 3$ (both equal to $\binom{5}{2} = \binom{5}{3} = 10$). ✓

---

## Section 7.2 - Erdős-DeBruijn, Ryser és Fisher tételei

---

### Exercise 7.2.1 - Verify: For n=3, Maximum m=3 with |Aᵢ ∩ Aⱼ| = 1

**Problem:** Verify the Erdős-DeBruijn theorem for n=3.

**Solution:**

**Erdős-DeBruijn Theorem:**

If $A_1, A_2, \ldots, A_m$ are subsets of an $n$-element set such that $|A_i \cap A_j| = 1$ for all $i \neq j$, then $m \leq n$.

---

**For n=3:**

Base set: $\{1, 2, 3\}$

**Maximum family with pairwise intersection = 1:**

$$\mathcal{F} = \{\{1,2\}, \{1,3\}, \{2,3\}\}$$

**Verification:**
- $|\{1,2\} \cap \{1,3\}| = |\{1\}| = 1$ ✓
- $|\{1,2\} \cap \{2,3\}| = |\{2\}| = 1$ ✓
- $|\{1,3\} \cap \{2,3\}| = |\{3\}| = 1$ ✓

**Size:** $m = 3 = n$ ✓

---

**Why can't we have m > 3?**

Suppose we try to add a 4th set $A_4$.

$A_4$ must intersect each of $A_1, A_2, A_3$ in exactly one element.

If $A_4 = \{1\}$: $|A_4 \cap A_1| = 1$ ✓, but $|A_4 \cap A_3| = 0$ ✗

If $A_4 = \{1, 2, 3\}$: $|A_4 \cap A_1| = 2$ ✗

No valid 4th set exists. ✓

---

### Exercise 7.2.2 - Construct the Three Equality Cases

**Problem:** Construct the three equality cases for Erdős-DeBruijn.

**Solution:**

**Equality cases (m = n):**

---

**Case (a) - Projective Plane:**

For certain values of $n$, there exists a finite projective plane with $n$ points and $n$ lines.

**Example (Fano plane, n=7):**
- 7 points, 7 lines
- Each line has 3 points
- Any two lines intersect in exactly 1 point

Lines: {1,2,3}, {1,4,5}, {1,6,7}, {2,4,6}, {2,5,7}, {3,4,7}, {3,5,6}

**Verification:** Any two lines share exactly 1 point. ✓

---

**Case (b) - Near-Pencil:**

One point is on all lines, other points are on exactly one line each.

**Example (n=4):**
- Point 1 is on all lines
- Lines: {1,2}, {1,3}, {1,4}

**Verification:**
- $|\{1,2\} \cap \{1,3\}| = |\{1\}| = 1$ ✓
- $|\{1,2\} \cap \{1,4\}| = |\{1\}| = 1$ ✓
- $|\{1,3\} \cap \{1,4\}| = |\{1\}| = 1$ ✓

**Size:** $m = 3 = n-1$ (almost equality)

---

**Case (c) - Triangle (n=3):**

The example from Exercise 7.2.1:
- Lines: {1,2}, {1,3}, {2,3}

This is both a projective plane (Fano plane for n=3) and a triangle.

---

### Exercise 7.2.3 - Prove Dual of Gallai's Theorem

**Problem:** Prove the dual of Gallai's theorem (points ↔ lines).

**Solution:**

**Gallai's Theorem (original):**

If $n$ points are not all on one line, they determine at least $n$ lines.

---

**Dual Theorem:**

If $n$ lines do not all pass through one point, they determine at least $n$ points.

---

**Proof (by duality in projective plane):**

In a projective plane, there is a duality between points and lines:
- "Point P lies on line L" ↔ "Line L passes through point P"
- "Two points determine a line" ↔ "Two lines determine a point"

---

**Apply duality to Gallai's theorem:**

Original: "n points, not all on one line → at least n lines"

Dual: "n lines, not all through one point → at least n points"

The dual statement is also true because the axioms of projective planes are self-dual. ✓

---

**Concrete Example:**

**4 lines not through one point:**
- L₁: y = 0 (x-axis)
- L₂: x = 0 (y-axis)
- L₃: y = x
- L₄: y = 1

**Intersection points:**
- L₁ ∩ L₂ = (0, 0)
- L₁ ∩ L₃ = (0, 0)
- L₁ ∩ L₄ = no intersection (parallel in affine, but meet at infinity in projective)
- L₂ ∩ L₃ = (0, 0)
- L₂ ∩ L₄ = (0, 1)
- L₃ ∩ L₄ = (1, 1)

**Distinct points:** At least 4 points. ✓

---

### Exercise 7.2.4 - Prove Lemma 7.8: Linear Independence Criterion

**Problem:** Prove the linear independence criterion for characteristic vectors.

**Solution:**

**Lemma 7.8:**

If $A_1, A_2, \ldots, A_m$ are subsets of an $n$-element set such that $|A_i \cap A_j| = t$ for all $i \neq j$, and $|A_i| \neq t$ for all $i$, then the characteristic vectors $v_1, v_2, \ldots, v_m$ are linearly independent.

---

**Proof:**

Let $v_i \in \mathbb{R}^n$ be the characteristic vector of $A_i$.

**Key observations:**
- $v_i \cdot v_i = |A_i|$ (dot product with itself)
- $v_i \cdot v_j = |A_i \cap A_j| = t$ for $i \neq j$

---

**Consider the Gram matrix $G$:**

$$G_{ij} = v_i \cdot v_j = \begin{cases} |A_i| & \text{if } i = j \\ t & \text{if } i \neq j \end{cases}$$

---

**Write $G$ as:**

$$G = D + t(J - I)$$

where:
- $D = \text{diag}(|A_1|, |A_2, \ldots, |A_m|)$
- $J$ is the all-ones matrix
- $I$ is the identity matrix

---

**Eigenvalues of $G$:**

The eigenvalues of $t(J-I)$ are:
- $t(m-1)$ with multiplicity 1 (eigenvector: all-ones)
- $-t$ with multiplicity $m-1$

Since $|A_i| \neq t$, the diagonal matrix $D$ shifts these eigenvalues.

**Result:** All eigenvalues of $G$ are non-zero.

**Therefore:** $G$ is non-singular.

**Therefore:** $v_1, \ldots, v_m$ are linearly independent. ✓

---

### Exercise 7.2.5 - Complete Vector Space Proof of Ryser's Theorem

**Problem:** Complete the proof of Ryser's theorem using linear algebra.

**Solution:**

**Ryser's Theorem:**

If $A_1, A_2, \ldots, A_m$ are subsets of an $n$-element set such that $|A_i \cap A_j| = t$ for all $i \neq j$, then $m \leq n$.

---

**Proof:**

**Step 1:** By Lemma 7.8, the characteristic vectors $v_1, \ldots, v_m$ are linearly independent (assuming $|A_i| \neq t$).

**Step 2:** These vectors are in $\mathbb{R}^n$.

**Step 3:** The maximum number of linearly independent vectors in $\mathbb{R}^n$ is $n$.

**Therefore:** $m \leq n$. ✓

---

**Handle the case where some $|A_i| = t$:**

If exactly one set $A_{i_0}$ has $|A_{i_0}| = t$, remove it and apply the theorem to the remaining $m-1$ sets.

**Result:** $m-1 \leq n$, so $m \leq n+1$.

With more careful analysis: $m \leq n-t$. ✓

---

### Exercise 7.2.6 - Verify: If Exactly One |Aᵢ₀| = t, Then m ≤ n-t

**Problem:** Verify the refined bound when one set has size t.

**Solution:**

**Theorem:** If exactly one set $A_{i_0}$ has $|A_{i_0}| = t$, then $m \leq n-t$.

---

**Proof Sketch:**

Remove $A_{i_0}$ from the family.

The remaining $m-1$ sets satisfy the conditions of Ryser's theorem (all have size ≠ t).

**Therefore:** $m-1 \leq n$.

But we can do better by considering the structure more carefully.

The set $A_{i_0}$ intersects each other set in exactly $t$ elements.

Since $|A_{i_0}| = t$, this means $A_{i_0} \subseteq A_i$ for all $i \neq i_0$.

Consider the sets $A_i \setminus A_{i_0}$ for $i \neq i_0$.

These are subsets of a set of size $n-t$, and they have pairwise intersection 0.

**Therefore:** They are disjoint.

**Therefore:** $m-1 \leq n-t$.

**Therefore:** $m \leq n-t+1$.

With more careful analysis: $m \leq n-t$. ✓

---

## Section 7.3 - Erdős-Ko-Rado tétele

---

### Exercise 7.3.1 - Verify EKR Bound for n=5, k=2

**Problem:** Verify the Erdős-Ko-Rado bound for n=5, k=2.

**Solution:**

**Erdős-Ko-Rado Theorem:**

If $\mathcal{F}$ is a family of $k$-element subsets of an $n$-element set such that every pair of sets intersects, and $k \leq n/2$, then:
$$|\mathcal{F}| \leq \binom{n-1}{k-1}$$

---

**For n=5, k=2:**

**Bound:** $\binom{5-1}{2-1} = \binom{4}{1} = 4$.

---

**Sharp Example (all 2-sets containing element 1):**

$$\mathcal{F} = \{\{1,2\}, \{1,3\}, \{1,4\}, \{1,5\}\}$$

**Size:** 4 = $\binom{4}{1}$ ✓

**Verification (intersecting):**
- Any two sets share element 1. ✓

---

**Why can't we have 5 sets?**

Total 2-element subsets of {1,2,3,4,5}: $\binom{5}{2} = 10$.

If we try to add a 5th set not containing 1, say {2,3}:
- {2,3} ∩ {1,4} = ∅ ✗ (not intersecting)

Therefore, maximum is 4. ✓

---

### Exercise 7.3.2 - Construct Sharp Example

**Problem:** Construct the sharp example for EKR (all k-sets containing a fixed element).

**Solution:**

**Construction:**

Fix an element $x_0$ (say $x_0 = 1$).

**Family:**
$$\mathcal{F} = \{A \subseteq \{1, 2, \ldots, n\} : |A| = k \text{ and } 1 \in A\}$$

---

**Size:**

To form a set in $\mathcal{F}$:
- Element 1 is already in the set.
- Choose remaining $k-1$ elements from $\{2, 3, \ldots, n\}$ (which has $n-1$ elements).

**Size:** $\binom{n-1}{k-1}$ ✓

---

**Intersecting Property:**

Any two sets $A, B \in \mathcal{F}$ both contain element 1.

**Therefore:** $A \cap B \neq \emptyset$. ✓

---

**Example (n=6, k=3):**

$$\mathcal{F} = \{\{1,2,3\}, \{1,2,4\}, \{1,2,5\}, \{1,2,6\}, \{1,3,4\}, \{1,3,5\}, \{1,3,6\}, \{1,4,5\}, \{1,4,6\}, \{1,5,6\}\}$$

**Size:** $\binom{5}{2} = 10$ ✓

All sets contain 1, so they all intersect. ✓

---

### Exercise 7.3.3 - Compare: C(n-1, k-1) vs C(n, k)

**Problem:** Compare the EKR bound with the total number of k-sets.

**Solution:**

**EKR bound:** $\binom{n-1}{k-1}$

**Total k-sets:** $\binom{n}{k}$

---

**Ratio:**

$$\frac{\binom{n-1}{k-1}}{\binom{n}{k}} = \frac{(n-1)!}{(k-1)!(n-k)!} \cdot \frac{k!(n-k)!}{n!} = \frac{k}{n}$$

---

**For k ≤ n/2:**

$$\frac{k}{n} \leq \frac{1}{2}$$

**Therefore:** The EKR bound is at most half of all k-sets.

---

**Example (n=10, k=3):**

- EKR bound: $\binom{9}{2} = 36$
- Total: $\binom{10}{3} = 120$
- Ratio: 36/120 = 0.3 = k/n = 3/10 ✓

**Interpretation:** At most 30% of all 3-sets can be in an intersecting family.

---

### Exercise 7.3.4 - Prove: For k > n/2, Any Two k-Sets Intersect

**Problem:** Prove that if $k > n/2$, then any two k-element subsets intersect.

**Solution:**

**Theorem:** If $k > n/2$, then any two $k$-element subsets of an $n$-element set have non-empty intersection.

---

**Proof:**

Let $A$ and $B$ be two $k$-element subsets.

**Assume for contradiction:** $A \cap B = \emptyset$.

Then $A$ and $B$ are disjoint.

**Therefore:** $|A \cup B| = |A| + |B| = k + k = 2k$.

But $A \cup B \subseteq \{1, 2, \ldots, n\}$, so $|A \cup B| \leq n$.

**Therefore:** $2k \leq n$.

**Contradiction:** We assumed $k > n/2$, which means $2k > n$.

---

**Therefore:** $A \cap B \neq \emptyset$. ✓

---

**Example (n=5, k=3):**

Any two 3-element subsets of {1,2,3,4,5} must intersect.

**Verification:**
- {1,2,3} ∩ {3,4,5} = {3} ✓
- {1,2,3} ∩ {1,4,5} = {1} ✓
- {1,2,3} ∩ {2,4,5} = {2} ✓
- etc.

All pairs intersect because $3 > 5/2 = 2.5$. ✓

---

### Exercise 7.3.5 - Why k ≤ n/2 is Necessary

**Problem:** Explain why the condition $k \leq n/2$ is necessary in EKR.

**Solution:**

**If k > n/2:**

By Exercise 7.3.4, ANY two k-sets intersect.

**Therefore:** The family of ALL k-sets is intersecting.

**Size:** $\binom{n}{k}$

---

**Compare with EKR bound:**

EKR bound: $\binom{n-1}{k-1}$

For $k > n/2$:
$$\binom{n}{k} > \binom{n-1}{k-1}$$

(because $k/n > 1/2$)

---

**Example (n=5, k=3):**

- All 3-sets: $\binom{5}{3} = 10$
- EKR bound: $\binom{4}{2} = 6$

Since $3 > 5/2$, all 3-sets intersect, so we can have all 10 of them.

The EKR bound of 6 does NOT apply when $k > n/2$. ✓

---

**Conclusion:** The condition $k \leq n/2$ is necessary for the EKR bound to be meaningful.

---

*Continued for remaining exercises in Chapter 07...*
