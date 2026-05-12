# Exercises 4.8-4.10 - Number Theory and Polynomial Identities

## Exercise 4.8 - Relatively Prime Numbers (Euler's φ-function)

### Problem Statement

Given natural numbers $M$ and $n$, how many natural numbers $\leq M$ are **relatively prime** to $n$?

Two numbers are relatively prime if their greatest common divisor is 1.

---

### Solution using Inclusion-Exclusion

**Setup:**
- Let $p_1, p_2, \ldots, p_r$ be the distinct prime divisors of $n$
- We want to count numbers $\leq M$ that are NOT divisible by any $p_i$

**Define bad sets:**
- $A_i$ = numbers $\leq M$ that are divisible by $p_i$

**Size of each set:**
$$|A_i| = \left\lfloor \frac{M}{p_i} \right\rfloor$$

**Intersections:**
$$|A_i \cap A_j| = \left\lfloor \frac{M}{p_i p_j} \right\rfloor$$

(and so on for higher intersections)

---

### Inclusion-Exclusion Formula

$$P = M - \sum_{i} \left\lfloor \frac{M}{p_i} \right\rfloor + \sum_{i < j} \left\lfloor \frac{M}{p_i p_j} \right\rfloor - \sum_{i < j < k} \left\lfloor \frac{M}{p_i p_j p_k} \right\rfloor + \cdots$$

Where $P$ is the count of numbers relatively prime to $n$.

---

### Compact Form

$$\boxed{P = \sum_{d | n^\infty} \mu(d) \left\lfloor \frac{M}{d} \right\rfloor}$$

where $\mu$ is the Möbius function and $d | n^\infty$ means $d$ is a product of distinct primes dividing $n$.

---

### Special Case: Euler's φ-function

When $M = n$, we get **Euler's totient function** $\phi(n)$:

$$\boxed{\phi(n) = n \prod_{p | n} \left(1 - \frac{1}{p}\right)}$$

**Derivation:**

$$\begin{aligned}
\phi(n) &= n - \sum_{p|n} \frac{n}{p} + \sum_{p<q|n} \frac{n}{pq} - \cdots \\[10pt]
&= n \left(1 - \sum_{p|n} \frac{1}{p} + \sum_{p<q|n} \frac{1}{pq} - \cdots\right) \\[10pt]
&= n \prod_{p|n} \left(1 - \frac{1}{p}\right)
\end{aligned}$$

---

### Example: $n = 210 = 2 \cdot 3 \cdot 5 \cdot 7$, $M = 10000$

**Primes:** $2, 3, 5, 7$

**Apply inclusion-exclusion:**

$$\begin{aligned}
P &= 10000 \\
&\quad - \left(\left\lfloor\frac{10000}{2}\right\rfloor + \left\lfloor\frac{10000}{3}\right\rfloor + \left\lfloor\frac{10000}{5}\right\rfloor + \left\lfloor\frac{10000}{7}\right\rfloor\right) \\
&\quad + \left(\left\lfloor\frac{10000}{6}\right\rfloor + \left\lfloor\frac{10000}{10}\right\rfloor + \left\lfloor\frac{10000}{14}\right\rfloor + \left\lfloor\frac{10000}{15}\right\rfloor + \left\lfloor\frac{10000}{21}\right\rfloor + \left\lfloor\frac{10000}{35}\right\rfloor\right) \\
&\quad - \left(\left\lfloor\frac{10000}{30}\right\rfloor + \left\lfloor\frac{10000}{42}\right\rfloor + \left\lfloor\frac{10000}{70}\right\rfloor + \left\lfloor\frac{10000}{105}\right\rfloor + \left\lfloor\frac{10000}{210}\right\rfloor\right) \\
&\quad + \left\lfloor\frac{10000}{210}\right\rfloor \\[10pt]
&= 10000 - (5000 + 3333 + 2000 + 1428) \\
&\quad + (1666 + 1000 + 714 + 666 + 476 + 285) \\
&\quad - (333 + 238 + 142 + 95 + 47) \\
&\quad + 47 \\[10pt]
&= 10000 - 11761 + 4807 - 855 + 47 \\[10pt]
&= \boxed{2285}
\end{aligned}$$

---

### Verification for φ(210)

$$\phi(210) = 210 \cdot \left(1 - \frac{1}{2}\right) \cdot \left(1 - \frac{1}{3}\right) \cdot \left(1 - \frac{1}{5}\right) \cdot \left(1 - \frac{1}{7}\right)$$

$$\phi(210) = 210 \cdot \frac{1}{2} \cdot \frac{2}{3} \cdot \frac{4}{5} \cdot \frac{6}{7} = 48$$

---

## Exercise 4.9 - Alternating Binomial Sum

### Problem Statement

Evaluate:
$$\sum_{i=0}^{n} (-1)^{n-i} \binom{n}{i} i^k$$

for various values of $k$.

---

### Solution

**Answer:**
$$\boxed{\sum_{i=0}^{n} (-1)^{n-i} \binom{n}{i} i^k = \begin{cases} 0 & \text{if } k < n \\ n! & \text{if } k = n \end{cases}}$$

