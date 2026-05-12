# Chapter 02 - Elemi leszámlálások (Elementary Counting) - Complete Solutions

## Section 2.1 - Általános módszerek (General Methods)

---

### Exercise 2.1.1 - Three Counting Principles

**Problem:** Verify the three counting principles with your own examples.

**Solution:**

**The Three Principles:**

1. **Did we count everything?** (Mindent összeszámoltunk?)
2. **Did we count nothing twice?** (Semmit sem kétszer?)
3. **Did we count only set elements?** (Csak a halmaz elemeit?)

---

**Example Problem:** Count integers from 1 to 100 divisible by 3 or 5.

**Step 1: Count everything relevant**

- Divisible by 3: ⌊100/3⌋ = 33 numbers
  - These are: 3, 6, 9, ..., 99
- Divisible by 5: ⌊100/5⌋ = 20 numbers
  - These are: 5, 10, 15, ..., 100

**Step 2: Check for double-counting**

- Divisible by both 3 and 5 = divisible by 15
- ⌊100/15⌋ = 6 numbers
  - These are: 15, 30, 45, 60, 75, 90

**Step 3: Apply inclusion-exclusion**

Total = (divisible by 3) + (divisible by 5) - (divisible by both)
      = 33 + 20 - 6
      = 47

**Verification:**
- Principle 1: We counted all numbers divisible by 3 or 5 ✓
- Principle 2: We subtracted the overlap, so nothing counted twice ✓
- Principle 3: We only counted integers in our range [1,100] ✓

**Answer:** 47 numbers ✓

---

### Exercise 2.1.2 - Addition Rule (Disjoint Sets)

**Problem:** Practice the addition rule for disjoint sets.

**Solution:**

**Addition Rule:** If A and B are disjoint (A ∩ B = ∅), then:
$$|A \cup B| = |A| + |B|$$

---

**Example 1:** Count cards that are Kings OR Queens in a deck.

- Kings: 4 cards (disjoint from Queens)
- Queens: 4 cards (disjoint from Kings)
- Total: 4 + 4 = 8 cards ✓

---

**Example 2:** Count students who are freshmen OR sophomores.

- Freshmen: 150 students
- Sophomores: 140 students
- No student is both (disjoint)
- Total: 150 + 140 = 290 students ✓

---

**Generalization:** For k disjoint sets:
$$|A_1 \cup A_2 \cup \cdots \cup A_k| = |A_1| + |A_2| + \cdots + |A_k|$$

---

### Exercise 2.1.3 - Multiplication Rule (Independent Choices)

**Problem:** Practice the multiplication rule for independent choices.

**Solution:**

**Multiplication Rule:** If we make k independent choices, where choice i has nᵢ options:
$$\text{Total outcomes} = n_1 \times n_2 \times \cdots \times n_k$$

---

**Example 1:** Count 3-letter codes using {A, B, C, D}.

- Position 1: 4 choices
- Position 2: 4 choices (independent of position 1)
- Position 3: 4 choices (independent of positions 1, 2)

**Total:** 4 × 4 × 4 = 64 codes ✓

**Verification by listing (partial):**
AAA, AAB, AAC, AAD, ABA, ABB, ABC, ABD, ..., DDD

---

**Example 2:** Count outfits from 3 shirts, 4 pants, 2 shoes.

- Shirt: 3 choices
- Pants: 4 choices (independent)
- Shoes: 2 choices (independent)

**Total:** 3 × 4 × 2 = 24 outfits ✓

---

**Example 3:** License plates with 3 letters followed by 3 digits.

- Letters: 26³ = 17,576 combinations
- Digits: 10³ = 1,000 combinations

**Total:** 26³ × 10³ = 17,576,000 plates ✓

---

### Exercise 2.1.4 - Bijection Method

**Problem:** Practice the bijection method for counting.

**Solution:**

**Bijection Method:** To count set A, find a bijection f: A → B where |B| is known.

Then |A| = |B|.

---

**Example 1:** Count subsets of {1, 2, 3}.

**Bijection:** Each subset ↔ binary string of length 3

| Subset | Binary | Explanation |
|--------|--------|-------------|
| ∅ | 000 | No elements selected |
| {1} | 100 | Element 1 selected |
| {2} | 010 | Element 2 selected |
| {3} | 001 | Element 3 selected |
| {1,2} | 110 | Elements 1,2 selected |
| {1,3} | 101 | Elements 1,3 selected |
| {2,3} | 011 | Elements 2,3 selected |
| {1,2,3} | 111 | All elements selected |

**Count:** 2³ = 8 subsets ✓

---

**Example 2:** Count paths from (0,0) to (3,2) moving only right (R) and up (U).

