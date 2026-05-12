# Chapter 05 - Rekurzív sorozatok (Recursive Sequences) - Complete Solutions

## Section 5.0 - Alapfogalmak (Basic Concepts)

---

### Exercise 5.0.1 - Verify n! Satisfies First-Order Recurrence

**Problem:** Verify that $n!$ satisfies a first-order recurrence.

**Solution:**

**Claim:** $n!$ satisfies the recurrence $a_n = n \cdot a_{n-1}$ with $a_0 = 1$.

---

**Verification:**

By definition: $n! = n \times (n-1) \times (n-2) \times \cdots \times 2 \times 1$

And: $(n-1)! = (n-1) \times (n-2) \times \cdots \times 2 \times 1$

**Therefore:** $n! = n \times (n-1)!$ ✓

---

**Recurrence relation:**
$$a_n = n \cdot a_{n-1}, \quad a_0 = 1$$

---

**First few values:**

| n | Calculation | aₙ = n! |
|---|-------------|---------|
| 0 | (given) | 1 |
| 1 | 1 × 1 | 1 |
| 2 | 2 × 1 | 2 |
| 3 | 3 × 2 | 6 |
| 4 | 4 × 6 | 24 |
| 5 | 5 × 24 | 120 |
| 6 | 6 × 120 | 720 |

All match the factorial values. ✓

---

**Closed form:** $a_n = n!$

---

### Exercise 5.0.2 - Compound Interest Recurrence

**Problem:** Write the recurrence for compound interest.

**Solution:**

**Problem Setup:**
- Initial amount: $A_0$ (principal)
- Annual interest rate: $r$ (as decimal, e.g., 5% = 0.05)
- Compounded annually

---

**Recurrence Relation:**

After one year: $A_1 = A_0 + rA_0 = A_0(1+r)$

After two years: $A_2 = A_1 + rA_1 = A_1(1+r)$

**General recurrence:**
$$A_n = A_{n-1}(1+r), \quad A_0 = \text{principal}$$

---

**Closed-form solution:**

$$A_n = A_0(1+r)^n$$

---

**Verification:**

| n | From recurrence | From formula |
|---|-----------------|--------------|
| 0 | $A_0$ | $A_0(1+r)^0 = A_0$ ✓ |
| 1 | $A_0(1+r)$ | $A_0(1+r)^1$ ✓ |
| 2 | $A_1(1+r) = A_0(1+r)^2$ | $A_0(1+r)^2$ ✓ |
| 3 | $A_2(1+r) = A_0(1+r)^3$ | $A_0(1+r)^3$ ✓ |

---

**Example:** $A_0 = 1000$, $r = 0.05$ (5% interest)

| Year | Amount |
|------|--------|
| 0 | $1000 |
| 1 | $1000 × 1.05 = $1050 |
| 2 | $1050 × 1.05 = $1102.50 |
| 3 | $1102.50 × 1.05 = $1157.63 |
| 10 | $1000 × 1.05^{10} = $1628.89 |

---

### Exercise 5.0.3 - Verify Fibonacci Values

**Problem:** Verify the first 10 Fibonacci numbers.

**Solution:**

**Fibonacci Recurrence:**
$$f_n = f_{n-1} + f_{n-2}, \quad f_1 = 1, f_2 = 1$$

(Some definitions use $f_0 = 0, f_1 = 1$)

---

**First 10 values:**

| n | Calculation | fₙ |
|---|-------------|-----|
| 1 | (given) | 1 |
| 2 | (given) | 1 |
| 3 | 1 + 1 | 2 |
| 4 | 2 + 1 | 3 |
| 5 | 3 + 2 | 5 |
| 6 | 5 + 3 | 8 |
| 7 | 8 + 5 | 13 |
| 8 | 13 + 8 | 21 |
| 9 | 21 + 13 | 34 |
| 10 | 34 + 21 | 55 |

---

**Verification:**

Each value is the sum of the two preceding values. ✓

**Example:** $f_7 = f_6 + f_5 = 8 + 5 = 13$ ✓

---

**Pattern:** The ratio $f_{n+1}/f_n$ approaches the golden ratio $\phi = \frac{1+\sqrt{5}}{2} \approx 1.618$.

| n | fₙ₊₁/fₙ | Approximation |
|---|---------|---------------|
| 5 | 8/5 | 1.6 |
| 6 | 13/8 | 1.625 |
| 7 | 21/13 | 1.615... |
| 8 | 34/21 | 1.619... |
| 9 | 55/34 | 1.6176... |
| 10 | 89/55 | 1.6181... |

Converges to $\phi = 1.6180339887...$ ✓

---

### Exercise 5.0.4 - Verify Binet Formula

**Problem:** Verify the Binet formula for Fibonacci numbers.

**Solution:**

**Binet Formula:**
$$f_n = \frac{\phi^n - \psi^n}{\sqrt{5}}$$

where $\phi = \frac{1+\sqrt{5}}{2}$ (golden ratio) and $\psi = \frac{1-\sqrt{5}}{2}$.

Note: $\phi \approx 1.618$ and $\psi \approx -0.618$.

---

**Verification for n = 1 through 6:**

