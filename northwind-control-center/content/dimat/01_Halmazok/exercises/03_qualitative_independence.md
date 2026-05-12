# Exercise 1.3 - Qualitative Independence in Boolean Algebras

## Problem Statement

From Section 1.3, Corollary 1.20:
> "Bár a minőségi függetlenséget csak halmazelgebrák esetén definiáltuk, tetszőleges Boole- algebrában ugyanúgy használhatjuk e fogalmat. (Újabb Házi Feladat, Kedves Olvasó!)"

**Task:** Show that the concept of qualitative independence can be used in any Boolean algebra (not just set algebras).

---

## Background

### Original Definition (1.13) - For Set Algebras

A₁, ..., Aₙ ⊆ I are **qualitatively independent** if for all ε₁, ..., εₙ ∈ {+1, -1}:

```
A₁^ε₁ ∩ ... ∩ Aₙ^εₙ ≠ ∅
```

where A⁺¹ = A and A⁻¹ = A' (complement).

### Generalized Definition - For Any Boolean Algebra

Let B = (B, ∨, ∧, ¬, ⊤, ⊥) be a Boolean algebra.

Elements a₁, ..., aₙ ∈ B are **qualitatively independent** if for all ε₁, ..., εₙ ∈ {+1, -1}:

```
a₁^ε₁ ∧ ... ∧ aₙ^εₙ ≠ ⊥
```

where:
- a⁺¹ = a
- a⁻¹ = ¬a (complement)
- ⊥ is the zero/bottom element of B

---

## Why This Generalization Works

### 1. Structural Correspondence

| Set Algebra | General Boolean Algebra |
|-------------|------------------------|
| ∩ (intersection) | ∧ (meet/AND) |
| ∅ (empty set) | ⊥ (bottom/zero) |
| A' (complement) | ¬a (complement) |
| A₁ ∩ ... ∩ Aₙ ≠ ∅ | a₁ ∧ ... ∧ aₙ ≠ ⊥ |

### 2. Stone's Representation Theorem

By **Stone's Theorem (1.11)**, every Boolean algebra B is isomorphic to a set algebra:

```
f: B → P(S)  (for some set S)

f(a ∧ b) = f(a) ∩ f(b)
f(¬a) = f(a)'
f(⊥) = ∅
```

Therefore, qualitative independence in B corresponds exactly to qualitative independence in the set algebra P(S).

---

## Example: Two-Valued Logic

**B = ({0, 1}, ∨, ∧, ¬, 1, 0)**

Can we find qualitatively independent elements?

### For n = 1:
Need: a ≠ 0 and ¬a ≠ 0

In {0, 1}:
- If a = 1: ¬a = 0 ❌
- If a = 0: a = 0 ❌

**Result:** No qualitatively independent element exists in 2-element BA.

This matches Proposition 1.14(i): |B| ≥ 2ⁿ requires |B| ≥ 2¹ = 2, but we need **strictly more** room for independence.

### For n = 2 in a 4-element BA:

**B = P({x, y}) = {∅, {x}, {y}, {x,y}}**

Let a₁ = {x}, a₂ = {y}

Check all 2² = 4 combinations:
```
ε = (+1, +1): a₁ ∧ a₂ = {x} ∩ {y} = ∅ = ⊥  ❌
```

These are **NOT** independent!

### Correct Construction for n = 2:

We need |B| ≥ 2² = 4 elements, but actually need **2^(2^n)** = 16 elements for 2 independent generators.

**B = P({1,2,3,4})** with 16 elements

Let a₁ = {1, 2}, a₂ = {1, 3}

Check all combinations:
```
(+1, +1): a₁ ∧ a₂ = {1,2} ∩ {1,3} = {1} ≠ ∅  ✓
(+1, -1): a₁ ∧ ¬a₂ = {1,2} ∩ {2,4} = {2} ≠ ∅  ✓
(-1, +1): ¬a₁ ∧ a₂ = {3,4} ∩ {1,3} = {3} ≠ ∅  ✓
(-1, -1): ¬a₁ ∧ ¬a₂ = {3,4} ∩ {2,4} = {4} ≠ ∅  ✓
```

**Success!** a₁ and a₂ are qualitatively independent.

---

## Example: Number Theory (Divisors of N)

**B = {divisors of N = 30}** with gcd, lcm operations

H = {1, 2, 3, 5, 6, 10, 15, 30}
- ⊥ = 1 (bottom)
- ⊤ = 30 (top)
- ¬a = 30/a

### Find n = 3 independent elements:

By Proposition 1.14, we need |H| ≥ 2³ = 8. We have exactly 8 elements! ✓

Let:
- a₁ = 2 (corresponds to prime {2})
- a₂ = 3 (corresponds to prime {3})
- a₃ = 5 (corresponds to prime {5})

