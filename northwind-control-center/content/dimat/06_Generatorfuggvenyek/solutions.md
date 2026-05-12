# Chapter 06 - Generátorfüggvények (Generating Functions) - Complete Solutions

## Section 6.0 - Alapfogalmak (Basic Concepts)

---

### Exercise 6.0.1 - Verify: If G(x) = xF(x), then bₙ = aₙ₋₁

**Problem:** Prove that if $G(x) = xF(x)$, then the coefficients satisfy $b_n = a_{n-1}$.

**Solution:**

**Given:**
$$F(x) = \sum_{n=0}^{\infty} a_n x^n = a_0 + a_1 x + a_2 x^2 + a_3 x^3 + \cdots$$

$$G(x) = x F(x)$$

---

**Compute G(x):**

$$G(x) = x \cdot \sum_{n=0}^{\infty} a_n x^n = \sum_{n=0}^{\infty} a_n x^{n+1}$$

---

**Reindex:** Let $m = n+1$, so $n = m-1$.

When $n = 0$: $m = 1$
When $n \to \infty$: $m \to \infty$

$$G(x) = \sum_{m=1}^{\infty} a_{m-1} x^m$$

---

**Write as standard form:**

$$G(x) = 0 \cdot x^0 + a_0 x^1 + a_1 x^2 + a_2 x^3 + \cdots$$

$$G(x) = \sum_{m=0}^{\infty} b_m x^m$$

where:
- $b_0 = 0$
- $b_m = a_{m-1}$ for $m \geq 1$

---

**Conclusion:** The coefficient of $x^n$ in $G(x)$ is $b_n = a_{n-1}$ for $n \geq 1$. ✓

---

**Example:**

If $F(x) = 1 + 2x + 3x^2 + 4x^3 + \cdots$ (i.e., $a_n = n+1$)

Then $G(x) = xF(x) = x + 2x^2 + 3x^3 + 4x^4 + \cdots$

Coefficients: $b_0 = 0, b_1 = 1, b_2 = 2, b_3 = 3, \ldots$

Indeed: $b_n = a_{n-1}$ ✓

---

### Exercise 6.0.2 - Compute First 5 Terms of Geometric Series

**Problem:** Compute the first 5 terms of the geometric series $\frac{1}{1-x}$.

**Solution:**

**Geometric Series Formula:**

$$\frac{1}{1-x} = \sum_{n=0}^{\infty} x^n = 1 + x + x^2 + x^3 + x^4 + \cdots$$

**Valid for:** $|x| < 1$

---

**First 5 terms:**

| n | Term | Coefficient |
|---|------|-------------|
| 0 | 1 | 1 |
| 1 | x | 1 |
| 2 | x² | 1 |
| 3 | x³ | 1 |
| 4 | x⁴ | 1 |

---

**Verification:**

Multiply $(1-x)$ by the series:

$$(1-x)(1 + x + x^2 + x^3 + x^4 + \cdots)$$
$$= (1 + x + x^2 + x^3 + x^4 + \cdots) - (x + x^2 + x^3 + x^4 + x^5 + \cdots)$$

All terms cancel except the first:
$$= 1$$ ✓

---

**Numerical Verification (x = 0.5):**

$$\frac{1}{1-0.5} = \frac{1}{0.5} = 2$$

Series: $1 + 0.5 + 0.25 + 0.125 + 0.0625 + \cdots$

Partial sums:
- S₁ = 1
- S₂ = 1.5
- S₃ = 1.75
- S₄ = 1.875
- S₅ = 1.9375

Converging to 2! ✓

---

### Exercise 6.0.3 - Connection to Laplace Transform

**Problem:** Understand the connection between generating functions and Laplace transform.

**Solution:**

**Generating Function (discrete):**
$$F(x) = \sum_{n=0}^{\infty} a_n x^n$$

**Laplace Transform (continuous):**
$$\mathcal{L}\{f(t)\} = \int_0^{\infty} f(t) e^{-st} dt$$

---

**Connection:**

Both are integral transforms that convert sequences/functions into algebraic objects.

**Analogy:**

| Generating Function | Laplace Transform |
|--------------------|-------------------|
| Sequence $(a_n)$ | Function $f(t)$ |
| Variable $x$ | Variable $s$ |
| Sum $\sum$ | Integral $\int$ |
| $x^n$ | $e^{-st}$ |
| Discrete index $n$ | Continuous variable $t$ |

---

**Z-Transform (bridge between them):**

$$X(z) = \sum_{n=0}^{\infty} x[n] z^{-n}$$

This is essentially a generating function with $z = 1/x$.

The Laplace transform is the continuous analog of the Z-transform.

---

## Section 6.1 - Lineáris rekurziók (Linear Recurrences)

---

### Exercise 6.1.1 - Verify f₀ = 0 Keeps Fibonacci Recurrence Valid

**Problem:** Verify that setting $f_0 = 0$ keeps the Fibonacci recurrence valid for $n = 2$.

**Solution:**

**Fibonacci Recurrence:**
$$f_n = f_{n-1} + f_{n-2} \quad \text{for } n \geq 2$$

**Standard initial conditions:** $f_1 = 1, f_2 = 1$

---

**For n = 2:**
$$f_2 = f_1 + f_0$$

We need: $1 = 1 + f_0$

**Therefore:** $f_0 = 0$ ✓

---

**Verification for n = 3:**
$$f_3 = f_2 + f_1 = 1 + 1 = 2$$

