# Exercise 5.4 - Fibonacci Identities

## Problem Statement

Prove the following Fibonacci identities where $f_1 = f_2 = 1$ and $f_n = f_{n-1} + f_{n-2}$:

---

## /1/ Sum of Fibonacci Numbers

$$\sum_{i=1}^n f_i = f_{n+2} - 1$$

### Proof by Induction

**Base case ($n=1$):**
$$f_1 = 1 = f_3 - 1 = 2 - 1 = 1$$ ✓

**Inductive step:**

Assume true for $n = k$: $\sum_{i=1}^k f_i = f_{k+2} - 1$

For $n = k+1$:
$$\begin{aligned}
\sum_{i=1}^{k+1} f_i &= \left(\sum_{i=1}^k f_i\right) + f_{k+1} \\
&= (f_{k+2} - 1) + f_{k+1} \\
&= (f_{k+1} + f_{k+2}) - 1 \\
&= f_{k+3} - 1 \\
&= f_{(k+1)+2} - 1
\end{aligned}$$

✓ **Q.E.D.**

---

## /2/ Sum of Odd-Indexed Fibonacci Numbers

$$\sum_{i=1}^n f_{2i-1} = f_{2n}$$

### Proof

**Base case ($n=1$):**
$$f_1 = 1 = f_2$$ ✓

**Inductive step:**

Assume $\sum_{i=1}^k f_{2i-1} = f_{2k}$

For $n = k+1$:
$$\begin{aligned}
\sum_{i=1}^{k+1} f_{2i-1} &= f_{2k} + f_{2k+1} \\
&= f_{2k+2} \\
&= f_{2(k+1)}
\end{aligned}$$

✓ **Q.E.D.**

---

## /3/ Sum of Even-Indexed Fibonacci Numbers

$$\sum_{i=1}^n f_{2i} = f_{2n+1} - 1$$

### Proof

**Base case ($n=1$):**
$$f_2 = 1 = f_3 - 1 = 2 - 1 = 1$$ ✓

**Inductive step:**

Assume $\sum_{i=1}^k f_{2i} = f_{2k+1} - 1$

For $n = k+1$:
$$\begin{aligned}
\sum_{i=1}^{k+1} f_{2i} &= (f_{2k+1} - 1) + f_{2k+2} \\
&= (f_{2k+1} + f_{2k+2}) - 1 \\
&= f_{2k+3} - 1 \\
&= f_{2(k+1)+1} - 1
\end{aligned}$$

✓ **Q.E.D.**

---

## /8/ Sum of Squares

$$\sum_{i=1}^n f_i^2 = f_n \cdot f_{n+1}$$

### Proof by Induction

**Base case ($n=1$):**
$$f_1^2 = 1 = 1 \cdot 1 = f_1 \cdot f_2$$ ✓

**Inductive step:**

Assume $\sum_{i=1}^k f_i^2 = f_k \cdot f_{k+1}$

For $n = k+1$:
$$\begin{aligned}
\sum_{i=1}^{k+1} f_i^2 &= f_k \cdot f_{k+1} + f_{k+1}^2 \\
&= f_{k+1}(f_k + f_{k+1}) \\
&= f_{k+1} \cdot f_{k+2}
\end{aligned}$$

✓ **Q.E.D.**

### Geometric Interpretation

This identity can be visualized by arranging squares of sizes $f_1, f_2, \ldots, f_n$ to form a rectangle of dimensions $f_n \times f_{n+1}$.

---

## /19/ Cassini's Identity

$$f_{n+1} f_{n-1} - f_n^2 = (-1)^n$$

### Proof by Induction

**Base case ($n=2$):**
$$f_3 f_1 - f_2^2 = 2 \cdot 1 - 1^2 = 1 = (-1)^2$$ ✓

**Inductive step:**

Assume $f_{k+1} f_{k-1} - f_k^2 = (-1)^k$

For $n = k+1$:
$$\begin{aligned}
f_{k+2} f_k - f_{k+1}^2 &= (f_{k+1} + f_k)f_k - f_{k+1}^2 \\
&= f_{k+1}f_k + f_k^2 - f_{k+1}^2 \\
&= f_{k+1}f_k + f_k^2 - f_{k+1}(f_k + f_{k-1}) \\
&= f_{k+1}f_k + f_k^2 - f_{k+1}f_k - f_{k+1}f_{k-1} \\
&= f_k^2 - f_{k+1}f_{k-1} \\
&= -(f_{k+1}f_{k-1} - f_k^2) \\
&= -(-1)^k \\
&= (-1)^{k+1}
\end{aligned}$$