**n = 1:**
$$f_1 = \frac{\phi - \psi}{\sqrt{5}} = \frac{\frac{1+\sqrt{5}}{2} - \frac{1-\sqrt{5}}{2}}{\sqrt{5}} = \frac{\sqrt{5}}{\sqrt{5}} = 1$$ ✓

**n = 2:**
$$f_2 = \frac{\phi^2 - \psi^2}{\sqrt{5}} = \frac{\phi^2 - \psi^2}{\sqrt{5}}$$

Note: $\phi^2 = \phi + 1$ and $\psi^2 = \psi + 1$ (properties of golden ratio)

$$\phi^2 - \psi^2 = (\phi + 1) - (\psi + 1) = \phi - \psi = \sqrt{5}$$

$$f_2 = \frac{\sqrt{5}}{\sqrt{5}} = 1$$ ✓

**n = 3:**
$$f_3 = \frac{\phi^3 - \psi^3}{\sqrt{5}}$$

Using $\phi^3 = 2\phi + 1$ and $\psi^3 = 2\psi + 1$:

$$\phi^3 - \psi^3 = (2\phi + 1) - (2\psi + 1) = 2(\phi - \psi) = 2\sqrt{5}$$

$$f_3 = \frac{2\sqrt{5}}{\sqrt{5}} = 2$$ ✓

---

**Numerical Verification:**

| n | φⁿ | ψⁿ | (φⁿ - ψⁿ)/√5 | fₙ |
|---|-----|-----|--------------|-----|
| 1 | 1.618 | -0.618 | 1.000 | 1 ✓ |
| 2 | 2.618 | 0.382 | 1.000 | 1 ✓ |
| 3 | 4.236 | -0.236 | 2.000 | 2 ✓ |
| 4 | 6.854 | 0.146 | 3.000 | 3 ✓ |
| 5 | 11.090 | -0.090 | 5.000 | 5 ✓ |
| 6 | 17.944 | 0.056 | 8.000 | 8 ✓ |
| 10 | 122.992 | 0.008 | 55.000 | 55 ✓ |

The formula gives exact integers despite involving irrational numbers! ✓

---

## Section 5.1 - Iterációs módszer (Iteration Method)

---

### Exercise 5.1.1 - Solve Hanoi Towers Recurrence

**Problem:** Solve the Hanoi towers recurrence $h_{n+1} = 2h_n + 1$ with $h_1 = 1$.

**Solution:**

**Recurrence:**
$$h_{n+1} = 2h_n + 1, \quad h_1 = 1$$

---

**Method 1: Iteration (Unrolling)**

$$h_2 = 2h_1 + 1 = 2(1) + 1 = 3$$
$$h_3 = 2h_2 + 1 = 2(3) + 1 = 7$$
$$h_4 = 2h_3 + 1 = 2(7) + 1 = 15$$

**Pattern:** $h_n = 2^n - 1$

---

**Proof by Iteration:**

$$h_n = 2h_{n-1} + 1$$
$$= 2(2h_{n-2} + 1) + 1 = 2^2 h_{n-2} + 2 + 1$$
$$= 2^2(2h_{n-3} + 1) + 2 + 1 = 2^3 h_{n-3} + 2^2 + 2 + 1$$
$$= \cdots$$
$$= 2^{n-1} h_1 + 2^{n-2} + 2^{n-3} + \cdots + 2 + 1$$
$$= 2^{n-1} \cdot 1 + \sum_{i=0}^{n-2} 2^i$$
$$= 2^{n-1} + (2^{n-1} - 1)$$ (geometric series sum)
$$= 2^n - 1$$ ✓

---

**Method 2: Proof by Induction**

**Claim:** $h_n = 2^n - 1$

**Base case (n=1):** $h_1 = 1 = 2^1 - 1$ ✓

**Inductive hypothesis:** Assume $h_k = 2^k - 1$ for some $k \geq 1$.

**Inductive step:**
$$h_{k+1} = 2h_k + 1 = 2(2^k - 1) + 1 = 2^{k+1} - 2 + 1 = 2^{k+1} - 1$$ ✓

**By induction:** $h_n = 2^n - 1$ for all $n \geq 1$. ∎

---

**Verification Table:**

| n | From recurrence | From formula 2ⁿ - 1 | Match? |
|---|-----------------|---------------------|--------|
| 1 | 1 (given) | 2 - 1 = 1 | ✓ |
| 2 | 2(1) + 1 = 3 | 4 - 1 = 3 | ✓ |
| 3 | 2(3) + 1 = 7 | 8 - 1 = 7 | ✓ |
| 4 | 2(7) + 1 = 15 | 16 - 1 = 15 | ✓ |
| 5 | 2(15) + 1 = 31 | 32 - 1 = 31 | ✓ |
| 6 | 2(31) + 1 = 63 | 64 - 1 = 63 | ✓ |

---

**Interpretation (Hanoi Towers):**

To move $n$ disks from peg A to peg C:
1. Move $n-1$ disks from A to B: $h_{n-1}$ moves
2. Move largest disk from A to C: 1 move
3. Move $n-1$ disks from B to C: $h_{n-1}$ moves

**Total:** $h_n = 2h_{n-1} + 1$ moves

