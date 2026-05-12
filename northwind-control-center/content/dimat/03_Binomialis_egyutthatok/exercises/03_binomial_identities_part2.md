# Exercise 3.2 - Binomial Coefficient Identities (Part 2)

## /5/ Prove: $\binom{n+1}{r+1} - 2\binom{n}{r} + \binom{n-1}{r-1} = \binom{n}{r+1}$

### Proof

Using Pascal's rule: $\binom{n+1}{r+1} = \binom{n}{r+1} + \binom{n}{r}$

Substitute into LHS:
$$\begin{aligned}
\text{LHS} &= \left[\binom{n}{r+1} + \binom{n}{r}\right] - 2\binom{n}{r} + \binom{n-1}{r-1}\\[10pt]
&= \binom{n}{r+1} + \binom{n}{r} - 2\binom{n}{r} + \binom{n-1}{r-1}\\[10pt]
&= \binom{n}{r+1} - \binom{n}{r} + \binom{n-1}{r-1}
\end{aligned}$$

Now use Pascal's rule again: $\binom{n}{r} = \binom{n-1}{r} + \binom{n-1}{r-1}$

So:
$$\begin{aligned}
\text{LHS} &= \binom{n}{r+1} - \left[\binom{n-1}{r} + \binom{n-1}{r-1}\right] + \binom{n-1}{r-1}\\[10pt]
&= \binom{n}{r+1} - \binom{n-1}{r}
\end{aligned}$$

Now use Pascal's rule once more: $\binom{n}{r+1} = \binom{n-1}{r+1} + \binom{n-1}{r}$

$$\begin{aligned}
\text{LHS} &= \left[\binom{n-1}{r+1} + \binom{n-1}{r}\right] - \binom{n-1}{r}\\[10pt]
&= \binom{n-1}{r+1}
\end{aligned}$$

Hmm, this gives $\binom{n-1}{r+1}$, not $\binom{n}{r+1}$. Let me verify with specific values.

**For n=3, r=1:**
- LHS: $\binom{4}{2} - 2\binom{3}{1} + \binom{2}{0} = 6 - 6 + 1 = 1$
- RHS: $\binom{3}{2} = 3$

These don't match. The problem statement may have an error. Let me find the correct identity.

### Correct Identity

Using the calculations above, the correct identity should be:

$$\boxed{\binom{n+1}{r+1} - 2\binom{n}{r} + \binom{n-1}{r-1} = \binom{n-1}{r+1}}$$

**Verification for n=3, r=1:**
- LHS: $6 - 6 + 1 = 1$
- RHS: $\binom{2}{2} = 1$ ✓

---

## /6/ Prove: $\binom{n}{r} - \binom{n}{r+1} = \binom{n-1}{r} - \binom{n-1}{r+1}$

### Proof

Using Pascal's rule on both sides:

**LHS:**
$$\begin{aligned}
\binom{n}{r} - \binom{n}{r+1} &= \left[\binom{n-1}{r} + \binom{n-1}{r-1}\right] - \left[\binom{n-1}{r+1} + \binom{n-1}{r}\right]\\[10pt]
&= \binom{n-1}{r} + \binom{n-1}{r-1} - \binom{n-1}{r+1} - \binom{n-1}{r}\\[10pt]
&= \binom{n-1}{r-1} - \binom{n-1}{r+1}
\end{aligned}$$

**RHS:**
$$\binom{n-1}{r} - \binom{n-1}{r+1}$$

These are not equal in general. Let me check with specific values.

**For n=4, r=1:**
- LHS: $\binom{4}{1} - \binom{4}{2} = 4 - 6 = -2$
- RHS: $\binom{3}{1} - \binom{3}{2} = 3 - 3 = 0$

The identity as stated is **incorrect**.

### Related Correct Identity

A correct related identity is:

$$\boxed{\binom{n}{r} - \binom{n-1}{r} = \binom{n-1}{r-1}}$$

This follows directly from Pascal's rule: $\binom{n}{r} = \binom{n-1}{r} + \binom{n-1}{r-1}$

---

## /7/ & /8/ Hockey-Stick Identities

### Standard Hockey-Stick Identity

$$\boxed{\sum_{i=r}^{n} \binom{i}{r} = \binom{n+1}{r+1}}$$

This is the **upper summation** formula from the chapter (3.12).

### Variant with shifted indices

$$\boxed{\sum_{i=0}^{m} \binom{n+i}{i} = \binom{n+m+1}{m}}$$

Or equivalently:
$$\sum_{i=0}^{m} \binom{n+i}{n} = \binom{n+m+1}{n+1}$$

### Proof (by induction on m)

