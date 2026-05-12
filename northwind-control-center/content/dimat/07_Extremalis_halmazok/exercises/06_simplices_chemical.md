# Exercise 7.6 - Simplices and Chemical Applications

## Problem Statement

Apply the simplex method to chemical reaction problems:
- (a) Find all minimal reactions for given compounds
- (b) Verify simplex structure
- (c) Connection to linear algebra

---

## Solution

### Background: Chemical Reactions as Linear Algebra

**Setup:**
- Elements: $E_1, \ldots, E_n$
- Compounds: $A_1, \ldots, A_m$
- Each compound $A_j$ is a vector in $\mathbb{R}^n$ (composition)

**Chemical reaction:**
$$\sum_{j=1}^m x_j A_j = 0$$

where $x_j \in \mathbb{R}$ (positive = product, negative = reactant).

**Minimal reaction:** No proper subset of compounds can react.

**Simplex:** A set of vectors that is linearly dependent, but every proper subset is linearly independent.

---

### Part (a): Example - Water Formation

**Elements:** $H, O$ ($n = 2$)

**Compounds:**
- $A_1 = H_2 = [2, 0]^T$
- $A_2 = O_2 = [0, 2]^T$
- $A_3 = H_2O = [2, 1]^T$

**Find minimal reactions:**

We need $x_1 A_1 + x_2 A_2 + x_3 A_3 = 0$:

$$x_1 \begin{pmatrix} 2 \\ 0 \end{pmatrix} + x_2 \begin{pmatrix} 0 \\ 2 \end{pmatrix} + x_3 \begin{pmatrix} 2 \\ 1 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}$$

This gives:
$$\begin{cases}
2x_1 + 2x_3 = 0 \\
2x_2 + x_3 = 0
\end{cases}$$

**Solution:** $x_1 = -x_3, x_2 = -x_3/2$

Choose $x_3 = 2$: $x_1 = -2, x_2 = -1, x_3 = 2$

**Reaction:** $-2H_2 - O_2 + 2H_2O = 0$

Or: $2H_2 + O_2 \rightarrow 2H_2O$ ✓

**Minimality check:**
- $\{H_2, O_2\}$: Linearly independent (no reaction)
- $\{H_2, H_2O\}$: Linearly independent
- $\{O_2, H_2O\}$: Linearly independent

So $\{H_2, O_2, H_2O\}$ is a **simplex**! ✓

---

### Part (b): Example - Carbon Compounds

**Elements:** $C, H, O$ ($n = 3$)

**Compounds:**
- $A_1 = CH_4 = [1, 4, 0]^T$
- $A_2 = O_2 = [0, 0, 2]^T$
- $A_3 = CO_2 = [1, 0, 2]^T$
- $A_4 = H_2O = [0, 2, 1]^T$

**Find all minimal reactions:**

We need to find all minimal linearly dependent subsets.

**Step 1: Check all 4-tuples**

Solve $x_1 A_1 + x_2 A_2 + x_3 A_3 + x_4 A_4 = 0$:

$$\begin{pmatrix}
1 & 0 & 1 & 0 \\
4 & 0 & 0 & 2 \\
0 & 2 & 2 & 1
\end{pmatrix}
\begin{pmatrix} x_1 \\ x_2 \\ x_3 \\ x_4 \end{pmatrix} = 0$$

**Row reduce:**
$$\begin{pmatrix}
1 & 0 & 1 & 0 \\
0 & 1 & 1 & 1/2 \\
0 & 0 & -4 & 2
\end{pmatrix}$$

Solution: One free variable, so there's a reaction!

**Find the reaction:**
- $x_4 = 2$ (choose)
- $x_3 = 1$ (from row 3)
- $x_2 = -2$ (from row 2)
- $x_1 = -1$ (from row 1)

**Reaction:** $-CH_4 - 2O_2 + CO_2 + 2H_2O = 0$

Or: $CH_4 + 2O_2 \rightarrow CO_2 + 2H_2O$ (combustion of methane) ✓

**Minimality check:** Check all 3-element subsets:

**{CH₄, O₂, CO₂}:**
$$\det\begin{pmatrix} 1 & 0 & 1 \\ 4 & 0 & 0 \\ 0 & 2 & 2 \end{pmatrix} = -8 \neq 0$$
Linearly independent ✓

