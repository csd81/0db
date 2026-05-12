# Exercise 5.1 - First-Order Linear Recurrence

## Problem Statement

Solve the first-order linear recurrence:
$$a_n = r a_{n-1} + b$$

with given initial condition $a_1 = A$.

---

## Solution by Iteration

### Step 1: Iterate the recurrence

$$\begin{aligned}
a_n &= r a_{n-1} + b \\
&= r(r a_{n-2} + b) + b = r^2 a_{n-2} + rb + b \\
&= r^2(r a_{n-3} + b) + rb + b = r^3 a_{n-3} + r^2b + rb + b \\
&= \cdots \\
&= r^{n-1} a_1 + b(r^{n-2} + r^{n-3} + \cdots + r + 1)
\end{aligned}$$

### Step 2: Sum the geometric series

**Case 1: $r \neq 1$**

$$\sum_{i=0}^{n-2} r^i = \frac{r^{n-1} - 1}{r - 1}$$

Therefore:
$$a_n = r^{n-1} A + b \cdot \frac{r^{n-1} - 1}{r - 1}$$

**Case 2: $r = 1$**

$$\sum_{i=0}^{n-2} 1 = n-1$$

Therefore:
$$a_n = A + b(n-1)$$

---

## Final Formula

$$\boxed{a_n = \begin{cases}
r^{n-1} A + \dfrac{b(r^{n-1} - 1)}{r - 1} & \text{if } r \neq 1 \\
A + b(n-1) & \text{if } r = 1
\end{cases}}$$

---

## Alternative Form

For $r \neq 1$, we can rewrite:

$$a_n = r^{n-1}\left(A + \frac{b}{r-1}\right) - \frac{b}{r-1}$$

Let $C = A + \frac{b}{r-1}$. Then:

$$a_n = C \cdot r^{n-1} - \frac{b}{r-1}$$

---

## Verification

**For $r = 2, b = 1, A = 1$ (Hanoi towers):**

$$a_n = 2^{n-1} \cdot 1 + \frac{1(2^{n-1} - 1)}{2 - 1} = 2^{n-1} + 2^{n-1} - 1 = 2^n - 1$$ ✓

**For $r = 1, b = d, A = a$ (arithmetic sequence):**

$$a_n = a + d(n-1)$$ ✓

---

## Applications

### 1. Compound Interest with Regular Deposit

- $a_n$ = balance after $n$ periods
- $r = 1 + i$ (interest rate)
- $b$ = regular deposit
- $A$ = initial deposit

### 2. Population with Migration

- $a_n$ = population at time $n$
- $r$ = growth factor
- $b$ = constant migration

---

*Exercise 5.1 from Chapter 05 - Rekurzív sorozatok*