✓ **Q.E.D.**

---

## /27/ Addition Formula

$$f_{m-1} f_n + f_m f_{n+1} = f_{n+m}$$

### Proof by Induction on $n$

**Base cases:**

For $n = 1$:
$$f_{m-1} f_1 + f_m f_2 = f_{m-1} \cdot 1 + f_m \cdot 1 = f_{m-1} + f_m = f_{m+1}$$ ✓

For $n = 2$:
$$f_{m-1} f_2 + f_m f_3 = f_{m-1} \cdot 1 + f_m \cdot 2 = f_{m-1} + 2f_m = f_{m+2}$$ ✓

**Inductive step:**

Assume true for $n = k$ and $n = k-1$.

For $n = k+1$:
$$\begin{aligned}
f_{m-1} f_{k+1} + f_m f_{k+2} &= f_{m-1}(f_k + f_{k-1}) + f_m(f_{k+1} + f_k) \\
&= (f_{m-1} f_k + f_m f_{k+1}) + (f_{m-1} f_{k-1} + f_m f_k) \\
&= f_{k+m} + f_{k+m-1} \\
&= f_{k+m+1} \\
&= f_{(k+1)+m}
\end{aligned}$$

✓ **Q.E.D.**

---

## /32/ Consecutive Fibonacci Numbers are Coprime

$$\gcd(f_n, f_{n+1}) = 1$$

### Proof

Use the Euclidean algorithm property:
$$\gcd(f_{n+1}, f_n) = \gcd(f_n, f_{n+1} - f_n) = \gcd(f_n, f_{n-1})$$

By repeated application:
$$\gcd(f_{n+1}, f_n) = \gcd(f_2, f_1) = \gcd(1, 1) = 1$$

✓ **Q.E.D.**

---

## /41/ Golden Ratio Limit

$$\lim_{n \to \infty} \frac{f_{n+1}}{f_n} = \phi = \frac{1+\sqrt{5}}{2}$$

### Proof

From Binet's formula:
$$f_n = \frac{\phi^n - \psi^n}{\sqrt{5}}$$

where $\phi = \frac{1+\sqrt{5}}{2}$ and $\psi = \frac{1-\sqrt{5}}{2}$.

Since $|\psi| < 1$, we have $\psi^n \to 0$ as $n \to \infty$.

Therefore:
$$\begin{aligned}
\frac{f_{n+1}}{f_n} &= \frac{\phi^{n+1} - \psi^{n+1}}{\phi^n - \psi^n} \\
&= \frac{\phi^{n+1}(1 - (\psi/\phi)^{n+1})}{\phi^n(1 - (\psi/\phi)^n)} \\
&= \phi \cdot \frac{1 - (\psi/\phi)^{n+1}}{1 - (\psi/\phi)^n} \\
&\to \phi \cdot \frac{1 - 0}{1 - 0} = \phi
\end{aligned}$$

✓ **Q.E.D.**

---

## Summary Table

| # | Identity | Result |
|---|----------|--------|
| /1/ | $\sum_{i=1}^n f_i$ | $f_{n+2} - 1$ |
| /2/ | $\sum_{i=1}^n f_{2i-1}$ | $f_{2n}$ |
| /3/ | $\sum_{i=1}^n f_{2i}$ | $f_{2n+1} - 1$ |
| /8/ | $\sum_{i=1}^n f_i^2$ | $f_n \cdot f_{n+1}$ |
| /19/ | $f_{n+1}f_{n-1} - f_n^2$ | $(-1)^n$ |
| /27/ | $f_{m-1}f_n + f_m f_{n+1}$ | $f_{n+m}$ |
| /32/ | $\gcd(f_n, f_{n+1})$ | $1$ |
| /41/ | $\lim_{n\to\infty} f_{n+1}/f_n$ | $\phi = \frac{1+\sqrt{5}}{2}$ |

---

*Exercise 5.4 from Chapter 05 - Rekurzív sorozatok*
