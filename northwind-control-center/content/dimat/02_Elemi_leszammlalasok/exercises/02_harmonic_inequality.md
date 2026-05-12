# Exercise 2.1/2 - Harmonic Sum Inequality

## Problem Statement

Prove by complete induction that for $n \geq 2$:

$$1 + \frac{1}{2} + \frac{1}{3} + ... + \frac{1}{2^n} \geq \frac{n}{2}$$

Or in compact notation:
$$H_{2^n} \geq \frac{n}{2}$$

where $H_k = \sum_{i=1}^{k} \frac{1}{i}$ is the $k$-th harmonic number.

---

## Proof by Mathematical Induction

### Step 1: Base Case (n = 2)

**Left side:** 
$$H_{2^2} = H_4 = 1 + \frac{1}{2} + \frac{1}{3} + \frac{1}{4}$$

Let's calculate:
$$H_4 = 1 + 0.5 + 0.333... + 0.25 = 2.083...$$

**Right side:**
$$\frac{2}{2} = 1$$

✓ **Base case verified:** $2.083... \geq 1$

---

### Step 2: Inductive Hypothesis

Assume the inequality holds for some $n = k$ where $k \geq 2$:

$$H_{2^k} = 1 + \frac{1}{2} + \frac{1}{3} + ... + \frac{1}{2^k} \geq \frac{k}{2}$$

---

### Step 3: Inductive Step (n = k+1)

We need to prove:
$$H_{2^{k+1}} \geq \frac{k+1}{2}$$

**Proof:**

First, let's understand the structure of $H_{2^{k+1}}$:

$$\begin{aligned}
H_{2^{k+1}} &= 1 + \frac{1}{2} + \frac{1}{3} + ... + \frac{1}{2^k} + \frac{1}{2^k + 1} + ... + \frac{1}{2^{k+1}}\\[10pt]
&= H_{2^k} + \sum_{i=2^k + 1}^{2^{k+1}} \frac{1}{i}
\end{aligned}$$

The key insight is to **bound the new terms** from below.

### Bounding the New Terms

The sum $\sum_{i=2^k + 1}^{2^{k+1}} \frac{1}{i}$ has:
- **Number of terms:** $2^{k+1} - 2^k = 2^k$ terms
- **Smallest term:** $\frac{1}{2^{k+1}}$ (the last one)
- **Largest term:** $\frac{1}{2^k + 1}$ (the first one)

Since each term $\frac{1}{i} \geq \frac{1}{2^{k+1}}$ for $i \in [2^k+1, 2^{k+1}]$:

$$\sum_{i=2^k + 1}^{2^{k+1}} \frac{1}{i} \geq \sum_{i=2^k + 1}^{2^{k+1}} \frac{1}{2^{k+1}} = 2^k \cdot \frac{1}{2^{k+1}} = \frac{2^k}{2^{k+1}} = \frac{1}{2}$$

### Completing the Proof

Now we can bound $H_{2^{k+1}}$:

$$\begin{aligned}
H_{2^{k+1}} &= H_{2^k} + \sum_{i=2^k + 1}^{2^{k+1}} \frac{1}{i}\\[10pt]
&\geq H_{2^k} + \frac{1}{2}\\[10pt]
&\geq \frac{k}{2} + \frac{1}{2} & \text{(by inductive hypothesis)}\\[10pt]
&= \frac{k+1}{2}
\end{aligned}$$

✓ **Inductive step complete!**

---

## Conclusion

By the Principle of Mathematical Induction, the inequality:

$$\boxed{H_{2^n} \geq \frac{n}{2} \quad \text{for all } n \geq 2}$$

---

## Verification Table

| n | $2^n$ | $H_{2^n}$ (approx) | $n/2$ | Inequality |
|---|-------|-------------------|-------|------------|
| 2 | 4 | 2.083 | 1.0 | ✓ |
| 3 | 8 | 2.718 | 1.5 | ✓ |
| 4 | 16 | 3.381 | 2.0 | ✓ |
| 5 | 32 | 4.059 | 2.5 | ✓ |
| 6 | 64 | 4.744 | 3.0 | ✓ |
| 7 | 128 | 5.434 | 3.5 | ✓ |
| 8 | 256 | 6.127 | 4.0 | ✓ |
| 9 | 512 | 6.822 | 4.5 | ✓ |
| 10 | 1024 | 7.518 | 5.0 | ✓ |

---

## Key Insight

The proof relies on the observation that:

$$H_{2^{k+1}} - H_{2^k} = \sum_{i=2^k + 1}^{2^{k+1}} \frac{1}{i} \geq \frac{1}{2}$$

Each time we double the number of terms, we add **at least 1/2** to the harmonic sum!

This is because we're adding $2^k$ terms, each at least $\frac{1}{2^{k+1}}$.

---

## Corollary: Harmonic Series Diverges

This inequality proves that the harmonic series **diverges**:

$$\lim_{n \to \infty} H_n = \infty$$

Because $H_{2^n} \geq \frac{n}{2}$ and $\frac{n}{2} \to \infty$ as $n \to \infty$.

This is **Oresme's proof** (14th century) of the divergence of the harmonic series!

---

## Stronger Bounds

Actually, a tighter bound can be proven:

$$\ln(2^n) < H_{2^n} < \ln(2^n) + 1$$

Which gives:
$$n \ln 2 < H_{2^n} < n \ln 2 + 1$$

Since $\ln 2 \approx 0.693 > 0.5$, this is a stronger result than $n/2$.

---

## Historical Note

This exercise demonstrates:
1. **Nicole Oresme** (1323-1382) first proved harmonic series divergence
2. The sum grows **logarithmically**: $H_n \approx \ln n + \gamma$
3. Euler's constant: $\gamma = \lim_{n\to\infty}(H_n - \ln n) \approx 0.57721$

---

*Exercise 2.1/2 from Chapter 02 - Elemi leszámlálások*
