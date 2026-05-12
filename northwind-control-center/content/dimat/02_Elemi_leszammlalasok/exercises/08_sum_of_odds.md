# Exercise 2.1/8 - Sum of First n Odd Numbers

## Problem Statement

Prove by complete induction:

The sum of the first $n$ odd natural numbers is exactly $n^2$.

$$1 + 3 + 5 + \ldots + (2n-1) = n^2$$

for all $n \in \mathbb{N}$.

---

## Proof by Mathematical Induction

### Step 1: Base Case (n = 1)

**Left side:** First odd number = 1

**Right side:** $1^2 = 1$

✓ **Base case verified:** 1 = 1

---

### Step 2: Inductive Hypothesis

Assume the formula holds for some $n = k$:

$$1 + 3 + 5 + \ldots + (2k-1) = k^2$$

---

### Step 3: Inductive Step (n = k+1)

We need to prove:
$$1 + 3 + 5 + \ldots + (2k-1) + (2(k+1)-1) = (k+1)^2$$

**Proof:**

Starting with the left side:

$$\begin{aligned}
1 + 3 + 5 + \ldots + (2k-1) + (2(k+1)-1) &= [1 + 3 + 5 + \ldots + (2k-1)] + (2k+1)\\[10pt]
&= k^2 + (2k+1) & \text{(by hypothesis)}\\[10pt]
&= k^2 + 2k + 1\\[10pt]
&= (k+1)^2 & \text{(perfect square formula)}
\end{aligned}$$

✓ **Inductive step complete!**

---

## Conclusion

By the Principle of Mathematical Induction:

$$\boxed{\sum_{i=1}^{n} (2i-1) = n^2 \quad \text{for all } n \in \mathbb{N}}$$

---

## Verification Table

| n | First n odd numbers | Sum | n² |
|---|---------------------|-----|-----|
| 1 | 1 | 1 | 1 |
| 2 | 1, 3 | 4 | 4 |
| 3 | 1, 3, 5 | 9 | 9 |
| 4 | 1, 3, 5, 7 | 16 | 16 |
| 5 | 1, 3, 5, 7, 9 | 25 | 25 |
| 6 | 1, 3, 5, 7, 9, 11 | 36 | 36 |
| 7 | 1, 3, 5, 7, 9, 11, 13 | 49 | 49 |
| 8 | 1, 3, 5, 7, 9, 11, 13, 15 | 64 | 64 |
| 9 | 1, 3, 5, 7, 9, 11, 13, 15, 17 | 81 | 81 |
| 10 | 1, 3, 5, 7, 9, 11, 13, 15, 17, 19 | 100 | 100 |

---

## Geometric Proof (Visual)

This identity has a beautiful **geometric interpretation**:

```
n = 1:    n = 2:    n = 3:    n = 4:
┌─┐       ┌───┐     ┌─────┐   ┌───────┐
│●│       │●●●│     │●●●●●│   │●●●●●●●│
└─┘       │●●○│     │●●○○○│   │●●○○○○○│
  1=1²    └───┘     │●○○○○│   │●○○○○○○│
          4=2²      └─────┘   │●○○○○○○│
                    9=3²      └───────┘
                              16=4²
```

Each odd number adds an **L-shaped layer** (gnomon) to form a larger square!

- 1 = first square (1×1)
- 1+3 = add 3 blocks around = 2×2 square
- 1+3+5 = add 5 blocks around = 3×3 square
- And so on...

---

## Alternative Proof: Arithmetic Series

The odd numbers form an **arithmetic sequence**:
- First term: $a_1 = 1$
- Common difference: $d = 2$
- $n$-th term: $a_n = 2n-1$

**Sum of arithmetic sequence:**
$$S_n = \frac{n}{2}(a_1 + a_n) = \frac{n}{2}(1 + (2n-1)) = \frac{n}{2}(2n) = n^2$$

---

## Key Insights

1. The $n$-th odd number is $2n-1$
2. Adding consecutive odd numbers creates **perfect squares**
3. This is one of the oldest known mathematical identities (Pythagoreans knew it!)

---

## Historical Note

This theorem was known to the **ancient Greeks**, particularly the **Pythagoreans** (6th century BCE).

They observed that:
- Square numbers can be represented as actual squares of dots
- Each new square is formed by adding an L-shaped border (gnomon)
- The gnomon always has an odd number of dots

This is sometimes called the **Gnomon Theorem**.

---

## Related Identities

| Sum | Formula |
|-----|---------|
| $\sum_{i=1}^{n} (2i-1)$ | $n^2$ |
| $\sum_{i=1}^{n} (2i)$ | $n(n+1)$ |
| $\sum_{i=1}^{n} i$ | $\frac{n(n+1)}{2}$ |
| $\sum_{i=1}^{n} i^2$ | $\frac{n(n+1)(2n+1)}{6}$ |
| $\sum_{i=1}^{n} i^3$ | $\left[\frac{n(n+1)}{2}\right]^2$ |

---

## Application: Perfect Square Test

A number $N$ is a perfect square if and only if it can be written as a sum of consecutive odd numbers starting from 1.

**Example:** Is 144 a perfect square?
$$1 + 3 + 5 + 7 + 9 + 11 + 13 + 15 + 17 + 19 + 21 + 23 = 144$$
Yes! It's $12^2$.

---

*Exercise 2.1/8 from Chapter 02 - Elemi leszámlálások*
