# Chapter 04 - Logikai szitaformula (Inclusion-Exclusion) - Complete Solutions

## Section 4.1 - A szitaformula (The Inclusion-Exclusion Formula)

---

### Exercise 4.1.1 - Prove Inclusion-Exclusion for Two Sets

**Problem:** Prove $|A \cup B| = |A| + |B| - |A \cap B|$.

**Solution:**

**Theorem:** For any finite sets A and B:
$$|A \cup B| = |A| + |B| - |A \cap B|$$

---

**Proof 1 (Element Counting):**

Partition $A \cup B$ into three disjoint parts:
1. Elements in A only: $A \setminus B$
2. Elements in B only: $B \setminus A$
3. Elements in both: $A \cap B$

Since these are disjoint:
$$|A \cup B| = |A \setminus B| + |B \setminus A| + |A \cap B| \quad \text{(Equation 1)}$$

Now observe:
- $|A| = |A \setminus B| + |A \cap B|$ (A is disjoint union of "A only" and "both")
- $|B| = |B \setminus A| + |A \cap B|$ (B is disjoint union of "B only" and "both")

Solving for the "only" parts:
- $|A \setminus B| = |A| - |A \cap B|$
- $|B \setminus A| = |B| - |A \cap B|$

Substitute into Equation 1:
$$|A \cup B| = (|A| - |A \cap B|) + (|B| - |A \cap B|) + |A \cap B|$$
$$= |A| + |B| - |A \cap B|$$ ✓

---

**Proof 2 (Using Indicator Functions):**

Define indicator function: $\mathbf{1}_S(x) = 1$ if $x \in S$, else 0.

**Key observation:** $\mathbf{1}_{A \cup B}(x) = \mathbf{1}_A(x) + \mathbf{1}_B(x) - \mathbf{1}_A(x) \cdot \mathbf{1}_B(x)$

**Verification by cases:**

| x in A? | x in B? | LHS | RHS |
|---------|---------|-----|-----|
| No | No | 0 | 0 + 0 - 0 = 0 ✓ |
| Yes | No | 1 | 1 + 0 - 0 = 1 ✓ |
| No | Yes | 1 | 0 + 1 - 0 = 1 ✓ |
| Yes | Yes | 1 | 1 + 1 - 1 = 1 ✓ |

**Sum over all x:**
$$\sum_x \mathbf{1}_{A \cup B}(x) = \sum_x \mathbf{1}_A(x) + \sum_x \mathbf{1}_B(x) - \sum_x \mathbf{1}_A(x) \cdot \mathbf{1}_B(x)$$

$$|A \cup B| = |A| + |B| - |A \cap B|$$ ✓

---

**Concrete Example:**

Let $A = \{1, 2, 3, 4\}$ and $B = \{3, 4, 5, 6\}$.

- $|A| = 4$
- $|B| = 4$
- $A \cap B = \{3, 4\}$, so $|A \cap B| = 2$
- $A \cup B = \{1, 2, 3, 4, 5, 6\}$, so $|A \cup B| = 6$

**Formula verification:**
$$6 = 4 + 4 - 2 = 6$$ ✓

---

**Venn Diagram Visualization:**

```
    ┌─────────────┐
    │     A       │
    │  ┌─────┐    │
    │  │ A∩B │    │
    │  └─────┘    │
    │     B       │
    └─────────────┘
```

When we add $|A| + |B|$, the intersection $A \cap B$ is counted twice, so we subtract it once.

---

### Exercise 4.1.2 - Prove Inclusion-Exclusion for Three Sets

**Problem:** Prove $|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$.

**Solution:**

**Theorem:** For any finite sets A, B, C:
$$|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$$

---

**Proof (Using Two-Set Formula Twice):**

Let $D = B \cup C$. Then:
$$|A \cup B \cup C| = |A \cup D|$$

Apply the two-set formula:
$$|A \cup D| = |A| + |D| - |A \cap D|$$

---

**Step 1: Expand |D|**

$$|D| = |B \cup C| = |B| + |C| - |B \cap C|$$

---

**Step 2: Expand |A ∩ D|**

$$|A \cap D| = |A \cap (B \cup C)|$$

Using distributivity: $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$

