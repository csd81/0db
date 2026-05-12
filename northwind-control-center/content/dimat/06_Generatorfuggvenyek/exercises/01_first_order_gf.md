# Exercise 6.1 - First-Order Linear Recurrence via Generating Functions

## Problem Statement

Solve the recurrence using generating functions:
$$a_n = r a_{n-1} + b, \quad a_0 = A$$

---

## Solution

### Step 1: Define the generating function

$$F(x) = \sum_{n=0}^{\infty} a_n x^n$$

### Step 2: Multiply recurrence by $x^n$ and sum

The recurrence holds for $n \geq 1$:
$$\sum_{n=1}^{\infty} a_n x^n = r \sum_{n=1}^{\infty} a_{n-1} x^n + b \sum_{n=1}^{\infty} x^n$$

### Step 3: Express in terms of $F(x)$

**Left side:**
$$\sum_{n=1}^{\infty} a_n x^n = F(x) - a_0 = F(x) - A$$

**First term on right:**
$$r \sum_{n=1}^{\infty} a_{n-1} x^n = r x \sum_{n=1}^{\infty} a_{n-1} x^{n-1} = r x F(x)$$

**Second term on right:**
$$b \sum_{n=1}^{\infty} x^n = b \cdot \frac{x}{1-x}$$

### Step 4: Set up the equation

$$F(x) - A = r x F(x) + \frac{bx}{1-x}$$

### Step 5: Solve for $F(x)$

$$\begin{aligned}
F(x) - r x F(x) &= A + \frac{bx}{1-x} \\
F(x)(1 - rx) &= A + \frac{bx}{1-x} \\
F(x) &= \frac{A}{1-rx} + \frac{bx}{(1-x)(1-rx)}
\end{aligned}$$

### Step 6: Partial fraction decomposition

**Case 1: $r \neq 1$**

$$\frac{bx}{(1-x)(1-rx)} = \frac{C}{1-x} + \frac{D}{1-rx}$$

Solving for $C$ and $D$:
$$bx = C(1-rx) + D(1-x)$$

Setting $x = 1$: $b = C(1-r) \Rightarrow C = \frac{b}{1-r}$

Setting $x = \frac{1}{r}$: $\frac{b}{r} = D(1-\frac{1}{r}) \Rightarrow D = \frac{b}{r-1} = -\frac{b}{1-r}$

Therefore:
$$F(x) = \frac{A}{1-rx} + \frac{b}{1-r}\left(\frac{1}{1-x} - \frac{1}{1-rx}\right)$$

$$F(x) = \left(A - \frac{b}{1-r}\right)\frac{1}{1-rx} + \frac{b}{1-r}\cdot\frac{1}{1-x}$$

### Step 7: Extract coefficients

$$\begin{aligned}
a_n &= \left(A - \frac{b}{1-r}\right) r^n + \frac{b}{1-r} \\
&= A r^n + \frac{b}{1-r}(1 - r^n) \\
&= A r^n + \frac{b(r^n - 1)}{r - 1}
\end{aligned}$$

**Case 2: $r = 1$**

The recurrence becomes $a_n = a_{n-1} + b$, which is arithmetic:

$$F(x) = \frac{A}{1-x} + \frac{bx}{(1-x)^2}$$

$$a_n = A + bn$$

---

## Final Formula

$$\boxed{a_n = \begin{cases}
A r^n + \dfrac{b(r^n - 1)}{r - 1} & \text{if } r \neq 1 \\
A + bn & \text{if } r = 1
\end{cases}}$$

---

## Verification

**For $r = 2, b = 1, A = 1$ (Hanoi-like):**
$$a_n = 1 \cdot 2^n + \frac{1(2^n - 1)}{2-1} = 2^n + 2^n - 1 = 2^{n+1} - 1$$

**For $r = 1, b = d, A = a$ (arithmetic):**
$$a_n = a + dn$$ ✓

---

## Comparison with Iteration Method

The generating function method gives the same result as the iteration method from Chapter 05, but:
- More systematic
- Works for higher-order recurrences
- Handles inhomogeneous terms automatically

---

*Exercise 6.1 from Chapter 06 - Generátorfüggvények*
