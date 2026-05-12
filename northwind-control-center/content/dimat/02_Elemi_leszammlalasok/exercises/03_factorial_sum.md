# Exercise 2.1/3 - Factorial Sum

## Problem Statement

Prove by complete induction:

$$\sum_{k=1}^{n} k! \cdot k = (n+1)! - 1$$

for all $n \in \mathbb{N}$.

---

## Proof by Mathematical Induction

### Step 1: Base Case (n = 1)

**Left side:**
$$\sum_{k=1}^{1} k! \cdot k = 1! \cdot 1 = 1 \cdot 1 = 1$$

**Right side:**
$$(1+1)! - 1 = 2! - 1 = 2 - 1 = 1$$

✓ **Base case verified:** LHS = RHS = 1

---

### Step 2: Inductive Hypothesis

Assume the formula holds for some $n = k$:

$$\sum_{i=1}^{k} i! \cdot i = (k+1)! - 1$$

---

### Step 3: Inductive Step (n = k+1)

We need to prove:
$$\sum_{i=1}^{k+1} i! \cdot i = (k+2)! - 1$$

**Proof:**

Starting with the left side:

$$\begin{aligned}
\sum_{i=1}^{k+1} i! \cdot i &= \sum_{i=1}^{k} i! \cdot i + (k+1)! \cdot (k+1) & \text{(split sum)}\\[10pt]
&= [(k+1)! - 1] + (k+1)! \cdot (k+1) & \text{(by hypothesis)}\\[10pt]
&= (k+1)! + (k+1)! \cdot (k+1) - 1 & \text{(rearrange)}\\[10pt]
&= (k+1)! \cdot [1 + (k+1)] - 1 & \text{(factor out $(k+1)!$)}\\[10pt]
&= (k+1)! \cdot (k+2) - 1 & \text{(simplify)}\\[10pt]
&= (k+2)! - 1 & \text{(by factorial def: $(k+2)! = (k+2)(k+1)!$)}
\end{aligned}$$

✓ **Inductive step complete!**

---

## Conclusion

By the Principle of Mathematical Induction:

$$\boxed{\sum_{k=1}^{n} k! \cdot k = (n+1)! - 1 \quad \text{for all } n \in \mathbb{N}}$$

---

## Verification Table

| n | Sum: $\sum_{k=1}^{n} k! \cdot k$ | Formula: $(n+1)! - 1$ |
|---|----------------------------------|----------------------|
| 1 | 1!·1 = 1 | 2! - 1 = 1 |
| 2 | 1 + 2!·2 = 1 + 4 = 5 | 3! - 1 = 5 |
| 3 | 5 + 3!·3 = 5 + 18 = 23 | 4! - 1 = 23 |
| 4 | 23 + 4!·4 = 23 + 96 = 119 | 5! - 1 = 119 |
| 5 | 119 + 5!·5 = 119 + 600 = 719 | 6! - 1 = 719 |
| 6 | 719 + 6!·6 = 719 + 4320 = 5039 | 7! - 1 = 5039 |

---

## Alternative Proof (Telescoping)

This identity can also be proven by observing a **telescoping pattern**:

### Key Observation:

$$k! \cdot k = (k+1)! - k!$$

**Verification:**
$$(k+1)! - k! = (k+1) \cdot k! - k! = k! \cdot [(k+1) - 1] = k! \cdot k$$ ✓

### Telescoping Sum:

$$\begin{aligned}
\sum_{k=1}^{n} k! \cdot k &= \sum_{k=1}^{n} [(k+1)! - k!]\\[10pt]
&= (2! - 1!) + (3! - 2!) + (4! - 3!) + ... + [(n+1)! - n!]\\[10pt]
&= (n+1)! - 1! & \text{(all middle terms cancel)}\\[10pt]
&= (n+1)! - 1
\end{aligned}$$

This gives the same result without induction!

---

## Key Algebraic Steps

The critical insight in the inductive proof:

1. **Separate the last term** from the sum
2. **Apply the inductive hypothesis** to the remaining sum
3. **Factor out $(k+1)!$** from the expression
4. **Recognize** $(k+1)! \cdot (k+2) = (k+2)!$

---

## Related Identities

| Sum | Result |
|-----|--------|
| $\sum_{k=1}^{n} k! \cdot k$ | $(n+1)! - 1$ |
| $\sum_{k=1}^{n} k!$ | No simple closed form |
| $\sum_{k=0}^{n} \binom{n}{k} k!$ | $\lfloor e \cdot n! \rfloor$ |

---

## Pattern Recognition

Notice the pattern in similar factorial sums:

$$\begin{aligned}
\sum_{k=1}^{n} k \cdot k! &= (n+1)! - 1\\[5pt]
\sum_{k=1}^{n} (k+1) \cdot k! &= (n+1)!\\[5pt]
\sum_{k=0}^{n} k \cdot k! &= (n+1)! - 1
\end{aligned}$$

---

*Exercise 2.1/3 from Chapter 02 - Elemi leszámlálások*
