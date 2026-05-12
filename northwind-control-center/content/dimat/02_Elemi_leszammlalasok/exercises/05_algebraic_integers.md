# Exercise 2.1/5 - Algebraic Integers

## Problem Statement

Prove by complete induction:

If $a \in \mathbb{R}$ such that $a + \frac{1}{a} \in \mathbb{Z}$, then $a^n + \frac{1}{a^n} \in \mathbb{Z}$ for all $n \in \mathbb{N}$.

---

## Proof by Mathematical Induction

### Step 1: Base Cases

We need **two base cases** because the inductive step will use the previous TWO values.

**n = 1:**
$$a^1 + \frac{1}{a^1} = a + \frac{1}{a} \in \mathbb{Z}$$
✓ Given in the hypothesis.

**n = 2:**
$$\begin{aligned}
a^2 + \frac{1}{a^2} &= \left(a + \frac{1}{a}\right)^2 - 2 \cdot a \cdot \frac{1}{a}\\[10pt]
&= \left(a + \frac{1}{a}\right)^2 - 2\\[10pt]
&= \left(a + \frac{1}{a}\right)^2 - 2
\end{aligned}$$

Since $a + \frac{1}{a} \in \mathbb{Z}$, its square is also an integer, and subtracting 2 gives an integer.

✓ **n = 2 verified.**

---

### Step 2: Inductive Hypothesis

Assume the statement holds for $n = k$ and $n = k-1$ (strong induction):

$$a^k + \frac{1}{a^k} \in \mathbb{Z} \quad \text{and} \quad a^{k-1} + \frac{1}{a^{k-1}} \in \mathbb{Z}$$

---

### Step 3: Inductive Step (n = k+1)

We need to prove:
$$a^{k+1} + \frac{1}{a^{k+1}} \in \mathbb{Z}$$

**Proof:**

Consider the product:
$$\left(a^k + \frac{1}{a^k}\right) \cdot \left(a + \frac{1}{a}\right)$$

Expanding:
$$\begin{aligned}
\left(a^k + \frac{1}{a^k}\right) \left(a + \frac{1}{a}\right) &= a^k \cdot a + a^k \cdot \frac{1}{a} + \frac{1}{a^k} \cdot a + \frac{1}{a^k} \cdot \frac{1}{a}\\[10pt]
&= a^{k+1} + a^{k-1} + \frac{1}{a^{k-1}} + \frac{1}{a^{k+1}}\\[10pt]
&= \left(a^{k+1} + \frac{1}{a^{k+1}}\right) + \left(a^{k-1} + \frac{1}{a^{k-1}}\right)
\end{aligned}$$

Therefore:
$$a^{k+1} + \frac{1}{a^{k+1}} = \left(a^k + \frac{1}{a^k}\right) \left(a + \frac{1}{a}\right) - \left(a^{k-1} + \frac{1}{a^{k-1}}\right)$$

Now let's analyze each term:

| Term | Status |
|------|--------|
| $a^k + \frac{1}{a^k}$ | ∈ ℤ (by inductive hypothesis) |
| $a + \frac{1}{a}$ | ∈ ℤ (given) |
| $a^{k-1} + \frac{1}{a^{k-1}}$ | ∈ ℤ (by inductive hypothesis) |

Since the product and difference of integers are integers:

$$a^{k+1} + \frac{1}{a^{k+1}} \in \mathbb{Z}$$

✓ **Inductive step complete!**

---

## Conclusion

By the Principle of (Strong) Mathematical Induction:

$$\boxed{\text{If } a + \frac{1}{a} \in \mathbb{Z}, \text{ then } a^n + \frac{1}{a^n} \in \mathbb{Z} \text{ for all } n \in \mathbb{N}}$$

---

## Verification Table

Let $x = a + \frac{1}{a} = 3$ (for example). Then:

| n | Expression | Value | Integer? |
|---|------------|-------|----------|
| 1 | $a + \frac{1}{a}$ | 3 | ✓ |
| 2 | $a^2 + \frac{1}{a^2}$ | $3^2 - 2 = 7$ | ✓ |
| 3 | $a^3 + \frac{1}{a^3}$ | $3 \cdot 7 - 3 = 18$ | ✓ |
| 4 | $a^4 + \frac{1}{a^4}$ | $3 \cdot 18 - 7 = 47$ | ✓ |
| 5 | $a^5 + \frac{1}{a^5}$ | $3 \cdot 47 - 18 = 123$ | ✓ |

---

## Recurrence Relation

This proof reveals a **recurrence relation**:

Let $S_n = a^n + \frac{1}{a^n}$. Then:

$$\boxed{S_{n+1} = S_1 \cdot S_n - S_{n-1}}$$

with initial conditions:
- $S_0 = a^0 + \frac{1}{a^0} = 2$
- $S_1 = a + \frac{1}{a}$ (given integer)

This is similar to the **Chebyshev polynomial** recurrence!

---

## Connection to Chebyshev Polynomials

If we let $a = e^{i\theta}$, then:
$$a + \frac{1}{a} = e^{i\theta} + e^{-i\theta} = 2\cos\theta$$

And:
$$a^n + \frac{1}{a^n} = e^{in\theta} + e^{-in\theta} = 2\cos(n\theta)$$

The recurrence becomes:
$$2\cos((n+1)\theta) = 2\cos\theta \cdot 2\cos(n\theta) - 2\cos((n-1)\theta)$$

Which is the **Chebyshev polynomial** recurrence relation!

---

## Key Insights

1. **Strong induction** is needed (use TWO previous cases)
2. The key identity is:
   $$\left(a^k + \frac{1}{a^k}\right)\left(a + \frac{1}{a}\right) = \left(a^{k+1} + \frac{1}{a^{k+1}}\right) + \left(a^{k-1} + \frac{1}{a^{k-1}}\right)$$

3. This creates a **linear recurrence** with integer coefficients

---

## Generalization

More generally, if $P(x)$ is a polynomial with integer coefficients and $a + \frac{1}{a} \in \mathbb{Z}$, then:
$$P\left(a^n + \frac{1}{a^n}\right) \in \mathbb{Z}$$

This is because $a^n + \frac{1}{a^n}$ can always be expressed as a polynomial in $a + \frac{1}{a}$ with integer coefficients!

---

## Related Problems

Similar techniques prove:
- If $a + b \in \mathbb{Z}$ and $ab = 1$, then $a^n + b^n \in \mathbb{Z}$
- If $a + b \in \mathbb{Z}$ and $ab \in \mathbb{Z}$, then $a^n + b^n \in \mathbb{Z}$ (Newton sums)

---

*Exercise 2.1/5 from Chapter 02 - Elemi leszámlálások*
