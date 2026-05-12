# Exercise 1.7 - Verify Boolean Algebra Examples

## Problem Statement

Prove that each example in Section 1.7 is actually a Boolean algebra (isomorphic to a set algebra with standard set operations).

---

## 1.7(a) Set Algebra ✓

**Definition:**
- H = P(I) (power set of I)
- ∨ = ∪ (union)
- ∧ = ∩ (intersection)
- ¬ = complement (')
- ⊤ = I (universal set)
- ⊥ = ∅ (empty set)

**Verification:** This is the **canonical Boolean algebra** - all axioms (BA1)-(BA14) are satisfied by definition of set operations.

---

## 1.7(b) Sub-algebra of Power Set ✓

**Definition:**
- X ⊆ P(I) closed under set operations
- I ∈ X, ∅ ∈ X
- A, B ∈ X → A ∪ B, A ∩ B, A' ∈ X

**Verification:** Since X inherits operations from P(I) and is closed, all axioms hold automatically.

---

## 1.7(c) Two-Valued Logic ✓

**Definition:**
- H = {h, i} = {false, true} = {0, 1}
- ∨ = OR (vagy)
- ∧ = AND (és)
- ¬ = NOT (nem)
- ⊤ = i (true/1)
- ⊥ = h (false/0)

### Truth Table Verification

**Commutativity (BA1):**
| a | b | a∨b | b∨a | a∧b | b∧a |
|---|---|-----|-----|-----|-----|
| 0 | 0 |  0  |  0  |  0  |  0  |
| 0 | 1 |  1  |  1  |  0  |  0  |
| 1 | 0 |  1  |  1  |  0  |  0  |
| 1 | 1 |  1  |  1  |  1  |  1  |

**Associativity (BA2):** (a∨b)∨c = a∨(b∨c) ✓ (verify all 8 combinations)

**Distributivity (BA3):**
```
a ∨ (b ∧ c) = (a ∨ b) ∧ (a ∨ c)  ✓
a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c)  ✓
```

**Absorption (BA4):**
```
a ∨ (a ∧ b) = a  ✓
a ∧ (a ∨ b) = a  ✓
```

**Idempotent (BA5):**
```
a ∨ a = a  ✓
a ∧ a = a  ✓
```

**Complement (BA6):**
| a | ¬a | a∨¬a | a∧¬a |
|---|----|------|------|
| 0 |  1 |  1=⊤ |  0=⊥ |
| 1 |  0 |  1=⊤ |  0=⊥ |

**Identity (BA9-BA10):**
```
a ∨ ⊥ = a ∨ 0 = a  ✓
a ∧ ⊤ = a ∧ 1 = a  ✓
a ∨ ⊤ = a ∨ 1 = 1 = ⊤  ✓
a ∧ ⊥ = a ∧ 0 = 0 = ⊥  ✓
```

**Isomorphism to Set Algebra:**
```
h (0) ↔ ∅
i (1) ↔ {x} (singleton set)
```

---

## 1.7(d) Three-Valued Logic (Quasi-BA) ⚠️

**Definition:**
- H = {h, k, i} = {0, ½, 1}
- a ∨ b = max(a, b)
- a ∧ b = min(a, b)
- ¬a = 1 - a

**Verification:**

✅ Commutativity, Associativity: Follow from properties of min/max

✅ Distributivity:
```
max(a, min(b,c)) = min(max(a,b), max(a,c))  ✓
min(a, max(b,c)) = max(min(a,b), min(a,c))  ✓
```

✅ Idempotent:
```
max(a,a) = a  ✓
min(a,a) = a  ✓
```

❌ **Complement FAILED:**
```
a ∨ ¬a = max(a, 1-a) ≠ 1 (for a = ½)
max(½, 1-½) = max(½, ½) = ½ ≠ 1  ❌

a ∧ ¬a = min(a, 1-a) ≠ 0 (for a = ½)
min(½, 1-½) = min(½, ½) = ½ ≠ 0  ❌
```

**Conclusion:** This is a **Quasi-Boolean Algebra** only (not a true BA).

---

## 1.7(e) Number Theory (Divisors) ✓

**Definition:**
- N = square-free number (e.g., N = 30 = 2×3×5)
- H = {divisors of N}
- a ∨ b = gcd(a, b) (legnagyobb közös osztó)
- a ∧ b = lcm(a, b) (legkisebb közös többszörös)
- ¬a = N/a
- ⊤ = N
- ⊥ = 1

### Example: N = 30

H = {1, 2, 3, 5, 6, 10, 15, 30}

**Verification:**

✅ Commutativity:
```
gcd(a,b) = gcd(b,a)  ✓
lcm(a,b) = lcm(b,a)  ✓
```

✅ Associativity:
```
gcd(a, gcd(b,c)) = gcd(gcd(a,b), c)  ✓
lcm(a, lcm(b,c)) = lcm(lcm(a,b), c)  ✓
```

✅ Distributivity:
```
gcd(a, lcm(b,c)) = lcm(gcd(a,b), gcd(a,c))  ✓
lcm(a, gcd(b,c)) = gcd(lcm(a,b), lcm(a,c))  ✓
```

✅ Absorption:
```
gcd(a, lcm(a,b)) = a  ✓  (since a|lcm(a,b))
lcm(a, gcd(a,b)) = a  ✓  (since gcd(a,b)|a)
```

✅ Idempotent:
```
gcd(a,a) = a  ✓
lcm(a,a) = a  ✓
```

✅ Complement:
```
a ∨ ¬a = gcd(a, N/a) = 1 = ⊥  ✓  (since N is square-free)
a ∧ ¬a = lcm(a, N/a) = N = ⊤  ✓  (since gcd(a, N/a) = 1)
```

✅ Identity:
```
gcd(a, 1) = a  ✓  (⊥ = 1)
lcm(a, N) = N  ✓  (⊤ = N)
gcd(a, N) = a  ✓  (since a|N)
lcm(a, 1) = a  ✓
```

**Isomorphism to Set Algebra:**

For N = p₁×p₂×...×pₙ (square-free), each divisor corresponds to a subset of primes:
```
d ↔ {pᵢ : pᵢ divides d}

Example N=30=2×3×5:
  1  ↔ ∅
  2  ↔ {2}
  3  ↔ {3}
  5  ↔ {5}
  6  ↔ {2,3}
  10 ↔ {2,5}
  15 ↔ {3,5}
  30 ↔ {2,3,5}

gcd ↔ ∩
lcm ↔ ∪
N/a ↔ complement
```

---

## 1.7(f) Event Algebra (Probability) ✓

**Definition:**
- Ω = sample space (eseménytér)
- H = P(Ω) (all events)
- A ∨ B = A ∪ B (sum of events)
- A ∧ B = A ∩ B (product of events)
- ¬A = A' (complement event)
- ⊤ = Ω (certain event)
- ⊥ = ∅ (impossible event)

**Verification:** Identical to 1.7(a) - this IS a set algebra!

---

## 1.7(g) Switch/Valve Algebra ✓

**Definition:**
- H = {0, 1} (off/open, closed/on)
- Series connection: a ∧ b = a × b (AND)
- Parallel connection: a ∨ b = a + b - ab (OR, or just max)
- ¬a = 1 - a (reverse switch)

**Verification:** Identical to 1.7(c) - isomorphic to two-valued logic!

**Physical interpretation:**
```
Series:    Current flows iff BOTH switches closed (AND)
Parallel:  Current flows iff AT LEAST ONE switch closed (OR)
Reverse:   Normally closed ↔ Normally open (NOT)
```

---

## 1.7(h) Color Mixing (Quasi-BA) ⚠️

**Definition:**
- H = {possible colors}
- ∨ = additive mixing (light)
- ∧ = subtractive mixing (pigment)
- ¬a = complementary color
- ⊤ = white
- ⊥ = black

**Note:** This is an **analogous** structure but not a strict Boolean algebra due to:
- Continuous color space (infinite elements)
- Complementary colors don't satisfy exact BA axioms
- Mixing is not perfectly associative/distributive

---

## Summary Table

| Example | Boolean Algebra? | Isomorphic to |
|---------|-----------------|---------------|
| (a) Set algebra | ✅ Yes | P(I) |
| (b) Sub-algebra | ✅ Yes | Subset of P(I) |
| (c) Two-valued logic | ✅ Yes | P({x}) ≅ {∅, {x}} |
| (d) Three-valued logic | ⚠️ Quasi-BA | - |
| (e) Number theory | ✅ Yes | P({primes of N}) |
| (f) Event algebra | ✅ Yes | P(Ω) |
| (g) Switch algebra | ✅ Yes | P({x}) ≅ {0,1} |
| (h) Color mixing | ⚠️ Analogous | - |

---

## Key Insight (Stone's Theorem)

By **Stone's Representation Theorem (1.11)**, every Boolean algebra is isomorphic to a set algebra. This exercise demonstrates that seemingly different structures (logic, numbers, switches, events) are all fundamentally the same mathematical object!
