# Exercise 3.2 - Binomial Coefficient Identities

## Problem Statement

Prove the following identities for binomial coefficients ($m, n, r \in \mathbb{N}$):

---

## /1/ Prove: $n\binom{n}{1} + 6\binom{n}{2} + 6\binom{n}{3} = n^3$

### Proof

Let me expand each term:

$$\begin{aligned}
n\binom{n}{1} &= n \cdot n = n^2\\[10pt]
6\binom{n}{2} &= 6 \cdot \frac{n(n-1)}{2} = 3n(n-1) = 3n^2 - 3n\\[10pt]
6\binom{n}{3} &= 6 \cdot \frac{n(n-1)(n-2)}{6} = n(n-1)(n-2) = n^3 - 3n^2 + 2n
\end{aligned}$$

**Sum:**
$$\begin{aligned}
\text{LHS} &= n^2 + (3n^2 - 3n) + (n^3 - 3n^2 + 2n)\\[10pt]
&= n^3 + (n^2 + 3n^2 - 3n^2) + (-3n + 2n)\\[10pt]
&= n^3 + n^2 - n
\end{aligned}$$

Hmm, this doesn't equal $n^3$. Let me check the problem statement again.

Actually, looking at the pattern, this identity should express $n^3$ in terms of binomial coefficients. Let me verify with small values:

**For n = 1:**
- LHS: $1\binom{1}{1} + 6\binom{1}{2} + 6\binom{1}{3} = 1 + 0 + 0 = 1$
- RHS: $1^3 = 1$ ✓

**For n = 2:**
- LHS: $2\binom{2}{1} + 6\binom{2}{2} + 6\binom{2}{3} = 2 \cdot 2 + 6 \cdot 1 + 0 = 4 + 6 = 10$
- RHS: $2^3 = 8$ ✗

There seems to be an issue with the problem statement. Let me derive the correct formula.

### Correct Formula

Using Stirling numbers of the second kind, we know:

$$n^3 = \binom{n}{1} + 6\binom{n}{2} + 6\binom{n}{3}$$

Let me verify:
$$\begin{aligned}
\binom{n}{1} + 6\binom{n}{2} + 6\binom{n}{3} &= n + 6 \cdot \frac{n(n-1)}{2} + 6 \cdot \frac{n(n-1)(n-2)}{6}\\[10pt]
&= n + 3n(n-1) + n(n-1)(n-2)\\[10pt]
&= n + 3n^2 - 3n + n^3 - 3n^2 + 2n\\[10pt]
&= n^3 + (3n^2 - 3n^2) + (n - 3n + 2n)\\[10pt]
&= n^3 ✓
\end{aligned}$$

**The correct identity is:**
$$\boxed{\binom{n}{1} + 6\binom{n}{2} + 6\binom{n}{3} = n^3}$$

---

## /2/ Prove: $(n+1)\binom{n}{1} + 12\binom{n}{2} + 6\binom{n}{3} = (n+1)^3$

### Analysis

Let me check if this is correct by expanding:

$$\begin{aligned}
(n+1)\binom{n}{1} &= (n+1) \cdot n = n^2 + n\\[10pt]
12\binom{n}{2} &= 12 \cdot \frac{n(n-1)}{2} = 6n(n-1) = 6n^2 - 6n\\[10pt]
6\binom{n}{3} &= n(n-1)(n-2) = n^3 - 3n^2 + 2n
\end{aligned}$$

**Sum:**
$$\begin{aligned}
\text{LHS} &= (n^2 + n) + (6n^2 - 6n) + (n^3 - 3n^2 + 2n)\\[10pt]
&= n^3 + (n^2 + 6n^2 - 3n^2) + (n - 6n + 2n)\\[10pt]
&= n^3 + 4n^2 - 3n
\end{aligned}$$

But $(n+1)^3 = n^3 + 3n^2 + 3n + 1$. These don't match.

Let me find the correct formula for $(n+1)^3$.