For $n = 64$ (legendary temple): $h_{64} = 2^{64} - 1 \approx 1.84 \times 10^{19}$ moves

At 1 move per second, this would take ~585 billion years!

---

### Exercise 5.1.2 - Prove hₙ = 2ⁿ⁻¹h₁ + 2ⁿ⁻¹ + ... + 1

**Problem:** Prove the general form before simplifying.

**Solution:**

**Claim:** 
$$h_n = 2^{n-1}h_1 + 2^{n-2} + 2^{n-3} + \cdots + 2 + 1$$

---

**Proof by Iteration:**

Starting from $h_n = 2h_{n-1} + 1$:

$$h_n = 2h_{n-1} + 1$$

Substitute $h_{n-1} = 2h_{n-2} + 1$:
$$= 2(2h_{n-2} + 1) + 1 = 2^2 h_{n-2} + 2 + 1$$

Substitute $h_{n-2} = 2h_{n-3} + 1$:
$$= 2^2(2h_{n-3} + 1) + 2 + 1 = 2^3 h_{n-3} + 2^2 + 2 + 1$$

Continue this pattern. After $(n-1)$ substitutions:
$$= 2^{n-1} h_1 + 2^{n-2} + 2^{n-3} + \cdots + 2 + 1$$ ✓

---

**Simplify using geometric series:**

$$\sum_{i=0}^{n-2} 2^i = 2^{n-1} - 1$$

Therefore:
$$h_n = 2^{n-1} h_1 + (2^{n-1} - 1)$$

With $h_1 = 1$:
$$h_n = 2^{n-1} + 2^{n-1} - 1 = 2^n - 1$$ ✓

---

## Section 5.2 - Lineáris rekurziók (Linear Recurrences)

---

### Exercise 5.2.1 - Prove S^Hom is Closed Under Addition

**Problem:** Prove that if $(a_n)$ and $(b_n)$ satisfy a homogeneous linear recurrence, then $(a_n + b_n)$ also satisfies it.

**Solution:**

**Homogeneous Linear Recurrence (order k):**
$$x_n = c_1 x_{n-1} + c_2 x_{n-2} + \cdots + c_k x_{n-k}$$

where $c_1, c_2, \ldots, c_k$ are constants.

---

**Given:**
- $(a_n)$ satisfies: $a_n = c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_k a_{n-k}$
- $(b_n)$ satisfies: $b_n = c_1 b_{n-1} + c_2 b_{n-2} + \cdots + c_k b_{n-k}$

---

**To prove:** $(a_n + b_n)$ satisfies the same recurrence.

Let $s_n = a_n + b_n$.

---

**Proof:**

$$s_n = a_n + b_n$$

Substitute the recurrences for $a_n$ and $b_n$:

$$= (c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_k a_{n-k}) + (c_1 b_{n-1} + c_2 b_{n-2} + \cdots + c_k b_{n-k})$$

Group by coefficients:

$$= c_1(a_{n-1} + b_{n-1}) + c_2(a_{n-2} + b_{n-2}) + \cdots + c_k(a_{n-k} + b_{n-k})$$

$$= c_1 s_{n-1} + c_2 s_{n-2} + \cdots + c_k s_{n-k}$$ ✓

---

**Therefore:** $(s_n) = (a_n + b_n)$ satisfies the same homogeneous recurrence.

**Conclusion:** The solution space $S^{\text{Hom}}$ is closed under addition. ∎

---

### Exercise 5.2.2 - Prove S^Hom is Closed Under Scalar Multiplication

**Problem:** Prove that if $(a_n)$ satisfies a homogeneous recurrence and $c$ is a scalar, then $(ca_n)$ also satisfies it.

**Solution:**

**Given:** $a_n = c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_k a_{n-k}$

**To prove:** $(ca_n)$ satisfies the same recurrence.

Let $t_n = c \cdot a_n$.

---

**Proof:**

$$t_n = c \cdot a_n$$

Substitute the recurrence for $a_n$:

$$= c \cdot (c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_k a_{n-k})$$

Distribute $c$:

$$= c_1 (c \cdot a_{n-1}) + c_2 (c \cdot a_{n-2}) + \cdots + c_k (c \cdot a_{n-k})$$

$$= c_1 t_{n-1} + c_2 t_{n-2} + \cdots + c_k t_{n-k}$$ ✓

---

**Therefore:** $(t_n) = (ca_n)$ satisfies the same recurrence.

**Conclusion:** $S^{\text{Hom}}$ is a vector space (closed under addition and scalar multiplication). ∎

---

### Exercise 5.2.3 - Construct k Linearly Independent Basis Sequences

**Problem:** Construct $k$ linearly independent basis sequences for a $k$-th order recurrence.

**Solution:**

**k-th order homogeneous recurrence:**
$$x_n = c_1 x_{n-1} + c_2 x_{n-2} + \cdots + c_k x_{n-k}$$

---

**Construction:**

Define $k$ sequences $s^{(1)}, s^{(2)}, \ldots, s^{(k)}$ by their initial conditions:

**Sequence $s^{(j)}$:** 
- $s^{(j)}_i = \delta_{ij}$ for $i = 0, 1, \ldots, k-1$

where $\delta_{ij}$ is the Kronecker delta ($\delta_{ij} = 1$ if $i=j$, else $0$).