**{CH₄, O₂, H₂O}:**
$$\det\begin{pmatrix} 1 & 0 & 0 \\ 4 & 0 & 2 \\ 0 & 2 & 1 \end{pmatrix} = -4 \neq 0$$
Linearly independent ✓

**{CH₄, CO₂, H₂O}:**
$$\det\begin{pmatrix} 1 & 1 & 0 \\ 4 & 0 & 2 \\ 0 & 2 & 1 \end{pmatrix} = -8 \neq 0$$
Linearly independent ✓

**{O₂, CO₂, H₂O}:**
$$\det\begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 2 \\ 2 & 2 & 1 \end{pmatrix} = 4 \neq 0$$
Linearly independent ✓

Therefore, $\{CH_4, O_2, CO_2, H_2O\}$ is a **simplex**! ✓

---

### Part (c): Systematic Simplex Finding

**Algorithm:**

1. **Input:** Composition matrix $M$ (rows = elements, columns = compounds)

2. **Find null space:** Solve $Mx = 0$

3. **Find minimal support vectors:** For each solution, find minimal set of non-zero entries

4. **Output:** All minimal reactions (simplices)

---

**Example: Extended System**

**Elements:** $C, H, O, N$ ($n = 4$)

**Compounds:**
- $A_1 = CH_4$
- $A_2 = NH_3$
- $A_3 = O_2$
- $A_4 = CO_2$
- $A_5 = H_2O$
- $A_6 = NO_2$

**Composition matrix:**
$$M = \begin{pmatrix}
1 & 0 & 0 & 1 & 0 & 0 \\
4 & 3 & 0 & 0 & 2 & 0 \\
0 & 0 & 2 & 2 & 1 & 2 \\
0 & 1 & 0 & 0 & 0 & 1
\end{pmatrix}$$

**Null space dimension:** $6 - 4 = 2$ (two independent reactions)

**Find basis for null space:**

After row reduction, we get two independent reactions:

**Reaction 1:** $CH_4 + 2O_2 \rightarrow CO_2 + 2H_2O$ (methane combustion)

**Reaction 2:** $4NH_3 + 7O_2 \rightarrow 4NO_2 + 6H_2O$ (ammonia oxidation)

**Check if these are minimal (simplices):**

- Reaction 1 involves 4 compounds
- Reaction 2 involves 4 compounds
- Both are minimal (no subset reacts)

**Result:** Two simplices in this system.

---

## Connection to Extremal Set Theory

**Observation:** The simplex problem is equivalent to finding minimal linearly dependent sets in a vector configuration.

**Theorem (7.19):** A set of vectors is a simplex if and only if:
1. They are linearly dependent
2. Every proper subset is linearly independent

**Connection to chemistry:**
- Minimal reactions = simplices
- Number of minimal reactions = number of simplices
- This is an extremal problem!

---

## Bounds on Number of Simplices

**Theorem:** For $m$ compounds in $n$ dimensions:
- Maximum number of simplices: $\binom{m}{n+1}$ (all $(n+1)$-tuples could be simplices)
- Minimum: Depends on the specific configuration

**Open problem:** Exact bounds for chemical systems?

---

## Verification Table

| System | Elements | Compounds | Minimal Reactions | Simplex Structure |
|--------|----------|-----------|-------------------|-------------------|
| Water | 2 | 3 | 1 | {H₂, O₂, H₂O} |
| Methane combustion | 3 | 4 | 1 | {CH₄, O₂, CO₂, H₂O} |
| Extended | 4 | 6 | 2 | Two 4-compound simplices |
| Fano plane | - | 7 | - | Geometric simplex |

---

## Applications

### 1. Chemical Engineering
- Find all possible reactions in a system
- Optimize reaction pathways

### 2. Metabolic Networks
- Identify minimal metabolic pathways
- Understand cellular metabolism

### 3. Materials Science
- Predict possible compound formations
- Design new materials

---

## Software Tools

**For finding simplices:**
- MATLAB: `null()` function for null space
- Python: `scipy.linalg.null_space()`
- Specialized: CHEMKIN, Cantera for chemical systems

---

*Exercise 7.6 from Chapter 07 - Extremális halmazrendszerek*