### Correct Formula

Since $(n+1)^3 = n^3 + 3n^2 + 3n + 1$, and we know $n^3 = \binom{n}{1} + 6\binom{n}{2} + 6\binom{n}{3}$:

$$(n+1)^3 = \binom{n}{0} + 7\binom{n}{1} + 12\binom{n}{2} + 6\binom{n}{3}$$

Let me verify:
$$\begin{aligned}
&\binom{n}{0} + 7\binom{n}{1} + 12\binom{n}{2} + 6\binom{n}{3}\\[10pt]
&= 1 + 7n + 6n(n-1) + n(n-1)(n-2)\\[10pt]
&= 1 + 7n + 6n^2 - 6n + n^3 - 3n^2 + 2n\\[10pt]
&= n^3 + 3n^2 + 3n + 1\\[10pt]
&= (n+1)^3 ✓
\end{aligned}$$

---

## /3/ & /4/ Fourth Power Identities

### Standard Formula

For $n^4$, the correct identity is:

$$\boxed{n^4 = \binom{n}{1} + 14\binom{n}{2} + 36\binom{n}{3} + 24\binom{n}{4}}$$

**Proof:**

Using Stirling numbers of the second kind: $S(4,1) = 1$, $S(4,2) = 7$, $S(4,3) = 6$, $S(4,4) = 1$.

But we need to account for the factorial factors:
$$n^4 = \sum_{k=1}^{4} k! \cdot S(4,k) \binom{n}{k}$$

So:
$$n^4 = 1!\cdot 1 \binom{n}{1} + 2!\cdot 7 \binom{n}{2} + 3!\cdot 6 \binom{n}{3} + 4!\cdot 1 \binom{n}{4}$$
$$n^4 = \binom{n}{1} + 14\binom{n}{2} + 36\binom{n}{3} + 24\binom{n}{4}$$

**Verification:**
$$\begin{aligned}
&\binom{n}{1} + 14\binom{n}{2} + 36\binom{n}{3} + 24\binom{n}{4}\\[10pt]
&= n + 14\frac{n(n-1)}{2} + 36\frac{n(n-1)(n-2)}{6} + 24\frac{n(n-1)(n-2)(n-3)}{24}\\[10pt]
&= n + 7n(n-1) + 6n(n-1)(n-2) + n(n-1)(n-2)(n-3)\\[10pt]
&= n + 7n^2 - 7n + 6n^3 - 18n^2 + 12n + n^4 - 6n^3 + 11n^2 - 6n\\[10pt]
&= n^4 + (7n^2 - 18n^2 + 11n^2) + (n - 7n + 12n - 6n)\\[10pt]
&= n^4 ✓
\end{aligned}$$

---

## General Pattern

The exercises reveal a general pattern for expressing powers in terms of binomial coefficients:

$$\boxed{n^k = \sum_{j=1}^{k} j! \cdot S(k,j) \binom{n}{j}}$$

where $S(k,j)$ are the **Stirling numbers of the second kind**.

### Table of Identities

| Power | Identity |
|-------|----------|
| $n^1$ | $\binom{n}{1}$ |
| $n^2$ | $\binom{n}{1} + 2\binom{n}{2}$ |
| $n^3$ | $\binom{n}{1} + 6\binom{n}{2} + 6\binom{n}{3}$ |
| $n^4$ | $\binom{n}{1} + 14\binom{n}{2} + 36\binom{n}{3} + 24\binom{n}{4}$ |

---

## Key Insight

These identities are useful for:
1. **Summing powers** using binomial coefficient sum formulas
2. **Converting between polynomial bases** (standard vs. binomial basis)
3. **Combinatorial proofs** of polynomial identities

The coefficients $j! \cdot S(k,j)$ count the number of ways to partition a set of $k$ elements into exactly $j$ non-empty subsets, then arrange those subsets.

---

*Exercise 3.2/1-4 from Chapter 03 - Binomiális és polinomiális együtthatók*
