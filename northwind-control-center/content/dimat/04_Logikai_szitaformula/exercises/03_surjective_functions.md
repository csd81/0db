# Exercises 4.5-4.7 - Surjective Functions

## Exercise 4.5 - Number of Surjections

### Problem Statement

How many **surjective (onto)** functions are there between two finite sets $B \to A$ where $|B| = m$ and $|A| = n$?

---

### Solution using Inclusion-Exclusion

**Setup:**
- Domain: $B$ with $|B| = m$ elements
- Codomain: $A$ with $|A| = n$ elements
- We want functions where **every** element of $A$ is hit (surjective)

**Necessary condition:** $m \geq n$ (otherwise no surjection exists)

---

### Step 1: Total functions (no constraint)

Each of $m$ elements can map to any of $n$ elements:
$$\text{Total} = n^m$$

---

### Step 2: Define bad sets

Let $A = \{a_1, a_2, \ldots, a_n\}$.

Define $A_i$ = functions where $a_i$ is **NOT** in the image (not hit).

We want to exclude functions where at least one $a_i$ is not hit.

---

### Step 3: Apply Inclusion-Exclusion

$$|N| = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n-i)^m$$

**Explanation:**
- Choose $i$ elements from $A$ to exclude from image: $\binom{n}{i}$ ways
- Map $m$ elements to remaining $(n-i)$ elements: $(n-i)^m$ ways
- Alternate signs

---

### Final Formula

$$\boxed{S(m,n) = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n-i)^m}$$

where $S(m,n)$ denotes the number of surjections $B \to A$.

---

### Alternative Form

Using $j = n-i$:

$$S(m,n) = \sum_{j=0}^{n} (-1)^{n-j} \binom{n}{j} j^m$$

---

### Connection to Stirling Numbers

Surjections are related to **Stirling numbers of the second kind** $\stirling{m}{n}$:

$$S(m,n) = n! \cdot \stirling{m}{n}$$

**Explanation:** 
- $\stirling{m}{n}$ = ways to partition $m$ elements into $n$ non-empty unlabeled subsets
- $n!$ = ways to assign these $n$ subsets to $n$ elements of codomain

---

## Exercise 4.6 - Distributing Toys

### Part (a)

**Problem:** In how many ways can 6 toys be distributed to 4 children so that **each child gets at least one toy**?

**Solution:**

This is exactly the surjection problem with $m = 6$, $n = 4$.

$$S(6,4) = \sum_{i=0}^{4} (-1)^i \binom{4}{i} (4-i)^6$$

Calculating:
$$\begin{aligned}
S(6,4) &= \binom{4}{0} \cdot 4^6 - \binom{4}{1} \cdot 3^6 + \binom{4}{2} \cdot 2^6 - \binom{4}{3} \cdot 1^6 + \binom{4}{4} \cdot 0^6 \\[10pt]
&= 1 \cdot 4096 - 4 \cdot 729 + 6 \cdot 64 - 4 \cdot 1 + 0 \\[10pt]
&= 4096 - 2916 + 384 - 4 \\[10pt]
&= \boxed{1560}
\end{aligned}$$

---

### Part (b)

**Problem:** In how many ways can 7 tasks be assigned to 5 workers so that:
- Each worker gets at least 1 task
- The hardest task goes to the best worker

**Solution:**

**Case 1:** Best worker gets only the hardest task.
- Remaining 6 tasks to 4 workers (each gets at least 1): $S(6,4) = 1560$

**Case 2:** Best worker gets the hardest task plus at least 1 more.
- This is equivalent to: 6 tasks to 5 workers (each gets at least 1), then give hardest to best worker
- $S(6,5)$ ways

**Total:**
$$S(6,5) + S(6,4)$$

