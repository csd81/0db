# Exercise 2.1/1 - Sum of Cubes

## Problem Statement

Prove by complete induction:

$$1^3 + 2^3 + 3^3 + ... + n^3 = \left[\frac{n(n+1)}{2}\right]^2$$

for all $n \in \mathbb{N}$.

---

## Proof by Mathematical Induction

### Step 1: Base Case (n = 1)

**Left side:** $1^3 = 1$

**Right side:** $\left[\frac{1(1+1)}{2}\right]^2 = \left[\frac{1 \cdot 2}{2}\right]^2 = 1^2 = 1$

✓ **Base case verified:** LHS = RHS = 1

---

### Step 2: Inductive Hypothesis

Assume the formula holds for some $n = k$:

$$1^3 + 2^3 + ... + k^3 = \left[\frac{k(k+1)}{2}\right]^2$$

---

### Step 3: Inductive Step (n = k+1)

We need to prove:

$$1^3 + 2^3 + ... + k^3 + (k+1)^3 = \left[\frac{(k+1)(k+2)}{2}\right]^2$$

**Proof:**

Starting with the left side:

$$\begin{aligned}
1^3 + 2^3 + ... + k^3 + (k+1)^3 &= \left[\frac{k(k+1)}{2}\right]^2 + (k+1)^3 & \text{(by hypothesis)}\\[10pt]
&= \frac{k^2(k+1)^2}{4} + (k+1)^3 & \text{(expand square)}\\[10pt]
&= \frac{k^2(k+1)^2}{4} + \frac{4(k+1)^3}{4} & \text{(common denominator)}\\[10pt]
&= \frac{k^2(k+1)^2 + 4(k+1)^3}{4} & \text{(combine fractions)}\\[10pt]
&= \frac{(k+1)^2[k^2 + 4(k+1)]}{4} & \text{(factor out $(k+1)^2$)}\\[10pt]
&= \frac{(k+1)^2[k^2 + 4k + 4]}{4} & \text{(expand)}\\[10pt]
&= \frac{(k+1)^2(k+2)^2}{4} & \text{(factor: $k^2+4k+4 = (k+2)^2$)}\\[10pt]
&= \left[\frac{(k+1)(k+2)}{2}\right]^2 & \text{(rewrite as square)}
\end{aligned}$$

✓ **Inductive step complete!**

---

## Conclusion

By the Principle of Mathematical Induction, the formula:

$$\boxed{\sum_{i=1}^{n} i^3 = \left[\frac{n(n+1)}{2}\right]^2}$$

holds for all $n \in \mathbb{N}$.

---

## Geometric Interpretation

Interestingly, the sum of the first $n$ cubes equals the **square of the sum of the first $n$ natural numbers**:

$$1^3 + 2^3 + ... + n^3 = (1 + 2 + ... + n)^2$$

This can be visualized geometrically by arranging cubes into a square pattern!

---

## Verification Table

| n | Sum of cubes | Formula result |
|---|--------------|----------------|
| 1 | 1³ = 1 | [1·2/2]² = 1 |
| 2 | 1³ + 2³ = 1 + 8 = 9 | [2·3/2]² = 3² = 9 |
| 3 | 1 + 8 + 27 = 36 | [3·4/2]² = 6² = 36 |
| 4 | 1 + 8 + 27 + 64 = 100 | [4·5/2]² = 10² = 100 |
| 5 | 1 + 8 + 27 + 64 + 125 = 225 | [5·6/2]² = 15² = 225 |

---

## Key Algebraic Steps

The critical insight in this proof is:

1. **Factor out $(k+1)^2$** from the numerator
2. **Recognize the perfect square**: $k^2 + 4k + 4 = (k+2)^2$
3. **Rewrite as a single squared fraction**

---

## Related Formulas

| Sum | Formula |
|-----|---------|
| $\sum i$ | $\frac{n(n+1)}{2}$ |
| $\sum i^2$ | $\frac{n(n+1)(2n+1)}{6}$ |
| $\sum i^3$ | $\left[\frac{n(n+1)}{2}\right]^2$ |
| $\sum i^4$ | $\frac{n(n+1)(2n+1)(3n^2+3n-1)}{30}$ |

---

*Exercise 2.1/1 from Chapter 02 - Elemi leszámlálások*
