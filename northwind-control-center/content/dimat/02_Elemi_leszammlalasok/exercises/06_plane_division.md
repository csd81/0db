# Exercise 2.1/6 - Plane Division by Lines

## Problem Statement

Prove by complete induction:

$n$ lines in the plane divide it into at most $\frac{n^2 + n + 2}{2}$ regions.

---

## Proof by Mathematical Induction

### Step 1: Base Case (n = 0)

**Zero lines:** The plane is undivided, so there is exactly 1 region.

**Formula:**
$$\frac{0^2 + 0 + 2}{2} = \frac{2}{2} = 1$$

✓ **Base case verified:** 1 region

---

### Step 2: Base Case (n = 1)

**One line:** Divides the plane into 2 regions.

**Formula:**
$$\frac{1^2 + 1 + 2}{2} = \frac{4}{2} = 2$$

✓ **Verified:** 2 regions

---

### Step 3: Inductive Hypothesis

Assume that $k$ lines divide the plane into at most:
$$R_k = \frac{k^2 + k + 2}{2}$$

regions.

---

### Step 4: Inductive Step (n = k+1)

We need to prove:
$$R_{k+1} = \frac{(k+1)^2 + (k+1) + 2}{2}$$

**Proof:**

Consider adding the $(k+1)$-th line to $k$ existing lines.

**Key observation:** The new line can intersect each of the $k$ existing lines at most once (two distinct lines intersect at most at one point).

So the $(k+1)$-th line has **at most $k$ intersection points** on it.

These $k$ points divide the new line into **at most $k+1$ segments** (including 2 unbounded rays).

Each segment **splits an existing region into two**, creating **one new region**.

Therefore, adding the $(k+1)$-th line creates **at most $k+1$ new regions**.

$$\begin{aligned}
R_{k+1} &= R_k + (k+1)\\[10pt]
&= \frac{k^2 + k + 2}{2} + (k+1) & \text{(by hypothesis)}\\[10pt]
&= \frac{k^2 + k + 2}{2} + \frac{2(k+1)}{2}\\[10pt]
&= \frac{k^2 + k + 2 + 2k + 2}{2}\\[10pt]
&= \frac{k^2 + 3k + 4}{2}\\[10pt]
&= \frac{(k+1)^2 + (k+1) + 2}{2} & \text{(expand: $(k+1)^2 = k^2 + 2k + 1$)}
\end{aligned}$$

✓ **Inductive step complete!**

---

## Conclusion

By the Principle of Mathematical Induction:

$$\boxed{R_n = \frac{n^2 + n + 2}{2} \quad \text{regions (maximum)}}$$

---

## Verification Table

| n (lines) | Maximum regions | Formula |
|-----------|-----------------|---------|
| 0 | 1 | (0+0+2)/2 = 1 |
| 1 | 2 | (1+1+2)/2 = 2 |
| 2 | 4 | (4+2+2)/2 = 4 |
| 3 | 7 | (9+3+2)/2 = 7 |
| 4 | 11 | (16+4+2)/2 = 11 |
| 5 | 16 | (25+5+2)/2 = 16 |
| 6 | 22 | (36+6+2)/2 = 22 |

---

## Visual Representation

```
n = 0:  1 region          n = 1:  2 regions
┌─────┐                   ┌──┬──┐
│     │                   │  │  │
│     │                   │  │  │
└─────┘                   └──┴──┘

n = 2:  4 regions         n = 3:  7 regions
┌──┬──┐                   ┌──┼──┐
├──┼──┤                   │  │  │
└──┴──┘                   └──┴──┘
```

---

## When is the Maximum Achieved?

The maximum is achieved when:
1. **No two lines are parallel** (every pair intersects)
2. **No three lines are concurrent** (no three meet at the same point)

This is called **general position**.

---

## Recurrence Relation

From the proof, we get a recurrence:

$$R_{n} = R_{n-1} + n$$

with $R_0 = 1$.

**Solving the recurrence:**

$$\begin{aligned}
R_n &= R_0 + \sum_{i=1}^{n} i\\[10pt]
&= 1 + \frac{n(n+1)}{2}\\[10pt]
&= \frac{2 + n^2 + n}{2}\\[10pt]
&= \frac{n^2 + n + 2}{2}
\end{aligned}$$

---

## Connection to Triangular Numbers

Notice:
$$R_n = 1 + T_n$$

where $T_n = \frac{n(n+1)}{2}$ is the $n$-th triangular number!

| n | $T_n$ | $R_n = 1 + T_n$ |
|---|-------|-----------------|
| 0 | 0 | 1 |
| 1 | 1 | 2 |
| 2 | 3 | 4 |
| 3 | 6 | 7 |
| 4 | 10 | 11 |
| 5 | 15 | 16 |

---

## Related Problems

### Lazy Caterer's Sequence

This sequence (1, 2, 4, 7, 11, 16, 22, ...) is known as the **Lazy Caterer's Sequence** or **Central Polygonal Numbers**.

**Question:** What's the maximum number of pieces you can cut a pizza into with $n$ straight cuts?

**Answer:** $\frac{n^2 + n + 2}{2}$ - the same formula!

---

### 3D Generalization

**Question:** What's the maximum number of regions created by $n$ planes in 3D space?

**Answer:** $\frac{n^3 + 5n + 6}{6}$

This is the **cake number** or 3D analogue of the lazy caterer's sequence.

---

## Key Insights

1. **Each new line intersects all previous lines** (at most $n-1$ points)
2. **Each intersection creates a new segment** on the new line
3. **Each segment splits one region** into two
4. The formula is **quadratic** in $n$

---

*Exercise 2.1/6 from Chapter 02 - Elemi leszámlálások*