Calculate $S(6,5)$:
$$\begin{aligned}
S(6,5) &= \sum_{i=0}^{5} (-1)^i \binom{5}{i} (5-i)^6 \\[10pt]
&= 5^6 - 5 \cdot 4^6 + 10 \cdot 3^6 - 10 \cdot 2^6 + 5 \cdot 1^6 - 0 \\[10pt]
&= 15625 - 5 \cdot 4096 + 10 \cdot 729 - 10 \cdot 64 + 5 \\[10pt]
&= 15625 - 20480 + 7290 - 640 + 5 \\[10pt]
&= 1800
\end{aligned}$$

**Answer:**
$$S(6,5) + S(6,4) = 1800 + 1560 = \boxed{3360}$$

---

## Exercise 4.7 - Special Cases of Surjections

### Formulas for Specific Values

| Case | Formula | Result |
|------|---------|--------|
| $S(m, 1)$ | $\sum_{i=0}^{1} (-1)^i \binom{1}{i} (1-i)^m$ | $1$ |
| $S(m, 2)$ | $\sum_{i=0}^{2} (-1)^i \binom{2}{i} (2-i)^m$ | $2^m - 2$ |
| $S(n, n)$ | $n! \cdot \stirling{n}{n}$ | $n!$ |
| $S(n+1, n)$ | $(n+1)! \cdot \stirling{n+1}{n}$ | $\binom{n+1}{2} \cdot n!$ |

---

### Proofs

**1. $S(m, 1) = 1$**

Only one function: everything maps to the single element.

$$S(m,1) = 1^m - \binom{1}{1} \cdot 0^m = 1 - 0 = 1$$ ✓

---

**2. $S(m, 2) = 2^m - 2$**

$$\begin{aligned}
S(m,2) &= 2^m - \binom{2}{1} \cdot 1^m + \binom{2}{2} \cdot 0^m \\[10pt]
&= 2^m - 2 \cdot 1 + 0 \\[10pt]
&= 2^m - 2
\end{aligned}$$

**Combinatorial interpretation:** Total functions minus 2 constant functions. ✓

---

**3. $S(n, n) = n!$**

A surjection from $n$ to $n$ is a bijection, i.e., a permutation.

$$S(n,n) = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n-i)^n = n!$$ ✓

---

**4. $S(n+1, n) = \binom{n+1}{2} \cdot n!$**

**Combinatorial proof:**
- We have $n+1$ elements mapping to $n$ elements surjectively
- Exactly one element in codomain gets hit twice, others get hit once
- Choose which 2 domain elements map to same codomain element: $\binom{n+1}{2}$ ways
- Arrange the $n$ images: $n!$ ways

$$S(n+1, n) = \binom{n+1}{2} \cdot n! = \frac{(n+1)n}{2} \cdot n!$$

**Algebraic verification:**
$$S(n+1, n) = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n-i)^{n+1} = \binom{n+1}{2} \cdot n!$$ ✓

---

**5. $S(n+2, n)$**

**Formula:**
$$S(n+2, n) = n! \cdot \stirling{n+2}{n}$$

Where $\stirling{n+2}{n} = \binom{n+2}{3} + 3\binom{n+2}{4}$ (Stirling number formula).

**Simplified:**
$$S(n+2, n) = n! \left[\frac{n+2}{3} \cdot \binom{n}{2} + \binom{n+2}{2}\right]$$

---

## Summary Table

| Surjection | Formula | Value |
|------------|---------|-------|
| $S(m, 1)$ | All to one | $1$ |
| $S(m, 2)$ | Onto 2 elements | $2^m - 2$ |
| $S(n, n)$ | Permutations | $n!$ |
| $S(n+1, n)$ | One collision | $\binom{n+1}{2} \cdot n!$ |
| $S(n+2, n)$ | Two collisions | See formula above |
| $S(6, 4)$ | Exercise 4.6a | $1560$ |
| $S(6, 5)$ | Exercise 4.6b | $1800$ |

---

*Exercises 4.5-4.7 from Chapter 04 - A logikai szitaformula*