**Bijection:** Each path ↔ string with 3 R's and 2 U's

**Example path:** RRUUR means: Right, Right, Up, Up, Right

**Count:** Number of ways to arrange 3 R's and 2 U's
$$= \binom{5}{3} = \binom{5}{2} = 10$$

**Verification by listing:**
RRRUU, RRURU, RRUUR, RURRU, RURUR, RUURR, URRRU, URRUR, URURR, UURRR

**Total:** 10 paths ✓

---

### Exercise 2.1.5 - Prove |P(A)| = 2ⁿ

**Problem:** Prove that the power set of an n-element set has 2ⁿ elements.

**Solution:**

**Theorem:** If |A| = n, then |P(A)| = 2ⁿ.

---

**Proof 1 (Bijection method):**

Let A = {a₁, a₂, ..., aₙ}.

**Bijection:** Each subset S ⊆ A ↔ binary string of length n.

**Construction:** For subset S, define string b₁b₂...bₙ where:
- bᵢ = 1 if aᵢ ∈ S
- bᵢ = 0 if aᵢ ∉ S

**Example:** A = {1, 2, 3}, S = {1, 3}
- String: 101 (1 is in S, 2 is not, 3 is in S)

This is a bijection because:
- Every subset gives a unique string
- Every string corresponds to a unique subset

**Count:** Number of binary strings of length n = 2ⁿ

**Therefore:** |P(A)| = 2ⁿ. ✓

---

**Proof 2 (Induction):**

**Base case (n=0):** A = ∅, P(A) = {∅}, |P(A)| = 1 = 2⁰. ✓

**Inductive step:** Assume |P(A)| = 2ⁿ for |A| = n.

Let B = A ∪ {x} where x ∉ A, so |B| = n+1.

Subsets of B are of two types:
1. Subsets not containing x: These are exactly subsets of A. Count = 2ⁿ.
2. Subsets containing x: Each is S ∪ {x} where S ⊆ A. Count = 2ⁿ.

**Total:** |P(B)| = 2ⁿ + 2ⁿ = 2 × 2ⁿ = 2ⁿ⁺¹. ✓

**By induction:** |P(A)| = 2ⁿ for all n ≥ 0. ✓

---

**Proof 3 (Binomial theorem):**

Subsets of size k: $\binom{n}{k}$

Total subsets: $\sum_{k=0}^{n} \binom{n}{k} = 2^n$ (by binomial theorem with a=b=1)

**Therefore:** |P(A)| = 2ⁿ. ✓

---

### Exercise 2.1.6 - Count Functions |Bᴬ|

**Problem:** Calculate the number of functions from A to B.

**Solution:**

**Theorem:** If |A| = n and |B| = m, then the number of functions f: A → B is mⁿ.

---

**Proof:**

Let A = {a₁, a₂, ..., aₙ} and B = {b₁, b₂, ..., bₘ}.

A function f is determined by specifying f(aᵢ) for each i.

- f(a₁): m choices (any element of B)
- f(a₂): m choices (independent of f(a₁))
- ...
- f(aₙ): m choices (independent of previous)

**Total:** m × m × ... × m (n times) = mⁿ ✓

---

**Example 1:** Functions from {1, 2} to {a, b, c}.

- n = 2, m = 3
- Total: 3² = 9 functions

**List:**
1. f(1)=a, f(2)=a
2. f(1)=a, f(2)=b
3. f(1)=a, f(2)=c
4. f(1)=b, f(2)=a
5. f(1)=b, f(2)=b
6. f(1)=b, f(2)=c
7. f(1)=c, f(2)=a
8. f(1)=c, f(2)=b
9. f(1)=c, f(2)=c

**Count:** 9 ✓

---

**Example 2:** Binary strings of length n.

- This is functions from {1, ..., n} to {0, 1}
- n positions, 2 choices each
- Total: 2ⁿ ✓

---

## Section 2.2 - Teljes indukció (Complete Induction)

---

### Exercise 2.2.1 - Sum of First n Odd Numbers

**Problem:** Prove: 1 + 3 + 5 + ... + (2n-1) = n².

**Solution:**

**Theorem:** For all n ≥ 1:
$$\sum_{i=1}^{n} (2i-1) = n^2$$

---

**Proof by Induction:**

**Base case (n=1):**
- Left side: 2(1)-1 = 1
- Right side: 1² = 1
- 1 = 1 ✓

---

**Inductive hypothesis:** Assume true for n = k:
$$1 + 3 + 5 + \cdots + (2k-1) = k^2$$

---

**Inductive step (n = k+1):**

We need to prove: 1 + 3 + ... + (2k-1) + (2(k+1)-1) = (k+1)²