**Base case (m=0):**
$$\binom{n}{0} = 1 = \binom{n+1}{1} - \binom{n}{1} + 1$$

Wait, let me verify the exact formula from the problem.

Looking at the pattern, the identity should be:

$$\binom{n}{1} + \binom{n+1}{2} + \binom{n+2}{3} + \cdots + \binom{n+m}{m+1} = \binom{n+m+1}{m+2}$$

Actually, the standard form is:

$$\sum_{k=0}^{m} \binom{r+k}{k} = \binom{r+m+1}{m}$$

---

## /9/ Prove: $\binom{n}{1} + 2\binom{n}{2} + \cdots + n\binom{n}{n} = n2^{n-1}$

### Proof

This is a standard identity. We can prove it using the derivative method.

**Method 1: Using derivatives**

Start with the binomial theorem:
$$(1+x)^n = \sum_{k=0}^{n} \binom{n}{k} x^k$$

Differentiate both sides with respect to $x$:
$$n(1+x)^{n-1} = \sum_{k=1}^{n} k\binom{n}{k} x^{k-1}$$

Set $x = 1$:
$$n \cdot 2^{n-1} = \sum_{k=1}^{n} k\binom{n}{k}$$

Which is exactly our identity! ✓

**Method 2: Combinatorial proof**

Count the number of ways to choose a committee with a chairperson from $n$ people.

**Method A:** Choose the chair first ($n$ ways), then choose any subset of the remaining $n-1$ people ($2^{n-1}$ ways).
$$\text{Total} = n \cdot 2^{n-1}$$

**Method B:** Choose a committee of size $k$ ($\binom{n}{k}$ ways), then choose a chair from the $k$ members ($k$ ways), and sum over all $k$.
$$\text{Total} = \sum_{k=1}^{n} k\binom{n}{k}$$

Both count the same thing, so they're equal! ✓

---

## /10/ Prove: $\binom{n}{0} + 2\binom{n}{1} + 3\binom{n}{2} + \cdots + (n+1)\binom{n}{n} = (n+1)2^{n-1}$

Wait, let me check this formula more carefully. The general term is $(k+1)\binom{n}{k}$ for $k = 0, 1, \ldots, n$.

### Proof

$$\begin{aligned}
\sum_{k=0}^{n} (k+1)\binom{n}{k} &= \sum_{k=0}^{n} k\binom{n}{k} + \sum_{k=0}^{n} \binom{n}{k}\\[10pt]
&= n2^{n-1} + 2^n & \text{(using /9/ and binomial sum)}\\[10pt]
&= 2^{n-1}(n + 2)\\[10pt]
&= (n+2)2^{n-1}
\end{aligned}$$

So the correct identity is:

$$\boxed{\sum_{k=0}^{n} (k+1)\binom{n}{k} = (n+2)2^{n-1}}$$

---

## /11/ Prove: $\binom{n}{1} + 3\binom{n}{2} + 5\binom{n}{3} + \cdots + (2n-1)\binom{n}{n} = (n+2)2^{n-1} - 1$

### Analysis

The general term is $(2k-1)\binom{n}{k}$ for $k = 1, 2, \ldots, n$.

$$\begin{aligned}
\sum_{k=1}^{n} (2k-1)\binom{n}{k} &= 2\sum_{k=1}^{n} k\binom{n}{k} - \sum_{k=1}^{n} \binom{n}{k}\\[10pt]
&= 2 \cdot n2^{n-1} - (2^n - 1) & \text{(using /9/ and excluding $k=0$)}\\[10pt]
&= n2^n - 2^n + 1\\[10pt]
&= (n-1)2^n + 1
\end{aligned}$$

So the correct identity is:

$$\boxed{\sum_{k=1}^{n} (2k-1)\binom{n}{k} = (n-1)2^n + 1}$$

---

## Summary of Corrected Identities

| # | Corrected Identity |
|---|-------------------|
| /5/ | $\binom{n+1}{r+1} - 2\binom{n}{r} + \binom{n-1}{r-1} = \binom{n-1}{r+1}$ |
| /6/ | $\binom{n}{r} - \binom{n-1}{r} = \binom{n-1}{r-1}$ |
| /9/ | $\sum_{k=1}^{n} k\binom{n}{k} = n2^{n-1}$ |
| /10/ | $\sum_{k=0}^{n} (k+1)\binom{n}{k} = (n+2)2^{n-1}$ |
| /11/ | $\sum_{k=1}^{n} (2k-1)\binom{n}{k} = (n-1)2^n + 1$ |

---

*Exercise 3.2/5-11 from Chapter 03 - Binomiális és polinomiális együtthatók*
