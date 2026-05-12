# Exercise 6.2 - Fibonacci Numbers via Generating Functions

## Problem Statement

Solve the Fibonacci recurrence using generating functions:
$$f_n = f_{n-1} + f_{n-2}, \quad f_0 = 0, f_1 = 1$$

---

## Solution

### Step 1: Define the generating function

$$F(x) = \sum_{n=0}^{\infty} f_n x^n$$

### Step 2: Multiply recurrence by $x^n$ and sum

The recurrence holds for $n \geq 2$:
$$\sum_{n=2}^{\infty} f_n x^n = \sum_{n=2}^{\infty} f_{n-1} x^n + \sum_{n=2}^{\infty} f_{n-2} x^n$$

### Step 3: Express in terms of $F(x)$

**Left side:**
$$\sum_{n=2}^{\infty} f_n x^n = F(x) - f_0 - f_1 x = F(x) - 0 - x = F(x) - x$$

**First term on right:**
$$\sum_{n=2}^{\infty} f_{n-1} x^n = x \sum_{n=2}^{\infty} f_{n-1} x^{n-1} = x \sum_{m=1}^{\infty} f_m x^m = x(F(x) - f_0) = xF(x)$$

**Second term on right:**
$$\sum_{n=2}^{\infty} f_{n-2} x^n = x^2 \sum_{n=2}^{\infty} f_{n-2} x^{n-2} = x^2 \sum_{m=0}^{\infty} f_m x^m = x^2 F(x)$$

### Step 4: Set up the equation

$$F(x) - x = xF(x) + x^2 F(x)$$

### Step 5: Solve for $F(x)$

$$\begin{aligned}
F(x) - xF(x) - x^2 F(x) &= x \\
F(x)(1 - x - x^2) &= x \\
F(x) &= \frac{x}{1 - x - x^2}
\end{aligned}$$

### Step 6: Factor the denominator

The roots of $1 - x - x^2 = 0$ are:
$$x = \frac{-1 \pm \sqrt{5}}{-2} = \frac{1 \mp \sqrt{5}}{2}$$

Let $\phi = \frac{1+\sqrt{5}}{2}$ and $\psi = \frac{1-\sqrt{5}}{2}$.

Then: $1 - x - x^2 = -(x - \phi)(x - \psi) = (1 - \phi x)(1 - \psi x) \cdot (-\phi\psi)$

Since $\phi\psi = -1$:
$$1 - x - x^2 = (1 - \phi x)(1 - \psi x)$$

### Step 7: Partial fraction decomposition

$$\frac{x}{1 - x - x^2} = \frac{x}{(1-\phi x)(1-\psi x)} = \frac{A}{1-\phi x} + \frac{B}{1-\psi x}$$

$$x = A(1-\psi x) + B(1-\phi x)$$

Setting $x = \frac{1}{\phi}$: $\frac{1}{\phi} = A(1-\frac{\psi}{\phi}) \Rightarrow A = \frac{1}{\phi-\psi} = \frac{1}{\sqrt{5}}$

Setting $x = \frac{1}{\psi}$: $\frac{1}{\psi} = B(1-\frac{\phi}{\psi}) \Rightarrow B = \frac{1}{\psi-\phi} = -\frac{1}{\sqrt{5}}$

Therefore:
$$F(x) = \frac{1}{\sqrt{5}}\left(\frac{1}{1-\phi x} - \frac{1}{1-\psi x}\right)$$

### Step 8: Expand as geometric series

$$\begin{aligned}
F(x) &= \frac{1}{\sqrt{5}}\left(\sum_{n=0}^{\infty} \phi^n x^n - \sum_{n=0}^{\infty} \psi^n x^n\right) \\
&= \frac{1}{\sqrt{5}}\sum_{n=0}^{\infty} (\phi^n - \psi^n) x^n
\end{aligned}$$

### Step 9: Extract coefficients

$$f_n = \frac{\phi^n - \psi^n}{\sqrt{5}}$$

---

## Final Formula (Binet's Formula)

$$\boxed{f_n = \frac{1}{\sqrt{5}}\left[\left(\frac{1+\sqrt{5}}{2}\right)^n - \left(\frac{1-\sqrt{5}}{2}\right)^n\right]}$$

---

## Verification Table

| n | Formula | Value | Check |
|---|---------|-------|-------|
| 0 | $\frac{\phi^0 - \psi^0}{\sqrt{5}}$ | 0 | $f_0 = 0$ ✓ |
| 1 | $\frac{\phi - \psi}{\sqrt{5}}$ | 1 | $f_1 = 1$ ✓ |
| 2 | $\frac{\phi^2 - \psi^2}{\sqrt{5}}$ | 1 | $f_2 = 1$ ✓ |
| 3 | $\frac{\phi^3 - \psi^3}{\sqrt{5}}$ | 2 | $f_3 = 2$ ✓ |
| 4 | $\frac{\phi^4 - \psi^4}{\sqrt{5}}$ | 3 | $f_4 = 3$ ✓ |
| 5 | $\frac{\phi^5 - \psi^5}{\sqrt{5}}$ | 5 | $f_5 = 5$ ✓ |
| 6 | $\frac{\phi^6 - \psi^6}{\sqrt{5}}$ | 8 | $f_6 = 8$ ✓ |
| 7 | $\frac{\phi^7 - \psi^7}{\sqrt{5}}$ | 13 | $f_7 = 13$ ✓ |
| 8 | $\frac{\phi^8 - \psi^8}{\sqrt{5}}$ | 21 | $f_8 = 21$ ✓ |
| 9 | $\frac{\phi^9 - \psi^9}{\sqrt{5}}$ | 34 | $f_9 = 34$ ✓ |
| 10 | $\frac{\phi^{10} - \psi^{10}}{\sqrt{5}}$ | 55 | $f_{10} = 55$ ✓ |

---

## Key Properties Used

| Property | Value |
|----------|-------|
| $\phi + \psi$ | $1$ |
| $\phi \psi$ | $-1$ |
| $\phi - \psi$ | $\sqrt{5}$ |
| $\phi^2$ | $\phi + 1$ |
| $\psi^2$ | $\psi + 1$ |

---

## Why This Method Works

1. **Linear recurrence** → **Rational generating function**
2. **Partial fractions** → **Geometric series**
3. **Coefficient extraction** → **Explicit formula**

The generating function method automatically handles:
- Initial conditions
- Homogeneous recurrences
- The algebraic structure of the solution

---

*Exercise 6.2 from Chapter 06 - Generátorfüggvények*