Left side:
$$= [1 + 3 + \cdots + (2k-1)] + (2k+1)$$
$$= k^2 + (2k+1)$$ (by inductive hypothesis)
$$= k^2 + 2k + 1$$
$$= (k+1)^2$$

**Therefore:** The formula holds for n = k+1. ✓

---

**By induction:** The formula holds for all n ≥ 1. ∎

---

**Alternative Proof (Visual):**

```
n=1: ■           = 1 = 1²
n=2: ■■
     ■■          = 4 = 2²
n=3: ■■■
     ■■■
     ■■■         = 9 = 3²
```

Each odd number adds an L-shaped layer to make a larger square.

---

### Exercise 2.2.2 - Triangle Inequality

**Problem:** Prove |z₁ + z₂| ≤ |z₁| + |z₂| for vectors/complex numbers.

**Solution:**

**Theorem (Triangle Inequality):** For any vectors $\vec{a}, \vec{b}$ in ℝⁿ:
$$|\vec{a} + \vec{b}| \leq |\vec{a}| + |\vec{b}|$$

---

**Proof for ℝ²:**

Let $\vec{a} = (a_1, a_2)$ and $\vec{b} = (b_1, b_2)$.

**Step 1:** Expand |$\vec{a} + \vec{b}$|²:
$$|\vec{a} + \vec{b}|^2 = (a_1+b_1)^2 + (a_2+b_2)^2$$
$$= a_1^2 + 2a_1b_1 + b_1^2 + a_2^2 + 2a_2b_2 + b_2^2$$
$$= |\vec{a}|^2 + |\vec{b}|^2 + 2(a_1b_1 + a_2b_2)$$
$$= |\vec{a}|^2 + |\vec{b}|^2 + 2\vec{a} \cdot \vec{b}$$

---

**Step 2:** Use Cauchy-Schwarz inequality:
$$\vec{a} \cdot \vec{b} \leq |\vec{a}||\vec{b}|$$

Therefore:
$$|\vec{a} + \vec{b}|^2 \leq |\vec{a}|^2 + |\vec{b}|^2 + 2|\vec{a}||\vec{b}|$$
$$= (|\vec{a}| + |\vec{b}|)^2$$

---

**Step 3:** Take square root (both sides non-negative):
$$|\vec{a} + \vec{b}| \leq |\vec{a}| + |\vec{b}|$$ ✓

---

**Geometric Interpretation:**

In a triangle with sides |$\vec{a}$|, |$\vec{b}$|, |$\vec{a} + \vec{b}$|:

The sum of any two sides ≥ the third side.

Equality holds when $\vec{a}$ and $\vec{b}$ point in the same direction.

---

**For Complex Numbers:**

Same proof works with complex modulus:
$$|z_1 + z_2| \leq |z_1| + |z_2|$$

---

### Exercise 2.2.3 - Complete Induction Practice

**Problem:** Practice the complete induction method.

**Solution:**

**Complete Induction (Strong Induction):**

To prove P(n) for all n ≥ n₀:
1. **Base case:** Prove P(n₀)
2. **Inductive step:** Assume P(k) for ALL k with n₀ ≤ k < n, prove P(n)

---

**Example:** Prove every integer n ≥ 2 can be written as a product of primes.

**Base case (n=2):** 2 is prime, so it's a product of one prime. ✓

**Inductive step:** Assume all integers from 2 to n-1 can be written as products of primes.

For n:
- **Case 1:** n is prime. Then n is a product of one prime. ✓
- **Case 2:** n is composite. Then n = ab where 2 ≤ a, b < n.
  - By induction hypothesis, a and b are products of primes.
  - Therefore n = ab is a product of primes. ✓

**By complete induction:** Every n ≥ 2 is a product of primes. ∎

---

## Section 2.3 - Permutációk, variációk, kombinációk

---

### Exercise 2.3.1 - Verify 0! = 1

**Problem:** Verify that 0! = 1 makes formulas work.

**Solution:**

**Why 0! = 1?**

---

**Reason 1: Empty product convention**

The product of no numbers (empty product) is defined as 1 (multiplicative identity).

n! = 1 × 2 × ... × n

For n = 0, this is an empty product = 1. ✓

---

**Reason 2: Permutation formula**

Pₙ = n! should count permutations of n elements.

For n = 0: There is exactly 1 way to arrange nothing (do nothing).

So P₀ = 0! = 1. ✓

---

**Reason 3: Binomial coefficient**

$$\binom{n}{0} = \frac{n!}{0! \cdot n!}$$

We know $\binom{n}{0} = 1$ (one way to choose nothing).

So: $1 = \frac{n!}{0! \cdot n!} = \frac{1}{0!}$

Therefore: 0! = 1. ✓

---

**Reason 4: Recursive formula**