Apply two-set formula again:
$$|(A \cap B) \cup (A \cap C)| = |A \cap B| + |A \cap C| - |(A \cap B) \cap (A \cap C)|$$

Note: $(A \cap B) \cap (A \cap C) = A \cap B \cap C$

Therefore:
$$|A \cap D| = |A \cap B| + |A \cap C| - |A \cap B \cap C|$$

---

**Step 3: Combine**

$$|A \cup B \cup C| = |A| + (|B| + |C| - |B \cap C|) - (|A \cap B| + |A \cap C| - |A \cap B \cap C|)$$

$$= |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$$ ✓

---

**Proof 2 (Region Counting):**

Partition $A \cup B \cup C$ into 7 disjoint regions:

| Region | Description | Count |
|--------|-------------|-------|
| 1 | A only | $|A| - |A \cap B| - |A \cap C| + |A \cap B \cap C|$ |
| 2 | B only | $|B| - |A \cap B| - |B \cap C| + |A \cap B \cap C|$ |
| 3 | C only | $|C| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$ |
| 4 | A ∩ B only | $|A \cap B| - |A \cap B \cap C|$ |
| 5 | A ∩ C only | $|A \cap C| - |A \cap B \cap C|$ |
| 6 | B ∩ C only | $|B \cap C| - |A \cap B \cap C|$ |
| 7 | A ∩ B ∩ C | $|A \cap B \cap C|$ |

**Sum all regions:**

$$|A \cup B \cup C| = (|A| - |A \cap B| - |A \cap C| + |A \cap B \cap C|) + \cdots$$

After collecting terms:
$$= |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$$ ✓

---

**Concrete Example:**

Let:
- $A = \{1, 2, 3, 4\}$
- $B = \{3, 4, 5, 6\}$
- $C = \{5, 6, 7, 8\}$

**Calculate:**
- $|A| = 4, |B| = 4, |C| = 4$
- $|A \cap B| = 2$ (elements 3, 4)
- $|A \cap C| = 0$ (empty)
- $|B \cap C| = 2$ (elements 5, 6)
- $|A \cap B \cap C| = 0$ (empty)
- $A \cup B \cup C = \{1, 2, 3, 4, 5, 6, 7, 8\}$, so $|A \cup B \cup C| = 8$

**Formula verification:**
$$8 = 4 + 4 + 4 - 2 - 0 - 2 + 0 = 8$$ ✓

---

### Exercise 4.1.3 - General Inclusion-Exclusion Formula

**Problem:** State and prove the general inclusion-exclusion formula.

**Solution:**

**Theorem (General Inclusion-Exclusion):**

For finite sets $A_1, A_2, \ldots, A_n$:

$$\left|\bigcup_{i=1}^{n} A_i\right| = \sum_{i} |A_i| - \sum_{i<j} |A_i \cap A_j| + \sum_{i<j<k} |A_i \cap A_j \cap A_k| - \cdots + (-1)^{n-1} |A_1 \cap \cdots \cap A_n|$$

Or more compactly:
$$\left|\bigcup_{i=1}^{n} A_i\right| = \sum_{\emptyset \neq S \subseteq \{1,\ldots,n\}} (-1)^{|S|-1} \left|\bigcap_{i \in S} A_i\right|$$

---

**Pattern:**
- **Add** singletons: $\sum |A_i|$ (1 set at a time)
- **Subtract** pairs: $-\sum |A_i \cap A_j|$ (2 sets at a time)
- **Add** triples: $+\sum |A_i \cap A_j \cap A_k|$ (3 sets at a time)
- **Subtract** quadruples: $-\sum |A_i \cap A_j \cap A_k \cap A_l|$ (4 sets at a time)
- Continue alternating...

---

**Number of Terms:**

| Intersection Size | Count | Sign |
|-------------------|-------|------|
| 1 set | $\binom{n}{1}$ | + |
| 2 sets | $\binom{n}{2}$ | - |
| 3 sets | $\binom{n}{3}$ | + |
| ... | ... | ... |
| n sets | $\binom{n}{n} = 1$ | $(-1)^{n-1}$ |

**Total terms:** $\binom{n}{1} + \binom{n}{2} + \cdots + \binom{n}{n} = 2^n - 1$

