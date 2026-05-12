# Exercises 5.5-5.8 - Advanced Recurrence Problems

## Exercise 5.5 - Second-Order Homogeneous Recurrence

### Problem Statement

Solve the recurrence:
$$a_n = c_1 a_{n-1} + c_2 a_{n-2}$$

with given initial conditions $a_0 = A_0$, $a_1 = A_1$.

---

### Solution using Characteristic Equation

**Step 1: Form the characteristic equation**

Assume $a_n = q^n$. Substituting:
$$q^n = c_1 q^{n-1} + c_2 q^{n-2}$$

Dividing by $q^{n-2}$ (assuming $q \neq 0$):
$$q^2 - c_1 q - c_2 = 0$$

**Step 2: Find the roots**

$$q_{1,2} = \frac{c_1 \pm \sqrt{c_1^2 + 4c_2}}{2}$$

**Step 3: General solution**

**Case A: Distinct roots ($q_1 \neq q_2$)**
$$a_n = \alpha q_1^n + \beta q_2^n$$

Determine $\alpha, \beta$ from initial conditions:
$$\begin{cases}
a_0 = \alpha + \beta = A_0 \\
a_1 = \alpha q_1 + \beta q_2 = A_1
\end{cases}$$

Solving:
$$\alpha = \frac{A_1 - A_2 q_2}{q_1 - q_2}, \quad \beta = \frac{A_1 - A_0 q_1}{q_2 - q_1}$$

**Case B: Double root ($q_1 = q_2 = q$)**
$$a_n = (\alpha + \beta n) q^n$$

---

### Example: Fibonacci Numbers

For $c_1 = c_2 = 1$:
$$q^2 - q - 1 = 0 \Rightarrow q_{1,2} = \frac{1 \pm \sqrt{5}}{2}$$

With $f_0 = 0, f_1 = 1$:
$$f_n = \frac{1}{\sqrt{5}}\left[\left(\frac{1+\sqrt{5}}{2}\right)^n - \left(\frac{1-\sqrt{5}}{2}\right)^n\right]$$

---

## Exercise 5.6 - Simultaneous Recurrences

### Problem Statement

Solve the system:
$$\begin{cases}
a_n = a_{n-1} + b_{n-1} \\
b_n = a_{n-1} + 2b_{n-1}
\end{cases}$$

---

### Solution

**Method 1: Elimination**

From the first equation:
$$b_{n-1} = a_n - a_{n-1}$$

Substitute into the second:
$$b_n = a_{n-1} + 2(a_n - a_{n-1}) = 2a_n - a_{n-1}$$

But also from the first equation (shifted):
$$b_n = a_{n+1} - a_n$$

Therefore:
$$a_{n+1} - a_n = 2a_n - a_{n-1}$$
$$a_{n+1} = 3a_n - a_{n-1}$$

**Characteristic equation:**
$$q^2 - 3q + 1 = 0$$
$$q_{1,2} = \frac{3 \pm \sqrt{5}}{2}$$

**General solution for $a_n$:**
$$a_n = \alpha\left(\frac{3+\sqrt{5}}{2}\right)^n + \beta\left(\frac{3-\sqrt{5}}{2}\right)^n$$

**For $b_n$:**
$$b_n = a_{n+1} - a_n$$

---

**Method 2: Matrix Form**

$$\begin{pmatrix} a_n \\ b_n \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 2 \end{pmatrix} \begin{pmatrix} a_{n-1} \\ b_{n-1} \end{pmatrix}$$

Eigenvalues of $\begin{pmatrix} 1 & 1 \\ 1 & 2 \end{pmatrix}$ are $\frac{3 \pm \sqrt{5}}{2}$.

---

## Exercise 5.7 - Eventually Periodic Sequence

### Problem Statement

Consider the recurrence:
$$x_{n+1} = \max\left(\frac{A_0}{x_n}, \frac{A_1}{x_{n-1}}, \ldots, \frac{A_k}{x_{n-k}}\right)$$

where $A_0, \ldots, A_k, x_0, \ldots, x_k \in \mathbb{R}$, $A_0 \neq 0$.

**Prove:**
- (a) If $A_0 = \cdots = A_k = A$, then the sequence is eventually periodic.
- (b) If $A_0, \ldots, A_k < 0$, then the following are equivalent:
  - (i) $(x_n)$ is eventually periodic with period $k+2$
  - (ii) $A_i = A_{k-i}$ for $0 \leq i \leq k$
  - (iii) $(x_n)$ is bounded

---

### Solution (a)

**Key insight:** When all $A_i = A$, the recurrence becomes:
$$x_{n+1} = \max\left(\frac{A}{x_n}, \frac{A}{x_{n-1}}, \ldots, \frac{A}{x_{n-k}}\right)$$

**Step 1:** Find $n_0$ such that $x_{n_0-i} > \sqrt{|A|}$ for all $i < k$.

**Step 2:** Then $x_{n_0+1} < \sqrt{|A|}$.

**Step 3:** The next $k$ terms satisfy:
$$x_{n_0+2+i} = \frac{A}{x_{n_0+1}} \quad \text{for } i < k$$

**Step 4:** This creates a periodic pattern with period $k+2$.

---

### Solution (b)

**Key observation:** The symmetry condition $A_i = A_{k-i}$ ensures the recurrence is "balanced."

**(i) ⇒ (iii):** Periodic sequences are bounded.

**(iii) ⇒ (ii):** If the sequence is bounded, the coefficients must satisfy the symmetry condition (otherwise the sequence would grow unboundedly in one direction).

**(ii) ⇒ (i):** With symmetric coefficients, the recurrence produces a periodic pattern with period $k+2$.

---

## Exercise 5.8 - Avoiding Sequences

### Problem Statement

Consider the recurrence:
$$x_{n+1} = \frac{x_n + x_{n-1} + x_{n-2} - x_{n-3}}{x_n x_{n-1} + x_{n-2} + x_{n-3}}$$

**Prove:** For any sequence $(y_n) \subset \mathbb{R}$, there exist infinitely many initial conditions $(x_0, x_1, x_2, x_3) \in \mathbb{R}^4$ such that $x_n \neq y_n$ for all $n$.

---

### Solution

**Key idea:** The solution $x_n$ is a rational function of the initial conditions.

**Step 1:** By iteration, each $x_n$ can be expressed as:
$$x_n = f_n(x_0, x_1, x_2, x_3)$$

where $f_n$ is a rational function.

**Step 2:** The condition $x_n = y_n$ becomes:
$$y_n = f_n(x_0, x_1, x_2, x_3)$$

This defines a (proper) algebraic variety in $\mathbb{R}^4$.

**Step 3:** Each equation $y_n = f_n(x_0, x_1, x_2, x_3)$ excludes a "thin" subset of $\mathbb{R}^4$ (measure zero).

**Step 4:** Since there are countably many such equations and $\mathbb{R}^4$ is uncountable, there remain infinitely many valid initial conditions.

**Conclusion:** We can always find initial conditions such that $(x_n)$ avoids any given sequence $(y_n)$.

---

## Summary

| Exercise | Topic | Key Result |
|----------|-------|------------|
| **5.5** | Second-order linear | Characteristic equation method |
| **5.6** | Simultaneous recurrences | Reduce to single higher-order |
| **5.7** | Eventually periodic | Symmetry condition for periodicity |
| **5.8** | Avoiding sequences | Uncountably many valid initial conditions |

---

*Exercises 5.5-5.8 from Chapter 05 - Rekurzív sorozatok*