n! = n × (n-1)!

For n = 1: 1! = 1 × 0!

Since 1! = 1: 1 = 1 × 0!

Therefore: 0! = 1. ✓

---

### Exercise 2.3.2 - Prove Pₙ = n!

**Problem:** Prove by induction that the number of permutations of n elements is n!.

**Solution:**

**Theorem:** Pₙ = n!

---

**Proof by Induction:**

**Base case (n=1):**
- One element: only 1 permutation
- 1! = 1
- P₁ = 1! ✓

---

**Inductive hypothesis:** Assume Pₖ = k! for some k ≥ 1.

---

**Inductive step (n = k+1):**

Consider permutations of {1, 2, ..., k+1}.

**Method:** Place element (k+1) in one of (k+1) positions, then permute the rest.

- Choose position for (k+1): (k+1) choices
- Permute remaining k elements: Pₖ = k! ways (by induction)

**Total:** Pₖ₊₁ = (k+1) × k! = (k+1)! ✓

---

**By induction:** Pₙ = n! for all n ≥ 1. ∎

---

**Alternative Proof (Direct counting):**

For permutation of {1, 2, ..., n}:
- Position 1: n choices
- Position 2: (n-1) choices
- ...
- Position n: 1 choice

**Total:** n × (n-1) × ... × 1 = n! ✓

---

### Exercise 2.3.3 - Repeated Permutations

**Problem:** Understand the formula for permutations with repetition.

**Solution:**

**Theorem:** The number of permutations of n objects where:
- k₁ are of type 1
- k₂ are of type 2
- ...
- kₛ are of type s
- k₁ + k₂ + ... + kₛ = n

is:
$$P_n^{(k_1, k_2, \ldots, k_s)} = \frac{n!}{k_1! k_2! \cdots k_s!}$$

---

**Example:** MISSISSIPPI

Letters: M(1), I(4), S(4), P(2)
Total: 11 letters

**Count:**
$$\frac{11!}{1! \cdot 4! \cdot 4! \cdot 2!} = \frac{39916800}{1 \cdot 24 \cdot 24 \cdot 2} = 34650$$

---

**Proof:**

Start with n! permutations if all were distinct.

But objects of the same type are indistinguishable:
- k₁! ways to permute type-1 objects (all same, so overcounted)
- k₂! ways to permute type-2 objects
- ...

**Correction:** Divide by each kᵢ!

**Result:** $\frac{n!}{k_1! k_2! \cdots k_s!}$ ✓

---

### Exercise 2.3.4 - Polynomial (Multinomial) Coefficients

**Problem:** Understand multinomial coefficients.

**Solution:**

**Definition:**
$$\binom{n}{k_1, k_2, \ldots, k_s} = \frac{n!}{k_1! k_2! \cdots k_s!}$$

where k₁ + k₂ + ... + kₛ = n.

---

**Interpretation:** Number of ways to partition n distinct objects into s groups of sizes k₁, k₂, ..., kₛ.

---

**Example:** Distribute 5 distinct books to 3 shelves with 2, 2, 1 books.

**Count:**
$$\binom{5}{2, 2, 1} = \frac{5!}{2! \cdot 2! \cdot 1!} = \frac{120}{4} = 30$$

---

**Multinomial Theorem:**
$$(x_1 + x_2 + \cdots + x_s)^n = \sum_{k_1 + \cdots + k_s = n} \binom{n}{k_1, \ldots, k_s} x_1^{k_1} \cdots x_s^{k_s}$$

---

**Example:** (a + b + c)³

$$= a^3 + b^3 + c^3 + 3a^2b + 3a^2c + 3b^2a + 3b^2c + 3c^2a + 3c^2b + 6abc$$

Coefficients:
- a³: $\binom{3}{3,0,0} = 1$
- a²b: $\binom{3}{2,1,0} = 3$
- abc: $\binom{3}{1,1,1} = 6$

---

### Exercise 2.3.5 - Prove Vₙᵏ = n(n-1)...(n-k+1)

**Problem:** Prove the formula for variations (permutations of k from n).

**Solution:**

**Theorem:** 
$$V_n^k = n(n-1)(n-2)\cdots(n-k+1) = \frac{n!}{(n-k)!}$$

---

**Proof (Direct counting):**

We want to count ordered k-tuples from n elements (no repetition).

