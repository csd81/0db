# Exercise 2.1/4 - Alternating Square Sum

## Problem Statement

Prove by complete induction:

$$\sum_{k=1}^{n} (-1)^k \cdot k^2 = (-1)^n \cdot \frac{n(n+1)}{2}$$

for all $n \in \mathbb{N}$.

---

## Proof by Mathematical Induction

### Step 1: Base Case (n = 1)

**Left side:**
$$\sum_{k=1}^{1} (-1)^k \cdot k^2 = (-1)^1 \cdot 1^2 = -1 \cdot 1 = -1$$

**Right side:**
$$(-1)^1 \cdot \frac{1(1+1)}{2} = -1 \cdot \frac{2}{2} = -1$$

✓ **Base case verified:** LHS = RHS = -1

---

### Step 2: Inductive Hypothesis

Assume the formula holds for some $n = k$:

$$\sum_{i=1}^{k} (-1)^i \cdot i^2 = (-1)^k \cdot \frac{k(k+1)}{2}$$

---

### Step 3: Inductive Step (n = k+1)

We need to prove:
$$\sum_{i=1}^{k+1} (-1)^i \cdot i^2 = (-1)^{k+1} \cdot \frac{(k+1)(k+2)}{2}$$

**Proof:**

Starting with the left side:

$$\begin{aligned}
\sum_{i=1}^{k+1} (-1)^i \cdot i^2 &= \sum_{i=1}^{k} (-1)^i \cdot i^2 + (-1)^{k+1} \cdot (k+1)^2 & \text{(split sum)}\\[10pt]
&= (-1)^k \cdot \frac{k(k+1)}{2} + (-1)^{k+1} \cdot (k+1)^2 & \text{(by hypothesis)}\\[10pt]
&= (-1)^k \cdot \frac{k(k+1)}{2} + (-1)^{k+1} \cdot (k+1)^2 & \\[10pt]
&= (-1)^k \cdot \frac{k(k+1)}{2} - (-1)^k \cdot (k+1)^2 & \text{(since $(-1)^{k+1} = -(-1)^k$)}\\[10pt]
&= (-1)^k \cdot (k+1) \cdot \left[\frac{k}{2} - (k+1)\right] & \text{(factor out $(-1)^k(k+1)$)}\\[10pt]
&= (-1)^k \cdot (k+1) \cdot \left[\frac{k - 2(k+1)}{2}\right] & \text{(common denominator)}\\[10pt]
&= (-1)^k \cdot (k+1) \cdot \left[\frac{k - 2k - 2}{2}\right] & \text{(expand)}\\[10pt]
&= (-1)^k \cdot (k+1) \cdot \left[\frac{-k - 2}{2}\right] & \text{(simplify)}\\[10pt]
&= (-1)^k \cdot (k+1) \cdot \left[\frac{-(k + 2)}{2}\right] & \text{(factor out -1)}\\[10pt]
&= (-1)^k \cdot (k+1) \cdot (-1) \cdot \frac{k+2}{2} & \\[10pt]
&= (-1)^{k+1} \cdot \frac{(k+1)(k+2)}{2} & \text{(since $(-1)^k \cdot (-1) = (-1)^{k+1}$)}
\end{aligned}$$

✓ **Inductive step complete!**

---

## Conclusion

By the Principle of Mathematical Induction:

$$\boxed{\sum_{k=1}^{n} (-1)^k \cdot k^2 = (-1)^n \cdot \frac{n(n+1)}{2} \quad \text{for all } n \in \mathbb{N}}$$

---

## Verification Table

| n | Sum: $\sum_{k=1}^{n} (-1)^k k^2$ | Formula: $(-1)^n \cdot \frac{n(n+1)}{2}$ |
|---|----------------------------------|-----------------------------------------|
| 1 | -1² = -1 | (-1)¹ · 1·2/2 = -1 |
| 2 | -1 + 4 = 3 | (-1)² · 2·3/2 = 3 |
| 3 | 3 - 9 = -6 | (-1)³ · 3·4/2 = -6 |
| 4 | -6 + 16 = 10 | (-1)⁴ · 4·5/2 = 10 |
| 5 | 10 - 25 = -15 | (-1)⁵ · 5·6/2 = -15 |
| 6 | -15 + 36 = 21 | (-1)⁶ · 6·7/2 = 21 |
| 7 | 21 - 49 = -28 | (-1)⁷ · 7·8/2 = -28 |
| 8 | -28 + 64 = 36 | (-1)⁸ · 8·9/2 = 36 |

---

## Pattern Observation

The results follow a clear pattern:

| n | Result | Triangular number |
|---|--------|-------------------|
| 1 | -1 | -T₁ |
| 2 | 3 | T₂ |
| 3 | -6 | -T₃ |
| 4 | 10 | T₄ |
| 5 | -15 | -T₅ |
| 6 | 21 | T₆ |

The sum equals **$(-1)^n \cdot T_n$** where $T_n = \frac{n(n+1)}{2}$ is the $n$-th triangular number!

---

## Key Algebraic Steps

The critical steps in this proof:

1. **Use $(-1)^{k+1} = -(-1)^k$** to factor out $(-1)^k$
2. **Factor out $(k+1)$** from both terms
3. **Simplify the bracket**: $\frac{k}{2} - (k+1) = \frac{-k-2}{2}$
4. **Recognize**: $(-1)^k \cdot (-1) = (-1)^{k+1}$

---

## Alternative Approach: Pairing Terms

For even $n = 2m$, we can pair consecutive terms:

$$\begin{aligned}
\sum_{k=1}^{2m} (-1)^k k^2 &= (-1^2 + 2^2) + (-3^2 + 4^2) + ... + (-(2m-1)^2 + (2m)^2)\\[5pt]
&= (4-1) + (16-9) + ... + ((2m)^2 - (2m-1)^2)\\[5pt]
&= 3 + 7 + 11 + ... + (4m-1)\\[5pt]
&= \sum_{j=1}^{m} (4j-1)\\[5pt]
&= 4 \cdot \frac{m(m+1)}{2} - m\\[5pt]
&= 2m(m+1) - m\\[5pt]
&= 2m^2 + m\\[5pt]
&= \frac{2m(2m+1)}{2} = T_{2m}
\end{aligned}$$

This confirms the formula for even $n$. A similar approach works for odd $n$.

---

## Related Identities

| Alternating Sum | Result |
|-----------------|--------|
| $\sum (-1)^k k$ | $(-1)^n \cdot \lceil n/2 \rceil$ |
| $\sum (-1)^k k^2$ | $(-1)^n \cdot \frac{n(n+1)}{2}$ |
| $\sum (-1)^k k^3$ | $(-1)^n \cdot \left[\frac{n(n+1)}{2}\right]^2$ |

---

*Exercise 2.1/4 from Chapter 02 - Elemi leszámlálások*
