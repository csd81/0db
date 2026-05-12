# Exercise 2.1/7 - Equal Sum Partition

## Problem Statement

Prove by complete induction:

The numbers $1, 2, \ldots, 2n$ can be partitioned into two disjoint groups $A$ and $B$ of equal size such that the sum of numbers in each group is equal.

---

## Proof by Mathematical Induction

### Step 1: Base Case (n = 1)

We have numbers $\{1, 2\}$.

**Partition:**
- $A = \{1\}$
- $B = \{2\}$

Wait - this doesn't work! Sum of A = 1, Sum of B = 2.

Let me reconsider. For $n = 1$, we have $2n = 2$ numbers, and we need groups of size $n = 1$ each.

**Total sum:** $1 + 2 = 3$

Since 3 is odd, we **cannot** split it into two equal integer sums!

---

### Correction: The problem likely starts at n = 2

Let me check $n = 2$:

Numbers: $\{1, 2, 3, 4\}$

**Total sum:** $1 + 2 + 3 + 4 = 10$

We need two groups of size 2, each summing to $10/2 = 5$.

**Valid partition:**
- $A = \{1, 4\}$ → sum = 5
- $B = \{2, 3\}$ → sum = 5

✓ **Base case n = 2 verified!**

---

### Step 2: Inductive Hypothesis

Assume that for some $k \geq 2$, the numbers $1, 2, \ldots, 2k$ can be partitioned into two groups $A_k$ and $B_k$ such that:
- $|A_k| = |B_k| = k$
- $\sum_{a \in A_k} a = \sum_{b \in B_k} b$

---

### Step 3: Inductive Step (n = k+1)

We need to partition $\{1, 2, \ldots, 2k, 2k+1, 2k+2\}$ into two equal-sum groups of size $k+1$.

**Total sum for $2(k+1)$ numbers:**
$$S_{k+1} = \sum_{i=1}^{2k+2} i = \frac{(2k+2)(2k+3)}{2} = (k+1)(2k+3)$$

Each group should sum to:
$$\frac{S_{k+1}}{2} = \frac{(k+1)(2k+3)}{2}$$

---

### Construction Method

**Strategy:** Start with the partition for $2k$ numbers and add the two new numbers strategically.

From the inductive hypothesis, we have:
- $A_k$ with sum $S_k/2$
- $B_k$ with sum $S_k/2$

where $S_k = \frac{2k(2k+1)}{2} = k(2k+1)$.

**New numbers to place:** $2k+1$ and $2k+2$

**Key observation:** 
$$(2k+2) - (2k+1) = 1$$

So we need to balance this difference of 1 by moving one element between groups.

---

### Explicit Construction

**New partition:**
- $A_{k+1} = A_k \cup \{2k+2\} \setminus \{x\}$ for some $x \in A_k$
- $B_{k+1} = B_k \cup \{2k+1\} \cup \{x\}$

We need:
$$\text{sum}(A_{k+1}) = \text{sum}(B_{k+1})$$

$$\frac{S_k}{2} + (2k+2) - x = \frac{S_k}{2} + (2k+1) + x$$

Simplifying:
$$2k+2 - x = 2k+1 + x$$
$$1 = 2x$$
$$x = \frac{1}{2}$$

This is not an integer! So this direct approach doesn't work.

---

### Alternative Construction

Let me try a different approach - **pairing strategy**.

**Pair the numbers:**
$$(1, 2k+2), (2, 2k+1), (3, 2k), \ldots, (k+1, k+2)$$

Each pair sums to $2k+3$.

There are $k+1$ pairs, total sum = $(k+1)(2k+3)$ ✓

**Assignment:**
- Put the **smaller** element of pairs $1, 3, 5, \ldots$ (odd-indexed) in $A$
- Put the **larger** element of pairs $1, 3, 5, \ldots$ in $B$
- Put the **larger** element of pairs $2, 4, 6, \ldots$ (even-indexed) in $A$
- Put the **smaller** element of pairs $2, 4, 6, \ldots$ in $B$

This ensures each group gets $k+1$ elements.

---

### Simpler Explicit Construction

**For any $n \geq 2$:**

