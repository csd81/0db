# Exercise 2.1/10 - Harmonic Numbers Inequality

## Problem Statement

Prove by complete induction:

$$H_{2^n} \geq 1 + \frac{n}{2}$$

for all $n \in \mathbb{N}$, where $H_k = \sum_{i=1}^{k} \frac{1}{i}$ is the $k$-th harmonic number.

---

## Proof by Mathematical Induction

### Step 1: Base Case (n = 0)

**Left side:**
$$H_{2^0} = H_1 = 1$$

**Right side:**
$$1 + \frac{0}{2} = 1$$

✓ **Base case verified:** 1 ≥ 1

---

### Step 2: Base Case (n = 1)

**Left side:**
$$H_{2^1} = H_2 = 1 + \frac{1}{2} = 1.5$$

**Right side:**
$$1 + \frac{1}{2} = 1.5$$

✓ **Verified:** 1.5 ≥ 1.5

---

### Step 3: Inductive Hypothesis

Assume the inequality holds for some $n = k$:

$$H_{2^k} \geq 1 + \frac{k}{2}$$

---

### Step 4: Inductive Step (n = k+1)

We need to prove:
$$H_{2^{k+1}} \geq 1 + \frac{k+1}{2}$$

**Proof:**

First, let's express $H_{2^{k+1}}$ in terms of $H_{2^k}$:

$$H_{2^{k+1}} = H_{2^k} + \sum_{i=2^k + 1}^{2^{k+1}} \frac{1}{i}$$

The sum has $2^{k+1} - 2^k = 2^k$ terms.

Each term satisfies: $\frac{1}{i} \geq \frac{1}{2^{k+1}}$ for $i \in [2^k+1, 2^{k+1}]$

Therefore:
$$\sum_{i=2^k + 1}^{2^{k+1}} \frac{1}{i} \geq \sum_{i=2^k + 1}^{2^{k+1}} \frac{1}{2^{k+1}} = 2^k \cdot \frac{1}{2^{k+1}} = \frac{1}{2}$$

Now we can bound $H_{2^{k+1}}$:

$$\begin{aligned}
H_{2^{k+1}} &= H_{2^k} + \sum_{i=2^k + 1}^{2^{k+1}} \frac{1}{i}\\[10pt]
&\geq H_{2^k} + \frac{1}{2}\\[10pt]
&\geq \left(1 + \frac{k}{2}\right) + \frac{1}{2} & \text{(by inductive hypothesis)}\\[10pt]
&= 1 + \frac{k+1}{2}
\end{aligned}$$

✓ **Inductive step complete!**

---

## Conclusion

By the Principle of Mathematical Induction:

$$\boxed{H_{2^n} \geq 1 + \frac{n}{2} \quad \text{for all } n \in \mathbb{N}}$$

---

## Verification Table

| n | $2^n$ | $H_{2^n}$ (exact) | $H_{2^n}$ (approx) | $1 + n/2$ | Inequality |
|---|-------|-------------------|-------------------|-----------|------------|
| 0 | 1 | 1 | 1.000 | 1 | ✓ |
| 1 | 2 | 1 + 1/2 | 1.500 | 1.5 | ✓ |
| 2 | 4 | 1 + 1/2 + 1/3 + 1/4 | 2.083 | 2 | ✓ |
| 3 | 8 | H₈ | 2.718 | 2.5 | ✓ |
| 4 | 16 | H₁₆ | 3.381 | 3 | ✓ |
| 5 | 32 | H₃₂ | 4.059 | 3.5 | ✓ |
| 6 | 64 | H₆₄ | 4.744 | 4 | ✓ |
| 7 | 128 | H₁₂₈ | 5.434 | 4.5 | ✓ |
| 8 | 256 | H₂₅₆ | 6.127 | 5 | ✓ |
| 9 | 512 | H₅₁₂ | 6.822 | 5.5 | ✓ |
| 10 | 1024 | H₁₀₂₄ | 7.518 | 6 | ✓ |

---

## Comparison with Exercise 2.1/2

**Exercise 2.1/2:** $H_{2^n} \geq \frac{n}{2}$ (for $n \geq 2$)

**Exercise 2.1/10:** $H_{2^n} \geq 1 + \frac{n}{2}$ (for all $n \geq 0$)

The bound in 2.1/10 is **stronger** by exactly 1!

Both use the same key insight: each doubling adds at least 1/2 to the harmonic sum.

---

## Key Insight

The proof shows:
$$H_{2^{k+1}} - H_{2^k} \geq \frac{1}{2}$$

This is because we add $2^k$ terms, each at least $\frac{1}{2^{k+1}}$.

**Geometric interpretation:**
```
H₁ = 1
H₂ = H₁ + 1/2     (add 1 term ≥ 1/2)
H₄ = H₂ + 1/2     (add 2 terms ≥ 1/4 each)
H₈ = H₄ + 1/2     (add 4 terms ≥ 1/8 each)
...
```

Each step adds at least 1/2!

---

## Corollary: Harmonic Series Divergence

Since $1 + \frac{n}{2} \to \infty$ as $n \to \infty$, and $H_{2^n} \geq 1 + \frac{n}{2}$:

$$\lim_{n \to \infty} H_n = \infty$$

The harmonic series **diverges**!

This is **Oresme's proof** (14th century).

---

## Stronger Bounds

The actual growth of harmonic numbers is:

$$H_n \approx \ln n + \gamma$$

where $\gamma \approx 0.57721$ is Euler's constant.

For $n = 2^k$:
$$H_{2^k} \approx \ln(2^k) + \gamma = k \ln 2 + \gamma \approx 0.693k + 0.577$$

Our bound gives:
$$H_{2^k} \geq 1 + \frac{k}{2} = 1 + 0.5k$$

Since $0.693 > 0.5$, the actual growth is faster than our bound!

---

## Alternative Proof Strategy

We can also prove this by **direct summation**:

$$\begin{aligned}
H_{2^n} &= 1 + \frac{1}{2} + \left(\frac{1}{3} + \frac{1}{4}\right) + \left(\frac{1}{5} + \ldots + \frac{1}{8}\right) + \ldots\\[10pt]
&\geq 1 + \frac{1}{2} + \left(\frac{1}{4} + \frac{1}{4}\right) + \left(\frac{1}{8} + \ldots + \frac{1}{8}\right) + \ldots\\[10pt]
&= 1 + \frac{1}{2} + \frac{2}{4} + \frac{4}{8} + \ldots + \frac{2^{n-1}}{2^n}\\[10pt]
&= 1 + \frac{1}{2} + \frac{1}{2} + \frac{1}{2} + \ldots + \frac{1}{2}\\[10pt]
&= 1 + \frac{n}{2}
\end{aligned}$$

---

## Historical Note

**Nicole Oresme** (1323-1382), French bishop and mathematician, was the first to prove the divergence of the harmonic series using this grouping method.

His proof was lost for centuries and rediscovered by Pietro Mengoli in 1647 and later by Johann Bernoulli.

---

## Related Inequalities

| Inequality | Bound |
|------------|-------|
| $H_{2^n} \geq 1 + \frac{n}{2}$ | This exercise |
| $H_{2^n} \geq \frac{n}{2}$ | Exercise 2.1/2 |
| $H_n \geq \ln(n+1)$ | Integral bound |
| $H_n \leq \ln n + 1$ | Upper bound |
| $\ln n + \gamma < H_n < \ln n + \gamma + \frac{1}{2n}$ | Precise bounds |

---

*Exercise 2.1/10 from Chapter 02 - Elemi leszámlálások*