---

**Explicit initial conditions:**

| Sequence | s₀ | s₁ | s₂ | ... | sₖ₋₁ |
|----------|----|----|----|-----|------|
| $s^{(1)}$ | 1 | 0 | 0 | ... | 0 |
| $s^{(2)}$ | 0 | 1 | 0 | ... | 0 |
| $s^{(3)}$ | 0 | 0 | 1 | ... | 0 |
| ... | ... | ... | ... | ... | ... |
| $s^{(k)}$ | 0 | 0 | 0 | ... | 1 |

---

**Linear Independence:**

Suppose $\alpha_1 s^{(1)} + \alpha_2 s^{(2)} + \cdots + \alpha_k s^{(k)} = 0$ (zero sequence).

Look at position $i = 0$:
$$\alpha_1 \cdot 1 + \alpha_2 \cdot 0 + \cdots + \alpha_k \cdot 0 = 0$$
Therefore: $\alpha_1 = 0$

Look at position $i = 1$:
$$\alpha_1 \cdot 0 + \alpha_2 \cdot 1 + \cdots + \alpha_k \cdot 0 = 0$$
Therefore: $\alpha_2 = 0$

Continue for all $k$ positions.

**Conclusion:** All $\alpha_i = 0$, so the sequences are linearly independent. ✓

---

**Basis Property:**

Any solution $(x_n)$ can be written as:
$$(x_n) = x_0 s^{(1)}_n + x_1 s^{(2)}_n + \cdots + x_{k-1} s^{(k)}_n$$

**Therefore:** These $k$ sequences form a basis for the solution space.

**Dimension:** The solution space has dimension $k$. ∎

---

### Exercise 5.2.4 - Prove: Difference of Two Inhomogeneous Solutions is Homogeneous

**Problem:** Prove that if $(a_n)$ and $(b_n)$ are two solutions to an inhomogeneous recurrence, then $(a_n - b_n)$ satisfies the homogeneous recurrence.

**Solution:**

**Inhomogeneous Recurrence:**
$$x_n = c_1 x_{n-1} + c_2 x_{n-2} + \cdots + c_k x_{n-k} + f(n)$$

where $f(n)$ is a non-zero function (the inhomogeneous part).

---

**Given:**
- $(a_n)$ satisfies: $a_n = c_1 a_{n-1} + \cdots + c_k a_{n-k} + f(n)$
- $(b_n)$ satisfies: $b_n = c_1 b_{n-1} + \cdots + c_k b_{n-k} + f(n)$

---

**To prove:** $(a_n - b_n)$ satisfies the homogeneous recurrence:
$$d_n = c_1 d_{n-1} + c_2 d_{n-2} + \cdots + c_k d_{n-k}$$

Let $d_n = a_n - b_n$.

---

**Proof:**

$$d_n = a_n - b_n$$

Substitute the recurrences:

$$= (c_1 a_{n-1} + \cdots + c_k a_{n-k} + f(n)) - (c_1 b_{n-1} + \cdots + c_k b_{n-k} + f(n))$$

The $f(n)$ terms cancel:

$$= c_1(a_{n-1} - b_{n-1}) + c_2(a_{n-2} - b_{n-2}) + \cdots + c_k(a_{n-k} - b_{n-k})$$

$$= c_1 d_{n-1} + c_2 d_{n-2} + \cdots + c_k d_{n-k}$$ ✓

---

**Therefore:** $(d_n) = (a_n - b_n)$ satisfies the homogeneous recurrence.

**Corollary:** General solution to inhomogeneous recurrence is:
$$\text{(particular solution)} + \text{(general homogeneous solution)}$$

This is the structure: $x_n = p_n + h_n$ where $p_n$ is any particular solution and $h_n$ is the general homogeneous solution. ∎

---

## Section 5.2.2 - Állandó együtthatójú egyenletek

---

### Exercise 5.2.5 - Derive Characteristic Equation

**Problem:** Derive the characteristic equation for a linear recurrence with constant coefficients.

**Solution:**

**k-th order linear recurrence with constant coefficients:**
$$a_n = c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_k a_{n-k}$$

---

**Ansatz (Trial Solution):**

Try a solution of the form $a_n = q^n$ where $q$ is a constant to be determined.

---

**Substitute into recurrence:**

$$q^n = c_1 q^{n-1} + c_2 q^{n-2} + \cdots + c_k q^{n-k}$$

Divide by $q^{n-k}$ (assuming $q \neq 0$):

$$q^k = c_1 q^{k-1} + c_2 q^{k-2} + \cdots + c_k$$

Rearrange:

$$q^k - c_1 q^{k-1} - c_2 q^{k-2} - \cdots - c_k = 0$$

---

**Characteristic Equation:**
$$q^k - c_1 q^{k-1} - c_2 q^{k-2} - \cdots - c_k = 0$$

The roots of this polynomial determine the form of the general solution.

---

**Why This Works:**

If $q$ is a root of the characteristic equation, then $a_n = q^n$ satisfies the recurrence.

**Verification:**

If $q^k - c_1 q^{k-1} - \cdots - c_k = 0$, then:
$$q^k = c_1 q^{k-1} + c_2 q^{k-2} + \cdots + c_k$$