- Position 1: n choices
- Position 2: (n-1) choices (can't repeat)
- Position 3: (n-2) choices
- ...
- Position k: (n-k+1) choices

**Total:** n × (n-1) × ... × (n-k+1) ✓

---

**Alternative form:**
$$n(n-1)\cdots(n-k+1) = \frac{n!}{(n-k)!}$$

**Verification:**
$$\frac{n!}{(n-k)!} = \frac{n(n-1)\cdots(n-k+1)(n-k)!}{(n-k)!} = n(n-1)\cdots(n-k+1)$$ ✓

---

**Example:** V₅³ = 5 × 4 × 3 = 60

Or: $\frac{5!}{(5-3)!} = \frac{120}{2} = 60$ ✓

---

### Exercise 2.3.6 - Prove Vₙᵏ⁽ⁱˢᵐ⁾ = nᵏ

**Problem:** Prove the formula for variations with repetition.

**Solution:**

**Theorem:** 
$$V_n^{k(\text{ism})} = n^k$$

(ismétléses = with repetition)

---

**Proof (Direct counting):**

We want to count ordered k-tuples from n elements (repetition allowed).

- Position 1: n choices
- Position 2: n choices (can repeat)
- Position 3: n choices
- ...
- Position k: n choices

**Total:** n × n × ... × n (k times) = nᵏ ✓

---

**Example:** V₃⁴⁽ⁱˢᵐ⁾ = 3⁴ = 81

Using digits {0, 1, 2}, count 4-digit sequences:
0000, 0001, 0002, 0010, ..., 2222

**Count:** 81 ✓

---

### Exercise 2.3.7 - Prove Cₙᵏ = $\binom{n}{k}$

**Problem:** Prove the formula for combinations.

**Solution:**

**Theorem:**
$$C_n^k = \binom{n}{k} = \frac{n!}{k!(n-k)!}$$

---

**Proof (Relation to variations):**

Variations Vₙᵏ count ORDERED selections.
Combinations Cₙᵏ count UNORDERED selections.

**Relationship:** Each k-element set can be ordered in k! ways.

Therefore: Vₙᵏ = Cₙᵏ × k!

Solving for Cₙᵏ:
$$C_n^k = \frac{V_n^k}{k!} = \frac{n!}{k!(n-k)!}$$ ✓

---

**Alternative Proof (Direct):**

Choose k elements from n:
- First choose k positions from n: $\binom{n}{k}$ ways
- Each choice gives one k-element subset

**Therefore:** Cₙᵏ = $\binom{n}{k}$ ✓

---

**Example:** C₅³ = $\binom{5}{3} = \frac{5!}{3!2!} = 10$

Subsets of size 3 from {1,2,3,4,5}:
{1,2,3}, {1,2,4}, {1,2,5}, {1,3,4}, {1,3,5}, {1,4,5}, {2,3,4}, {2,3,5}, {2,4,5}, {3,4,5}

**Count:** 10 ✓

---

### Exercise 2.3.8 - Prove Cₙᵏ⁽ⁱˢᵐ⁾ = $\binom{n+k-1}{k}$

**Problem:** Prove the formula for combinations with repetition.

**Solution:**

**Theorem:**
$$C_n^{k(\text{ism})} = \binom{n+k-1}{k}$$

---

**Proof (Stars and Bars):**

We want to count multisets of size k from n types.

**Bijection:** Multiset ↔ Sequence of k stars and (n-1) bars.

**Example:** n=3 types {A, B, C}, k=4 elements
- **|*|** means: 1 A, 0 B, 3 C

**Count:**
- Total positions: k + (n-1) = n+k-1
- Choose k positions for stars: $\binom{n+k-1}{k}$

**Therefore:** Cₙᵏ⁽ⁱˢᵐ⁾ = $\binom{n+k-1}{k}$ ✓

---

**Example:** Choose 3 fruits from {apple, banana, cherry} with repetition.

n=3, k=3

$$C_3^{3(\text{ism})} = \binom{3+3-1}{3} = \binom{5}{3} = 10$$

**List:** AAA, AAB, AAC, ABB, ABC, ACC, BBB, BBC, BCC, CCC

**Count:** 10 ✓

---

### Exercise 2.3.9 - Prove Cₙᵏ = Cₙⁿ⁻ᵏ

**Problem:** Prove the symmetry of binomial coefficients.

**Solution:**

**Theorem:**
$$\binom{n}{k} = \binom{n}{n-k}$$

---

**Proof 1 (Algebraic):**

$$\binom{n}{k} = \frac{n!}{k!(n-k)!}$$

$$\binom{n}{n-k} = \frac{n!}{(n-k)!(n-(n-k))!} = \frac{n!}{(n-k)!k!}$$

**Therefore:** $\binom{n}{k} = \binom{n}{n-k}$ ✓

---

**Proof 2 (Combinatorial):**

Choosing k elements to INCLUDE is the same as choosing (n-k) elements to EXCLUDE.

**Example:** From {1,2,3,4,5}:
- Choose 2 to include: {1,2} → Exclude {3,4,5}
- Choose 3 to exclude: {3,4,5} → Include {1,2}

**Same choice!**

**Therefore:** $\binom{n}{k} = \binom{n}{n-k}$ ✓

---

**Example:** $\binom{5}{2} = \binom{5}{3} = 10$ ✓

---

### Exercise 2.3.10 - Bijection: Elements with Replacement ↔ Dash Sequences

**Problem:** Prove the bijection between multisets and dash sequences.

**Solution:**

**Theorem:** There is a bijection between:
- Multisets of size k from n types
- Sequences of k stars and (n-1) bars

---

**Construction:**

Given multiset, create sequence:
- For each type i, place kᵢ stars (where kᵢ = count of type i)
- Separate types with bars

**Example:** n=4 types {A,B,C,D}, multiset = {A,A,B,D,D,D}

Sequence: **|*||*** 

(2 A's, 1 B, 0 C's, 3 D's)

---

**Reverse:** Given sequence, read off counts between bars.

**Example:** *|**||* means: 1 A, 2 B's, 0 C's, 1 D

---

**Verification:**

- Every multiset gives a unique sequence
- Every sequence gives a unique multiset
- Total sequences: $\binom{n+k-1}{k}$ (choose k positions for stars)

**Therefore:** The bijection is valid. ✓

---

## Gyakorló feladatok (kombB előadás, 2021-03-06)

A 2021. március 6-i levelező-kombinatorika gyakorló előadás négy fő típusfeladata kidolgozva.

---

### Exercise 2.4.1 - Csónak feladat (eset-szétbontás + binomiális együtthatók)

**Probléma:** Egy 8 férőhelyes csónakba (4-4 hely a két oldalon) 43 ember akar beszállni. Közülük

- **12 fő** csak a **jobb** oldalra hajlandó ülni,
- **13 fő** csak a **bal** oldalra hajlandó ülni,
- **18 fő** mindegyik oldalra hajlandó ülni.

Hányféle 8-fős utaslista állítható össze úgy, hogy mindenki a saját preferenciájának megfelelő oldalra ülhessen? Az emberek megkülönböztethetők; a sorrend (ki ül elöl/hátul) **nem** számít — csak az számít, kik kerülnek be.

**Megoldás:**

**Lépés 1 — Változók bevezetése.** Legyen $j$ = beválasztott jobboldaliak száma, $b$ = beválasztott baloldaliaké. A maradék $8 - j - b$ embert a 18-fős „mindegy" csoportból választjuk.

**Lépés 2 — Korlátok rögzítése.** A csónak mindkét oldalán pontosan **4** hely van, így

$$0 \leq j \leq 4, \quad 0 \leq b \leq 4, \quad 0 \leq 8 - j - b \leq 4$$

(a harmadik feltétel mindenkire vonatkozik, akár jobbra, akár balra ül).
Az utolsó feltétel átrendezve: $4 \leq j + b \leq 8$.

**Lépés 3 — Egy fix $(j, b)$ eset.** Egymástól független választások szorzódnak:

$$N(j, b) = \binom{12}{j} \binom{13}{b} \binom{18}{8 - j - b}$$

- Jobboldaliak közül $j$-t: $\binom{12}{j}$ módon.
- Baloldaliak közül $b$-t: $\binom{13}{b}$ módon.
- „Mindegy" csoportból $8 - j - b$-t: $\binom{18}{8 - j - b}$ módon.

**Lépés 4 — Esetek összeadása.** A különböző $(j, b)$ esetek **kizárják egymást** (egy konkrét utaslistában a $j, b$ értékek egyértelműen meghatározottak), tehát:

$$\text{Összes} = \sum_{j=0}^{4} \sum_{b=0}^{4} [\,4 \leq j + b \leq 8\,] \cdot \binom{12}{j} \binom{13}{b} \binom{18}{8 - j - b}$$

**Számoljuk ki egy mintát** $(j, b) = (2, 2)$: $\binom{12}{2}\binom{13}{2}\binom{18}{4} = 66 \cdot 78 \cdot 3060 = 15\,750\,360$.

**Két alapelv emlékezetes:**

- 🔢 **Szorzás:** „bármelyik bármelyikkel" — független választások.
- ➕ **Összeadás:** „vagy-vagy esetek" — egymást kizáró alternatívák.

---

### Exercise 2.4.2 - Stars-and-bars: $x_1 + x_2 + \cdots + x_n = K$

**Probléma:** Hány megoldása van az

$$x_1 + x_2 + \cdots + x_n = K$$

egyenletnek, ha $x_i \in \mathbb{N}_0$ (nem-negatív egészek, $0$ megengedett, sorrend számít)?

**Megoldás:**

**Megjegyzés a vektoros értelmezésről.** Egy megoldás egy $(x_1, \dots, x_n)$ rendezett vektor; pl. $(5, 2) \neq (2, 5)$. Ez nem keverendő össze a szám-partíciókkal (`tétel 10`), ahol a sorrend nem számít.

**„Gyöngyök és dobozok" modell.**

Vegyünk $K$ darab azonos gyöngyöt és $n$ darab címkézett dobozt. Az $i$-edik dobozba tegyünk $x_i$ gyöngyöt. Az egyenlet automatikusan teljesül (mert összesen $K$ gyöngyünk van).

Tehát: **hányféleképpen oszthatunk szét $K$ azonos gyöngyöt $n$ különböző dobozba?**

**Stars-and-bars konstrukció.** Sorbarendezünk $K$ darab `★`-ot és $n - 1$ darab `|` választóvonalat. A vonalak közti csillagok adják meg az egyes dobozokba kerülő gyöngyök számát. Pl. $n = 4, K = 6$:

```
★★|★|  |★★★    →    (x₁, x₂, x₃, x₄) = (2, 1, 0, 3)
```

Az **összes** ilyen sor leírható $\binom{n + K - 1}{K}$-féleképpen — annyi módon, ahányféleképpen kiválasztjuk a csillagok helyét a $n + K - 1$ pozícióból.

**Képlet:**

$$\boxed{\;\#\{\text{megoldás}\} = \binom{n + K - 1}{K} = \binom{n + K - 1}{n - 1}\;}$$

A két alak a szimmetria miatt egyenlő.

**Példák:**

- $n = 3, K = 5$: $\binom{7}{5} = 21$. (3 dobozba 5 gyöngy.)
- $n = 10, K = 5$: $\binom{14}{5} = 2002$.

---

### Exercise 2.4.3 - Korlátos egyenletek (B / C / D változatok)

**Az alapegyenlet:** $x_1 + x_2 + \cdots + x_n = K$, $x_i \in \mathbb{N}_0$.

#### B-változat: alsó korlátok

**Probléma:** Hány megoldás van, ha minden változónak megadunk egy minimum értéket: $x_i \geq a_i$ ($a_i \in \mathbb{Z}$)?

**Megoldás — szubsztitúció.** Vezessük be $y_i := x_i - a_i \geq 0$. Ekkor:

$$\sum y_i = K - \sum a_i =: K'$$

Ez visszavezetődik az alapfeladatra! **Megoldások száma:** $\binom{n + K' - 1}{K'}$, ha $K' \geq 0$; egyébként $0$.

**Példa:** $x_1 + x_2 + x_3 = 10$, $x_1 \geq 2, x_2 \geq 1, x_3 \geq 0$. Szubsztitúció: $K' = 10 - 3 = 7$, megoldások: $\binom{9}{7} = 36$.

A negatív alsó korlát is működik (csak a „gyöngyös" modell esik szét) — pl. $x \geq -2$ → $y = x + 2 \geq 0$.

#### C-változat: felső korlátok

**Probléma:** $\sum x_i = K$, $0 \leq x_i \leq b_i$.

**Megoldás — inklúzió-kizárás (`tétel 5`).** Legyen $A_i$ = azok a megoldások, ahol $x_i \geq b_i + 1$ (a tiltott eset). A keresett szám az **összes** nemnegatív megoldás mínusz $|A_1 \cup A_2 \cup \cdots \cup A_n|$, amit a szita formulával számolunk. Egy $|A_{i_1} \cap \cdots \cap A_{i_t}|$ metszet egy B-változatra szól: $y_{i_j} = x_{i_j} - (b_{i_j} + 1) \geq 0$, ezért

$$|A_{i_1} \cap \cdots \cap A_{i_t}| = \binom{n + K - \sum_{j} (b_{i_j} + 1) - 1}{K - \sum_{j} (b_{i_j} + 1)}$$

(ha a kitevő nem-negatív; egyébként $0$).

Összegezve:

$$\#\{\text{megold.}\} = \sum_{S \subseteq [n]} (-1)^{|S|} \binom{n + K - \sum_{i\in S}(b_i + 1) - 1}{n - 1}$$

#### D-változat: dobókocka példa

**Probléma:** 10 szabályos kockával dobunk. Hányféleképp lehet az összeg pontosan $30$?

**Megoldás.** A kockák megkülönböztethetők (különben rendezett összegekről beszélnénk), és minden $x_i \in \{1, 2, 3, 4, 5, 6\}$. Tehát alsó korlát $a_i = 1$ minden $i$-re, felső korlát $b_i = 6$.

**Lépés 1.** Alsó korlátok eltüntetése: $y_i = x_i - 1 \in \{0, 1, \dots, 5\}$, $\sum y_i = 30 - 10 = 20$.

**Lépés 2.** Felső korlát C-szita: $y_i \leq 5$, azaz „tiltott": $y_i \geq 6$. Inklúzió-kizárás:

$$N = \sum_{t=0}^{\lfloor 20/6 \rfloor} (-1)^t \binom{10}{t} \binom{10 + (20 - 6t) - 1}{10 - 1} = \sum_{t=0}^{3} (-1)^t \binom{10}{t} \binom{29 - 6t}{9}$$

Számolva:

$$N = \binom{29}{9} - 10\binom{23}{9} + 45\binom{17}{9} - 120\binom{11}{9}$$

$$= 10\,015\,005 - 8\,170\,400 + 1\,931\,940 - 6\,600 = 2\,930\,455$$ (lehetőség).

---

### Exercise 2.4.4 - "MEGFELLEBBEZHETETLEN" anagrammák

**Probléma:** Hányféleképpen rendezhetjük át a `MEGFELLEBBEZHETETLEN` szó betűit?

**Megoldás — ismétléses permutáció.**

**Lépés 1.** Számoljuk meg az ismétléseket. A szóban összesen **20** betű van. Betűgyakoriságok:

| Betű | Gyakoriság |
|---|---|
| E | 6 |
| L | 3 |
| B | 2 |
| H | 2 |
| T | 2 |
| Z | 1 |
| M | 1 |
| G | 1 |
| F | 1 |
| N | 1 |

Ellenőrzés: $6 + 3 + 2 + 2 + 2 + 1 + 1 + 1 + 1 + 1 = 20$ ✓.

**Lépés 2.** Az ismétléses permutáció képlete (lásd `tétel 1`):

$$P_n^{k_1, \ldots, k_s} = \frac{n!}{k_1!\,k_2!\,\cdots\,k_s!}$$

Behelyettesítve:

$$\frac{20!}{6!\cdot 3!\cdot 2!\cdot 2!\cdot 2!\cdot 1!\cdot 1!\cdot 1!\cdot 1!\cdot 1!} = \frac{20!}{6! \cdot 3! \cdot 8}$$

Számoljuk:

- $20! = 2\,432\,902\,008\,176\,640\,000$
- $6! = 720$, $3! = 6$, nevező $= 720 \cdot 6 \cdot 8 = 34\,560$
- Eredmény: $\frac{2\,432\,902\,008\,176\,640\,000}{34\,560} \approx 7.04 \times 10^{13}$

**Pontosan:** $70\,397\,164\,357\,200$ anagramma.

**Vizsga-variáns:** "ABRAKADABRA" — $11$ betű, gyakoriságok $A:5, B:2, R:2, K:1, D:1$ → $\dfrac{11!}{5!\,2!\,2!} = \dfrac{39\,916\,800}{480} = 83\,160$.

---

## Formal Exercises 2.1

---

### Exercise 2.1.Feladat /1/ - Sum of Cubes

**Problem:** Prove: 1³ + 2³ + ... + n³ = [n(n+1)/2]².

**Solution:**

**Theorem:**
$$\sum_{i=1}^{n} i^3 = \left[\frac{n(n+1)}{2}\right]^2$$

---

**Proof by Induction:**

**Base case (n=1):**
- Left: 1³ = 1
- Right: [1(2)/2]² = 1
- 1 = 1 ✓

---

**Inductive hypothesis:** Assume true for n = k:
$$\sum_{i=1}^{k} i^3 = \left[\frac{k(k+1)}{2}\right]^2$$

---

**Inductive step (n = k+1):**

$$\sum_{i=1}^{k+1} i^3 = \sum_{i=1}^{k} i^3 + (k+1)^3$$
$$= \left[\frac{k(k+1)}{2}\right]^2 + (k+1)^3$$ (by hypothesis)
$$= \frac{k^2(k+1)^2}{4} + (k+1)^3$$
$$= \frac{k^2(k+1)^2 + 4(k+1)^3}{4}$$
$$= \frac{(k+1)^2[k^2 + 4(k+1)]}{4}$$
$$= \frac{(k+1)^2(k^2 + 4k + 4)}{4}$$
$$= \frac{(k+1)^2(k+2)^2}{4}$$
$$= \left[\frac{(k+1)(k+2)}{2}\right]^2$$ ✓

---

**By induction:** Formula holds for all n ≥ 1. ∎

---

**Verification for small n:**

| n | 1³+2³+...+n³ | [n(n+1)/2]² |
|---|--------------|-------------|
| 1 | 1 | 1 |
| 2 | 1+8=9 | 9 |
| 3 | 9+27=36 | 36 |
| 4 | 36+64=100 | 100 |

All match ✓

---

*Continued in next part due to length...*
