# Exercise 6.3 - Catalan Numbers via Generating Functions

## Problem Statement

The Catalan numbers satisfy the recurrence:
$$C_0 = 1, \quad C_{n+1} = \sum_{i=0}^{n} C_i C_{n-i} \quad \text{for } n \geq 0$$

Find the generating function and explicit formula.

---

## Solution

### Step 1: Define the generating function

$$C(x) = \sum_{n=0}^{\infty} C_n x^n$$

### Step 2: Multiply recurrence by $x^{n+1}$ and sum

$$\sum_{n=0}^{\infty} C_{n+1} x^{n+1} = \sum_{n=0}^{\infty} \left(\sum_{i=0}^{n} C_i C_{n-i}\right) x^{n+1}$$

### Step 3: Express in terms of $C(x)$

**Left side:**
$$\sum_{n=0}^{\infty} C_{n+1} x^{n+1} = C(x) - C_0 = C(x) - 1$$

**Right side:**

The inner sum is a **convolution** (Cauchy product):
$$\sum_{i=0}^{n} C_i C_{n-i} = [x^n] C(x)^2$$

Therefore:
$$\sum_{n=0}^{\infty} \left(\sum_{i=0}^{n} C_i C_{n-i}\right) x^{n+1} = x \sum_{n=0}^{\infty} \left(\sum_{i=0}^{n} C_i C_{n-i}\right) x^n = x C(x)^2$$

### Step 4: Set up the equation

$$C(x) - 1 = x C(x)^2$$

### Step 5: Solve the quadratic equation

$$x C(x)^2 - C(x) + 1 = 0$$

Using the quadratic formula:
$$C(x) = \frac{1 \pm \sqrt{1 - 4x}}{2x}$$

### Step 6: Choose the correct sign

We need $C(0) = C_0 = 1$.

**With plus sign:**
$$\lim_{x \to 0} \frac{1 + \sqrt{1-4x}}{2x} = \frac{1+1}{0} = \infty$$ ✗

**With minus sign:**
$$\lim_{x \to 0} \frac{1 - \sqrt{1-4x}}{2x} = \lim_{x \to 0} \frac{1 - (1-2x + O(x^2))}{2x} = \lim_{x \to 0} \frac{2x + O(x^2)}{2x} = 1$$ ✓

Therefore:
$$C(x) = \frac{1 - \sqrt{1-4x}}{2x}$$

### Step 7: Expand using Newton's binomial series

$$(1-4x)^{1/2} = \sum_{n=0}^{\infty} \binom{1/2}{n} (-4x)^n$$

Where:
$$\binom{1/2}{n} = \frac{\frac{1}{2}(\frac{1}{2}-1)(\frac{1}{2}-2)\cdots(\frac{1}{2}-n+1)}{n!} = \frac{(\frac{1}{2})(-\frac{1}{2})(-\frac{3}{2})\cdots(\frac{3-2n}{2})}{n!}$$

$$= \frac{(-1)^{n-1} \cdot 1 \cdot 3 \cdot 5 \cdots (2n-3)}{2^n n!} = \frac{(-1)^{n-1} (2n-3)!!}{2^n n!}$$

Using $(2n-3)!! = \frac{(2n-2)!}{2^{n-1}(n-1)!}$:

$$\binom{1/2}{n} = \frac{(-1)^{n-1} (2n-2)!}{2^{2n-1} n! (n-1)!} = \frac{(-1)^{n-1}}{2^{2n-1} n} \binom{2n-2}{n-1}$$

Therefore:
$$(1-4x)^{1/2} = 1 + \sum_{n=1}^{\infty} \frac{(-1)^{n-1}}{2^{2n-1} n} \binom{2n-2}{n-1} (-4)^n x^n$$

$$= 1 - \sum_{n=1}^{\infty} \frac{2}{n} \binom{2n-2}{n-1} x^n$$

### Step 8: Extract coefficients

$$C(x) = \frac{1 - (1-4x)^{1/2}}{2x} = \frac{1}{2x} \sum_{n=1}^{\infty} \frac{2}{n} \binom{2n-2}{n-1} x^n$$

$$= \sum_{n=1}^{\infty} \frac{1}{n} \binom{2n-2}{n-1} x^{n-1} = \sum_{n=0}^{\infty} \frac{1}{n+1} \binom{2n}{n} x^n$$

Therefore:
$$C_n = \frac{1}{n+1} \binom{2n}{n}$$

---

## Final Formula

$$\boxed{C_n = \frac{1}{n+1} \binom{2n}{n}}$$

$$\boxed{C(x) = \frac{1 - \sqrt{1-4x}}{2x}}$$

---

## Verification Table

| n | Formula | Value | Recurrence Check |
|---|---------|-------|------------------|
| 0 | $\frac{1}{1}\binom{0}{0}$ | 1 | $C_0 = 1$ ✓ |
| 1 | $\frac{1}{2}\binom{2}{1}$ | 1 | $C_1 = C_0 C_0 = 1$ ✓ |
| 2 | $\frac{1}{3}\binom{4}{2}$ | 2 | $C_2 = C_0 C_1 + C_1 C_0 = 2$ ✓ |
| 3 | $\frac{1}{4}\binom{6}{3}$ | 5 | $C_3 = C_0 C_2 + C_1 C_1 + C_2 C_0 = 5$ ✓ |
| 4 | $\frac{1}{5}\binom{8}{4}$ | 14 | $C_4 = 1\cdot 5 + 1\cdot 2 + 2\cdot 1 + 5\cdot 1 = 14$ ✓ |
| 5 | $\frac{1}{6}\binom{10}{5}$ | 42 | ✓ |
| 6 | $\frac{1}{7}\binom{12}{6}$ | 132 | ✓ |
| 7 | $\frac{1}{8}\binom{14}{7}$ | 429 | ✓ |

---

## Applications of Catalan Numbers

| Combinatorial Object | Count |
|---------------------|-------|
| Valid parenthesis expressions with n pairs | $C_n$ |
| Binary trees with n internal nodes | $C_n$ |
| Triangulations of (n+2)-gon | $C_n$ |
| Dyck paths of length 2n | $C_n$ |
| Non-crossing partitions of {1,...,n} | $C_n$ |

---

## Key Insight: Convolution → Squared GF

The recurrence $C_{n+1} = \sum_{i=0}^n C_i C_{n-i}$ is a **convolution**, which corresponds to:
$$[x^n] C(x)^2$$

This is why the generating function satisfies the quadratic equation $C(x) - 1 = x C(x)^2$.

---

## Alternative Derivation

Using the **Lagrange Inversion Formula** on $C(x) = 1 + xC(x)^2$:

Let $C(x) = 1 + y$ where $y = x(1+y)^2$.

By Lagrange inversion:
$$C_n = \frac{1}{n} [t^{n-1}] (1+t)^{2n} = \frac{1}{n} \binom{2n}{n-1} = \frac{1}{n+1} \binom{2n}{n}$$

---

*Exercise 6.3 from Chapter 06 - Generátorfüggvények*