**Group A:** $\{1, 2, \ldots, n-1, 2n\}$
- Size: $(n-1) + 1 = n$ ✓
- Sum: $\frac{(n-1)n}{2} + 2n = \frac{n^2 - n + 4n}{2} = \frac{n^2 + 3n}{2}$

**Group B:** $\{n, n+1, \ldots, 2n-1\}$
- Size: $(2n-1) - n + 1 = n$ ✓
- Sum: $\frac{(n + 2n-1) \cdot n}{2} = \frac{(3n-1)n}{2} = \frac{3n^2 - n}{2}$

Hmm, these don't match. Let me recalculate.

---

### Correct Explicit Construction

**For $n$ even:** $n = 2m$

**Group A:** $\{1, 2, \ldots, m, 3m+1, 3m+2, \ldots, 4m\}$
**Group B:** $\{m+1, m+2, \ldots, 3m\}$

**For $n$ odd:** $n = 2m+1$

**Group A:** $\{1, 2, \ldots, m, 2m+2, 2m+3, \ldots, 4m+2\}$
**Group B:** $\{m+1, m+2, \ldots, 2m+1\} \cup \{4m+3, \ldots\}$

This is getting complicated. Let me use a cleaner inductive construction.

---

### Clean Inductive Proof

**Base case (n = 2):**
- $A = \{1, 4\}$, sum = 5
- $B = \{2, 3\}$, sum = 5

**Inductive step:**

Given a valid partition for $2k$ numbers, construct for $2(k+1)$ numbers:

**New numbers:** $2k+1, 2k+2, 2k+3, 2k+4$

**Add to groups:**
- $A_{k+1} = A_k \cup \{2k+1, 2k+4\}$
- $B_{k+1} = B_k \cup \{2k+2, 2k+3\}$

**Check sums:**
- New sum for $A$: $\frac{S_k}{2} + (2k+1) + (2k+4) = \frac{S_k}{2} + 4k + 5$
- New sum for $B$: $\frac{S_k}{2} + (2k+2) + (2k+3) = \frac{S_k}{2} + 4k + 5$

✓ **Equal!**

**Check sizes:**
- $|A_{k+1}| = k + 2 = k+1$ ✗

Wait, that gives $k+2$ elements, not $k+1$.

---

### Final Correct Construction

**Base case (n = 2):** $A = \{1, 4\}$, $B = \{2, 3\}$

**Inductive step from $n$ to $n+2$** (skip by 2):

Add four new numbers: $2n+1, 2n+2, 2n+3, 2n+4$

- $A_{n+2} = A_n \cup \{2n+1, 2n+4\}$
- $B_{n+2} = B_n \cup \{2n+2, 2n+3\}$

Each group gains 2 elements and the same sum $(4n+5)$.

**For odd $n$:** Use $n = 3$ as base:
- $A = \{1, 2, 6\}$, sum = 9
- $B = \{3, 4, 5\}$, sum = 12 ✗

Let me find $n = 3$:
- Total = $1+2+3+4+5+6 = 21$ (odd, impossible!)

---

## Important Realization

**The sum $1 + 2 + \ldots + 2n = \frac{2n(2n+1)}{2} = n(2n+1)$**

For equal partition, this must be **even**.

- If $n$ is **even**: $n(2n+1)$ is even ✓
- If $n$ is **odd**: $n(2n+1)$ is odd ✗

**The problem only works for EVEN $n$!**

---

## Corrected Statement & Proof

**Theorem:** For **even** $n$, the numbers $1, 2, \ldots, 2n$ can be partitioned into two equal-sum groups of size $n$.

**Proof by induction on $m$ where $n = 2m$:**

**Base case (m = 1, n = 2):**
- $A = \{1, 4\}$, $B = \{2, 3\}$
- Both sum to 5 ✓

**Inductive step:** Assume valid for $n = 2m$.

For $n' = 2(m+1) = 2m+2$:

Start with partition for $2m$, add:
- $A' = A \cup \{4m+1, 4m+4\}$
- $B' = B \cup \{4m+2, 4m+3\}$

Both groups gain equal sum $8m+5$. ✓

---

## Conclusion

$$\boxed{\text{The partition exists for all EVEN } n \geq 2}$$

For odd $n$, the total sum is odd, making equal partition **impossible**.

---

*Exercise 2.1/7 from Chapter 02 - Elemi leszámlálások*