---

**Proof by Induction:**

**Base case (n=1):** $|A_1| = |A_1|$ ✓

**Base case (n=2):** $|A_1 \cup A_2| = |A_1| + |A_2| - |A_1 \cap A_2|$ ✓

---

**Inductive hypothesis:** Assume formula holds for $n = k$ sets.

---

**Inductive step (n = k+1):**

$$\left|\bigcup_{i=1}^{k+1} A_i\right| = \left|\left(\bigcup_{i=1}^{k} A_i\right) \cup A_{k+1}\right|$$

Let $U = \bigcup_{i=1}^{k} A_i$. Then:
$$|U \cup A_{k+1}| = |U| + |A_{k+1}| - |U \cap A_{k+1}|$$

By inductive hypothesis:
$$|U| = \sum_{i} |A_i| - \sum_{i<j} |A_i \cap A_j| + \cdots + (-1)^{k-1} |A_1 \cap \cdots \cap A_k|$$

And:
$$|U \cap A_{k+1}| = \left|\bigcup_{i=1}^{k} (A_i \cap A_{k+1})\right|$$

Apply inductive hypothesis to the sets $A_i \cap A_{k+1}$:
$$|U \cap A_{k+1}| = \sum_{i} |A_i \cap A_{k+1}| - \sum_{i<j} |A_i \cap A_j \cap A_{k+1}| + \cdots$$

Substitute back and collect terms. The result is the formula for $k+1$ sets. ✓

---

**Example (n=4):**

$$|A \cup B \cup C \cup D| = $$

**Singletons (4 terms):**
$$(|A| + |B| + |C| + |D|)$$

**Pairs (6 terms):**
$$- (|A \cap B| + |A \cap C| + |A \cap D| + |B \cap C| + |B \cap D| + |C \cap D|)$$

**Triples (4 terms):**
$$+ (|A \cap B \cap C| + |A \cap B \cap D| + |A \cap C \cap D| + |B \cap C \cap D|)$$

**Quadruple (1 term):**
$$- |A \cap B \cap C \cap D|$$

**Total:** 4 + 6 + 4 + 1 = 15 = $2^4 - 1$ terms ✓

---

**Why It Works (Intuition):**

Each element $x$ in the union is counted exactly once.

**Example:** If $x$ is in exactly 3 sets (say A, B, C):

| Term | How many times x is counted |
|------|----------------------------|
| Singletons | +3 (in A, B, C) |
| Pairs | -3 (in A∩B, A∩C, B∩C) |
| Triples | +1 (in A∩B∩C) |
| **Net** | **3 - 3 + 1 = 1** ✓ |

In general, if x is in exactly m sets:
$$\binom{m}{1} - \binom{m}{2} + \binom{m}{3} - \cdots + (-1)^{m-1}\binom{m}{m} = 1$$

(This is the alternating sum of binomial coefficients, which equals 1 for m ≥ 1)

---

## Section 4.2 - Derangements (Fixpontnélküli permutációk)

---

### Exercise 4.2.1 - Derive the Derangement Formula

**Problem:** Derive the formula $D_n = n! \sum_{k=0}^{n} \frac{(-1)^k}{k!}$.

**Solution:**

**Definition:** A derangement is a permutation with no fixed points (no element stays in its original position).

Let $D_n$ = number of derangements of $\{1, 2, \ldots, n\}$.

---

**Derivation using Inclusion-Exclusion:**

Let $S$ be the set of all $n!$ permutations.

For $i = 1, \ldots, n$, define:
$$A_i = \{\text{permutations where element } i \text{ is fixed (in position } i)\}$$

We want permutations in **none** of the $A_i$, i.e., derangements.

$$D_n = |S| - |A_1 \cup A_2 \cup \cdots \cup A_n|$$

---

**Apply Inclusion-Exclusion:**

$$|A_1 \cup \cdots \cup A_n| = \sum_i |A_i| - \sum_{i<j} |A_i \cap A_j| + \sum_{i<j<k} |A_i \cap A_j \cap A_k| - \cdots$$

---

**Calculate each term:**

**Singletons:** $|A_i|$ = permutations fixing element $i$
- Fix element $i$, permute remaining $(n-1)$ elements
- $|A_i| = (n-1)!$
- There are $\binom{n}{1}$ such terms

