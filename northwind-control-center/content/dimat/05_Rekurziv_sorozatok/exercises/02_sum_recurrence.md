# Exercise 5.2 - Sum Recurrence

## Problem Statement

Solve the recurrence:
$$a_n = \sum_{i=0}^{n-1} a_i, \quad a_0 = 1$$

---

## Solution

### Step 1: Compute first few terms

$$\begin{aligned}
a_0 &= 1 \\
a_1 &= a_0 = 1 \\
a_2 &= a_0 + a_1 = 1 + 1 = 2 \\
a_3 &= a_0 + a_1 + a_2 = 1 + 1 + 2 = 4 \\
a_4 &= a_0 + a_1 + a_2 + a_3 = 1 + 1 + 2 + 4 = 8
\end{aligned}$$

**Pattern:** $a_n = 2^{n-1}$ for $n \geq 1$

---

### Step 2: Derive a simpler recurrence

Write the recurrence for $n$ and $n-1$:

$$\begin{aligned}
a_n &= \sum_{i=0}^{n-1} a_i = a_0 + a_1 + \cdots + a_{n-1} \\
a_{n-1} &= \sum_{i=0}^{n-2} a_i = a_0 + a_1 + \cdots + a_{n-2}
\end{aligned}$$

Subtract:
$$a_n - a_{n-1} = a_{n-1}$$

Therefore:
$$\boxed{a_n = 2a_{n-1} \quad \text{for } n \geq 2}$$

---

### Step 3: Solve the simplified recurrence

This is a geometric sequence with ratio 2:

$$a_n = a_1 \cdot 2^{n-1} = 1 \cdot 2^{n-1} = 2^{n-1}$$

---

## Final Formula

$$\boxed{a_n = \begin{cases}
1 & \text{if } n = 0 \\
2^{n-1} & \text{if } n \geq 1
\end{cases}}$$

---

## Verification

| n | Formula | Sum | Check |
|---|---------|-----|-------|
| 0 | 1 | - | ✓ |
| 1 | $2^0 = 1$ | $a_0 = 1$ | ✓ |
| 2 | $2^1 = 2$ | $1 + 1 = 2$ | ✓ |
| 3 | $2^2 = 4$ | $1 + 1 + 2 = 4$ | ✓ |
| 4 | $2^3 = 8$ | $1 + 1 + 2 + 4 = 8$ | ✓ |
| 5 | $2^4 = 16$ | $1 + 1 + 2 + 4 + 8 = 16$ | ✓ |

---

## Generalization

For $a_n = c + \sum_{i=0}^{n-1} a_i$ with $a_0 = A$:

$$a_n - a_{n-1} = a_{n-1} \Rightarrow a_n = 2a_{n-1}$$

Same solution pattern!

---

## Application: Subset Counting

**Problem:** Count subsets of $\{1, 2, \ldots, n\}$ by their maximum element.

- $a_n$ = subsets with maximum element $n$
- Any such subset is formed by taking $n$ plus any subset of $\{1, \ldots, n-1\}$
- Therefore: $a_n = \sum_{i=0}^{n-1} a_i$ where $a_0 = 1$ (empty set)

**Result:** $2^{n-1}$ subsets have maximum element $n$ (for $n \geq 1$).

---

*Exercise 5.2 from Chapter 05 - Rekurzív sorozatok*
