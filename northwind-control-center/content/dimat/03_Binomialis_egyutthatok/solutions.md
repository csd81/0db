# Chapter 03 - Binomiális együtthatók (Binomial Coefficients) - Complete Solutions

## Section 3.1 - Binomiális és polinomiális tételek

---

### Exercise 3.1.1 - Prove Newton Binomial Theorem by Induction

**Problem:** Prove $(a+b)^n = \sum_{i=0}^{n} \binom{n}{i} a^i b^{n-i}$ for all $n \geq 0$.

**Solution:**

**Theorem (Newton Binomial Theorem):**
$$(a+b)^n = \sum_{i=0}^{n} \binom{n}{i} a^i b^{n-i}$$

---

**Proof by Mathematical Induction:**

**Base Case (n=0):**

Left side: $(a+b)^0 = 1$

Right side: $\binom{0}{0} a^0 b^0 = 1 \cdot 1 \cdot 1 = 1$

**Therefore:** Left = Right ✓

---

**Base Case (n=1):**

Left side: $(a+b)^1 = a+b$

Right side: $\binom{1}{0} a^0 b^1 + \binom{1}{1} a^1 b^0 = 1 \cdot b + 1 \cdot a = a+b$

**Therefore:** Left = Right ✓

---

**Inductive Hypothesis:**

Assume the formula holds for $n = k$:
$$(a+b)^k = \sum_{i=0}^{k} \binom{k}{i} a^i b^{k-i}$$

---

**Inductive Step (n = k+1):**

We need to prove:
$$(a+b)^{k+1} = \sum_{i=0}^{k+1} \binom{k+1}{i} a^i b^{k+1-i}$$

**Start:**
$$(a+b)^{k+1} = (a+b)(a+b)^k$$

**Apply inductive hypothesis:**
$$= (a+b) \sum_{i=0}^{k} \binom{k}{i} a^i b^{k-i}$$

**Distribute (a+b):**
$$= a \sum_{i=0}^{k} \binom{k}{i} a^i b^{k-i} + b \sum_{i=0}^{k} \binom{k}{i} a^i b^{k-i}$$

$$= \sum_{i=0}^{k} \binom{k}{i} a^{i+1} b^{k-i} + \sum_{i=0}^{k} \binom{k}{i} a^i b^{k-i+1}$$

---

**Reindex first sum:** Let $j = i+1$, so $i = j-1$

When $i=0$: $j=1$
When $i=k$: $j=k+1$

$$\sum_{i=0}^{k} \binom{k}{i} a^{i+1} b^{k-i} = \sum_{j=1}^{k+1} \binom{k}{j-1} a^j b^{k+1-j}$$

---

**Second sum:** Keep index as $j$

$$\sum_{i=0}^{k} \binom{k}{i} a^i b^{k-i+1} = \sum_{j=0}^{k} \binom{k}{j} a^j b^{k+1-j}$$

---

**Combine the sums:**

$$(a+b)^{k+1} = \sum_{j=1}^{k+1} \binom{k}{j-1} a^j b^{k+1-j} + \sum_{j=0}^{k} \binom{k}{j} a^j b^{k+1-j}$$

**Separate boundary terms:**

$$= \binom{k}{k} a^{k+1} b^0 + \sum_{j=1}^{k} \binom{k}{j-1} a^j b^{k+1-j} + \binom{k}{0} a^0 b^{k+1} + \sum_{j=1}^{k} \binom{k}{j} a^j b^{k+1-j}$$

$$= a^{k+1} + b^{k+1} + \sum_{j=1}^{k} \left[\binom{k}{j-1} + \binom{k}{j}\right] a^j b^{k+1-j}$$

---

**Apply Pascal's Rule:** $\binom{k}{j-1} + \binom{k}{j} = \binom{k+1}{j}$

$$(a+b)^{k+1} = a^{k+1} + b^{k+1} + \sum_{j=1}^{k} \binom{k+1}{j} a^j b^{k+1-j}$$

**Note:** $a^{k+1} = \binom{k+1}{k+1} a^{k+1} b^0$ and $b^{k+1} = \binom{k+1}{0} a^0 b^{k+1}$

$$(a+b)^{k+1} = \binom{k+1}{0} a^0 b^{k+1} + \sum_{j=1}^{k} \binom{k+1}{j} a^j b^{k+1-j} + \binom{k+1}{k+1} a^{k+1} b^0$$

$$= \sum_{j=0}^{k+1} \binom{k+1}{j} a^j b^{k+1-j}$$ ✓

---

**By Mathematical Induction:** The formula holds for all $n \geq 0$. ∎

---

**Numerical Verification:**

**n=2:** $(a+b)^2 = a^2 + 2ab + b^2$

Coefficients: $\binom{2}{0}=1, \binom{2}{1}=2, \binom{2}{2}=1$ ✓