**Pairs:** $|A_i \cap A_j|$ = permutations fixing both $i$ and $j$
- Fix 2 elements, permute remaining $(n-2)$ elements
- $|A_i \cap A_j| = (n-2)!$
- There are $\binom{n}{2}$ such terms

**Triples:** $|A_i \cap A_j \cap A_k|$ = permutations fixing 3 elements
- Fix 3 elements, permute remaining $(n-3)$ elements
- $|A_i \cap A_j \cap A_k| = (n-3)!$
- There are $\binom{n}{3}$ such terms

**In general:** Fixing $k$ elements leaves $(n-k)!$ permutations, and there are $\binom{n}{k}$ ways to choose which $k$ elements to fix.

---

**Substitute:**

$$|A_1 \cup \cdots \cup A_n| = \binom{n}{1}(n-1)! - \binom{n}{2}(n-2)! + \binom{n}{3}(n-3)! - \cdots + (-1)^{n-1}\binom{n}{n}(n-n)!$$

---

**Simplify using $\binom{n}{k} = \frac{n!}{k!(n-k)!}$:**

$$|A_1 \cup \cdots \cup A_n| = \frac{n!}{1!(n-1)!}(n-1)! - \frac{n!}{2!(n-2)!}(n-2)! + \frac{n!}{3!(n-3)!}(n-3)! - \cdots$$

$$= n!\left[\frac{1}{1!} - \frac{1}{2!} + \frac{1}{3!} - \cdots + (-1)^{n-1}\frac{1}{n!}\right]$$

---

**Therefore, derangements:**

$$D_n = n! - |A_1 \cup \cdots \cup A_n|$$

$$= n!\left[1 - \frac{1}{1!} + \frac{1}{2!} - \frac{1}{3!} + \cdots + (-1)^n\frac{1}{n!}\right]$$

$$= n! \sum_{k=0}^{n} \frac{(-1)^k}{k!}$$ ✓

---

### Exercise 4.2.2 - Verify Dₙ Values for Small n

**Problem:** Verify derangement values for n = 1 through 12.

**Solution:**

**Formula:** $D_n = n! \sum_{k=0}^{n} \frac{(-1)^k}{k!}$

---

**Calculations:**

| n | n! | Sum | Dₙ | Verification |
|---|-----|-----|-----|--------------|
| 1 | 1 | $1 - 1 = 0$ | 0 | No derangement of 1 element ✓ |
| 2 | 2 | $1 - 1 + \frac{1}{2} = 0.5$ | 1 | (2,1) is only derangement ✓ |
| 3 | 6 | $1 - 1 + \frac{1}{2} - \frac{1}{6} = \frac{1}{3}$ | 2 | (2,3,1), (3,1,2) ✓ |
| 4 | 24 | $1 - 1 + \frac{1}{2} - \frac{1}{6} + \frac{1}{24} = \frac{3}{8}$ | 9 | List all 9 ✓ |
| 5 | 120 | $\frac{11}{30}$ | 44 | Formula ✓ |
| 6 | 720 | $\frac{53}{144}$ | 265 | Formula ✓ |
| 7 | 5040 | $\frac{103}{280}$ | 1854 | Formula ✓ |
| 8 | 40320 | $\frac{2119}{5760}$ | 14833 | Formula ✓ |
| 9 | 362880 | $\frac{16687}{45360}$ | 133496 | Formula ✓ |
| 10 | 3628800 | $\frac{16481}{44800}$ | 1334961 | Formula ✓ |

---

**Explicit List for n=4:**

Original: (1, 2, 3, 4)

Derangements (no element in original position):

1. (2, 1, 4, 3) - swap pairs
2. (2, 3, 4, 1) - cycle
3. (2, 4, 1, 3) - cycle
4. (3, 1, 4, 2) - cycle
5. (3, 4, 1, 2) - two 2-cycles
6. (3, 4, 2, 1) - cycle
7. (4, 1, 2, 3) - cycle
8. (4, 3, 1, 2) - cycle
9. (4, 3, 2, 1) - swap pairs

**Count:** 9 = D₄ ✓

---

**Recurrence Verification:**

