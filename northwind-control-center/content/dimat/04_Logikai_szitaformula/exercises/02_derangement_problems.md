# Exercises 4.2-4.4 - Derangement Problems

## Exercise 4.2 - Exactly One Fixed Point

### Problem Statement

In how many ways can 5 letters be delivered so that **exactly 1 person** receives their own letter?

---

### Solution

**Strategy:** Choose 1 person to get their own letter, then derange the remaining 4.

**Step 1:** Choose 1 person from 5 to receive their own letter.
$$\binom{5}{1} = 5 \text{ ways}$$

**Step 2:** The remaining 4 letters must all go to wrong addresses (derangement).
$$D_4 = 9 \text{ ways}$$

(From the derangement table: $D_4 = 4! \cdot (1 - 1 + \frac{1}{2} - \frac{1}{6} + \frac{1}{24}) = 24 \cdot \frac{9}{24} = 9$)

**Total:**
$$\binom{5}{1} \cdot D_4 = 5 \cdot 9 = \boxed{45}$$

---

### General Formula

For exactly $k$ fixed points out of $n$:

$$\binom{n}{k} \cdot D_{n-k}$$

---

## Exercise 4.3 - At Least One Object

### Problem Statement

In how many ways can $r$ **distinct** objects be distributed among $n+p$ people such that the **first $n$ people each receive at least 1 object**?

---

### Solution using Inclusion-Exclusion

**Setup:**
- Total people: $n + p$
- Total objects: $r$ (distinct)
- Constraint: First $n$ people each get at least 1 object
- The remaining $p$ people have no constraints

**Step 1: Total distributions (no constraints)**

Each of the $r$ objects can go to any of $(n+p)$ people:
$$\text{Total} = (n+p)^r$$

**Step 2: Define bad sets**

Let $A_i$ = distributions where person $i$ (among first $n$) gets **no** object.

We want to exclude all cases where at least one of the first $n$ people gets nothing.

**Step 3: Apply inclusion-exclusion**

$$|N| = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n+p-i)^r$$

**Explanation:**
- Choose $i$ people from the first $n$ to get nothing: $\binom{n}{i}$ ways
- Distribute $r$ objects among remaining $(n+p-i)$ people: $(n+p-i)^r$ ways
- Alternate signs for inclusion-exclusion

---

### Final Formula

$$\boxed{\sum_{i=0}^{n} (-1)^i \binom{n}{i} (n+p-i)^r}$$

---

### Special Cases

**Case 1:** $p = 0$ (exactly $n$ people, each gets at least 1)

This counts **surjective functions** from $r$ objects to $n$ people:
$$S(r, n) = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n-i)^r$$

**Case 2:** $r = n$ (n objects to n people, each gets exactly 1)

$$\sum_{i=0}^{n} (-1)^i \binom{n}{i} (n-i)^n = n!$$

(This is just permutations, as expected!)

---

## Exercise 4.4 - Derangement Recurrence

### Problem Statement

Prove the recurrence relation:

$$D_n = n D_{n-1} + (-1)^n$$

for all $n \geq 2$.

---

### Proof 1: From the Closed Formula

Recall:
$$D_n = n! \sum_{k=0}^{n} \frac{(-1)^k}{k!}$$

Compute $n D_{n-1}$:

$$\begin{aligned}
n D_{n-1} &= n \cdot (n-1)! \sum_{k=0}^{n-1} \frac{(-1)^k}{k!} \\[10pt]
&= n! \sum_{k=0}^{n-1} \frac{(-1)^k}{k!}
\end{aligned}$$

Now add $(-1)^n$:

$$\begin{aligned}
n D_{n-1} + (-1)^n &= n! \sum_{k=0}^{n-1} \frac{(-1)^k}{k!} + (-1)^n \\[10pt]
&= n! \sum_{k=0}^{n-1} \frac{(-1)^k}{k!} + n! \cdot \frac{(-1)^n}{n!} \\[10pt]
&= n! \left(\sum_{k=0}^{n-1} \frac{(-1)^k}{k!} + \frac{(-1)^n}{n!}\right) \\[10pt]
&= n! \sum_{k=0}^{n} \frac{(-1)^k}{k!} \\[10pt]
&= D_n
\end{aligned}$$

✓ **Q.E.D.**

---

### Proof 2: Combinatorial Argument

**Alternative recurrence:** $D_n = (n-1)(D_{n-1} + D_{n-2})$

**Combinatorial proof:**

Consider element 1 in a derangement of $\{1, 2, \ldots, n\}$.

**Case A:** Element 1 goes to position $k$ (where $k \neq 1$), and element $k$ goes to position 1.
- Choose $k$: $(n-1)$ ways
- Remaining $(n-2)$ elements must be deranged: $D_{n-2}$ ways

**Case B:** Element 1 goes to position $k$, but element $k$ does NOT go to position 1.
- Choose $k$: $(n-1)$ ways
- Now we need a derangement of $(n-1)$ elements where $k$ cannot go to position 1
- This is equivalent to $D_{n-1}$ (relabel position 1 as position $k$)

**Total:**
$$D_n = (n-1)(D_{n-2} + D_{n-1})$$

---

### Equivalence of the Two Recurrences

From $D_n = (n-1)(D_{n-1} + D_{n-2})$:

$$\begin{aligned}
D_n &= (n-1)D_{n-1} + (n-1)D_{n-2} \\[10pt]
&= (n-1)D_{n-1} + (n-1)D_{n-2}
\end{aligned}$$

From the other recurrence $D_{n-1} = (n-2)D_{n-2} + (-1)^{n-1}$:

$$(n-1)D_{n-2} = \frac{n-1}{n-2}(D_{n-1} - (-1)^{n-1})$$

Substituting and simplifying gives $D_n = n D_{n-1} + (-1)^n$. ✓

---

### Verification Table

| n | Dₙ | n·Dₙ₋₁ + (-1)ⁿ | Check |
|---|-----|-----------------|-------|
| 2 | 1 | 2·0 + 1 = 1 | ✓ |
| 3 | 2 | 3·1 - 1 = 2 | ✓ |
| 4 | 9 | 4·2 + 1 = 9 | ✓ |
| 5 | 44 | 5·9 - 1 = 44 | ✓ |
| 6 | 265 | 6·44 + 1 = 265 | ✓ |

---

## Summary

| Exercise | Topic | Result |
|----------|-------|--------|
| **4.2** | Exactly 1 fixed point | $\binom{n}{k} D_{n-k}$ |
| **4.3** | At least 1 object each | $\sum_{i=0}^{n} (-1)^i \binom{n}{i} (n+p-i)^r$ |
| **4.4** | Derangement recurrence | $D_n = n D_{n-1} + (-1)^n$ |

---

*Exercises 4.2-4.4 from Chapter 04 - A logikai szitaformula*
