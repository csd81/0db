# Exercise 3.1 - Factorial Identity

## Problem Statement

Prove the following identity for $n \in \mathbb{N}$:

$$\frac{1}{0!1![(n-1)!]^2} + \frac{1}{1!2![(n-2)!]^2} + \frac{1}{2!3![(n-3)!]^2} + \cdots = \frac{(2n-1)!}{[n!(n-1)!]^2}$$

---

## Analysis

Let me first understand the pattern of the sum. The general term appears to be:

$$\frac{1}{k!(k+1)![(n-k-1)!]^2}$$

where $k = 0, 1, 2, \ldots, n-1$.

So we need to prove:

$$\sum_{k=0}^{n-1} \frac{1}{k!(k+1)![(n-k-1)!]^2} = \frac{(2n-1)!}{[n!(n-1)!]^2}$$

---

## Proof

### Step 1: Rewrite in terms of binomial coefficients

Let me manipulate the general term:

$$\begin{aligned}
\frac{1}{k!(k+1)![(n-k-1)!]^2} &= \frac{1}{k!(k+1) \cdot k! \cdot [(n-k-1)!]^2}\\[10pt]
&= \frac{1}{(k+1) \cdot [k!]^2 \cdot [(n-k-1)!]^2}
\end{aligned}$$

Hmm, let me try a different approach. Let me multiply both sides by $[n!(n-1)!]^2$:

**LHS multiplied:**
$$\sum_{k=0}^{n-1} \frac{[n!(n-1)!]^2}{k!(k+1)![(n-k-1)!]^2}$$

Let me simplify one term:

$$\begin{aligned}
\frac{[n!(n-1)!]^2}{k!(k+1)![(n-k-1)!]^2} &= \frac{[n!]^2}{k!(k+1)!} \cdot \frac{[(n-1)!]^2}{[(n-k-1)!]^2}\\[10pt]
&= \frac{[n!]^2}{k!(k+1)!} \cdot \left[\frac{(n-1)!}{(n-k-1)!}\right]^2
\end{aligned}$$

Now:
$$\frac{(n-1)!}{(n-k-1)!} = (n-1)(n-2)\cdots(n-k)$$

This is getting complicated. Let me try a different approach.

---

### Step 2: Recognize binomial coefficient structure

Let me rewrite the term more carefully:

$$\frac{1}{k!(k+1)![(n-k-1)!]^2} = \frac{1}{k!(k+1)!} \cdot \frac{1}{[(n-k-1)!]^2}$$

Notice that:
$$\binom{n}{k} = \frac{n!}{k!(n-k)!}$$

So:
$$\frac{1}{k!(n-k)!} = \frac{1}{n!}\binom{n}{k}$$

Let me try to express our sum in terms of products of binomial coefficients.

$$\begin{aligned}
\frac{1}{k!(k+1)![(n-k-1)!]^2} &= \frac{1}{(k+1)} \cdot \frac{1}{k!k![(n-k-1)!]^2}\\[10pt]
&= \frac{1}{(k+1)} \cdot \frac{1}{[k!(n-k-1)!]^2}
\end{aligned}$$

Now:
$$\frac{1}{k!(n-k-1)!} = \frac{1}{(n-1)!} \cdot \binom{n-1}{k}$$

Therefore:
$$\begin{aligned}
\frac{1}{[k!(n-k-1)!]^2} &= \frac{1}{[(n-1)!]^2} \cdot \binom{n-1}{k}^2
\end{aligned}$$

So our term becomes:
$$\frac{1}{k!(k+1)![(n-k-1)!]^2} = \frac{1}{k+1} \cdot \frac{1}{[(n-1)!]^2} \cdot \binom{n-1}{k}^2$$

---

### Step 3: Sum the series

Now our sum is:

$$\begin{aligned}
\text{LHS} &= \sum_{k=0}^{n-1} \frac{1}{k+1} \cdot \frac{1}{[(n-1)!]^2} \cdot \binom{n-1}{k}^2\\[10pt]
&= \frac{1}{[(n-1)!]^2} \sum_{k=0}^{n-1} \frac{1}{k+1} \binom{n-1}{k}^2
\end{aligned}$$

Now I need to evaluate $\sum_{k=0}^{n-1} \frac{1}{k+1} \binom{n-1}{k}^2$.

Using the identity $\frac{1}{k+1}\binom{n-1}{k} = \frac{1}{n}\binom{n}{k+1}$:

$$\begin{aligned}
\sum_{k=0}^{n-1} \frac{1}{k+1} \binom{n-1}{k}^2 &= \sum_{k=0}^{n-1} \binom{n-1}{k} \cdot \frac{1}{k+1}\binom{n-1}{k}\\[10pt]
&= \sum_{k=0}^{n-1} \binom{n-1}{k} \cdot \frac{1}{n}\binom{n}{k+1}\\[10pt]
&= \frac{1}{n} \sum_{k=0}^{n-1} \binom{n-1}{k} \binom{n}{k+1}
\end{aligned}$$

Let $j = k+1$, then $j = 1, 2, \ldots, n$:

$$= \frac{1}{n} \sum_{j=1}^{n} \binom{n-1}{j-1} \binom{n}{j}$$

By Vandermonde's identity (or by inspection):

$$\sum_{j=0}^{n} \binom{n-1}{j-1} \binom{n}{j} = \binom{2n-1}{n}$$

(Note: the $j=0$ term is 0 since $\binom{n-1}{-1} = 0$)

Therefore:

$$\sum_{k=0}^{n-1} \frac{1}{k+1} \binom{n-1}{k}^2 = \frac{1}{n} \binom{2n-1}{n} = \frac{1}{n} \cdot \frac{(2n-1)!}{n!(n-1)!}$$