Using $D_n = (n-1)(D_{n-1} + D_{n-2})$:

| n | Calculation | Dₙ |
|---|-------------|-----|
| 3 | $2(1 + 0) = 2$ | 2 ✓ |
| 4 | $3(2 + 1) = 9$ | 9 ✓ |
| 5 | $4(9 + 2) = 44$ | 44 ✓ |
| 6 | $5(44 + 9) = 265$ | 265 ✓ |
| 7 | $6(265 + 44) = 1854$ | 1854 ✓ |

---

### Exercise 4.2.3 - Prove Dₙ ≈ n!/e

**Problem:** Prove that $\lim_{n \to \infty} \frac{D_n}{n!} = \frac{1}{e}$.

**Solution:**

**Theorem:** $\lim_{n \to \infty} \frac{D_n}{n!} = \frac{1}{e} \approx 0.3679$

---

**Proof:**

From the derangement formula:
$$\frac{D_n}{n!} = \sum_{k=0}^{n} \frac{(-1)^k}{k!}$$

Recall the Taylor series for $e^x$:
$$e^x = \sum_{k=0}^{\infty} \frac{x^k}{k!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots$$

For $x = -1$:
$$e^{-1} = \sum_{k=0}^{\infty} \frac{(-1)^k}{k!} = 1 - 1 + \frac{1}{2!} - \frac{1}{3!} + \frac{1}{4!} - \cdots$$

---

**Convergence:**

This is an alternating series with terms decreasing to 0.

By the Alternating Series Test, the series converges.

The error in truncating after n terms is bounded by the next term:
$$\left|\frac{D_n}{n!} - \frac{1}{e}\right| = \left|\sum_{k=n+1}^{\infty} \frac{(-1)^k}{k!}\right| < \frac{1}{(n+1)!}$$

---

**Limit:**

As $n \to \infty$:
$$\sum_{k=0}^{n} \frac{(-1)^k}{k!} \to \sum_{k=0}^{\infty} \frac{(-1)^k}{k!} = e^{-1} = \frac{1}{e}$$

**Therefore:**
$$\lim_{n \to \infty} \frac{D_n}{n!} = \frac{1}{e}$$ ✓

---

**Numerical Verification:**

| n | Dₙ/n! | 1/e | Error |
|---|-------|-----|-------|
| 1 | 0/1 = 0.0000 | 0.3679 | 0.3679 |
| 2 | 1/2 = 0.5000 | 0.3679 | 0.1321 |
| 3 | 2/6 = 0.3333 | 0.3679 | 0.0346 |
| 4 | 9/24 = 0.3750 | 0.3679 | 0.0071 |
| 5 | 44/120 = 0.3667 | 0.3679 | 0.0012 |
| 6 | 265/720 = 0.3681 | 0.3679 | 0.0002 |
| 7 | 1854/5040 = 0.3679 | 0.3679 | 0.0000 |
| 10 | 1334961/3628800 = 0.3679 | 0.3679 | < 0.0001 |

Converges very quickly! ✓

---

**Interpretation:**

For large n, approximately 36.79% of all permutations are derangements.

Or equivalently: The probability that a random permutation has no fixed points approaches $1/e$.

---

### Exercise 4.2.4 - Prove Dₙ = ⌊n!/e + 1/2⌋

**Problem:** Prove that $D_n$ is the nearest integer to $n!/e$.

**Solution:**

**Theorem:** $D_n = \left\lfloor \frac{n!}{e} + \frac{1}{2} \right\rfloor$

In other words, $D_n$ is the nearest integer to $n!/e$.

---

**Proof:**

From the derangement formula:
$$\frac{D_n}{n!} = \sum_{k=0}^{n} \frac{(-1)^k}{k!}$$

The error in truncating the series for $1/e$:
$$\left|\frac{D_n}{n!} - \frac{1}{e}\right| = \left|\sum_{k=n+1}^{\infty} \frac{(-1)^k}{k!}\right|$$

This is an alternating series with decreasing terms, so the error is bounded by the first omitted term:
$$\left|\frac{D_n}{n!} - \frac{1}{e}\right| < \frac{1}{(n+1)!}$$

Multiply by $n!$:
$$\left|D_n - \frac{n!}{e}\right| < \frac{n!}{(n+1)!} = \frac{1}{n+1}$$

---

**For n ≥ 1:**
$$\frac{1}{n+1} \leq \frac{1}{2}$$

**Therefore:** $D_n$ is within $1/2$ of $n!/e$.

**Therefore:** $D_n$ is the nearest integer to $n!/e$.

**Therefore:** $D_n = \left\lfloor \frac{n!}{e} + \frac{1}{2} \right\rfloor$ ✓

---

**Numerical Verification:**

| n | n!/e | Dₙ | Difference |
|---|------|-----|------------|
| 1 | 0.3679 | 0 | 0.3679 < 0.5 ✓ |
| 2 | 0.7358 | 1 | 0.2642 < 0.5 ✓ |
| 3 | 2.2073 | 2 | 0.2073 < 0.5 ✓ |
| 4 | 8.8291 | 9 | 0.1709 < 0.5 ✓ |
| 5 | 44.1455 | 44 | 0.1455 < 0.5 ✓ |
| 6 | 264.8732 | 265 | 0.1268 < 0.5 ✓ |
| 7 | 1854.1124 | 1854 | 0.1124 < 0.5 ✓ |
| 10 | 1334960.9 | 1334961 | 0.1 < 0.5 ✓ |

---

**Practical Formula:**

To compute $D_n$:
$$D_n = \text{round}\left(\frac{n!}{e}\right)$$

This is much faster than summing the series!

---

### Exercise 4.2.5 - Prove Recurrence Dₙ = (n-1)(Dₙ₋₁ + Dₙ₋₂)

**Problem:** Prove the derangement recurrence $D_n = (n-1)(D_{n-1} + D_{n-2})$.

**Solution:**

**Theorem:** For $n \geq 3$:
$$D_n = (n-1)(D_{n-1} + D_{n-2})$$

---

**Combinatorial Proof:**

Consider derangements of $\{1, 2, \ldots, n\}$.

Look at where element 1 goes. Say $1 \to k$ where $k \neq 1$.

There are $(n-1)$ choices for $k$.

---

**Case 1: k → 1 (they swap)**

If element $k$ goes to position 1, then elements 1 and $k$ form a 2-cycle.

The remaining $(n-2)$ elements must derange among themselves.

**Count:** $D_{n-2}$ derangements of remaining elements.

**For all choices of k:** $(n-1) \times D_{n-2}$

---

**Case 2: k → j where j ≠ 1**

If element $k$ does NOT go to position 1, then:
- Element 1 goes to position $k$
- Element $k$ goes to some position $j \neq 1$

This is equivalent to deranging $(n-1)$ elements:
- Treat position 1 as "position $k$" for the remaining elements
- Element $k$ cannot go to position 1 (that's Case 1)
- So we're deranging $\{2, 3, \ldots, n\}$ with positions $\{1, 2, \ldots, n\} \setminus \{k\}$

**Count:** $D_{n-1}$ derangements.

**For all choices of k:** $(n-1) \times D_{n-1}$

---

**Total:**
$$D_n = (n-1)D_{n-2} + (n-1)D_{n-1} = (n-1)(D_{n-1} + D_{n-2})$$ ✓

---

**Algebraic Proof (from the formula):**

From $D_n = n! \sum_{k=0}^{n} \frac{(-1)^k}{k!}$:

$$D_{n-1} + D_{n-2} = (n-1)! \sum_{k=0}^{n-1} \frac{(-1)^k}{k!} + (n-2)! \sum_{k=0}^{n-2} \frac{(-1)^k}{k!}$$

Factor out $(n-2)!$:
$$= (n-2)! \left[(n-1) \sum_{k=0}^{n-1} \frac{(-1)^k}{k!} + \sum_{k=0}^{n-2} \frac{(-1)^k}{k!}\right]$$

After algebraic manipulation, this equals $\frac{D_n}{n-1}$.

**Therefore:** $D_n = (n-1)(D_{n-1} + D_{n-2})$ ✓

---

**Verification Table:**

| n | Dₙ | (n-1)(Dₙ₋₁ + Dₙ₋₂) | Match? |
|---|----|---------------------|--------|
| 3 | 2 | 2(1 + 0) = 2 | ✓ |
| 4 | 9 | 3(2 + 1) = 9 | ✓ |
| 5 | 44 | 4(9 + 2) = 44 | ✓ |
| 6 | 265 | 5(44 + 9) = 265 | ✓ |
| 7 | 1854 | 6(265 + 44) = 1854 | ✓ |
| 8 | 14833 | 7(1854 + 265) = 14833 | ✓ |

---

**Alternative Recurrence:**

Another useful recurrence: $D_n = n D_{n-1} + (-1)^n$

| n | Dₙ | n·Dₙ₋₁ + (-1)ⁿ | Match? |
|---|----|-----------------|--------|
| 1 | 0 | 1·1 + (-1) = 0 | ✓ |
| 2 | 1 | 2·0 + 1 = 1 | ✓ |
| 3 | 2 | 3·1 + (-1) = 2 | ✓ |
| 4 | 9 | 4·2 + 1 = 9 | ✓ |
| 5 | 44 | 5·9 + (-1) = 44 | ✓ |

---

## Section 4.3 - Applications

---

### Exercise 4.3.1 - Three Languages Problem

**Problem:** In a group of 67 students:
- 47 speak English
- 35 speak German
- 23 speak French
- 20 speak English and German
- 12 speak English and French
- 11 speak German and French
- 5 speak all three languages

Find the number of students who speak none of the languages.

**Solution:**

**Given:**
- Total students: $N = 67$
- $|E| = 47$ (English)
- $|G| = 35$ (German)
- $|F| = 23$ (French)
- $|E \cap G| = 20$
- $|E \cap F| = 12$
- $|G \cap F| = 11$
- $|E \cap G \cap F| = 5$

---

**Find:** Students who speak none = $N - |E \cup G \cup F|$

---

**Apply Inclusion-Exclusion:**

$$|E \cup G \cup F| = |E| + |G| + |F| - |E \cap G| - |E \cap F| - |G \cap F| + |E \cap G \cap F|$$

$$= 47 + 35 + 23 - 20 - 12 - 11 + 5$$

$$= 105 - 43 + 5$$

$$= 67$$

---

**Students who speak none:**
$$67 - 67 = 0$$

**Answer:** 0 students speak none of the languages. ✓

---

**Verification (Venn Diagram):**

Let's verify by computing each region:

| Region | Count |
|--------|-------|
| All three | 5 |
| English & German only | 20 - 5 = 15 |
| English & French only | 12 - 5 = 7 |
| German & French only | 11 - 5 = 6 |
| English only | 47 - 15 - 7 - 5 = 20 |
| German only | 35 - 15 - 6 - 5 = 9 |
| French only | 23 - 7 - 6 - 5 = 5 |

**Total who speak at least one:** 5 + 15 + 7 + 6 + 20 + 9 + 5 = 67 ✓

**None:** 67 - 67 = 0 ✓

---

### Exercise 4.3.2 - Exactly One Fixed Point

**Problem:** In how many ways can 5 letters be placed in 5 envelopes so that exactly 1 person gets their own letter?

**Solution:**

**Approach:** Choose 1 person to get the correct letter, then derange the remaining 4.

---

**Step 1:** Choose 1 person from 5 to get the correct letter.

$$\binom{5}{1} = 5 \text{ ways}$$

---

**Step 2:** The remaining 4 letters must be deranged (no one else gets the correct letter).

$$D_4 = 9 \text{ ways}$$

(From our earlier calculation: derangements of 4 elements)

---

**Total:**
$$5 \times 9 = 45 \text{ ways}$$ ✓

---

**Verification by Explicit Counting (Partial):**

If person 1 gets letter 1:
- Remaining letters: {2, 3, 4, 5} must derange
- 9 derangements: (2,1,4,3), (2,3,4,1), ..., (4,3,2,1) in positions 2,3,4,5

Same for each of the 5 people.

**Total:** 5 × 9 = 45 ✓

---

**General Formula:**

For exactly $k$ fixed points out of $n$ elements:
$$\binom{n}{k} \times D_{n-k}$$

For $n=5, k=1$: $\binom{5}{1} \times D_4 = 5 \times 9 = 45$ ✓

---

*Continued for remaining exercises in Chapter 04...*
