# Exercise 7.3 - Erdős-DeBruijn and Fisher Theorems

## Problem Statement

Apply the intersection theorems:
- (a) Erdős-DeBruijn: $|A_i \cap A_j| = 1 \Rightarrow m \leq n$
- (b) Fisher: $|A_i| = k, |A_i \cap A_j| = t \Rightarrow m \leq n$
- (c) Verify with Fano plane example

---

## Solution

### Part (a): Erdős-DeBruijn Theorem (7.5 Tétel)

**Theorem:** If $|A_i \cap A_j| = 1$ for all $i \neq j$, then $m \leq n$.

**Example: $n = 3$**

Maximum $m = 3$ sets.

**Construction (case b - star):**
- $A_1 = \{1\}$
- $A_2 = \{1, 2\}$
- $A_3 = \{1, 3\}$

**Verification:**
- $|A_1 \cap A_2| = |\{1\}| = 1$ ✓
- $|A_1 \cap A_3| = |\{1\}| = 1$ ✓
- $|A_2 \cap A_3| = |\{1\}| = 1$ ✓

**Alternative construction (triangle):**
- $A_1 = \{1, 2\}$
- $A_2 = \{2, 3\}$
- $A_3 = \{3, 1\}$

**Verification:**
- $|A_1 \cap A_2| = |\{2\}| = 1$ ✓
- $|A_1 \cap A_3| = |\{1\}| = 1$ ✓
- $|A_2 \cap A_3| = |\{3\}| = 1$ ✓

---

**Example: $n = 4$**

Maximum $m = 4$ sets.

**Construction (star):**
- $A_1 = \{1\}$
- $A_2 = \{1, 2\}$
- $A_3 = \{1, 3\}$
- $A_4 = \{1, 4\}$

All pairwise intersections have size 1 ✓

---

### Part (b): Fisher's Theorem (7.9 Tétel)

**Theorem:** If $|A_i| = k$ (constant) and $|A_i \cap A_j| = t$ (constant) for all $i \neq j$, then $m \leq n$.

**Example: $n = 7, k = 3, t = 1$ (Fano Plane)**

This is the famous **Fano plane** - a finite projective plane of order 2.

**Points:** $S = \{1, 2, 3, 4, 5, 6, 7\}$

**Lines (7 sets of size 3):**
```
A₁ = {1, 2, 3}
A₂ = {1, 4, 5}
A₃ = {1, 6, 7}
A₄ = {2, 4, 6}
A₅ = {2, 5, 7}
A₆ = {3, 4, 7}
A₇ = {3, 5, 6}
```

**Verification:**
- Each set has size 3 ✓
- Each pair of sets intersects in exactly 1 element ✓
- $m = 7 = n$ ✓ (achieves the bound!)

**Visual representation:**
```
        1
       /|\
      / | \
     2--3--7
     |\ | /|
     | \|/ |
     4--5--6
```

(Triangle with medians and inscribed circle)

---

### Part (c): Fano Plane Detailed Analysis

The Fano plane is a **finite projective plane** of order $q = 2$.

**Properties:**
- $n = q^2 + q + 1 = 7$ points
- $m = q^2 + q + 1 = 7$ lines
- Each line contains $q + 1 = 3$ points
- Each point lies on $q + 1 = 3$ lines
- Any two lines intersect in exactly 1 point
- Any two points determine exactly 1 line

**Incidence Matrix:**

Rows = points, Columns = lines, Entry = 1 if incident, 0 otherwise:

$$
\begin{pmatrix}
1 & 1 & 1 & 0 & 0 & 0 & 0 \\
1 & 0 & 0 & 1 & 1 & 0 & 0 \\
1 & 0 & 0 & 0 & 0 & 1 & 1 \\
0 & 1 & 0 & 1 & 0 & 1 & 0 \\
0 & 1 & 0 & 0 & 1 & 0 & 1 \\
0 & 0 & 1 & 1 & 0 & 0 & 1 \\
0 & 0 & 1 & 0 & 1 & 1 & 0
\end{pmatrix}
$$

**Properties of incidence matrix:**
- Each row has exactly 3 ones (each point on 3 lines)
- Each column has exactly 3 ones (each line has 3 points)
- Any two columns have dot product = 1 (any two lines intersect in 1 point)

---

## Proof Sketch: Erdős-DeBruijn Theorem

**Linear algebra method:**

1. **Characteristic vectors:** For each $A_i$, define $v_i \in \mathbb{R}^n$ where $(v_i)_j = 1$ if $j \in A_i$, else 0.

2. **Inner products:** $\langle v_i, v_j \rangle = |A_i \cap A_j| = 1$ for $i \neq j$.

3. **Linear independence:** Show $v_1, \ldots, v_m$ are linearly independent.

4. **Conclusion:** Since vectors are in $\mathbb{R}^n$, we have $m \leq n$.

---

## Proof Sketch: Fisher's Theorem

Same method as above, but:
- All vectors have same length: $|v_i|^2 = k$
- All pairwise inner products equal: $\langle v_i, v_j \rangle = t$

The Gram matrix $G_{ij} = \langle v_i, v_j \rangle$ has:
- Diagonal entries: $k$
- Off-diagonal entries: $t$

This matrix is non-singular (for $k > t$), so vectors are independent, giving $m \leq n$.

---

## Block Designs Connection

Fisher's theorem is fundamental in **block design theory**.

**Balanced Incomplete Block Design (BIBD):**
- $v$ points (our $n$)
- $b$ blocks (our $m$)
- Each block has $k$ points
- Each point in $r$ blocks
- Any two points in exactly $\lambda$ blocks

**Fisher's inequality for BIBD:** $b \geq v$ (or $m \geq n$ in our notation)

**Symmetric BIBD:** When $b = v$ (or $m = n$)
- Fano plane is a symmetric BIBD with parameters $(7, 3, 1)$

---

## Verification Table

| Theorem | $n$ | Parameters | Max $m$ | Example |
|---------|-----|------------|---------|---------|
| Erdős-DeBruijn | 3 | $|A_i \cap A_j| = 1$ | 3 | Star or triangle |
| Erdős-DeBruijn | 4 | $|A_i \cap A_j| = 1$ | 4 | Star with center |
| Fisher | 7 | $k=3, t=1$ | 7 | Fano plane |
| Fisher | 13 | $k=4, t=1$ | 13 | Projective plane order 3 |
| Fisher | 21 | $k=5, t=1$ | 21 | Projective plane order 4 |

---

## When is the Bound Achieved?

**Erdős-DeBruijn:** $m = n$ achieved by:
1. **Star:** One element in all sets
2. **Near-pencil:** One set of size $n-1$, others of size 2
3. **Finite projective plane:** Special combinatorial structure

**Fisher:** $m = n$ achieved by:
- **Symmetric BIBDs** (Balanced Incomplete Block Designs)
- **Finite projective planes** (when they exist)

**Open problem:** For which values of $q$ does a projective plane of order $q$ exist?
- Known: Exists when $q$ is a prime power
- Open: $q = 10, 12, 15, \ldots$

---

*Exercise 7.3 from Chapter 07 - Extremális halmazrendszerek*