Using $f_0$: $f_3 = f_2 + f_1$ (doesn't involve $f_0$) ✓

---

**Extended Fibonacci Sequence:**

| n | -2 | -1 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|----|----|---|---|---|---|---|---|
| fₙ | -1 | 1 | 0 | 1 | 1 | 2 | 3 | 5 |

The recurrence works backwards too: $f_0 = f_1 - f_{-1} = 1 - 1 = 0$ ✓

---

### Exercise 6.1.2 - Derive F(x) = x/(1-x-x²) for Fibonacci

**Problem:** Derive the generating function for Fibonacci numbers.

**Solution:**

**Fibonacci:** $f_n = f_{n-1} + f_{n-2}$ with $f_0 = 0, f_1 = 1$

**Generating function:** $F(x) = \sum_{n=0}^{\infty} f_n x^n$

---

**Derivation:**

$$F(x) = f_0 + f_1 x + f_2 x^2 + f_3 x^3 + \cdots$$

$$= 0 + 1 \cdot x + f_2 x^2 + f_3 x^3 + \cdots$$

$$= x + \sum_{n=2}^{\infty} f_n x^n$$

---

**Use recurrence for n ≥ 2:**

$$\sum_{n=2}^{\infty} f_n x^n = \sum_{n=2}^{\infty} (f_{n-1} + f_{n-2}) x^n$$

$$= \sum_{n=2}^{\infty} f_{n-1} x^n + \sum_{n=2}^{\infty} f_{n-2} x^n$$

---

**First sum:** Let $m = n-1$

$$\sum_{n=2}^{\infty} f_{n-1} x^n = x \sum_{m=1}^{\infty} f_m x^m = x(F(x) - f_0) = xF(x)$$

---

**Second sum:** Let $m = n-2$

$$\sum_{n=2}^{\infty} f_{n-2} x^n = x^2 \sum_{m=0}^{\infty} f_m x^m = x^2 F(x)$$

---

**Combine:**

$$F(x) = x + xF(x) + x^2 F(x)$$

$$F(x) - xF(x) - x^2 F(x) = x$$

$$F(x)(1 - x - x^2) = x$$

---

**Solve for F(x):**

$$F(x) = \frac{x}{1 - x - x^2}$$ ✓

---

### Exercise 6.1.3 - Partial Fraction Decomposition of x/(1-x-x²)

**Problem:** Decompose $\frac{x}{1-x-x^2}$ into partial fractions.

**Solution:**

**Factor the denominator:**

$1 - x - x^2 = -(x^2 + x - 1)$

Roots of $x^2 + x - 1 = 0$:
$$x = \frac{-1 \pm \sqrt{5}}{2}$$

Let $\phi = \frac{1+\sqrt{5}}{2}$ and $\psi = \frac{1-\sqrt{5}}{2}$.

Then: $1 - x - x^2 = (1 - \phi x)(1 - \psi x)$

---

**Partial fraction form:**

$$\frac{x}{1-x-x^2} = \frac{x}{(1-\phi x)(1-\psi x)} = \frac{A}{1-\phi x} + \frac{B}{1-\psi x}$$

---

**Solve for A and B:**

$$x = A(1-\psi x) + B(1-\phi x)$$

Set $x = 1/\phi$:
$$\frac{1}{\phi} = A\left(1 - \frac{\psi}{\phi}\right) = A \cdot \frac{\phi - \psi}{\phi}$$

$$A = \frac{1}{\phi - \psi} = \frac{1}{\sqrt{5}}$$

Set $x = 1/\psi$:
$$\frac{1}{\psi} = B\left(1 - \frac{\phi}{\psi}\right) = B \cdot \frac{\psi - \phi}{\psi}$$

$$B = \frac{1}{\psi - \phi} = -\frac{1}{\sqrt{5}}$$

---

**Result:**

$$\frac{x}{1-x-x^2} = \frac{1}{\sqrt{5}}\left(\frac{1}{1-\phi x} - \frac{1}{1-\psi x}\right)$$ ✓

---

### Exercise 6.1.4 - Extract Coefficients to Get Binet Formula

**Problem:** Extract coefficients from the partial fraction to derive Binet's formula.

**Solution:**

**From partial fractions:**

$$F(x) = \frac{1}{\sqrt{5}}\left(\frac{1}{1-\phi x} - \frac{1}{1-\psi x}\right)$$

---

**Use geometric series:**

$$\frac{1}{1-\phi x} = \sum_{n=0}^{\infty} \phi^n x^n$$

$$\frac{1}{1-\psi x} = \sum_{n=0}^{\infty} \psi^n x^n$$

---

**Therefore:**

$$F(x) = \frac{1}{\sqrt{5}} \sum_{n=0}^{\infty} (\phi^n - \psi^n) x^n$$

---

**Coefficient of $x^n$:**

$$f_n = \frac{\phi^n - \psi^n}{\sqrt{5}}$$ ✓

This is the **Binet formula** for Fibonacci numbers!

---

**Verification for small n:**

| n | (φⁿ - ψⁿ)/√5 | fₙ |
|---|---------------|-----|
| 0 | (1-1)/√5 = 0 | 0 ✓ |
| 1 | (φ-ψ)/√5 = √5/√5 = 1 | 1 ✓ |
| 2 | (φ²-ψ²)/√5 = (φ-ψ)(φ+ψ)/√5 = √5·1/√5 = 1 | 1 ✓ |
| 3 | (φ³-ψ³)/√5 = 2 | 2 ✓ |
| 4 | (φ⁴-ψ⁴)/√5 = 3 | 3 ✓ |
| 5 | (φ⁵-ψ⁵)/√5 = 5 | 5 ✓ |

---

### Exercise 6.1.5 - Derive H(x) = x/[(1-x)(1-2x)] for Hanoi

**Problem:** Derive the generating function for Hanoi towers sequence.

**Solution:**

**Hanoi recurrence:** $h_{n+1} = 2h_n + 1$ with $h_1 = 1, h_0 = 0$

**Generating function:** $H(x) = \sum_{n=0}^{\infty} h_n x^n$

---

**Derivation:**

$$H(x) = h_0 + h_1 x + h_2 x^2 + h_3 x^3 + \cdots$$

$$= 0 + 1 \cdot x + h_2 x^2 + h_3 x^3 + \cdots$$

$$= x + \sum_{n=2}^{\infty} h_n x^n$$

---

**Use recurrence for n ≥ 1:**

$$h_{n+1} = 2h_n + 1$$

Multiply by $x^{n+1}$ and sum from $n=1$ to $\infty$:

$$\sum_{n=1}^{\infty} h_{n+1} x^{n+1} = 2 \sum_{n=1}^{\infty} h_n x^{n+1} + \sum_{n=1}^{\infty} x^{n+1}$$

---

**Left side:** Let $m = n+1$

$$\sum_{m=2}^{\infty} h_m x^m = H(x) - h_0 - h_1 x = H(x) - x$$

---

**First term on right:**

$$2 \sum_{n=1}^{\infty} h_n x^{n+1} = 2x \sum_{n=1}^{\infty} h_n x^n = 2x(H(x) - h_0) = 2xH(x)$$

---

**Second term on right:**

$$\sum_{n=1}^{\infty} x^{n+1} = x^2 + x^3 + x^4 + \cdots = \frac{x^2}{1-x}$$

---

**Combine:**

$$H(x) - x = 2xH(x) + \frac{x^2}{1-x}$$

$$H(x) - 2xH(x) = x + \frac{x^2}{1-x}$$

$$H(x)(1-2x) = \frac{x(1-x) + x^2}{1-x} = \frac{x}{1-x}$$

---

**Solve for H(x):**

$$H(x) = \frac{x}{(1-x)(1-2x)}$$ ✓

---

### Exercise 6.1.6 - Partial Fractions for H(x)

**Problem:** Decompose $\frac{x}{(1-x)(1-2x)}$ into partial fractions.

**Solution:**

**Form:**

$$\frac{x}{(1-x)(1-2x)} = \frac{A}{1-x} + \frac{B}{1-2x}$$

---

**Solve for A and B:**

$$x = A(1-2x) + B(1-x)$$

Set $x = 1$:
$$1 = A(1-2) + B(0) = -A$$
$$A = -1$$

Set $x = 1/2$:
$$1/2 = A(0) + B(1-1/2) = B/2$$
$$B = 1$$

---

**Result:**

$$\frac{x}{(1-x)(1-2x)} = \frac{1}{1-2x} - \frac{1}{1-x}$$ ✓

---

### Exercise 6.1.7 - Extract Coefficients to Get hₙ = 2ⁿ - 1

**Problem:** Extract coefficients from H(x) to find the closed form.

**Solution:**

**From partial fractions:**

$$H(x) = \frac{1}{1-2x} - \frac{1}{1-x}$$

---

**Use geometric series:**

$$\frac{1}{1-2x} = \sum_{n=0}^{\infty} (2x)^n = \sum_{n=0}^{\infty} 2^n x^n$$

$$\frac{1}{1-x} = \sum_{n=0}^{\infty} x^n$$

---

**Therefore:**

$$H(x) = \sum_{n=0}^{\infty} 2^n x^n - \sum_{n=0}^{\infty} x^n = \sum_{n=0}^{\infty} (2^n - 1) x^n$$

---

**Coefficient of $x^n$:**

$$h_n = 2^n - 1$$ ✓

---

**Verification:**

| n | 2ⁿ - 1 | hₙ (from recurrence) |
|---|--------|---------------------|
| 0 | 1 - 1 = 0 | 0 ✓ |
| 1 | 2 - 1 = 1 | 1 ✓ |
| 2 | 4 - 1 = 3 | 3 ✓ |
| 3 | 8 - 1 = 7 | 7 ✓ |
| 4 | 16 - 1 = 15 | 15 ✓ |
| 5 | 32 - 1 = 31 | 31 ✓ |

---

## Section 6.2 - Newton Binomiális Sora

---

### Exercise 6.2.1 - Prove: (1-x)⁻ᵏ = Σ C(n+k-1, k-1) xⁿ

**Problem:** Prove the negative binomial series formula.

**Solution:**

**Theorem:**
$$(1-x)^{-k} = \sum_{n=0}^{\infty} \binom{n+k-1}{k-1} x^n$$

---

**Proof using Generalized Binomial Theorem:**

$$(1-x)^{-k} = \sum_{n=0}^{\infty} \binom{-k}{n} (-x)^n$$

---

**Compute $\binom{-k}{n}$:**

$$\binom{-k}{n} = \frac{(-k)(-k-1)(-k-2)\cdots(-k-n+1)}{n!}$$

$$= \frac{(-1)^n \cdot k(k+1)(k+2)\cdots(k+n-1)}{n!}$$

$$= (-1)^n \cdot \frac{(k+n-1)!}{(k-1)! \cdot n!}$$

$$= (-1)^n \binom{n+k-1}{k-1}$$

---

**Substitute back:**

$$(1-x)^{-k} = \sum_{n=0}^{\infty} (-1)^n \binom{n+k-1}{k-1} (-x)^n$$

$$= \sum_{n=0}^{\infty} (-1)^n \binom{n+k-1}{k-1} (-1)^n x^n$$

$$= \sum_{n=0}^{\infty} \binom{n+k-1}{k-1} x^n$$ ✓

---

**Example (k=2):**

$$(1-x)^{-2} = \sum_{n=0}^{\infty} \binom{n+1}{1} x^n = \sum_{n=0}^{\infty} (n+1) x^n$$

$$= 1 + 2x + 3x^2 + 4x^3 + \cdots$$

**Verification:** $\frac{d}{dx}\left(\frac{1}{1-x}\right) = \frac{1}{(1-x)^2}$ ✓

---

### Exercise 6.2.2 - Expand (1+x)⁻¹/² Using Generalized Binomial

**Problem:** Expand $(1+x)^{-1/2}$ using generalized binomial coefficients.

**Solution:**

**Generalized Binomial Theorem:**

$$(1+x)^{\alpha} = \sum_{n=0}^{\infty} \binom{\alpha}{n} x^n$$

For $\alpha = -1/2$:

$$(1+x)^{-1/2} = \sum_{n=0}^{\infty} \binom{-1/2}{n} x^n$$

---

**Compute $\binom{-1/2}{n}$:**

$$\binom{-1/2}{n} = \frac{(-1/2)(-3/2)(-5/2)\cdots(-(2n-1)/2)}{n!}$$

$$= \frac{(-1)^n \cdot 1 \cdot 3 \cdot 5 \cdots (2n-1)}{2^n \cdot n!}$$

$$= \frac{(-1)^n (2n-1)!!}{2^n n!}$$

where $(2n-1)!! = 1 \cdot 3 \cdot 5 \cdots (2n-1)$ is the double factorial.

---

**Alternative form:**

$$(2n-1)!! = \frac{(2n)!}{2^n n!}$$

Therefore:

$$\binom{-1/2}{n} = \frac{(-1)^n (2n)!}{2^n n! \cdot 2^n n!} = (-1)^n \frac{\binom{2n}{n}}{4^n}$$

---

**Result:**

$$(1+x)^{-1/2} = \sum_{n=0}^{\infty} (-1)^n \frac{\binom{2n}{n}}{4^n} x^n$$

$$= 1 - \frac{1}{2}x + \frac{3}{8}x^2 - \frac{5}{16}x^3 + \frac{35}{128}x^4 - \cdots$$

---

**Verification (x = 0.25):**

$(1+0.25)^{-1/2} = (1.25)^{-1/2} \approx 0.8944$

Series: $1 - 0.125 + 0.0234 - 0.0049 + 0.0011 - \cdots \approx 0.8944$ ✓

---

### Exercise 6.2.3 - Show: C(-1/2, n) = (-1)ⁿ C(2n,n)/4ⁿ

**Problem:** Prove the identity for generalized binomial coefficients.

**Solution:**

**To prove:**
$$\binom{-1/2}{n} = (-1)^n \frac{\binom{2n}{n}}{4^n}$$

---

**Proof:**

$$\binom{-1/2}{n} = \frac{(-1/2)(-3/2)(-5/2)\cdots(-(2n-1)/2)}{n!}$$

Factor out $(-1/2)$ from each term:

$$= \frac{(-1)^n}{2^n n!} \cdot 1 \cdot 3 \cdot 5 \cdots (2n-1)$$

$$= \frac{(-1)^n (2n-1)!!}{2^n n!}$$

---

**Convert double factorial:**

$$(2n-1)!! = \frac{(2n)!}{(2n)!!} = \frac{(2n)!}{2^n n!}$$

---

**Substitute:**

$$\binom{-1/2}{n} = \frac{(-1)^n}{2^n n!} \cdot \frac{(2n)!}{2^n n!}$$

$$= (-1)^n \frac{(2n)!}{4^n (n!)^2}$$

$$= (-1)^n \frac{\binom{2n}{n}}{4^n}$$ ✓

---

## Section 6.3 - Nemlineáris rekurziók (Nonlinear Recurrences)

---

### Exercise 6.3.1 - Derive C(x) = 1 + xC(x)² for Catalan Numbers

**Problem:** Derive the generating function equation for Catalan numbers.

**Solution:**

**Catalan Recurrence:**
$$C_0 = 1, \quad C_{n+1} = \sum_{i=0}^{n} C_i C_{n-i} \text{ for } n \geq 0$$

**Generating function:** $C(x) = \sum_{n=0}^{\infty} C_n x^n$

---

**Derivation:**

$$C(x) = C_0 + \sum_{n=0}^{\infty} C_{n+1} x^{n+1}$$

$$= 1 + \sum_{n=0}^{\infty} \left(\sum_{i=0}^{n} C_i C_{n-i}\right) x^{n+1}$$

---

**Recognize convolution:**

The inner sum $\sum_{i=0}^{n} C_i C_{n-i}$ is the coefficient of $x^n$ in $C(x)^2$.

Therefore:
$$\sum_{n=0}^{\infty} \left(\sum_{i=0}^{n} C_i C_{n-i}\right) x^{n+1} = x \cdot C(x)^2$$

---

**Result:**

$$C(x) = 1 + x C(x)^2$$ ✓

---

### Exercise 6.3.2 - Solve Quadratic for C(x)

**Problem:** Solve $C(x) = 1 + xC(x)^2$ for $C(x)$.

**Solution:**

**Equation:**
$$xC(x)^2 - C(x) + 1 = 0$$

This is a quadratic in $C(x)$.

---

**Quadratic formula:**

$$C(x) = \frac{1 \pm \sqrt{1 - 4x}}{2x}$$

---

**Two solutions:**
- $C_+(x) = \frac{1 + \sqrt{1-4x}}{2x}$
- $C_-(x) = \frac{1 - \sqrt{1-4x}}{2x}$

---

**Determine which is correct:**

We need $C(0) = C_0 = 1$.

**For $C_+(x)$:** As $x \to 0$, numerator $\to 2$, so $C_+(x) \to \infty$. ✗

**For $C_-(x)$:** Use L'Hôpital's rule:

$$\lim_{x \to 0} \frac{1 - \sqrt{1-4x}}{2x} = \lim_{x \to 0} \frac{\frac{2}{\sqrt{1-4x}}}{2} = 1$$ ✓

---

**Therefore:**
$$C(x) = \frac{1 - \sqrt{1-4x}}{2x}$$ ✓

---

### Exercise 6.3.3 - Extract Coefficients to Get Cₙ = (1/(n+1))C(2n,n)

**Problem:** Extract coefficients from $C(x)$ to find the closed form for Catalan numbers.

**Solution:**

**Generating function:**
$$C(x) = \frac{1 - \sqrt{1-4x}}{2x}$$

---

**Expand $\sqrt{1-4x}$:**

Using $(1+x)^{-1/2}$ with $x \to -4x$:

$$\sqrt{1-4x} = (1-4x)^{1/2} = \sum_{n=0}^{\infty} \binom{1/2}{n} (-4x)^n$$

$$= 1 + \sum_{n=1}^{\infty} \binom{1/2}{n} (-4)^n x^n$$

---

**Compute $\binom{1/2}{n}$:**

$$\binom{1/2}{n} = \frac{(1/2)(-1/2)(-3/2)\cdots(-(2n-3)/2)}{n!}$$

$$= \frac{(-1)^{n-1} (2n-3)!!}{2^n n!}$$

For $n \geq 1$.

---

**Therefore:**

$$1 - \sqrt{1-4x} = -\sum_{n=1}^{\infty} \binom{1/2}{n} (-4)^n x^n$$

$$= \sum_{n=1}^{\infty} \frac{(2n-3)!!}{2^n n!} 4^n x^n$$

$$= \sum_{n=1}^{\infty} \frac{(2n-3)!! \cdot 2^n}{n!} x^n$$

---

**Divide by 2x:**

$$C(x) = \frac{1}{2} \sum_{n=1}^{\infty} \frac{(2n-3)!! \cdot 2^n}{n!} x^{n-1}$$

Let $m = n-1$:

$$= \sum_{m=0}^{\infty} \frac{(2m-1)!! \cdot 2^m}{2(m+1)!} x^m$$

---

**Simplify using $(2m-1)!! = \frac{(2m)!}{2^m m!}$:**

$$C_m = \frac{(2m)!}{2^m m!} \cdot \frac{2^m}{2(m+1)!} = \frac{(2m)!}{2 \cdot m! \cdot (m+1)!}$$

$$= \frac{1}{m+1} \cdot \frac{(2m)!}{m! \cdot m!} = \frac{1}{m+1} \binom{2m}{m}$$

---

**Result:**
$$C_n = \frac{1}{n+1} \binom{2n}{n}$$ ✓

---

**Verification:**

| n | C(2n,n)/(n+1) | Cₙ |
|---|---------------|-----|
| 0 | 1/1 = 1 | 1 ✓ |
| 1 | 2/2 = 1 | 1 ✓ |
| 2 | 6/3 = 2 | 2 ✓ |
| 3 | 20/4 = 5 | 5 ✓ |
| 4 | 70/5 = 14 | 14 ✓ |
| 5 | 252/6 = 42 | 42 ✓ |

---

## Section 6.4 - Feladatok (Formal Exercises)

---

### 6.1. Feladat - Plane Regions (Sikresz) via Generating Functions

**Problem:** Solve the problem from Chapter 5.3 using generating functions. If $c_n$ denotes the number of plane regions created by $n$ lines in general position, then $c_0 = 1$, and each new line crosses the previous $n$ lines creating $n+1$ new regions, giving the recurrence:

$$c_{n+1} = c_n + 1 + n \quad (n \in \mathbb{N})$$

Find the generating function $F(x) = \sum_{n=0}^{\infty} c_n x^n$ and extract the closed form.

**Solution:**

**Step 1: Set up the generating function equation.**

We have $c_{n+1} = c_n + n + 1$ for $n \geq 0$, with $c_0 = 1$.

Multiply both sides by $x^{n+1}$ and sum over $n \geq 0$:

$$\sum_{n=0}^{\infty} c_{n+1} x^{n+1} = \sum_{n=0}^{\infty} c_n x^{n+1} + \sum_{n=0}^{\infty} n x^{n+1} + \sum_{n=0}^{\infty} x^{n+1}$$

**Step 2: Evaluate each sum.**

**Left side:**
$$\sum_{n=0}^{\infty} c_{n+1} x^{n+1} = \sum_{m=1}^{\infty} c_m x^m = F(x) - c_0 = F(x) - 1$$

**First term on right:**
$$\sum_{n=0}^{\infty} c_n x^{n+1} = x F(x)$$

**Second term on right:**
$$\sum_{n=0}^{\infty} n x^{n+1} = x \sum_{n=0}^{\infty} n x^n = x \cdot \frac{x}{(1-x)^2} = \frac{x^2}{(1-x)^2}$$

(using the known identity $\sum_{n=0}^{\infty} n x^n = \frac{x}{(1-x)^2}$)

**Third term on right:**
$$\sum_{n=0}^{\infty} x^{n+1} = \frac{x}{1-x}$$

**Step 3: Combine and solve for $F(x)$.**

$$F(x) - 1 = x F(x) + \frac{x^2}{(1-x)^2} + \frac{x}{1-x}$$

$$F(x)(1 - x) = 1 + \frac{x^2}{(1-x)^2} + \frac{x}{1-x}$$

Combine the right side over a common denominator $(1-x)^2$:

$$F(x)(1-x) = \frac{(1-x)^2 + x^2 + x(1-x)}{(1-x)^2}$$

Expand the numerator:

$$(1-x)^2 + x^2 + x(1-x) = 1 - 2x + x^2 + x^2 + x - x^2 = 1 - x + x^2$$

Therefore:

$$F(x) = \frac{1 - x + x^2}{(1-x)^3}$$

**Step 4: Partial fraction decomposition.**

We write:

$$F(x) = \frac{1 - x + x^2}{(1-x)^3}$$

Perform polynomial long division or decompose directly. Since $\deg(\text{num}) < \deg(\text{den})$, we write:

$$\frac{1 - x + x^2}{(1-x)^3} = \frac{A}{1-x} + \frac{B}{(1-x)^2} + \frac{C}{(1-x)^3}$$

Multiplying both sides by $(1-x)^3$:

$$1 - x + x^2 = A(1-x)^2 + B(1-x) + C$$

Set $x = 1$: $1 - 1 + 1 = C$, so $C = 1$.

Expand: $A(1 - 2x + x^2) + B(1 - x) + 1 = A + B + 1 + (-2A - B)x + Ax^2$

Comparing coefficients:
- $x^0$: $1 = A + B + 1$, so $A + B = 0$
- $x^1$: $-1 = -2A - B$
- $x^2$: $1 = A$

From $A = 1$: $B = -1$.

Check: $-2(1) - (-1) = -1$. Correct.

$$F(x) = \frac{1}{1-x} - \frac{1}{(1-x)^2} + \frac{1}{(1-x)^3}$$

**Step 5: Extract coefficients.**

Using the known expansions:

$$\frac{1}{(1-x)^k} = \sum_{n=0}^{\infty} \binom{n+k-1}{k-1} x^n$$

We get:

$$[x^n] \frac{1}{1-x} = 1$$

$$[x^n] \frac{1}{(1-x)^2} = n + 1$$

$$[x^n] \frac{1}{(1-x)^3} = \binom{n+2}{2} = \frac{(n+1)(n+2)}{2}$$

Therefore:

$$c_n = 1 - (n+1) + \frac{(n+1)(n+2)}{2}$$

$$= 1 - n - 1 + \frac{n^2 + 3n + 2}{2}$$

$$= \frac{n^2 + 3n + 2 - 2n}{2} = \frac{n^2 + n + 2}{2}$$

---

**Result:**

$$c_n = \frac{n^2 + n + 2}{2} = \frac{n(n+1)}{2} + 1 = \binom{n}{2} + n + 1$$

---

**Verification:**

| n | $\frac{n^2+n+2}{2}$ | $c_n$ (from recurrence) |
|---|---------------------|------------------------|
| 0 | 1 | 1 |
| 1 | 2 | 2 |
| 2 | 4 | 4 |
| 3 | 7 | 7 |
| 4 | 11 | 11 |
| 5 | 16 | 16 |

All match. This confirms the result from Chapter 5, now derived via generating functions.

---

### 6.2. Feladat - Parenthesizations of a Product (Catalan Numbers)

**Problem:** In how many ways can we parenthesize an $n$-factor product $a_1 \cdot a_2 \cdots a_n$, where the binary operation $\cdot$ is not necessarily associative?

**Solution:**

**Step 1: Define the sequence.**

Let $b_n$ denote the number of ways to fully parenthesize a product of $n$ factors. In the last multiplication performed, the two sub-products consist of the first $i$ factors and the last $n - i$ factors, for some $1 \leq i \leq n-1$:

$$(a_1 \cdots a_i) \cdot (a_{i+1} \cdots a_n)$$

The number of ways to parenthesize each part is $b_i$ and $b_{n-i}$ respectively, so:

$$b_n = \sum_{i=1}^{n-1} b_i \cdot b_{n-i} \quad (n \geq 2)$$

with $b_1 = 1$ (a single factor needs no parentheses).

**Step 2: Reduce to Catalan recurrence.**

Define $b'_n := b_{n+1}$ for $n \geq 0$, so $b'_0 = b_1 = 1$. Then:

$$b'_{n} = b_{n+1} = \sum_{i=1}^{n} b_i \cdot b_{n+1-i} = \sum_{i=0}^{n-1} b'_i \cdot b'_{n-1-i}$$

Rewriting with index shift, this becomes:

$$b'_{n+1} = \sum_{i=0}^{n} b'_i \cdot b'_{n-i} \quad (n \geq 0), \quad b'_0 = 1$$

This is exactly the Catalan recurrence (6.14) from the chapter! Therefore $b'_n = t_n = C_n$, the $n$-th Catalan number.

**Step 3: Apply the Catalan formula.**

Since $b_n = b'_{n-1} = t_{n-1} = C_{n-1}$:

$$b_n = \frac{1}{n} \binom{2n-2}{n-1} \quad (n \geq 1)$$

---

**Result:**

$$b_n = C_{n-1} = \frac{1}{n}\binom{2n-2}{n-1}$$

---

**Verification:**

| n | $b_n$ | Parenthesizations |
|---|-------|-------------------|
| 1 | 1 | $a_1$ |
| 2 | 1 | $(a_1 \cdot a_2)$ |
| 3 | 2 | $((a_1 \cdot a_2) \cdot a_3)$, $(a_1 \cdot (a_2 \cdot a_3))$ |
| 4 | 5 | All 5 binary trees with 3 internal nodes |
| 5 | 14 | $C_4 = 14$ |

These match the known Catalan numbers $C_0 = 1, C_1 = 1, C_2 = 2, C_3 = 5, C_4 = 14$.

**Generating function approach:** Let $B(x) = \sum_{n=1}^{\infty} b_n x^n$. From the convolution recurrence:

$$B(x) = x + B(x)^2$$

Solving: $B(x) = \frac{1 - \sqrt{1 - 4x}}{2}$, confirming $b_n = C_{n-1}$ by coefficient extraction.

---

### 6.3. Feladat - Triangulations of a Convex Polygon

**Problem:** How many ways can a convex $(n+2)$-gon be triangulated using non-crossing diagonals? (The polygon's vertices are numbered, i.e., rotations are considered distinct.)

**Solution:**

**Step 1: Define the sequence.**

Let $c_n$ denote the number of triangulations of a convex $(n+2)$-gon ($n \geq 1$), and set $c_0 = 1$ (degenerate case: a "2-gon" has one trivial triangulation, or equivalently, the empty triangulation).

Clearly $c_1 = 1$ (a triangle has exactly one triangulation -- itself).

**Step 2: Derive the recurrence.**

Fix one edge of the $(n+2)$-gon, say the edge between vertex $n+1$ and vertex $n+2$. Every triangulation contains exactly one triangle that uses this edge. The third vertex of this triangle is some vertex $s$, where $1 \leq s \leq n$.

This triangle divides the polygon into two smaller polygons:
- A polygon with $s + 1$ vertices (vertices $n+2, 1, 2, \ldots, s$) -- this is an $(s+1)$-gon, which has $c_{s-1}$ triangulations.
- A polygon with $n - s + 2$ vertices (vertices $s, s+1, \ldots, n+1$) -- this is an $(n-s+2)$-gon, which has $c_{n-s}$ triangulations.

Since the two parts are independent:

$$c_n = \sum_{s=1}^{n} c_{s-1} \cdot c_{n-s} \quad (n \geq 1)$$

Substituting $i = s - 1$:

$$c_n = \sum_{i=0}^{n-1} c_i \cdot c_{n-1-i}$$

This is equivalent to:

$$c_{n+1} = \sum_{i=0}^{n} c_i \cdot c_{n-i} \quad (n \geq 0), \quad c_0 = 1$$

**Step 3: Recognize the Catalan recurrence.**

This is precisely the Catalan number recurrence (6.14). Therefore $c_n = t_n = C_n$.

**Step 4: Apply the generating function result.**

From the chapter, the generating function is:

$$C(x) = \frac{1 - \sqrt{1-4x}}{2x}$$

and the closed-form is:

$$c_n = C_n = \frac{1}{n+1}\binom{2n}{n}$$

---

**Result:**

The number of triangulations of a convex $(n+2)$-gon is:

$$c_n = \frac{1}{n+1}\binom{2n}{n}$$

---

**Verification:**

| Polygon | n | $C_n$ | Triangulations |
|---------|---|-------|---------------|
| Triangle (3-gon) | 1 | 1 | 1 (itself) |
| Quadrilateral (4-gon) | 2 | 2 | 2 diagonals, each giving 1 triangulation |
| Pentagon (5-gon) | 3 | 5 | 5 distinct triangulations |
| Hexagon (6-gon) | 4 | 14 | 14 distinct triangulations |

---

### 6.4. Feladat - Non-crossing Chord Pairings on a Circle

**Problem:** In how many ways can we connect $2n$ points on a circle pairwise with $n$ chords such that the chords do not cross each other?

**Solution:**

**Step 1: Define the sequence.**

Let $d_n$ denote the number of non-crossing perfect matchings of $2n$ points arranged on a circle. Clearly $d_0 = 1$ (empty matching) and $d_1 = 1$ (the single pair).

**Step 2: Derive the recurrence.**

Label the points $1, 2, \ldots, 2n$ around the circle. Consider point 1. It must be matched to some point $2k$ for $1 \leq k \leq n$ (it must be matched to an even-numbered point, because the chord from 1 to $2k$ separates the remaining points into two groups of even size).

More precisely, if point 1 is connected to point $2k$, then:
- The chord $(1, 2k)$ encloses points $2, 3, \ldots, 2k-1$ on one side (this is $2k - 2$ points, which must be matched among themselves): $d_{k-1}$ ways.
- On the other side, we have points $2k+1, 2k+2, \ldots, 2n$ (this is $2n - 2k$ points): $d_{n-k}$ ways.

Therefore:

$$d_n = \sum_{k=1}^{n} d_{k-1} \cdot d_{n-k} \quad (n \geq 1)$$

Substituting $i = k - 1$:

$$d_n = \sum_{i=0}^{n-1} d_i \cdot d_{n-1-i}$$

Equivalently:

$$d_{n+1} = \sum_{i=0}^{n} d_i \cdot d_{n-i} \quad (n \geq 0), \quad d_0 = 1$$

**Step 3: Recognize the Catalan recurrence.**

This is again exactly the Catalan recurrence (6.14)!

**Step 4: Generating function and closed form.**

The generating function is $D(x) = C(x) = \frac{1 - \sqrt{1 - 4x}}{2x}$, so:

$$d_n = C_n = \frac{1}{n+1}\binom{2n}{n}$$

---

**Result:**

$$d_n = \frac{1}{n+1}\binom{2n}{n}$$

---

**Verification:**

| $2n$ points | $n$ | $d_n$ | Description |
|-------------|-----|-------|-------------|
| 0 | 0 | 1 | Empty matching |
| 2 | 1 | 1 | One chord |
| 4 | 2 | 2 | Two non-crossing chord patterns |
| 6 | 3 | 5 | Five non-crossing perfect matchings |
| 8 | 4 | 14 | Fourteen non-crossing perfect matchings |

**Example for $n = 2$ (4 points labeled 1,2,3,4):** The two non-crossing matchings are $\{(1,2),(3,4)\}$ and $\{(1,4),(2,3)\}$. The matching $\{(1,3),(2,4)\}$ has crossing chords, so it is excluded. Count = 2 = $C_2$.

**Connection to other Catalan structures:** Non-crossing chord diagrams on $2n$ points are in bijection with:
- Triangulations of an $(n+2)$-gon (Exercise 6.3)
- Parenthesizations of an $(n+1)$-factor product (Exercise 6.2)
- Dyck paths of length $2n$
- Binary trees with $n$ internal nodes

---

### 6.5. Feladat - Non-negative Integer Solutions of $y_1 + \ldots + y_k = n$

**Problem:** How many non-negative integer solutions does the equation $y_1 + y_2 + \ldots + y_k = n$ have, for arbitrary $n \in \mathbb{N}$ and fixed $k$?

**Solution:**

**Step 1: Identify the generating function.**

This is a special case of the coin-change problem (6.11 Penzvaltas problema) with $h_1 = h_2 = \ldots = h_k = 1$.

By Theorem 6.12, the generating function for the number of solutions $a_n$ is:

$$F(x) = \frac{1}{(1 - x^{h_1})(1 - x^{h_2}) \cdots (1 - x^{h_k})}$$

With $h_1 = h_2 = \ldots = h_k = 1$:

$$F(x) = \frac{1}{(1-x)^k}$$

**Step 2: Expand using the negative binomial series.**

From Exercise 6.2.1 (proved earlier in the chapter), we have:

$$(1-x)^{-k} = \sum_{n=0}^{\infty} \binom{n+k-1}{k-1} x^n$$

**Step 3: Extract the coefficient.**

The coefficient of $x^n$ gives us the number of solutions:

$$a_n = \binom{n+k-1}{k-1}$$

---

**Result:**

$$C_k^{n\;(ism)} = \binom{n+k-1}{k-1}$$

This is the formula for combinations with repetition -- choosing $n$ items from $k$ types with unlimited repetition. This result matches the well-known "stars and bars" formula from combinatorics.

---

**Verification:**

**Case $k = 2$, $n = 3$:** Solutions of $y_1 + y_2 = 3$:

$(0,3), (1,2), (2,1), (3,0)$ -- that is 4 solutions.

$$\binom{3+2-1}{2-1} = \binom{4}{1} = 4 \quad \checkmark$$

**Case $k = 3$, $n = 2$:** Solutions of $y_1 + y_2 + y_3 = 2$:

$(2,0,0), (0,2,0), (0,0,2), (1,1,0), (1,0,1), (0,1,1)$ -- that is 6 solutions.

$$\binom{2+3-1}{3-1} = \binom{4}{2} = 6 \quad \checkmark$$

**Case $k = 1$, $n = n$:** Only solution is $y_1 = n$, count = 1.

$$\binom{n+0}{0} = 1 \quad \checkmark$$

---

**Alternative derivation (direct combinatorial):**

Represent each solution as a sequence of $n$ stars and $k-1$ bars. For example, for $k=3, n=4$: $\star\star|\star\star|$ represents $(2,2,0)$.

The number of arrangements is $\binom{n+k-1}{k-1}$, confirming the generating function result.

---

**Note:** The chapter text (p. 126) references this as $C_k^{n\;(ism)} = \binom{n+k-1}{k-1}$, confirming that this is the formula for combinations with repetition (ismetleses kombinacio). The generating function approach via $(1-x)^{-k}$ provides an elegant derivation that unifies with the coin-change problem framework.
