# Exercise 1.2 - Real Numbers are NOT a Boolean Algebra

## Problem Statement

Verify that real numbers (ℝ) with standard addition (+) and multiplication (×) do **NOT** satisfy the Boolean algebra axioms (BA1)-(BA14).

---

## Analysis

We need to check the Boolean algebra axioms with the following mapping:
- **H** = ℝ (real numbers)
- **∨** → + (addition)
- **∧** → × (multiplication)
- Need to identify: **¬** (complement), **⊤** (top/one), **⊥** (bottom/zero)

---

## Checking the Axioms

### ✅ (BA1) Commutativity - SATISFIED
```
a + b = b + a  ✓
a × b = b × a  ✓
```

### ✅ (BA2) Associativity - SATISFIED
```
a + (b + c) = (a + b) + c  ✓
a × (b × c) = (a × b) × c  ✓
```

### ✅ (BA3) Distributivity - SATISFIED
```
a × (b + c) = (a × b) + (a × c)  ✓  (multiplication distributes over addition)
```
*Note: In Boolean algebra, both distributive laws hold. In ℝ, only one direction works.*

### ❌ (BA4) Absorption - **FAILED**

Boolean algebra requires:
```
a ∨ (a ∧ b) = a    →    a + (a × b) = a  ❌
a ∧ (a ∨ b) = a    →    a × (a + b) = a  ❌
```

**Counter-example:** Let a = 2, b = 3
```
2 + (2 × 3) = 2 + 6 = 8 ≠ 2  ❌
2 × (2 + 3) = 2 × 5 = 10 ≠ 2  ❌
```

### ❌ (BA5) Idempotent - **FAILED**

Boolean algebra requires:
```
a ∨ a = a    →    a + a = a  ❌
a ∧ a = a    →    a × a = a  ❌
```

**Counter-example:** Let a = 2
```
2 + 2 = 4 ≠ 2  ❌
2 × 2 = 4 ≠ 2  ❌
```

Only works for a = 0 (for addition) or a ∈ {0, 1} (for multiplication).

### ❌ (BA6) Complement - **FAILED**

Boolean algebra requires for every element a:
```
a ∨ ¬a = ⊤    →    a + (¬a) = ⊤
a ∧ ¬a = ⊥    →    a × (¬a) = ⊥
```

**Problem:** There is no complement operation ¬a in ℝ that satisfies both:
- For addition: we need a + (¬a) = some constant ⊤
- For multiplication: we need a × (¬a) = some constant ⊥

If we try ⊥ = 0 (additive identity for +):
```
a × (¬a) = 0  →  ¬a = 0/a = 0 (for a ≠ 0)
But then: a + 0 = a ≠ ⊤  ❌
```

If we try ⊥ = 1 (multiplicative identity for ×):
```
a + (¬a) = 1  →  ¬a = 1 - a
But then: a × (1-a) = a - a² ≠ constant  ❌
```

### ❌ (BA9)-(BA10) Identity Elements - **FAILED**

Boolean algebra requires elements ⊤ and ⊥ such that:
```
a ∨ ⊥ = a    →    a + ⊥ = a  →  ⊥ = 0  ✓
a ∧ ⊤ = a    →    a × ⊤ = a  →  ⊤ = 1  ✓

But also:
a ∨ ⊤ = ⊤    →    a + 1 = 1  ❌  (false for any a ≠ 0)
a ∧ ⊥ = ⊥    →    a × 0 = 0  ✓
```

---

## Summary Table

| Axiom | Property | ℝ with (+,×) |
|-------|----------|--------------|
| BA1 | Commutativity | ✅ |
| BA2 | Associativity | ✅ |
| BA3 | Distributivity | ⚠️ Partial |
| BA4 | Absorption | ❌ |
| BA5 | Idempotent | ❌ |
| BA6 | Complement | ❌ |
| BA9-BA10 | Identity | ❌ |

---

## Conclusion

**ℝ with standard (+, ×) is NOT a Boolean algebra** because it fails multiple axioms:
1. **Absorption law** fails
2. **Idempotent law** fails  
3. **Complement** does not exist
4. **Identity element properties** fail

The structure (ℝ, +, ×) is actually a **field**, which is a completely different algebraic structure with different axioms.

---

## What IS a Boolean Algebra on Numbers?

For comparison, see Section 1.7(e) in the chapter: 
- Take N = square-free number
- H = {divisors of N}
- a ∨ b = gcd(a, b) (greatest common divisor)
- a ∧ b = lcm(a, b) (least common multiple)
- ¬a = N/a
- ⊤ = N, ⊥ = 1

This **does** form a Boolean algebra! ✓