Multiply by $q^{n-k}$:
$$q^n = c_1 q^{n-1} + c_2 q^{n-2} + \cdots + c_k q^{n-k}$$

This is exactly the recurrence for $a_n = q^n$. ✓

---

### Exercise 5.2.6 - Verify aₙ = cqⁿ Leads to Characteristic Equation

**Problem:** Verify that substituting $a_n = cq^n$ leads to the characteristic equation.

**Solution:**

**Recurrence:** $a_n = c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_k a_{n-k}$

**Trial solution:** $a_n = cq^n$ where $c \neq 0$ is a constant.

---

**Substitute:**

$$cq^n = c_1 \cdot cq^{n-1} + c_2 \cdot cq^{n-2} + \cdots + c_k \cdot cq^{n-k}$$

Divide by $c$ (since $c \neq 0$):

$$q^n = c_1 q^{n-1} + c_2 q^{n-2} + \cdots + c_k q^{n-k}$$

Divide by $q^{n-k}$ (assuming $q \neq 0$):

$$q^k = c_1 q^{k-1} + c_2 q^{k-2} + \cdots + c_k$$

Rearrange:

$$q^k - c_1 q^{k-1} - c_2 q^{k-2} - \cdots - c_k = 0$$ ✓

---

**Conclusion:** The trial solution $a_n = cq^n$ works if and only if $q$ is a root of the characteristic equation.

---

### Exercise 5.2.7 - Prove Vandermonde Determinant Formula

**Problem:** Prove the Vandermonde determinant formula by induction.

**Solution:**

**Vandermonde Determinant:**

$$V_n = \begin{vmatrix}
1 & 1 & \cdots & 1 \\
q_1 & q_2 & \cdots & q_n \\
q_1^2 & q_2^2 & \cdots & q_n^2 \\
\vdots & \vdots & \ddots & \vdots \\
q_1^{n-1} & q_2^{n-1} & \cdots & q_n^{n-1}
\end{vmatrix} = \prod_{1 \leq i < j \leq n} (q_j - q_i)$$

---

**Proof by Induction:**

**Base case (n=2):**

$$V_2 = \begin{vmatrix}
1 & 1 \\
q_1 & q_2
\end{vmatrix} = q_2 - q_1 = \prod_{1 \leq i < j \leq 2} (q_j - q_i)$$ ✓

---

**Inductive hypothesis:** Assume the formula holds for $(n-1) \times (n-1)$ Vandermonde.

---

**Inductive step (n × n):**

Consider $V_n$ as a polynomial in $q_n$.

**Key observation:** If $q_n = q_i$ for any $i < n$, then two columns are identical, so the determinant is 0.

**Therefore:** $(q_n - q_1)(q_n - q_2)\cdots(q_n - q_{n-1})$ divides $V_n$.

The degree of $V_n$ as a polynomial in $q_n$ is $(n-1)$ (from the last row).

**Therefore:**
$$V_n = C \cdot \prod_{i=1}^{n-1} (q_n - q_i)$$

where $C$ is the coefficient of $q_n^{n-1}$.

---

**Find C:**

The coefficient of $q_n^{n-1}$ is the $(n-1) \times (n-1)$ Vandermonde determinant in $q_1, \ldots, q_{n-1}$.

By inductive hypothesis:
$$C = \prod_{1 \leq i < j \leq n-1} (q_j - q_i)$$

---

**Therefore:**
$$V_n = \left(\prod_{1 \leq i < j \leq n-1} (q_j - q_i)\right) \cdot \left(\prod_{i=1}^{n-1} (q_n - q_i)\right)$$

$$= \prod_{1 \leq i < j \leq n} (q_j - q_i)$$ ✓

---

**By induction:** The formula holds for all $n \geq 2$. ∎

---

### Exercise 5.2.8 - Verify Linear Independence of (qᵢⁿ) for Distinct qᵢ

**Problem:** Prove that sequences $(q_1^n), (q_2^n), \ldots, (q_k^n)$ are linearly independent if the $q_i$ are distinct.

**Solution:**

**Given:** $q_1, q_2, \ldots, q_k$ are distinct non-zero constants.

**Sequences:** $s^{(i)}_n = q_i^n$ for $i = 1, \ldots, k$.

---

**To prove:** Linear independence.

Suppose $\alpha_1 q_1^n + \alpha_2 q_2^n + \cdots + \alpha_k q_k^n = 0$ for all $n \geq 0$.

---

**Set up system:**

For $n = 0, 1, \ldots, k-1$:

$$\alpha_1 + \alpha_2 + \cdots + \alpha_k = 0$$
$$\alpha_1 q_1 + \alpha_2 q_2 + \cdots + \alpha_k q_k = 0$$
$$\alpha_1 q_1^2 + \alpha_2 q_2^2 + \cdots + \alpha_k q_k^2 = 0$$
$$\vdots$$
$$\alpha_1 q_1^{k-1} + \alpha_2 q_2^{k-1} + \cdots + \alpha_k q_k^{k-1} = 0$$

---

**Matrix form:**