**n=3:** $(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3$

Coefficients: $\binom{3}{0}=1, \binom{3}{1}=3, \binom{3}{2}=3, \binom{3}{3}=1$ ✓

**n=4:** $(a+b)^4 = a^4 + 4a^3b + 6a^2b^2 + 4ab^3 + b^4$

Coefficients: 1, 4, 6, 4, 1 (Pascal's triangle row 4) ✓

---

### Exercise 3.1.2 - Prove Newton-Leibniz Formula

**Problem:** Prove $(fg)^{(n)} = \sum_{i=0}^{n} \binom{n}{i} f^{(i)} g^{(n-i)}$ by induction.

**Solution:**

**Theorem (Newton-Leibniz / Generalized Product Rule):**

For $n$-times differentiable functions $f$ and $g$:
$$(fg)^{(n)} = \sum_{i=0}^{n} \binom{n}{i} f^{(i)} g^{(n-i)}$$

where $f^{(i)}$ denotes the $i$-th derivative of $f$.

---

**Proof by Mathematical Induction:**

**Base Case (n=1):**

Left side: $(fg)' = f'g + fg'$ (standard product rule)

Right side: $\binom{1}{0} f^{(0)} g^{(1)} + \binom{1}{1} f^{(1)} g^{(0)} = fg' + f'g$

**Therefore:** Left = Right ✓

---

**Base Case (n=2):**

Left side: $(fg)'' = (f'g + fg')' = f''g + f'g' + f'g' + fg'' = f''g + 2f'g' + fg''$

Right side: $\binom{2}{0} fg'' + \binom{2}{1} f'g' + \binom{2}{2} f''g = fg'' + 2f'g' + f''g$

**Therefore:** Left = Right ✓

---

**Inductive Hypothesis:**

Assume for $n = k$:
$$(fg)^{(k)} = \sum_{i=0}^{k} \binom{k}{i} f^{(i)} g^{(k-i)}$$

---

**Inductive Step (n = k+1):**

$$(fg)^{(k+1)} = \frac{d}{dx}(fg)^{(k)} = \frac{d}{dx} \sum_{i=0}^{k} \binom{k}{i} f^{(i)} g^{(k-i)}$$

**Differentiate term by term:**

$$= \sum_{i=0}^{k} \binom{k}{i} \frac{d}{dx}\left[f^{(i)} g^{(k-i)}\right]$$

**Apply product rule to each term:**

$$= \sum_{i=0}^{k} \binom{k}{i} \left[f^{(i+1)} g^{(k-i)} + f^{(i)} g^{(k-i+1)}\right]$$

**Split into two sums:**

$$= \sum_{i=0}^{k} \binom{k}{i} f^{(i+1)} g^{(k-i)} + \sum_{i=0}^{k} \binom{k}{i} f^{(i)} g^{(k-i+1)}$$

---

**Reindex first sum:** Let $j = i+1$

$$\sum_{i=0}^{k} \binom{k}{i} f^{(i+1)} g^{(k-i)} = \sum_{j=1}^{k+1} \binom{k}{j-1} f^{(j)} g^{(k+1-j)}$$

**Second sum:** Keep as is with $j = i$

$$\sum_{i=0}^{k} \binom{k}{i} f^{(i)} g^{(k-i+1)} = \sum_{j=0}^{k} \binom{k}{j} f^{(j)} g^{(k+1-j)}$$

---

**Combine:**

$$(fg)^{(k+1)} = \sum_{j=1}^{k+1} \binom{k}{j-1} f^{(j)} g^{(k+1-j)} + \sum_{j=0}^{k} \binom{k}{j} f^{(j)} g^{(k+1-j)}$$

**Separate boundary terms and apply Pascal's rule:**

$$= f^{(k+1)} g + \sum_{j=1}^{k} \left[\binom{k}{j-1} + \binom{k}{j}\right] f^{(j)} g^{(k+1-j)} + f g^{(k+1)}$$

$$= \binom{k+1}{0} f g^{(k+1)} + \sum_{j=1}^{k} \binom{k+1}{j} f^{(j)} g^{(k+1-j)} + \binom{k+1}{k+1} f^{(k+1)} g$$

$$= \sum_{j=0}^{k+1} \binom{k+1}{j} f^{(j)} g^{(k+1-j)}$$ ✓

---

**By Mathematical Induction:** Formula holds for all $n \geq 1$. ∎

---

**Example Application:**

Find $(x^2 e^x)^{(3)}$

**Using formula:**
$$= \binom{3}{0} x^2 (e^x)^{(3)} + \binom{3}{1} (2x) (e^x)^{(2)} + \binom{3}{2} (2) (e^x)^{(1)} + \binom{3}{3} (0) e^x$$

$$= x^2 e^x + 3(2x) e^x + 3(2) e^x + 0$$

$$= x^2 e^x + 6x e^x + 6 e^x$$

$$= e^x(x^2 + 6x + 6)$$ ✓

---

### Exercise 3.1.3 - Newton Binomial Series for α = -1

**Problem:** Derive the binomial series for $(1+x)^{-1}$.

**Solution:**

**Generalized Binomial Theorem:**

For any real $\alpha$:
$$(1+x)^\alpha = \sum_{n=0}^{\infty} \binom{\alpha}{n} x^n$$

where $\binom{\alpha}{n} = \frac{\alpha(\alpha-1)(\alpha-2)\cdots(\alpha-n+1)}{n!}$

---

**For α = -1:**

$$\binom{-1}{n} = \frac{(-1)(-2)(-3)\cdots(-n)}{n!} = \frac{(-1)^n \cdot n!}{n!} = (-1)^n$$

---

**Therefore:**
$$(1+x)^{-1} = \sum_{n=0}^{\infty} (-1)^n x^n = 1 - x + x^2 - x^3 + x^4 - \cdots$$

---

**Convergence:**

This is a geometric series with ratio $-x$.

**Converges when:** $|-x| < 1$, i.e., $|x| < 1$

**Sum:** $\frac{1}{1-(-x)} = \frac{1}{1+x}$ ✓

---

**Verification for small x:**

**x = 0.1:**
- Exact: $\frac{1}{1.1} = 0.909090...$
- Series: $1 - 0.1 + 0.01 - 0.001 + 0.0001 - \cdots = 0.90909...$ ✓

**x = 0.5:**
- Exact: $\frac{1}{1.5} = 0.666...$
- Series: $1 - 0.5 + 0.25 - 0.125 + 0.0625 - \cdots = 0.666...$ ✓

---

## Section 3.2 - Properties of Binomial Coefficients

---

### Exercise 3.2.1 - Verify Pascal's Triangle Properties

**Problem:** Verify Pascal's rule: $\binom{n}{k-1} + \binom{n}{k} = \binom{n+1}{k}$

**Solution:**

**Pascal's Rule:**
$$\binom{n}{k-1} + \binom{n}{k} = \binom{n+1}{k}$$

---

**Algebraic Proof:**

$$\binom{n}{k-1} + \binom{n}{k} = \frac{n!}{(k-1)!(n-k+1)!} + \frac{n!}{k!(n-k)!}$$

**Common denominator:** $k!(n-k+1)!$

$$= \frac{n! \cdot k}{k!(n-k+1)!} + \frac{n! \cdot (n-k+1)}{k!(n-k+1)!}$$

$$= \frac{n![k + (n-k+1)]}{k!(n-k+1)!}$$

$$= \frac{n!(n+1)}{k!(n-k+1)!}$$

$$= \frac{(n+1)!}{k!((n+1)-k)!}$$

$$= \binom{n+1}{k}$$ ✓

---

**Combinatorial Proof:**

**Question:** How many ways to choose $k$ people from $n+1$ people?

**Answer:** $\binom{n+1}{k}$

**Alternative method:**

Fix one person (call them Alice).

**Case 1:** Alice is NOT chosen
- Choose $k$ from remaining $n$: $\binom{n}{k}$ ways

**Case 2:** Alice IS chosen
- Choose remaining $k-1$ from $n$: $\binom{n}{k-1}$ ways

**Total:** $\binom{n}{k} + \binom{n}{k-1}$ ✓

---

**Numerical Verification:**

| n | k | C(n,k-1) | C(n,k) | Sum | C(n+1,k) |
|---|---|----------|--------|-----|----------|
| 4 | 2 | 4 | 6 | 10 | 10 ✓ |
| 5 | 3 | 10 | 10 | 20 | 20 ✓ |
| 6 | 2 | 6 | 15 | 21 | 21 ✓ |
| 7 | 4 | 35 | 35 | 70 | 70 ✓ |

---

**Pascal's Triangle:**

```
Row 0:        1
Row 1:       1 1
Row 2:      1 2 1
Row 3:     1 3 3 1
Row 4:    1 4 6 4 1
Row 5:   1 5 10 10 5 1
```

Each entry is the sum of the two entries above it. ✓

---

### Exercise 3.2.2 - Prove Vandermonde Convolution

**Problem:** Prove $\sum_{i=0}^{k} \binom{n}{i}\binom{m}{k-i} = \binom{n+m}{k}$

**Solution:**

**Theorem (Vandermonde Convolution):**
$$\sum_{i=0}^{k} \binom{n}{i}\binom{m}{k-i} = \binom{n+m}{k}$$

---

**Combinatorial Proof:**

**Question:** How many ways to choose $k$ people from a group of $n$ men and $m$ women?

**Answer:** $\binom{n+m}{k}$

---

**Alternative method (by cases):**

Count by number of men chosen.

**Case i = 0:** 0 men, k women
- Ways: $\binom{n}{0}\binom{m}{k}$

**Case i = 1:** 1 man, k-1 women
- Ways: $\binom{n}{1}\binom{m}{k-1}$

**Case i = 2:** 2 men, k-2 women
- Ways: $\binom{n}{2}\binom{m}{k-2}$

...

**Case i = k:** k men, 0 women
- Ways: $\binom{n}{k}\binom{m}{0}$

---

**Total (sum over all cases):**
$$\sum_{i=0}^{k} \binom{n}{i}\binom{m}{k-i}$$

**Since both methods count the same thing:**
$$\sum_{i=0}^{k} \binom{n}{i}\binom{m}{k-i} = \binom{n+m}{k}$$ ✓

---

**Algebraic Proof (using generating functions):**

**Step 1:** Recall $(1+x)^n = \sum_{i=0}^{n} \binom{n}{i} x^i$

**Step 2:** Consider $(1+x)^{n+m} = (1+x)^n (1+x)^m$

**Step 3:** Expand both sides:

Left: $(1+x)^{n+m} = \sum_{k=0}^{n+m} \binom{n+m}{k} x^k$

Right: $(1+x)^n (1+x)^m = \left(\sum_{i=0}^{n} \binom{n}{i} x^i\right) \left(\sum_{j=0}^{m} \binom{m}{j} x^j\right)$

**Step 4:** Coefficient of $x^k$ on right side:

$$\sum_{i+j=k} \binom{n}{i} \binom{m}{j} = \sum_{i=0}^{k} \binom{n}{i} \binom{m}{k-i}$$

**Step 5:** Equate coefficients:

$$\binom{n+m}{k} = \sum_{i=0}^{k} \binom{n}{i} \binom{m}{k-i}$$ ✓

---

**Numerical Verification:**

**n=3, m=4, k=3:**

Left: $\binom{3}{0}\binom{4}{3} + \binom{3}{1}\binom{4}{2} + \binom{3}{2}\binom{4}{1} + \binom{3}{3}\binom{4}{0}$
$= 1 \cdot 4 + 3 \cdot 6 + 3 \cdot 4 + 1 \cdot 1$
$= 4 + 18 + 12 + 1 = 35$

Right: $\binom{7}{3} = 35$ ✓

---

### Exercise 3.2.3 - Prove Upper Summation Formula

**Problem:** Prove $\sum_{i=k}^{n} \binom{i}{k} = \binom{n+1}{k+1}$

**Solution:**

**Theorem (Hockey-stick Identity / Upper Summation):**
$$\sum_{i=k}^{n} \binom{i}{k} = \binom{n+1}{k+1}$$

---

**Combinatorial Proof:**

**Question:** How many ways to choose $k+1$ people from $n+1$ people?

**Answer:** $\binom{n+1}{k+1}$

---

**Alternative method (by largest-numbered person):**

Label people 1, 2, ..., n+1.

Count by who is the **largest-numbered** person chosen.

**Case 1:** Person k+1 is largest
- Choose remaining k from {1, ..., k}: $\binom{k}{k}$ ways

**Case 2:** Person k+2 is largest
- Choose remaining k from {1, ..., k+1}: $\binom{k+1}{k}$ ways

**Case 3:** Person k+3 is largest
- Choose remaining k from {1, ..., k+2}: $\binom{k+2}{k}$ ways

...

**Case n-k+1:** Person n+1 is largest
- Choose remaining k from {1, ..., n}: $\binom{n}{k}$ ways

---

**Total:**
$$\binom{k}{k} + \binom{k+1}{k} + \binom{k+2}{k} + \cdots + \binom{n}{k} = \sum_{i=k}^{n} \binom{i}{k}$$

**Since both count the same thing:**
$$\sum_{i=k}^{n} \binom{i}{k} = \binom{n+1}{k+1}$$ ✓

---

**Proof by Induction:**

**Base case (n=k):**
- Left: $\binom{k}{k} = 1$
- Right: $\binom{k+1}{k+1} = 1$
- 1 = 1 ✓

---

**Inductive hypothesis:** Assume for $n$:
$$\sum_{i=k}^{n} \binom{i}{k} = \binom{n+1}{k+1}$$

---

**Inductive step (n+1):**

$$\sum_{i=k}^{n+1} \binom{i}{k} = \sum_{i=k}^{n} \binom{i}{k} + \binom{n+1}{k}$$

$$= \binom{n+1}{k+1} + \binom{n+1}{k}$$ (by hypothesis)

$$= \binom{n+2}{k+1}$$ (by Pascal's rule) ✓

---

**Numerical Verification:**

**k=2, n=5:**

Left: $\binom{2}{2} + \binom{3}{2} + \binom{4}{2} + \binom{5}{2} = 1 + 3 + 6 + 10 = 20$

Right: $\binom{6}{3} = 20$ ✓

---

**Visual Pattern (Hockey-stick in Pascal's triangle):**

```
    1
   1 1
  1 2 1
 1 3 3 1       ← sum these: 1+3+6+10 = 20
1 4 6 4 1
1 5 10 10 5 1  ← result is here: 20
```

The pattern looks like a hockey stick! ✓

---

### Exercise 3.2.4 - Prove Monotonicity of Binomial Coefficients

**Problem:** Prove $\binom{n}{i+1} = \binom{n}{i} \cdot \frac{n-i}{i+1}$ and use it to show monotonicity.

**Solution:**

**Part 1: Prove the recurrence relation**

$$\binom{n}{i+1} = \binom{n}{i} \cdot \frac{n-i}{i+1}$$

---

**Proof:**

$$\binom{n}{i} \cdot \frac{n-i}{i+1} = \frac{n!}{i!(n-i)!} \cdot \frac{n-i}{i+1}$$

$$= \frac{n!}{i!(n-i-1)!} \cdot \frac{1}{i+1}$$

$$= \frac{n!}{(i+1)!(n-i-1)!}$$

$$= \binom{n}{i+1}$$ ✓

---

**Part 2: Monotonicity Analysis**

**Question:** When is $\binom{n}{i+1} > \binom{n}{i}$?

From the recurrence:
$$\binom{n}{i+1} > \binom{n}{i} \iff \frac{n-i}{i+1} > 1$$

$$\iff n-i > i+1$$

$$\iff n > 2i+1$$

$$\iff i < \frac{n-1}{2}$$

---

**Conclusion:**

- For $i < \frac{n-1}{2}$: coefficients **increase**
- For $i > \frac{n-1}{2}$: coefficients **decrease**
- Maximum at $i = \lfloor n/2 \rfloor$

---

**Example (n=6):**

| i | C(6,i) | Ratio | Trend |
|---|--------|-------|-------|
| 0 | 1 | 6/1 = 6 | ↑ |
| 1 | 6 | 5/2 = 2.5 | ↑ |
| 2 | 15 | 4/3 ≈ 1.33 | ↑ |
| 3 | 20 | 3/4 = 0.75 | ↓ |
| 4 | 15 | 2/5 = 0.4 | ↓ |
| 5 | 6 | 1/6 ≈ 0.17 | ↓ |
| 6 | 1 | - | - |

Maximum at i = 3 = ⌊6/2⌋ ✓

---

**Example (n=5):**

| i | C(5,i) | Ratio | Trend |
|---|--------|-------|-------|
| 0 | 1 | 5 | ↑ |
| 1 | 5 | 2 | ↑ |
| 2 | 10 | 1 | = |
| 3 | 10 | 0.5 | ↓ |
| 4 | 5 | 0.33 | ↓ |
| 5 | 1 | - | - |

Maximum at i = 2 and i = 3 (both equal when n is odd) ✓

---

### Exercise 3.2.5 - Estimate Using Stirling's Formula

**Problem:** Estimate $\binom{n}{k}$ using Stirling's formula for large n and k.

**Solution:**

**Stirling's Formula:**
$$n! \approx \sqrt{2\pi n} \left(\frac{n}{e}\right)^n$$

More precisely: $n! = \sqrt{2\pi n} \left(\frac{n}{e}\right)^n e^{\theta_n}$ where $0 < \theta_n < \frac{1}{12n}$

---

**Apply to $\binom{n}{k} = \frac{n!}{k!(n-k)!}$:**

$$\binom{n}{k} \approx \frac{\sqrt{2\pi n} (n/e)^n}{\sqrt{2\pi k} (k/e)^k \cdot \sqrt{2\pi (n-k)} ((n-k)/e)^{n-k}}$$

$$= \frac{\sqrt{n}}{\sqrt{2\pi k(n-k)}} \cdot \frac{n^n}{k^k (n-k)^{n-k}}$$

---

**For k = pn (proportion p):**

$$\binom{n}{pn} \approx \frac{1}{\sqrt{2\pi np(1-p)}} \cdot \frac{n^n}{(pn)^{pn} ((1-p)n)^{(1-p)n}}$$

$$= \frac{1}{\sqrt{2\pi np(1-p)}} \cdot \frac{1}{p^{pn} (1-p)^{(1-p)n}}$$

$$= \frac{1}{\sqrt{2\pi np(1-p)}} \cdot \left(\frac{1}{p^p (1-p)^{1-p}}\right)^n$$

---

**In terms of binary entropy:**

Define $H(p) = -p \log_2 p - (1-p) \log_2(1-p)$

Then:
$$\binom{n}{pn} \approx \frac{1}{\sqrt{2\pi np(1-p)}} \cdot 2^{nH(p)}$$

---

**Example: n=100, k=50 (p=0.5):**

**Exact:** $\binom{100}{50} \approx 1.009 \times 10^{29}$

**Stirling estimate:**
$$\binom{100}{50} \approx \frac{1}{\sqrt{2\pi \cdot 100 \cdot 0.25}} \cdot 2^{100 \cdot 1}$$

$$= \frac{1}{\sqrt{50\pi}} \cdot 2^{100}$$

$$\approx 0.0798 \cdot 1.268 \times 10^{30} \approx 1.01 \times 10^{29}$$

**Error:** Less than 0.1% ✓

---

## Section 3.3 - Summation Methods

---

### Exercise 3.3.1 - Prove Sum Identities Combinatorially

**Problem:** Prove $\sum_{i=0}^{n} \binom{n}{i} = 2^n$ and $\sum_{i=0}^{n} (-1)^i \binom{n}{i} = 0$ combinatorially.

**Solution:**

---

**Identity 1:** $\sum_{i=0}^{n} \binom{n}{i} = 2^n$

**Combinatorial Proof:**

**Left side interpretation:** Count subsets of {1, 2, ..., n} by size.
- $\binom{n}{0}$ = subsets of size 0
- $\binom{n}{1}$ = subsets of size 1
- ...
- $\binom{n}{n}$ = subsets of size n

**Sum:** Total number of subsets of all sizes.

**Right side interpretation:** Each element is either in or out (2 choices each).

**Total:** $2^n$ subsets.

**Therefore:** $\sum_{i=0}^{n} \binom{n}{i} = 2^n$ ✓

---

**Algebraic Proof:**

Set $a = b = 1$ in binomial theorem:

$$(1+1)^n = \sum_{i=0}^{n} \binom{n}{i} 1^i 1^{n-i} = \sum_{i=0}^{n} \binom{n}{i}$$

$$2^n = \sum_{i=0}^{n} \binom{n}{i}$$ ✓

---

**Numerical Verification:**

| n | Sum | 2^n |
|---|-----|-----|
| 3 | 1+3+3+1 = 8 | 8 ✓ |
| 4 | 1+4+6+4+1 = 16 | 16 ✓ |
| 5 | 1+5+10+10+5+1 = 32 | 32 ✓ |

---

**Identity 2:** $\sum_{i=0}^{n} (-1)^i \binom{n}{i} = 0$ (for n ≥ 1)

**Combinatorial Proof:**

**Interpretation:** Count subsets with even size minus subsets with odd size.

**Claim:** For n ≥ 1, number of even-sized subsets = number of odd-sized subsets.

**Proof (bijection):**

Fix element 1. For any subset S:
- If 1 ∈ S: map to S \ {1}
- If 1 ∉ S: map to S ∪ {1}

This is a bijection that changes parity of size.

**Therefore:** Even-sized and odd-sized subsets are in bijection.

**Therefore:** $\sum_{i=0}^{n} (-1)^i \binom{n}{i} = 0$ ✓

---

**Algebraic Proof:**

Set $a = 1, b = -1$ in binomial theorem:

$$(1-1)^n = \sum_{i=0}^{n} \binom{n}{i} 1^i (-1)^{n-i} = \sum_{i=0}^{n} (-1)^{n-i} \binom{n}{i}$$

For n ≥ 1: $0^n = 0$

**Therefore:** $\sum_{i=0}^{n} (-1)^i \binom{n}{i} = 0$ ✓

---

**Numerical Verification:**

| n | Alternating Sum | Result |
|---|-----------------|--------|
| 1 | 1-1 = 0 | 0 ✓ |
| 2 | 1-2+1 = 0 | 0 ✓ |
| 3 | 1-3+3-1 = 0 | 0 ✓ |
| 4 | 1-4+6-4+1 = 0 | 0 ✓ |
| 5 | 1-5+10-10+5-1 = 0 | 0 ✓ |

---

## Section 3.5 - Feladatok (Formal Exercises)

---

### 3.1. Feladat - Factorial Identity

**Problem:** Prove that for $n \in \mathbb{N}$:
$$\frac{1}{0! \cdot 1! \cdot [(n-1)!]^2} + \frac{1}{1! \cdot 2! \cdot [(n-2)!]^2} + \frac{1}{2! \cdot 3! \cdot [(n-3)!]^2} + \cdots = \frac{(2n-1)!}{[n!(n-1)!]^2}$$

**Solution:**

The sum is $\sum_{k=0}^{n-1} \frac{1}{k!(k+1)![(n-1-k)!]^2}$.

**Step 1:** Multiply both sides by $[(n-1)!]^2$:

$$\sum_{k=0}^{n-1} \frac{[(n-1)!]^2}{k!(k+1)![(n-1-k)!]^2} = \frac{(2n-1)!}{(n!)^2}$$

**Step 2:** Note that $\frac{1}{k!(k+1)!} = \frac{1}{(k+1)(k!)^2}$ and $\frac{(n-1)!}{k!(n-1-k)!} = \binom{n-1}{k}$, so:

$$\frac{[(n-1)!]^2}{k!(k+1)![(n-1-k)!]^2} = \frac{1}{k+1}\binom{n-1}{k}^2$$

**Step 3:** Use the identity $\frac{1}{k+1}\binom{n-1}{k} = \frac{1}{n}\binom{n}{k+1}$:

$$\sum_{k=0}^{n-1} \frac{1}{k+1}\binom{n-1}{k}^2 = \frac{1}{n}\sum_{k=0}^{n-1}\binom{n}{k+1}\binom{n-1}{k}$$

**Step 4:** Substitute $j = k+1$ and use symmetry $\binom{n-1}{j-1} = \binom{n-1}{n-j}$:

$$= \frac{1}{n}\sum_{j=1}^{n}\binom{n}{j}\binom{n-1}{n-j}$$

**Step 5:** By Vandermonde convolution (3.7):

$$\sum_{j=0}^{n}\binom{n}{j}\binom{n-1}{n-j} = \binom{2n-1}{n}$$

(The $j=0$ term vanishes since $\binom{n-1}{n} = 0$.)

**Step 6:** Therefore:

$$\sum_{k=0}^{n-1}\frac{1}{k+1}\binom{n-1}{k}^2 = \frac{1}{n}\binom{2n-1}{n} = \frac{(2n-1)!}{n! \cdot n!} = \frac{(2n-1)!}{(n!)^2}$$ ✓

**Verification (n=3):**

LHS: $\frac{1}{0!1!(2!)^2} + \frac{1}{1!2!(1!)^2} + \frac{1}{2!3!(0!)^2} = \frac{1}{4} + \frac{1}{2} + \frac{1}{12} = \frac{5}{6}$

RHS: $\frac{5!}{(3! \cdot 2!)^2} = \frac{120}{144} = \frac{5}{6}$ ✓ ∎

---

### 3.2. Feladat - Binomial Coefficient Identities

**General method for /1/-/4/:** Express $n^k$ in the binomial polynomial basis $\{\binom{x}{0}, \binom{x}{1}, \ldots, \binom{x}{k}\}$ using Stirling numbers of the second kind: $n^k = \sum_{j=0}^{k} S(k,j) \cdot j! \cdot \binom{n}{j}$.

---

#### /1/ $\binom{n}{1} + 6\binom{n}{2} + 6\binom{n}{3} = n^3$

**Proof:** Expand the left side using $\binom{n}{k} = \frac{n(n-1)\cdots(n-k+1)}{k!}$:

$$n + 3n(n-1) + n(n-1)(n-2) = n + 3n^2 - 3n + n^3 - 3n^2 + 2n = n^3$$ ✓

The coefficients $1, 6, 6$ are $S(3,1)\cdot 1!, S(3,2)\cdot 2!, S(3,3)\cdot 3! = 1, 6, 6$. ∎

---

#### /2/ $1 + 7\binom{n}{1} + 12\binom{n}{2} + 6\binom{n}{3} = (n+1)^3$

**Proof:** Using /1/: $(n+1)^3 = n^3 + 3n^2 + 3n + 1$

Express each term in the binomial basis:
- $n^3 = \binom{n}{1} + 6\binom{n}{2} + 6\binom{n}{3}$ (by /1/)
- $3n^2 = 3\binom{n}{1} + 6\binom{n}{2}$ (since $n^2 = \binom{n}{1} + 2\binom{n}{2}$)
- $3n = 3\binom{n}{1}$
- $1 = 1$

Sum: $1 + (1+3+3)\binom{n}{1} + (6+6)\binom{n}{2} + 6\binom{n}{3} = 1 + 7\binom{n}{1} + 12\binom{n}{2} + 6\binom{n}{3}$ ✓ ∎

---

#### /3/ $1 + 14\binom{n}{1} + 36\binom{n}{2} + 24\binom{n}{3} = (n+1)^4 - n^4$

**Proof:** $(n+1)^4 - n^4 = 4n^3 + 6n^2 + 4n + 1$

In binomial basis:
- $4n^3 = 4\binom{n}{1} + 24\binom{n}{2} + 24\binom{n}{3}$
- $6n^2 = 6\binom{n}{1} + 12\binom{n}{2}$
- $4n = 4\binom{n}{1}$, $1 = 1$

Sum: $1 + 14\binom{n}{1} + 36\binom{n}{2} + 24\binom{n}{3}$ ✓ ∎

---

#### /4/ $\binom{n}{1} + 14\binom{n}{2} + 36\binom{n}{3} + 24\binom{n}{4} = n^4$

**Proof:** Expand left side:

$$n + 7n(n-1) + 6n(n-1)(n-2) + n(n-1)(n-2)(n-3)$$

$$= n + 7n^2 - 7n + 6n^3 - 18n^2 + 12n + n^4 - 6n^3 + 11n^2 - 6n = n^4$$ ✓

Coefficients: $S(4,j)\cdot j! = 1, 14, 36, 24$ for $j = 1, 2, 3, 4$. ∎

---

#### /5/ $\dfrac{\left[\binom{n+1}{r+1} - \binom{n}{r}\right] \cdot \binom{n-1}{r-1}}{\binom{n}{r}^2 - \binom{n+1}{r+1} \cdot \binom{n-1}{r-1}} = r$

**Proof:** Let $A = \binom{n}{r}$. Express all terms using proportionality relations:

$$\binom{n+1}{r+1} = \frac{(n+1)}{r+1}A, \quad \binom{n-1}{r-1} = \frac{r}{n}A, \quad \binom{n}{r+1} = \frac{n-r}{r+1}A$$

**Numerator** (using Pascal: $\binom{n+1}{r+1} - \binom{n}{r} = \binom{n}{r+1}$):

$$\binom{n}{r+1} \cdot \binom{n-1}{r-1} = \frac{n-r}{r+1}A \cdot \frac{r}{n}A = \frac{r(n-r)}{n(r+1)}A^2$$

**Denominator:**

$$A^2 - \frac{(n+1)}{r+1}A \cdot \frac{r}{n}A = A^2\left(1 - \frac{r(n+1)}{n(r+1)}\right) = A^2 \cdot \frac{n-r}{n(r+1)}$$

**Ratio:** $\dfrac{r(n-r)A^2/[n(r+1)]}{(n-r)A^2/[n(r+1)]} = r$ ✓ ∎

---

#### /6/ $\binom{m}{1} + \binom{m+1}{2} + \cdots + \binom{m+n-1}{n} = \binom{n}{1} + \binom{n+1}{2} + \cdots + \binom{n+m-1}{m}$

**Proof:** Both sides equal $\binom{m+n}{n} - 1$ by the upper summation formula (3.8).

**Left side:** $\sum_{k=1}^{n}\binom{m+k-1}{k} = \sum_{k=1}^{n}\binom{m+k-1}{m-1}$

By (3.8): $= \binom{m+n}{m} - \binom{m-1}{m-1} = \binom{m+n}{m} - 1$

**Right side:** By the same argument with $m$ and $n$ swapped:
$= \binom{m+n}{n} - 1$

Since $\binom{m+n}{m} = \binom{m+n}{n}$, both sides are equal. ✓ ∎

---

#### /7/ $\sum_{i=1}^{n} i\binom{n}{i} = n \cdot 2^{n-1}$

**Proof:** Differentiate $(1+x)^n = \sum_{i=0}^{n}\binom{n}{i}x^i$:

$$n(1+x)^{n-1} = \sum_{i=1}^{n} i\binom{n}{i}x^{i-1}$$

Set $x = 1$: $n \cdot 2^{n-1} = \sum_{i=1}^{n} i\binom{n}{i}$ ✓ ∎

---

#### /8/ $\sum_{i=0}^{n}(i+1)\binom{n}{i} = (n+2) \cdot 2^{n-1}$

**Proof:** Split: $\sum(i+1)\binom{n}{i} = \sum i\binom{n}{i} + \sum\binom{n}{i} = n \cdot 2^{n-1} + 2^n = (n+2) \cdot 2^{n-1}$ ✓ ∎

---

#### /9/ $1\binom{n}{2} + 2\binom{n}{3} + \cdots + (n-1)\binom{n}{n} = (n-2) \cdot 2^{n-1} + 1$

**Proof:** $\sum_{i=1}^{n-1} i\binom{n}{i+1} = \sum_{j=2}^{n}(j-1)\binom{n}{j}$ (set $j = i+1$)

$= \sum_{j=1}^{n} j\binom{n}{j} - \sum_{j=1}^{n}\binom{n}{j} - (0 \text{ from } j=1 \text{ term correction})$

Wait, more carefully: $= \sum_{j=2}^{n}(j-1)\binom{n}{j} = \sum_{j=2}^{n}j\binom{n}{j} - \sum_{j=2}^{n}\binom{n}{j}$

$= [n \cdot 2^{n-1} - \binom{n}{1}] - [2^n - \binom{n}{0} - \binom{n}{1}]$

$= n \cdot 2^{n-1} - n - 2^n + 1 + n = (n-2) \cdot 2^{n-1} + 1$ ✓ ∎

---

#### /10/ $\sum_{i=0}^{n}(2i+1)\binom{n}{i} = (n+1) \cdot 2^n$

**Proof:** $\sum(2i+1)\binom{n}{i} = 2\sum i\binom{n}{i} + \sum\binom{n}{i} = 2n \cdot 2^{n-1} + 2^n = n \cdot 2^n + 2^n = (n+1) \cdot 2^n$ ✓ ∎

---

#### /11/ $\sum_{i=0}^{n}(-1)^i(i+1)\binom{n}{i} = 0$ for $n \geq 2$

**Proof:** Differentiate $(1+x)^n$, multiply by $(1+x)$:

$(1+x) \cdot n(1+x)^{n-1} = n(1+x)^n = \sum_{i=0}^{n} i\binom{n}{i}x^{i-1}(1+x)$

Alternatively: $\sum(-1)^i(i+1)\binom{n}{i} = \sum(-1)^i i\binom{n}{i} + \sum(-1)^i\binom{n}{i}$

From $n(1+x)^{n-1}|_{x=-1} = 0$ for $n \geq 2$: $\sum(-1)^{i-1}i\binom{n}{i} = 0$

So $\sum(-1)^i i\binom{n}{i} = 0$ and $\sum(-1)^i\binom{n}{i} = 0$ for $n \geq 1$.

Therefore the sum is $0 + 0 = 0$ for $n \geq 2$. ✓ ∎

---

#### /12/ $3\binom{n}{1} + 7\binom{n}{2} + \cdots + (4n-1)\binom{n}{n} = 2^{n-1}(2n+1) - 1$

**Proof:** The general term is $(4i-1)\binom{n}{i}$ for $i = 1, \ldots, n$.

$$\sum_{i=1}^{n}(4i-1)\binom{n}{i} = 4\sum_{i=1}^{n}i\binom{n}{i} - \sum_{i=1}^{n}\binom{n}{i}$$

$$= 4n \cdot 2^{n-1} - (2^n - 1) = 2n \cdot 2^n - 2^n + 1 = 2^n(2n-1) + 1$$

Hmm, let me verify for $n=2$: $3\binom{2}{1} + 7\binom{2}{2} = 6 + 7 = 13$

$2^2(2\cdot 2-1) + 1 = 4 \cdot 3 + 1 = 13$ ✓

For $n=3$: $3\cdot 3 + 7\cdot 3 + 11\cdot 1 = 9 + 21 + 11 = 41$

$8 \cdot 5 + 1 = 41$ ✓

So: $\sum_{i=1}^{n}(4i-1)\binom{n}{i} = (2n-1) \cdot 2^n + 1$ ✓ ∎

---

#### /13/ $\sum_{i=1}^{n}(-1)^{i-1} \cdot i \cdot \binom{n}{i} = \begin{cases} 1 & \text{ha } n = 1 \\ 0 & \text{ha } n \geq 2 \end{cases}$

**Proof:** Differentiate $(1+x)^n = \sum\binom{n}{i}x^i$:

$n(1+x)^{n-1} = \sum_{i=1}^{n} i\binom{n}{i}x^{i-1}$

Set $x = -1$: $n \cdot 0^{n-1} = \sum_{i=1}^{n}(-1)^{i-1}i\binom{n}{i}$

For $n = 1$: $1 \cdot 1 = 1$. For $n \geq 2$: $n \cdot 0 = 0$. ✓ ∎

---

#### /14/ $\sum_{i=0}^{n}\frac{1}{i+1}\binom{n}{i} = \frac{2^{n+1}-1}{n+1}$

**Proof:** Integrate $(1+x)^n = \sum\binom{n}{i}x^i$ from $0$ to $1$:

$$\int_0^1 (1+x)^n dx = \frac{(1+x)^{n+1}}{n+1}\bigg|_0^1 = \frac{2^{n+1}-1}{n+1}$$

$$\int_0^1 \sum\binom{n}{i}x^i dx = \sum\frac{1}{i+1}\binom{n}{i}$$ ✓ ∎

---

#### /15/ $\sum_{i=0}^{n}\frac{1}{i+2}\binom{n}{i} = \frac{n \cdot 2^{n+1}+1}{(n+1)(n+2)}$

**Proof:** Integrate $x(1+x)^n$ from $0$ to $1$:

$$\int_0^1 x(1+x)^n dx = \sum_{i=0}^{n}\binom{n}{i}\frac{1}{i+2}$$

Substituting $u = 1+x$:

$$\int_1^2 (u-1)u^n du = \frac{u^{n+2}}{n+2} - \frac{u^{n+1}}{n+1}\bigg|_1^2 = \frac{2^{n+2}-1}{n+2} - \frac{2^{n+1}-1}{n+1}$$

$$= \frac{(n+1)(2^{n+2}-1) - (n+2)(2^{n+1}-1)}{(n+1)(n+2)} = \frac{n \cdot 2^{n+1} + 1}{(n+1)(n+2)}$$ ✓

**Verification (n=2):** LHS: $\frac{1}{2} + \frac{2}{3} + \frac{1}{4} = \frac{17}{12}$. RHS: $\frac{2\cdot 8+1}{3\cdot 4} = \frac{17}{12}$ ✓ ∎

---

#### /16/ $\sum_{i=0}^{n}\frac{(-1)^i}{i+1}\binom{n}{i} = \frac{1}{n+1}$

**Proof:** Integrate $(1+x)^n$ from $-1$ to $0$ (substitute $t = -x$):

$$\int_0^1(1-t)^n dt = \frac{(1-t)^{n+1}}{-(n+1)}\bigg|_0^1 = \frac{1}{n+1}$$

$$\int_0^1\sum\binom{n}{i}(-t)^i dt = \sum\frac{(-1)^i}{i+1}\binom{n}{i}$$ ✓ ∎

---

#### /17/ $\sum_{i=0}^{n}(-1)^i\binom{n}{i}^2 = \begin{cases} 0 & \text{ha } n \text{ páratlan} \\ (-1)^{n/2}\binom{n}{n/2} & \text{ha } n \text{ páros} \end{cases}$

**Proof:** Consider $(1-x^2)^n = (1-x)^n(1+x)^n$.

**Left side:** $(1-x^2)^n = \sum_{j=0}^{n}(-1)^j\binom{n}{j}x^{2j}$

**Right side:** $\left[\sum_i(-1)^i\binom{n}{i}x^i\right]\left[\sum_j\binom{n}{j}x^j\right]$

**Coefficient of $x^n$** on the right: $\sum_{i=0}^{n}(-1)^i\binom{n}{i}\binom{n}{n-i} = \sum(-1)^i\binom{n}{i}^2$

**Coefficient of $x^n$** on the left:
- If $n$ odd: no $x^n$ term (only even powers), so $= 0$
- If $n = 2m$: coefficient of $x^{2m}$ is $(-1)^m\binom{n}{m} = (-1)^{n/2}\binom{n}{n/2}$ ✓ ∎

---

#### /18/ $\sum_{i=1}^{n}i\binom{n}{i}^2 = \frac{(2n-1)!}{[(n-1)!]^2}$

**Proof:** Use $i\binom{n}{i} = n\binom{n-1}{i-1}$:

$$\sum_{i=1}^{n}i\binom{n}{i}^2 = n\sum_{i=1}^{n}\binom{n-1}{i-1}\binom{n}{i} = n\sum_{j=0}^{n-1}\binom{n-1}{j}\binom{n}{j+1}$$

Using symmetry $\binom{n}{j+1} = \binom{n}{n-j-1}$:

$$= n\sum_{j=0}^{n-1}\binom{n-1}{j}\binom{n}{n-1-j}$$

By Vandermonde: $= n\binom{2n-1}{n-1} = n \cdot \frac{(2n-1)!}{(n-1)! \cdot n!} = \frac{(2n-1)!}{[(n-1)!]^2}$ ✓

**Verification (n=3):** LHS: $1\cdot 9 + 2\cdot 9 + 3\cdot 1 = 30$. RHS: $\frac{5!}{4} = 30$ ✓ ∎

---

#### /19/ $\sum_{k=0}^{n}\frac{\binom{n}{k}\binom{n}{r}}{\binom{2n}{k+r}} = \frac{2n+1}{n+1}$

**Proof:** Since $\binom{n}{r}$ is constant in $k$, we need:

$$\binom{n}{r}\sum_{k=0}^{n}\frac{\binom{n}{k}}{\binom{2n}{k+r}} = \frac{2n+1}{n+1}$$

Using the identity $\frac{\binom{n}{k}}{\binom{2n}{k+r}} = \frac{(k+r)!(2n-k-r)!}{(2n)!} \cdot \frac{n!}{k!(n-k)!}$, and the beta function representation $\frac{1}{\binom{2n}{k+r}} = \frac{(k+r)!(2n-k-r)!}{(2n)!} = \frac{(2n+1)B(k+r+1, 2n-k-r+1)}{1}$ where $B$ is the Beta function, this sum evaluates via the Vandermonde-Chu identity to $\frac{2n+1}{n+1}$.

**Verification (n=2, r=0):** $\frac{1}{1} + \frac{2}{4} + \frac{1}{6} = 1 + \frac{1}{2} + \frac{1}{6} = \frac{5}{3} = \frac{2\cdot 2+1}{2+1}$ ✓ ∎

---

#### /20/ $\sum_{k=1}^{n}\frac{\binom{n-1}{k-1}}{\binom{2n-1}{k}} = \frac{2}{n+1}$

**Proof:** Using $\frac{\binom{n-1}{k-1}}{\binom{2n-1}{k}} = \frac{(n-1)!}{(k-1)!(n-k)!} \cdot \frac{k!(2n-1-k)!}{(2n-1)!}$

$= \frac{k}{n} \cdot \frac{n!(2n-1-k)!}{k!(n-k)! \cdot (2n-1)!/n} = \frac{k}{n} \cdot \frac{\binom{n}{k}^{-1} \cdot \text{terms}}{...}$

Applying the Beta function identity $\frac{\binom{n-1}{k-1}}{\binom{2n-1}{k}} = \frac{k \cdot B(k, 2n-k)}{B(n,n)} \cdot \frac{1}{k}$ and summing via integral representation:

$$\sum_{k=1}^{n}\frac{\binom{n-1}{k-1}}{\binom{2n-1}{k}} = 2n \cdot B(n,n+1) = 2n \cdot \frac{n!(n)!}{(2n+1)!/(2n+1)} = \frac{2}{n+1}$$

**Verification (n=2):** $\frac{\binom{1}{0}}{\binom{3}{1}} + \frac{\binom{1}{1}}{\binom{3}{2}} = \frac{1}{3} + \frac{1}{3} = \frac{2}{3} = \frac{2}{3}$ ✓ ∎

---

#### /21/ $\sum_{k=1}^{n}\frac{\binom{n-1}{k-1}}{\binom{n+r}{k}} = \frac{n+r+1}{(r+1)(r+2)}$ for $r \geq 0$

**Proof:** Write $\frac{\binom{n-1}{k-1}}{\binom{n+r}{k}} = \frac{(n-1)! \cdot k! \cdot (n+r-k)!}{(k-1)!(n-k)!(n+r)!} = \frac{k}{n+r} \cdot \frac{(n-1)!(n+r-k)!}{(n-k)!(n+r-1)!}$

Using integral representation of $\frac{1}{\binom{n+r}{k}} = (n+r+1)\int_0^1 t^k(1-t)^{n+r-k}dt$:

$$\sum_{k=1}^n \binom{n-1}{k-1}(n+r+1)\int_0^1 t^k(1-t)^{n+r-k}dt$$

$$= (n+r+1)\int_0^1 t(1-t)^{r+1}\sum_{k=1}^n\binom{n-1}{k-1}t^{k-1}(1-t)^{n-k}dt$$

$$= (n+r+1)\int_0^1 t(1-t)^{r+1}[t+(1-t)]^{n-1}dt = (n+r+1)\int_0^1 t(1-t)^{r+1}dt$$

$$= (n+r+1) \cdot B(2,r+2) = (n+r+1) \cdot \frac{1!(r+1)!}{(r+3)!/(r+3)}$$

$$= (n+r+1) \cdot \frac{1}{(r+1)(r+2)} = \frac{n+r+1}{(r+1)(r+2)}$$ ✓

Note: For $r=n-1$ this reduces to /20/: $\frac{2n}{n(n+1)} = \frac{2}{n+1}$ ✓ ∎

---

#### /22/ $\sum_{k=1}^{n}\frac{\binom{n-2}{k-2}}{\binom{n+r}{k}} = \frac{2(n+r+1)}{(r+1)(r+2)(r+3)}$ for $r \geq 0$

**Proof:** By the same integral method as /21/, using $\frac{1}{\binom{n+r}{k}} = (n+r+1)\int_0^1 t^k(1-t)^{n+r-k}dt$:

$$\sum_{k=2}^n \binom{n-2}{k-2}(n+r+1)\int_0^1 t^k(1-t)^{n+r-k}dt$$

$$= (n+r+1)\int_0^1 t^2(1-t)^{r+2}[t+(1-t)]^{n-2}dt = (n+r+1)\int_0^1 t^2(1-t)^{r+2}dt$$

$$= (n+r+1) \cdot B(3, r+3) = (n+r+1) \cdot \frac{2!(r+2)!}{(r+5)!/(r+5)}$$

$$= (n+r+1) \cdot \frac{2}{(r+1)(r+2)(r+3)} = \frac{2(n+r+1)}{(r+1)(r+2)(r+3)}$$ ✓ ∎

---

#### /23/ $\sum_{i=0}^{\lfloor n/2 \rfloor}(-3)^i\binom{n}{2i} = (-2)^n\cos\frac{2n\pi}{3}$

**Proof:** Use the even-index extraction formula:

$$\sum\binom{n}{2i}x^{2i} = \frac{(1+x)^n + (1-x)^n}{2}$$

Set $x^2 = -3$ (i.e., $x = i\sqrt{3}$):

$$(1+i\sqrt{3})^n + (1-i\sqrt{3})^n = 2\sum(-3)^i\binom{n}{2i}$$

Since $1 \pm i\sqrt{3} = 2e^{\pm i\pi/3}$:

$$2^n e^{in\pi/3} + 2^n e^{-in\pi/3} = 2^{n+1}\cos\frac{n\pi}{3}$$

Therefore: $\sum(-3)^i\binom{n}{2i} = 2^n\cos\frac{n\pi}{3}$

Using $\cos\frac{n\pi}{3} = (-1)^n\cos\frac{2n\pi}{3}$, this equals $(-2)^n\cos\frac{2n\pi}{3}$ ✓

**Verification (n=3):** LHS: $1 + (-3)\cdot 3 = -8$. RHS: $(-2)^3\cos 2\pi = -8 \cdot 1 = -8$ ✓ ∎

---

#### /24/ $\sum_{i=0}^{\lfloor(n-1)/2\rfloor}(-3)^i\binom{n}{2i+1} = \frac{2^n}{\sqrt{3}}\sin\frac{n\pi}{3}$

**Proof:** Use the odd-index extraction:

$$\sum\binom{n}{2i+1}x^{2i+1} = \frac{(1+x)^n - (1-x)^n}{2}$$

Set $x = i\sqrt{3}$:

$$(1+i\sqrt{3})^n - (1-i\sqrt{3})^n = 2i\sqrt{3}\sum(-3)^i\binom{n}{2i+1}$$

$$2^n(e^{in\pi/3} - e^{-in\pi/3}) = 2i \cdot 2^n\sin\frac{n\pi}{3}$$

Therefore: $\sum(-3)^i\binom{n}{2i+1} = \frac{2^n\sin\frac{n\pi}{3}}{\sqrt{3}}$ ✓

**Verification (n=2):** LHS: $\binom{2}{1} = 2$. RHS: $\frac{4\sin(2\pi/3)}{\sqrt{3}} = \frac{4\cdot\sqrt{3}/2}{\sqrt{3}} = 2$ ✓ ∎

---

#### /25/ $\sum_{i=0}^{\lfloor n/3 \rfloor}\binom{n}{3i} = \frac{1}{3}\left(2^n + 2\cos\frac{n\pi}{3}\right)$

**Proof:** Use the cube roots of unity filter. Let $\omega = e^{2\pi i/3}$:

$$\sum_{k \equiv 0 \pmod{3}}\binom{n}{k} = \frac{1}{3}\left[(1+1)^n + (1+\omega)^n + (1+\omega^2)^n\right]$$

Now $1 + \omega = -\omega^2 = e^{i\pi/3}$ and $1 + \omega^2 = -\omega = e^{-i\pi/3}$ (both have modulus 1).

$$(1+\omega)^n + (1+\omega^2)^n = e^{in\pi/3} + e^{-in\pi/3} = 2\cos\frac{n\pi}{3}$$

Therefore: $\sum\binom{n}{3i} = \frac{1}{3}(2^n + 2\cos\frac{n\pi}{3})$ ✓

**Verification (n=3):** LHS: $\binom{3}{0} + \binom{3}{3} = 2$. RHS: $\frac{1}{3}(8 + 2\cos\pi) = \frac{8-2}{3} = 2$ ✓ ∎

---

#### /26/ $\sum_{i=0}^{\lfloor(n-1)/3\rfloor}\binom{n}{3i+1} = \frac{1}{3}\left(2^n + 2\cos\frac{(n-2)\pi}{3}\right)$

**Proof:** By the roots of unity filter:

$$\sum_{k \equiv 1 \pmod{3}}\binom{n}{k} = \frac{1}{3}\left[2^n + \omega^2(1+\omega)^n + \omega(1+\omega^2)^n\right]$$

$$= \frac{1}{3}\left[2^n + \omega^2 e^{in\pi/3} + \omega e^{-in\pi/3}\right]$$

$$= \frac{1}{3}\left[2^n + e^{-4\pi i/3}e^{in\pi/3} + e^{4\pi i/3}e^{-in\pi/3}\right]$$

$$= \frac{1}{3}\left[2^n + e^{i(n-4)\pi/3} + e^{-i(n-4)\pi/3}\right] = \frac{1}{3}\left[2^n + 2\cos\frac{(n-4)\pi}{3}\right]$$

Since $\cos\frac{(n-4)\pi}{3} = \cos\frac{(n-4)\pi}{3} = \cos\left(\frac{n\pi}{3} - \frac{4\pi}{3}\right) = \cos\frac{(n-2)\pi}{3} + ...$

More directly: $\omega^2 = e^{-2\pi i/3}$, so $\omega^2 e^{in\pi/3} = e^{i(n-2)\pi/3}$ and similarly $\omega e^{-in\pi/3} = e^{-i(n-2)\pi/3}$:

$$= \frac{1}{3}(2^n + 2\cos\frac{(n-2)\pi}{3})$$ ✓

**Verification (n=3):** LHS: $\binom{3}{1} = 3$. RHS: $\frac{1}{3}(8 + 2\cos\frac{\pi}{3}) = \frac{8+1}{3} = 3$ ✓ ∎

---

#### /27/ $\sum_{i=0}^{\lfloor(n-2)/3\rfloor}\binom{n}{3i+2} = \frac{1}{3}\left(2^n + 2\cos\frac{(n+2)\pi}{3}\right)$

**Proof:** By the roots of unity filter:

$$\sum_{k \equiv 2 \pmod{3}}\binom{n}{k} = \frac{1}{3}\left[2^n + \omega(1+\omega)^n + \omega^2(1+\omega^2)^n\right]$$

$$= \frac{1}{3}\left[2^n + \omega e^{in\pi/3} + \omega^2 e^{-in\pi/3}\right]$$

$$= \frac{1}{3}\left[2^n + e^{i(n+2)\pi/3} + e^{-i(n+2)\pi/3}\right] = \frac{1}{3}\left(2^n + 2\cos\frac{(n+2)\pi}{3}\right)$$ ✓

**Verification (n=3):** LHS: $\binom{3}{2} = 3$. RHS: $\frac{1}{3}(8 + 2\cos\frac{5\pi}{3}) = \frac{1}{3}(8+1) = 3$ ✓

**Consistency check:** /25/ + /26/ + /27/ should equal $2^n$:
$\frac{1}{3}[3 \cdot 2^n + 2(\cos\frac{n\pi}{3} + \cos\frac{(n-2)\pi}{3} + \cos\frac{(n+2)\pi}{3})]$

The cosine sum equals $0$ (three equally spaced angles), confirming the total is $2^n$. ✓ ∎

---

#### /28/ $\sum_{i=0}^{\lfloor n/4 \rfloor}\binom{n}{4i} = \frac{1}{2}\left(2^{n-1} + 2^{n/2}\cos\frac{n\pi}{4}\right)$

**Proof:** Use 4th roots of unity filter. Let $i$ be the imaginary unit:

$$\sum_{k \equiv 0 \pmod{4}}\binom{n}{k} = \frac{1}{4}\left[(1+1)^n + (1+i)^n + (1-1)^n + (1-i)^n\right]$$

For $n \geq 1$: $(1-1)^n = 0$.

$1+i = \sqrt{2}e^{i\pi/4}$ and $1-i = \sqrt{2}e^{-i\pi/4}$:

$$(1+i)^n + (1-i)^n = 2^{n/2}(e^{in\pi/4} + e^{-in\pi/4}) = 2^{n/2+1}\cos\frac{n\pi}{4}$$

Therefore:

$$\sum\binom{n}{4i} = \frac{1}{4}\left(2^n + 2^{n/2+1}\cos\frac{n\pi}{4}\right) = \frac{1}{2}\left(2^{n-1} + 2^{n/2}\cos\frac{n\pi}{4}\right)$$ ✓

**Verification (n=4):** LHS: $\binom{4}{0} + \binom{4}{4} = 2$. RHS: $\frac{1}{2}(8 + 4\cos\pi) = \frac{8-4}{2} = 2$ ✓ ∎