Check some combinations (using gcd for ∧):
```
(+1, +1, +1): gcd(2, 3, 5) = 1 = ⊥  ❌
```

These are **NOT** independent!

### Correct Construction:

Use the isomorphism to P({2, 3, 5}):
- a₁ = 6 = 2×3 ↔ {2, 3}
- a₂ = 10 = 2×5 ↔ {2, 5}
- a₃ = 15 = 3×5 ↔ {3, 5}

Check:
```
(+1, +1, +1): gcd(6, 10, 15) = 1  ❌ Still doesn't work!
```

The issue: We need to construct elements corresponding to the **binary representation** construction from Proposition 1.14(ii).

### Using Binary Construction:

For n = 3, label elements 0, 1, ..., 7 by their binary representation:

| Element | Binary | Bits |
|---------|--------|------|
| 1 | 000 | (0,0,0) |
| 2 | 001 | (0,0,1) |
| 3 | 010 | (0,1,0) |
| 5 | 011 | (0,1,1) |
| 6 | 100 | (1,0,0) |
| 10 | 101 | (1,0,1) |
| 15 | 110 | (1,1,0) |
| 30 | 111 | (1,1,1) |

Define:
- a₁ = lcm of elements with bit 1 = 1: lcm(6, 10, 15, 30) = 30
- a₂ = lcm of elements with bit 2 = 1: lcm(3, 5, 15, 30) = 30
- a₃ = lcm of elements with bit 3 = 1: lcm(2, 5, 10, 30) = 30

This construction doesn't work directly because our algebra is too small.

**Key Point:** The number-theoretic BA on divisors of N = p₁p₂...pₙ is isomorphic to P({p₁, ..., pₙ}), which has 2ⁿ elements. For n independent elements, we need 2^(2ⁿ) elements!

---

## Proposition 1.14 - Generalized Proof

### (i) Lower Bound: |B| ≥ 2ⁿ

**Proof:** 
For qualitatively independent a₁, ..., aₙ, all 2ⁿ combinations:
```
a₁^ε₁ ∧ ... ∧ aₙ^εₙ ≠ ⊥
```
are distinct and non-zero. 

These elements are **pairwise disjoint** (their pairwise meet is ⊥):
```
(a₁^ε₁ ∧ ... ∧ aₙ^εₙ) ∧ (a₁^δ₁ ∧ ... ∧ aₙ^δₙ) = ⊥
```
when ε ≠ δ (since for some i, εᵢ ≠ δᵢ, giving aᵢ ∧ ¬aᵢ = ⊥).

In a finite Boolean algebra, disjoint non-zero elements must be distinct, so we need at least 2ⁿ distinct elements. □

### (ii) Existence: Construction for Any n

**Proof:**
Take B = P({0, 1}ⁿ) (power set of all n-bit strings).

Define aᵢ = {x ∈ {0,1}ⁿ : xᵢ = 1} (strings with i-th bit = 1).

Then for any ε ∈ {+1, -1}ⁿ:
```
a₁^ε₁ ∧ ... ∧ aₙ^εₙ = {ε₁...εₙ} (singleton set)
```
which is non-empty. ✓

By Stone's theorem, this construction works in **any** Boolean algebra with at least 2^(2ⁿ) elements. □

---

## Application: Corollary 1.20

**Statement:** If B is generated by m elements, then |B| ≤ 2^(2^m).

**Equality holds** if and only if the generators are qualitatively independent.

### Proof Sketch:

1. **Upper bound:** Every element has a DNF with at most 2^m minterms, each minterm is a combination of m generators. Total: 2^(2^m) possible DNFs.

2. **Equality condition:** If generators are independent, all 2^(2^m) DNFs are distinct.

3. **Generalized to any BA:** By Stone's theorem, B ≅ some set algebra, where the proof works identically.

---

## Summary

| Concept | Set Algebra | General Boolean Algebra |
|---------|-------------|------------------------|
| Independence | A₁^ε₁ ∩ ... ∩ Aₙ^εₙ ≠ ∅ | a₁^ε₁ ∧ ... ∧ aₙ^εₙ ≠ ⊥ |
| Empty set | ∅ | ⊥ |
| Intersection | ∩ | ∧ |
| Complement | A' | ¬a |
| Minimum size | 2ⁿ | 2ⁿ |
| Construction | Binary representation | Same (via Stone) |

**Key Insight:** Stone's Representation Theorem allows us to transfer all set-theoretic concepts to arbitrary Boolean algebras!

---

## References

- Section 1.3 - Qualitative independence definition
- Theorem 1.11 - Stone's Representation Theorem
- Proposition 1.14 - Bounds on independent sets
- Corollary 1.20 - Size of finitely generated Boolean algebras