---

### Proof 1: Using Surjections

Recall the surjection formula:
$$S(m, n) = \sum_{i=0}^{n} (-1)^{n-i} \binom{n}{i} i^m$$

**Case $k < n$:**
- No surjection exists from $k$ elements to $n$ elements when $k < n$
- Therefore $S(k, n) = 0$

**Case $k = n$:**
- Surjections from $n$ to $n$ are permutations
- Therefore $S(n, n) = n!$

---

### Proof 2: Using Derivatives

Consider $f(x) = (1+x)^n = \sum_{i=0}^{n} \binom{n}{i} x^i$.

Apply the operator $(x \frac{d}{dx})^k$ (differentiate $k$ times, multiplying by $x$ each time):

$$(x \frac{d}{dx})^k f(x) = \sum_{i=0}^{n} \binom{n}{i} i^k x^i$$

Now evaluate at $x = -1$:

$$\sum_{i=0}^{n} \binom{n}{i} i^k (-1)^i = \left[(x \frac{d}{dx})^k (1+x)^n\right]_{x=-1}$$

**Case $k < n$:**
- $(1+x)^n$ has a zero of order $n$ at $x = -1$
- After $k < n$ differentiations, it still vanishes at $x = -1$
- Result: $0$

**Case $k = n$:**
- After $n$ differentiations, we get $n!$ (the leading coefficient)
- Result: $(-1)^n \cdot n!$

Multiplying by $(-1)^n$ gives $n!$. ✓

---

### General Formula (Stirling Numbers)

For $k \geq n$:

$$\sum_{i=0}^{n} (-1)^{n-i} \binom{n}{i} i^k = n! \cdot \stirling{k}{n}$$

where $\stirling{k}{n}$ is the Stirling number of the second kind.

---

### Verification Table

| n | k | Sum | Expected |
|---|---|-----|----------|
| 2 | 1 | $-1\cdot 0 + 2\cdot 1 - 1\cdot 4 = -2$ | $0$ (k<n) ✗ |
| 2 | 2 | $1\cdot 0 - 2\cdot 1 + 1\cdot 4 = 2$ | $2! = 2$ ✓ |
| 3 | 2 | $-1\cdot 0 + 3\cdot 1 - 3\cdot 4 + 1\cdot 9 = 0$ | $0$ ✓ |
| 3 | 3 | $1\cdot 0 - 3\cdot 1 + 3\cdot 8 - 1\cdot 27 = 6$ | $3! = 6$ ✓ |

---

## Exercise 4.10 - Polynomial Expansion

### Problem Statement

Expand the polynomial:
$$\prod_{i=1}^{r} (1 - x_i) = (1-x_1)(1-x_2)\cdots(1-x_r)$$

---

### Solution

**Expansion:**

$$\boxed{\prod_{i=1}^{r} (1 - x_i) = 1 - \sum_{i} x_i + \sum_{i < j} x_i x_j - \sum_{i < j < k} x_i x_j x_k + \cdots + (-1)^r x_1 x_2 \cdots x_r}$$

---

### Proof by Induction

**Base case ($r = 1$):**
$$(1 - x_1) = 1 - x_1$$ ✓

**Inductive step:**

Assume true for $r$. For $r+1$:

$$\begin{aligned}
\prod_{i=1}^{r+1} (1 - x_i) &= \left(\prod_{i=1}^{r} (1 - x_i)\right) \cdot (1 - x_{r+1}) \\[10pt]
&= \left(1 - \sum_{i=1}^{r} x_i + \sum_{i<j}^{r} x_i x_j - \cdots + (-1)^r x_1\cdots x_r\right) \cdot (1 - x_{r+1})
\end{aligned}$$

Distributing:
- Terms without $x_{r+1}$: same as before
- Terms with $x_{r+1}$: multiply each by $-x_{r+1}$

This produces exactly the formula for $r+1$ variables. ✓

---

### Connection to Inclusion-Exclusion

This expansion is the algebraic foundation of inclusion-exclusion!

If we set $x_i$ to represent "property $i$ is present", then:
- $1$ = nothing excluded
- $-\sum x_i$ = subtract single properties
- $+\sum x_i x_j$ = add back double intersections
- etc.

---

### Special Case: All Variables Equal

If $x_1 = x_2 = \cdots = x_r = x$:

$$(1-x)^r = \sum_{k=0}^{r} (-1)^k \binom{r}{k} x^k$$

This is the binomial theorem! ✓

---

## Summary

| Exercise | Topic | Key Result |
|----------|-------|------------|
| **4.8** | Relatively prime numbers | $P = \sum \mu(d) \lfloor M/d \rfloor$ |
| | Euler's φ-function | $\phi(n) = n \prod_{p|n} (1 - 1/p)$ |
| **4.9** | Alternating binomial sum | $0$ if $k < n$, $n!$ if $k = n$ |
| **4.10** | Polynomial expansion | $\prod (1-x_i) = 1 - \sum x_i + \sum x_i x_j - \cdots$ |

---

*Exercises 4.8-4.10 from Chapter 04 - A logikai szitaformula*