---

### Step 4: Complete the proof

Now substituting back:

$$\begin{aligned}
\text{LHS} &= \frac{1}{[(n-1)!]^2} \cdot \frac{1}{n} \cdot \frac{(2n-1)!}{n!(n-1)!}\\[10pt]
&= \frac{(2n-1)!}{n \cdot [(n-1)!]^3 \cdot n!}\\[10pt]
&= \frac{(2n-1)!}{n! \cdot n \cdot [(n-1)!]^3}
\end{aligned}$$

Now, $n! = n \cdot (n-1)!$, so:

$$\begin{aligned}
\text{LHS} &= \frac{(2n-1)!}{n \cdot (n-1)! \cdot n \cdot [(n-1)!]^3}\\[10pt]
&= \frac{(2n-1)!}{n^2 \cdot [(n-1)!]^4}
\end{aligned}$$

Hmm, this doesn't match the RHS. Let me recalculate more carefully.

---

### Step 5: Careful recalculation

Let me start fresh with the RHS:

$$\text{RHS} = \frac{(2n-1)!}{[n!(n-1)!]^2} = \frac{(2n-1)!}{[n!]^2 \cdot [(n-1)!]^2}$$

Now for the LHS, let me be more careful with the general term. Looking at the pattern again:

$$a_k = \frac{1}{k!(k+1)![(n-1-k)!]^2}$$

for $k = 0, 1, \ldots, n-1$.

Let me multiply LHS by $[n!(n-1)!]^2$:

$$\begin{aligned}
[n!(n-1)!]^2 \cdot a_k &= \frac{[n!]^2 [(n-1)!]^2}{k!(k+1)![(n-1-k)!]^2}\\[10pt]
&= \frac{[n!]^2}{k!(k+1)!} \cdot \frac{[(n-1)!]^2}{[(n-1-k)!]^2}\\[10pt]
&= \frac{[n!]^2}{k!(k+1)!} \cdot \left[\frac{(n-1)!}{(n-1-k)!}\right]^2
\end{aligned}$$

Now:
$$\frac{(n-1)!}{(n-1-k)!} = (n-1)(n-2)\cdots(n-k) = \frac{(n-1)!}{(n-1-k)!}$$

And:
$$\binom{n-1}{k} = \frac{(n-1)!}{k!(n-1-k)!}$$

So:
$$\frac{(n-1)!}{(n-1-k)!} = k! \binom{n-1}{k}$$

Therefore:
$$\begin{aligned}
[n!(n-1)!]^2 \cdot a_k &= \frac{[n!]^2}{k!(k+1)!} \cdot [k!]^2 \binom{n-1}{k}^2\\[10pt]
&= \frac{[n!]^2 \cdot k!}{(k+1)!} \binom{n-1}{k}^2\\[10pt]
&= \frac{[n!]^2}{k+1} \binom{n-1}{k}^2
\end{aligned}$$

So:
$$\text{LHS} \cdot [n!(n-1)!]^2 = [n!]^2 \sum_{k=0}^{n-1} \frac{1}{k+1} \binom{n-1}{k}^2$$

From my earlier calculation:
$$\sum_{k=0}^{n-1} \frac{1}{k+1} \binom{n-1}{k}^2 = \frac{1}{n} \binom{2n-1}{n}$$

Therefore:
$$\begin{aligned}
\text{LHS} \cdot [n!(n-1)!]^2 &= [n!]^2 \cdot \frac{1}{n} \binom{2n-1}{n}\\[10pt]
&= \frac{[n!]^2}{n} \cdot \frac{(2n-1)!}{n!(n-1)!}\\[10pt]
&= \frac{n!}{n} \cdot \frac{(2n-1)!}{(n-1)!}\\[10pt]
&= (n-1)! \cdot \frac{(2n-1)!}{(n-1)!}\\[10pt]
&= (2n-1)!
\end{aligned}$$

Therefore:
$$\text{LHS} = \frac{(2n-1)!}{[n!(n-1)!]^2} = \text{RHS}$$

✓ **Q.E.D.**

---

## Verification Table

| n | LHS (first few terms) | RHS |
|---|----------------------|-----|
| 1 | $\frac{1}{0!1!0!^2} = 1$ | $\frac{1!}{[1!0!]^2} = 1$ |
| 2 | $\frac{1}{0!1!1!^2} + \frac{1}{1!2!0!^2} = 1 + \frac{1}{2} = \frac{3}{2}$ | $\frac{3!}{[2!1!]^2} = \frac{6}{4} = \frac{3}{2}$ |
| 3 | $\frac{1}{0!1!2!^2} + \frac{1}{1!2!1!^2} + \frac{1}{2!3!0!^2} = \frac{1}{4} + \frac{1}{2} + \frac{1}{12} = \frac{3+6+1}{12} = \frac{10}{12} = \frac{5}{6}$ | $\frac{5!}{[3!2!]^2} = \frac{120}{36 \cdot 4} = \frac{120}{144} = \frac{5}{6}$ |

---

## Key Identities Used

1. **Binomial coefficient definition:** $\binom{n}{k} = \frac{n!}{k!(n-k)!}$

2. **Fractional binomial identity:** $\frac{1}{k+1}\binom{n-1}{k} = \frac{1}{n}\binom{n}{k+1}$

3. **Vandermonde-type sum:** $\sum_{j=0}^{n} \binom{n-1}{j-1}\binom{n}{j} = \binom{2n-1}{n}$

---

## Alternative Approach: Generating Functions

This identity can also be proved using generating functions by considering the coefficient of $x^n$ in appropriate power series expansions.

---

*Exercise 3.1 from Chapter 03 - Binomiális és polinomiális együtthatók*
