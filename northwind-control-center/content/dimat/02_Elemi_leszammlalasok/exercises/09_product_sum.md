# Exercise 2.1/9 - Product Sum

## Problem Statement

Prove by complete induction:

$$1 \cdot 2 + 2 \cdot 3 + 3 \cdot 4 + \ldots + n(n+1) = \frac{n(n+1)(n+2)}{3}$$

for all $n \in \mathbb{N}$.

---

## Proof by Mathematical Induction

### Step 1: Base Case (n = 1)

**Left side:**
$$1 \cdot 2 = 2$$

**Right side:**
$$\frac{1(1+1)(1+2)}{3} = \frac{1 \cdot 2 \cdot 3}{3} = \frac{6}{3} = 2$$

✓ **Base case verified:** 2 = 2

---

### Step 2: Inductive Hypothesis

Assume the formula holds for some $n = k$:

$$\sum_{i=1}^{k} i(i+1) = \frac{k(k+1)(k+2)}{3}$$

---

### Step 3: Inductive Step (n = k+1)

We need to prove:
$$\sum_{i=1}^{k+1} i(i+1) = \frac{(k+1)(k+2)(k+3)}{3}$$

**Proof:**

Starting with the left side:

$$\begin{aligned}
\sum_{i=1}^{k+1} i(i+1) &= \sum_{i=1}^{k} i(i+1) + (k+1)(k+2) & \text{(split sum)}\\[10pt]
&= \frac{k(k+1)(k+2)}{3} + (k+1)(k+2) & \text{(by hypothesis)}\\[10pt]
&= \frac{k(k+1)(k+2)}{3} + \frac{3(k+1)(k+2)}{3} & \text{(common denominator)}\\[10pt]
&= \frac{k(k+1)(k+2) + 3(k+1)(k+2)}{3} & \text{(combine fractions)}\\[10pt]
&= \frac{(k+1)(k+2)[k + 3]}{3} & \text{(factor out $(k+1)(k+2)$)}\\[10pt]
&= \frac{(k+1)(k+2)(k+3)}{3} & \text{(simplify)}
\end{aligned}$$

✓ **Inductive step complete!**

---

## Conclusion

By the Principle of Mathematical Induction:

$$\boxed{\sum_{i=1}^{n} i(i+1) = \frac{n(n+1)(n+2)}{3} \quad \text{for all } n \in \mathbb{N}}$$

---

## Verification Table

| n | Sum: $\sum_{i=1}^{n} i(i+1)$ | Formula: $\frac{n(n+1)(n+2)}{3}$ |
|---|------------------------------|----------------------------------|
| 1 | 1·2 = 2 | 1·2·3/3 = 2 |
| 2 | 2 + 2·3 = 2 + 6 = 8 | 2·3·4/3 = 8 |
| 3 | 8 + 3·4 = 8 + 12 = 20 | 3·4·5/3 = 20 |
| 4 | 20 + 4·5 = 20 + 20 = 40 | 4·5·6/3 = 40 |
| 5 | 40 + 5·6 = 40 + 30 = 70 | 5·6·7/3 = 70 |
| 6 | 70 + 6·7 = 70 + 42 = 112 | 6·7·8/3 = 112 |
| 7 | 112 + 7·8 = 112 + 56 = 168 | 7·8·9/3 = 168 |
| 8 | 168 + 8·9 = 168 + 72 = 240 | 8·9·10/3 = 240 |

---

## Alternative Proof: Telescoping Sum

### Key Observation:

$$i(i+1) = \frac{(i+1)(i+2)(i+3) - i(i+1)(i+2)}{3}$$

Wait, that's complicated. Let me use a simpler approach.

### Better: Expand and use known formulas

$$\begin{aligned}
\sum_{i=1}^{n} i(i+1) &= \sum_{i=1}^{n} (i^2 + i)\\[10pt]
&= \sum_{i=1}^{n} i^2 + \sum_{i=1}^{n} i\\[10pt]
&= \frac{n(n+1)(2n+1)}{6} + \frac{n(n+1)}{2}\\[10pt]
&= \frac{n(n+1)(2n+1)}{6} + \frac{3n(n+1)}{6}\\[10pt]
&= \frac{n(n+1)(2n+1+3)}{6}\\[10pt]
&= \frac{n(n+1)(2n+4)}{6}\\[10pt]
&= \frac{n(n+1) \cdot 2(n+2)}{6}\\[10pt]
&= \frac{n(n+1)(n+2)}{3}
\end{aligned}$$

✓ Same result!

---

## Another Approach: Combinatorial Identity

Notice that:
$$i(i+1) = 2 \cdot \binom{i+1}{2}$$

So:
$$\begin{aligned}
\sum_{i=1}^{n} i(i+1) &= 2 \sum_{i=1}^{n} \binom{i+1}{2}\\[10pt]
&= 2 \binom{n+2}{3} & \text{(Hockey-stick identity)}\\[10pt]
&= 2 \cdot \frac{(n+2)(n+1)n}{6}\\[10pt]
&= \frac{n(n+1)(n+2)}{3}
\end{aligned}$$

---

## Key Algebraic Steps

The critical steps in the inductive proof:

1. **Separate the last term** from the sum
2. **Apply the inductive hypothesis**
3. **Get common denominator** (3)
4. **Factor out $(k+1)(k+2)$** from the numerator
5. **Simplify** to get the desired form

---

## Pattern: Products of Consecutive Integers

This is part of a general pattern:

| Sum | Result |
|-----|--------|
| $\sum i$ | $\frac{n(n+1)}{2}$ |
| $\sum i(i+1)$ | $\frac{n(n+1)(n+2)}{3}$ |
| $\sum i(i+1)(i+2)$ | $\frac{n(n+1)(n+2)(n+3)}{4}$ |
| $\sum i(i+1)\cdots(i+k-1)$ | $\frac{n(n+1)\cdots(n+k)}{k+1}$ |

---

## General Formula

For any $k \geq 1$:

$$\sum_{i=1}^{n} i(i+1)(i+2)\cdots(i+k-1) = \frac{n(n+1)(n+2)\cdots(n+k)}{k+1}$$

This can be proven by induction on $n$ (with the same technique)!

---

## Connection to Binomial Coefficients

The general formula can be written as:

$$\sum_{i=1}^{n} \binom{i+k-1}{k} = \binom{n+k}{k+1}$$

This is the **Hockey-stick identity** (also called the Christmas stocking theorem)!

---

## Visual Pattern (Hockey-stick)

In Pascal's triangle:
```
    1
   1 1
  1 2 1
 1 3 3 1
1 4 6 4 1
```

The hockey-stick identity says: Sum along a diagonal = the number perpendicular to it at the end.

---

*Exercise 2.1/9 from Chapter 02 - Elemi leszámlálások*