$$\begin{pmatrix}
1 & 1 & \cdots & 1 \\
q_1 & q_2 & \cdots & q_k \\
q_1^2 & q_2^2 & \cdots & q_k^2 \\
\vdots & \vdots & \ddots & \vdots \\
q_1^{k-1} & q_2^{k-1} & \cdots & q_k^{k-1}
\end{pmatrix}
\begin{pmatrix}
\alpha_1 \\ \alpha_2 \\ \vdots \\ \alpha_k
\end{pmatrix}
=
\begin{pmatrix}
0 \\ 0 \\ \vdots \\ 0
\end{pmatrix}$$

The coefficient matrix is a Vandermonde matrix with determinant:
$$\det(V) = \prod_{1 \leq i < j \leq k} (q_j - q_i)$$

Since all $q_i$ are distinct, $\det(V) \neq 0$.

**Therefore:** The only solution is $\alpha_1 = \alpha_2 = \cdots = \alpha_k = 0$. ✓

---

**Conclusion:** The sequences $(q_1^n), (q_2^n), \ldots, (q_k^n)$ are linearly independent. ∎

---

## Section 5.7 - Feladatok (Exercises)

---

### Exercise 5.3 - Explicit Formulas for Named Sequences

**Problem (5.3. Feladat):** Adjuk meg az alabbi nevezetes sorozatok explicit kepletat (Find explicit formulas for the following named sequences):

**(a)** Lucas numbers: $L_0 = 2$, $L_1 = 1$, $L_n = L_{n-1} + L_{n-2}$

**(b)** Perrin sequence: $a_0 = 3$, $a_1 = 0$, $a_2 = 2$, $a_n = a_{n-2} + a_{n-3}$

**(c)** Padovan sequence: $b_0 = 0$, $b_1 = 1$, $b_2 = 1$, $b_n = b_{n-2} + b_{n-3}$

---

#### Part (a): Lucas Numbers

**Recurrence:** $L_n = L_{n-1} + L_{n-2}$, with $L_0 = 2$, $L_1 = 1$.

---

**Step 1: Characteristic equation.**

This is the same recurrence as Fibonacci, so the characteristic equation is:

$$q^2 - q - 1 = 0$$

with roots:

$$\phi = \frac{1 + \sqrt{5}}{2}, \quad \psi = \frac{1 - \sqrt{5}}{2}$$

---

**Step 2: General solution.**

$$L_n = c_1 \phi^n + c_2 \psi^n$$

---

**Step 3: Apply initial conditions.**

From $L_0 = 2$:
$$c_1 + c_2 = 2$$

From $L_1 = 1$:
$$c_1 \phi + c_2 \psi = 1$$

$$c_1 \cdot \frac{1+\sqrt{5}}{2} + c_2 \cdot \frac{1-\sqrt{5}}{2} = 1$$

---

**Step 4: Solve the system.**

From the first equation: $c_2 = 2 - c_1$.

Substitute into the second:

$$c_1 \phi + (2 - c_1)\psi = 1$$

$$c_1(\phi - \psi) + 2\psi = 1$$

$$c_1 \cdot \sqrt{5} + 2 \cdot \frac{1 - \sqrt{5}}{2} = 1$$

$$c_1 \cdot \sqrt{5} + 1 - \sqrt{5} = 1$$

$$c_1 \cdot \sqrt{5} = \sqrt{5}$$

$$c_1 = 1$$

Therefore: $c_2 = 2 - 1 = 1$.

---

**Step 5: Explicit formula.**

$$\boxed{L_n = \phi^n + \psi^n = \left(\frac{1+\sqrt{5}}{2}\right)^n + \left(\frac{1-\sqrt{5}}{2}\right)^n}$$

---

**Verification:**

| n | $\phi^n + \psi^n$ | $L_n$ (from recurrence) | Match? |
|---|-------------------|------------------------|--------|
| 0 | $1 + 1 = 2$ | 2 (given) | ✓ |
| 1 | $\phi + \psi = 1$ | 1 (given) | ✓ |
| 2 | $\phi^2 + \psi^2 = (\phi + 1) + (\psi + 1) = 1 + 2 = 3$ | $1 + 2 = 3$ | ✓ |
| 3 | $L_2 + L_1 = 3 + 1 = 4$ | $\phi^3 + \psi^3 = 2\phi + 1 + 2\psi + 1 = 2 + 2 = 4$ | ✓ |
| 4 | $L_3 + L_2 = 4 + 3 = 7$ | 7 | ✓ |
| 5 | $L_4 + L_3 = 7 + 4 = 11$ | 11 | ✓ |

---

**Remark:** Comparing with the Binet formula for Fibonacci $f_n = \frac{\phi^n - \psi^n}{\sqrt{5}}$, the Lucas formula is remarkably simpler: $L_n = \phi^n + \psi^n$. The key relationship is $L_n = f_{n-1} + f_{n+1}$. ∎

---

#### Part (b): Perrin Sequence

**Recurrence:** $a_n = a_{n-2} + a_{n-3}$, with $a_0 = 3$, $a_1 = 0$, $a_2 = 2$.

---

**Step 1: Characteristic equation.**

Substituting $a_n = q^n$ into $a_n = a_{n-2} + a_{n-3}$:

$$q^n = q^{n-2} + q^{n-3}$$

Dividing by $q^{n-3}$:

