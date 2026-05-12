# Exercises 2.2 & 2.3 - Diophantine Equation & Polygon Diagonals

## Exercise 2.2 - Non-negative Solutions

### Problem Statement

How many non-negative integer solutions does the equation have:

$$x_1 + x_2 + \ldots + x_k = n$$

where $n, k \in \mathbb{N}$ are given?

---

### Solution

This is a classic **stars and bars** (or **balls and urns**) combinatorial problem.

#### Method 1: Bijection to Combinations

Think of the problem as distributing $n$ identical objects (stars) into $k$ distinct boxes.

**Visual representation:**
```
n = 5, k = 3
One solution: x₁=2, x₂=1, x₃=2

Visual: ★★ | ★ | ★★
         x₁=2  x₂=1  x₃=2
```

We need:
- $n$ stars (●) representing the total
- $k-1$ bars (|) to create $k$ groups

**Total positions:** $n + (k-1) = n + k - 1$

**Choose positions for bars:** $\binom{n+k-1}{k-1}$

Or equivalently, choose positions for stars: $\binom{n+k-1}{n}$

Both are equal since $\binom{n+k-1}{k-1} = \binom{n+k-1}{n}$.

---

### Answer

$$\boxed{\text{Number of solutions} = \binom{n+k-1}{k-1} = \binom{n+k-1}{n}}$$

This is the formula for **combinations with repetition** (also called multichoose).

---

### Verification Examples

**Example 1:** $n = 3, k = 2$

Formula: $\binom{3+2-1}{2-1} = \binom{4}{1} = 4$

Solutions: $(0,3), (1,2), (2,1), (3,0)$ ✓

**Example 2:** $n = 4, k = 3$

Formula: $\binom{4+3-1}{3-1} = \binom{6}{2} = 15$

Solutions:
| x₁ | x₂ | x₃ |
|----|----|----|
| 0 | 0 | 4 |
| 0 | 1 | 3 |
| 0 | 2 | 2 |
| 0 | 3 | 1 |
| 0 | 4 | 0 |
| 1 | 0 | 3 |
| 1 | 1 | 2 |
| 1 | 2 | 1 |
| 1 | 3 | 0 |
| 2 | 0 | 2 |
| 2 | 1 | 1 |
| 2 | 2 | 0 |
| 3 | 0 | 1 |
| 3 | 1 | 0 |
| 4 | 0 | 0 |

15 solutions ✓

---

### Connection to Chapter 02

This is exactly the formula for **combinations with repetition** (ismétléses kombináció):

$$C_{n}^{k\text{ (ism)}} = \binom{n+k-1}{k}$$

From Section 2.3.2, Exercise 2.21!

---

## Exercise 2.3 - Convex Polygon Diagonals

### Problem Statement

What is the maximum number of intersection points of the diagonals of a convex $n$-gon?

---

### Solution

#### Key Insight

**Four vertices determine exactly one intersection point.**

In a convex polygon:
- Any 4 vertices form a convex quadrilateral
- A convex quadrilateral has exactly 2 diagonals
- These 2 diagonals intersect at exactly 1 point (inside the quadrilateral)

Therefore, choosing any 4 vertices gives us exactly one interior intersection point.

#### No Three Diagonals Concurrent

For the **maximum** number of intersections, we assume:
- No three diagonals meet at the same interior point
- This is the "general position" case

#### Counting

The number of ways to choose 4 vertices from $n$ vertices is:

$$\binom{n}{4}$$

Each choice of 4 vertices determines exactly one intersection point.

---

### Answer

$$\boxed{\text{Maximum intersections} = \binom{n}{4} = \frac{n(n-1)(n-2)(n-3)}{24}}$$

---

### Verification Examples

**n = 4 (Quadrilateral):**
$$\binom{4}{4} = 1$$
A quadrilateral has 2 diagonals intersecting at 1 point ✓

**n = 5 (Pentagon):**
$$\binom{5}{4} = 5$$
A pentagon has 5 diagonals with 5 interior intersections ✓

**n = 6 (Hexagon):**
$$\binom{6}{4} = \binom{6}{2} = 15$$

**n = 3 (Triangle):**
$$\binom{3}{4} = 0$$
A triangle has no diagonals, hence no intersections ✓

---

### Verification Table

| n | Polygon | Diagonals | Max Intersections | Formula |
|---|---------|-----------|-------------------|---------|
| 3 | Triangle | 0 | 0 | C(3,4) = 0 |
| 4 | Quadrilateral | 2 | 1 | C(4,4) = 1 |
| 5 | Pentagon | 5 | 5 | C(5,4) = 5 |
| 6 | Hexagon | 9 | 15 | C(6,4) = 15 |
| 7 | Heptagon | 14 | 35 | C(7,4) = 35 |
| 8 | Octagon | 20 | 70 | C(8,4) = 70 |

---

### Why This Works: Detailed Explanation

Consider 4 vertices A, B, C, D in counterclockwise order:

```
    A
   / \
  /   \
 D     B
  \   /
   \ /
    C
```

The diagonals AC and BD intersect at exactly one point inside the quadrilateral ABCD.

**Key observations:**
1. Every intersection point comes from exactly 4 vertices
2. Every set of 4 vertices produces exactly 1 intersection
3. For maximum, no three diagonals should be concurrent

---

### Related Formulas

| Quantity | Formula |
|----------|---------|
| Number of diagonals | $\frac{n(n-1)(n-3)}{2}$ |
| Number of triangles formed | $\binom{n}{3}$ |
| Number of interior intersections | $\binom{n}{4}$ |
| Number of regions created | $\binom{n}{4} + \binom{n}{2} + 1$ |

---

### Connection to Chapter 02

This uses **combinations without repetition** (ismétlés nélküli kombináció):

$$C_n^k = \binom{n}{k}$$

From Section 2.3.2, where order doesn't matter and we select without replacement.

---

## Summary

| Exercise | Problem | Answer |
|----------|---------|--------|
| **2.2** | Non-negative solutions to $x_1 + \ldots + x_k = n$ | $\binom{n+k-1}{k-1}$ |
| **2.3** | Max diagonal intersections in convex n-gon | $\binom{n}{4}$ |

Both exercises demonstrate the power of **bijective counting** - transforming a difficult counting problem into a simpler one!

---

*Exercises 2.2 & 2.3 from Chapter 02 - Elemi leszámlálások*