$$q^3 = q + 1$$

$$q^3 - q - 1 = 0$$

---

**Step 2: Find the roots.**

We factor or analyze $p(q) = q^3 - q - 1$.

Since $p(1) = -1 < 0$ and $p(2) = 5 > 0$, there is one real root between 1 and 2.

More precisely, the cubic $q^3 - q - 1 = 0$ has one real root and two complex conjugate roots. Let these be:

$$r_1 \in \mathbb{R}, \quad r_2 = \alpha + \beta i, \quad r_3 = \alpha - \beta i$$

The real root (the so-called **plastic ratio**) is:

$$r_1 = \frac{1}{6}\left(108 + 12\sqrt{69}\right)^{1/3} + \frac{2}{\left(108 + 12\sqrt{69}\right)^{1/3}} \approx 1.3247$$

By Vieta's formulas for $q^3 + 0 \cdot q^2 - q - 1 = 0$:

$$r_1 + r_2 + r_3 = 0, \quad r_1 r_2 + r_1 r_3 + r_2 r_3 = -1, \quad r_1 r_2 r_3 = 1$$

So $r_2 + r_3 = -r_1$ and $r_2 r_3 = 1/r_1$.

---

**Step 3: General solution.**

$$a_n = c_1 r_1^n + c_2 r_2^n + c_3 r_3^n$$

---

**Step 4: Apply initial conditions.**

From $a_0 = 3$: $\quad c_1 + c_2 + c_3 = 3$

From $a_1 = 0$: $\quad c_1 r_1 + c_2 r_2 + c_3 r_3 = 0$

From $a_2 = 2$: $\quad c_1 r_1^2 + c_2 r_2^2 + c_3 r_3^2 = 2$

---

**Step 5: Solve the system.**

The key observation is that the initial values $(3, 0, 2)$ are chosen so that $c_1 = c_2 = c_3 = 1$.

**Verification that $c_1 = c_2 = c_3 = 1$ works:**

- $a_0 = r_1^0 + r_2^0 + r_3^0 = 1 + 1 + 1 = 3$ ✓

- $a_1 = r_1 + r_2 + r_3 = 0$ (by Vieta's: sum of roots of $q^3 + 0q^2 - q - 1$) ✓

- $a_2 = r_1^2 + r_2^2 + r_3^2 = (r_1 + r_2 + r_3)^2 - 2(r_1 r_2 + r_1 r_3 + r_2 r_3) = 0^2 - 2(-1) = 2$ ✓

---

**Step 6: Explicit formula.**

$$\boxed{a_n = r_1^n + r_2^n + r_3^n}$$

where $r_1, r_2, r_3$ are the three roots of $q^3 - q - 1 = 0$.

Equivalently, using Newton's identities, $a_n = r_1^n + r_2^n + r_3^n$ is the **power sum** $p_n$ of the roots.

---

**Verification (first few values):**

| n | $a_n$ (from recurrence) | Check |
|---|------------------------|-------|
| 0 | 3 (given) | $p_0 = 3$ ✓ |
| 1 | 0 (given) | $p_1 = 0$ ✓ |
| 2 | 2 (given) | $p_2 = 2$ ✓ |
| 3 | $a_1 + a_0 = 0 + 3 = 3$ | $p_3 = r_1^3 + r_2^3 + r_3^3 = (r_1 + 1) + (r_2 + 1) + (r_3 + 1) = 0 + 3 = 3$ ✓ |
| 4 | $a_2 + a_1 = 2 + 0 = 2$ | ✓ |
| 5 | $a_3 + a_2 = 3 + 2 = 5$ | ✓ |
| 6 | $a_4 + a_3 = 2 + 3 = 5$ | ✓ |
| 7 | $a_5 + a_4 = 5 + 2 = 7$ | ✓ |

(In step $n=3$ we used $r_i^3 = r_i + 1$ from the characteristic equation.)

---

**Remark:** The Perrin sequence has the remarkable property that if $p$ is prime, then $p \mid a_p$ (i.e., $a_p \equiv 0 \pmod{p}$). This is analogous to Fermat's little theorem and can be used as a primality test (though the converse is not always true -- there exist Perrin pseudoprimes). ∎

---

#### Part (c): Padovan Sequence

**Recurrence:** $b_n = b_{n-2} + b_{n-3}$, with $b_0 = 0$, $b_1 = 1$, $b_2 = 1$.

---

**Step 1: Characteristic equation.**

The recurrence is the same as for Perrin, so the characteristic equation is again:

$$q^3 - q - 1 = 0$$

with the same three roots $r_1, r_2, r_3$ (where $r_1 \approx 1.3247$ is the plastic ratio).

---

**Step 2: General solution.**

$$b_n = c_1 r_1^n + c_2 r_2^n + c_3 r_3^n$$

---

**Step 3: Apply initial conditions.**

From $b_0 = 0$: $\quad c_1 + c_2 + c_3 = 0$

From $b_1 = 1$: $\quad c_1 r_1 + c_2 r_2 + c_3 r_3 = 1$

From $b_2 = 1$: $\quad c_1 r_1^2 + c_2 r_2^2 + c_3 r_3^2 = 1$

---

**Step 4: Solve the system.**

This is a $3 \times 3$ linear system with a Vandermonde-type coefficient matrix. From the first equation, $c_3 = -c_1 - c_2$. Substituting into the second and third:

$$c_1(r_1 - r_3) + c_2(r_2 - r_3) = 1$$

$$c_1(r_1^2 - r_3^2) + c_2(r_2^2 - r_3^2) = 1$$

The second simplifies (using $a^2 - b^2 = (a-b)(a+b)$):

$$c_1(r_1 - r_3)(r_1 + r_3) + c_2(r_2 - r_3)(r_2 + r_3) = 1$$

From the first equation: let $u = c_1(r_1 - r_3)$ and $v = c_2(r_2 - r_3)$, so $u + v = 1$.

The second becomes: $u(r_1 + r_3) + v(r_2 + r_3) = 1$.

Since $r_1 + r_2 + r_3 = 0$, we have $r_1 + r_3 = -r_2$ and $r_2 + r_3 = -r_1$:

$$-ur_2 - vr_1 = 1$$

Together with $u + v = 1$ (so $v = 1 - u$):

$$-ur_2 - (1-u)r_1 = 1$$

$$-ur_2 - r_1 + ur_1 = 1$$

$$u(r_1 - r_2) = 1 + r_1$$

$$u = \frac{1 + r_1}{r_1 - r_2}$$

Since $u = c_1(r_1 - r_3)$:

$$c_1 = \frac{1 + r_1}{(r_1 - r_2)(r_1 - r_3)}$$

By symmetry (or repeating the calculation cyclically):

$$c_i = \frac{1 + r_i}{(r_i - r_j)(r_i - r_k)}$$

where $\{i, j, k\} = \{1, 2, 3\}$.

Using the fact that $r_i^3 = r_i + 1$ (from the characteristic equation), we can write $1 + r_i = r_i^3$, so:

$$c_i = \frac{r_i^3}{(r_i - r_j)(r_i - r_k)}$$

Also, the derivative of the characteristic polynomial $p(q) = q^3 - q - 1$ is $p'(q) = 3q^2 - 1$. Since $p(q) = (q - r_1)(q - r_2)(q - r_3)$, evaluating the derivative at a root gives:

$$p'(r_i) = (r_i - r_j)(r_i - r_k) = 3r_i^2 - 1$$

Therefore:

$$c_i = \frac{r_i^3}{3r_i^2 - 1}$$

---

**Step 5: Explicit formula.**

$$\boxed{b_n = \sum_{i=1}^{3} \frac{r_i^{n+3}}{3r_i^2 - 1}}$$

where $r_1, r_2, r_3$ are the three roots of $q^3 - q - 1 = 0$.

Equivalently:

$$b_n = \frac{r_1^{n+3}}{3r_1^2 - 1} + \frac{r_2^{n+3}}{3r_2^2 - 1} + \frac{r_3^{n+3}}{3r_3^2 - 1}$$

---

**Verification:**

| n | $b_n$ (from recurrence) |
|---|------------------------|
| 0 | 0 (given) |
| 1 | 1 (given) |
| 2 | 1 (given) |
| 3 | $b_1 + b_0 = 1 + 0 = 1$ |
| 4 | $b_2 + b_1 = 1 + 1 = 2$ |
| 5 | $b_3 + b_2 = 1 + 1 = 2$ |
| 6 | $b_4 + b_3 = 2 + 1 = 3$ |
| 7 | $b_5 + b_4 = 2 + 2 = 4$ |

**Verify $b_0 = 0$:**

$$b_0 = \sum_{i=1}^{3} \frac{r_i^3}{3r_i^2 - 1} = \sum_{i=1}^{3} \frac{r_i + 1}{3r_i^2 - 1}$$

Using partial fractions and the fact that $\sum_{i=1}^3 \frac{1}{p'(r_i)} = 0$ (a standard identity for partial fraction decomposition of $1/p(q)$) along with $\sum_{i=1}^3 \frac{r_i}{p'(r_i)} = 0$ (coefficient of $1/q$ in the expansion), this equals 0. ✓

**Verify $b_1 = 1$:**

$$b_1 = \sum_{i=1}^{3} \frac{r_i^4}{3r_i^2 - 1} = \sum_{i=1}^{3} \frac{r_i \cdot r_i^3}{3r_i^2 - 1} = \sum_{i=1}^{3} \frac{r_i(r_i + 1)}{3r_i^2 - 1} = \sum_{i=1}^{3} \frac{r_i^2 + r_i}{3r_i^2 - 1}$$

By the partial fraction decomposition of $q^2/(q^3 - q - 1)$, the sum of residues gives 1. ✓

---

**Remark:** The Padovan and Perrin sequences share the same characteristic equation $q^3 - q - 1 = 0$. The real root $r_1 \approx 1.3247$ is known as the **plastic ratio** (or plastic number), discovered by Gerard Cordonnier in 1924. It plays a role in architecture and art analogous to the golden ratio. Since $|r_2| = |r_3| = 1/\sqrt{r_1} < 1$, for large $n$ both sequences are approximately $c \cdot r_1^n$ for an appropriate constant $c$. ∎

---

*Continued for remaining exercises in Chapter 05...*
