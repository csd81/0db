# Exercise - Prove De Morgan's Laws from Boolean Algebra Axioms

## Problem Statement

From Section 1.2, Proposition 1.8:

Prove De Morgan's laws using only the Boolean algebra axioms (BA1)-(BA14):

```
(d) ¬(a ∨ b) = ¬a ∧ ¬b
(e) ¬(a ∧ b) = ¬a ∨ ¬b
```

---

## Boolean Algebra Axioms (BA1)-(BA14)

For reference, here are the axioms we can use:

| Axiom | Name | Formula |
|-------|------|---------|
| (BA1) | Commutativity (∨) | a ∨ b = b ∨ a |
| (BA2) | Commutativity (∧) | a ∧ b = b ∧ a |
| (BA3) | Associativity (∨) | a ∨ (b ∨ c) = (a ∨ b) ∨ c |
| (BA4) | Associativity (∧) | a ∧ (b ∧ c) = (a ∧ b) ∧ c |
| (BA5) | Distributivity (∨) | a ∨ (b ∧ c) = (a ∨ b) ∧ (a ∨ c) |
| (BA6) | Distributivity (∧) | a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c) |
| (BA7) | Absorption (∨) | a ∨ (a ∧ b) = a |
| (BA8) | Absorption (∧) | a ∧ (a ∨ b) = a |
| (BA9) | Idempotent (∨) | a ∨ a = a |
| (BA10) | Idempotent (∧) | a ∧ a = a |
| (BA11) | Complement (∨) | a ∨ ¬a = ⊤ |
| (BA12) | Complement (∧) | a ∧ ¬a = ⊥ |
| (BA13) | Identity (∨) | a ∨ ⊥ = a, a ∨ ⊤ = ⊤ |
| (BA14) | Identity (∧) | a ∧ ⊤ = a, a ∧ ⊥ = ⊥ |

---

## Key Lemma: Uniqueness of Complement

### Proposition 1.8(c)

**Statement:** If a ∨ x = ⊤ and a ∧ x = ⊥, then x = ¬a.

**Proof:**

Assume a ∨ x = ⊤ and a ∧ x = ⊥.

We need to show x = ¬a.

```
x = x ∧ ⊤                    (BA14: identity)
  = x ∧ (a ∨ ¬a)             (BA11: complement)
  = (x ∧ a) ∨ (x ∧ ¬a)       (BA6: distributivity)
  = (a ∧ x) ∨ (x ∧ ¬a)       (BA2: commutativity)
  = ⊥ ∨ (x ∧ ¬a)             (assumption: a ∧ x = ⊥)
  = (x ∧ ¬a) ∨ ⊥             (BA1: commutativity)
  = x ∧ ¬a                   (BA13: identity)
```

So we have: **x = x ∧ ¬a** ... (1)

Now similarly for ¬a:

```
¬a = ¬a ∧ ⊤                  (BA14: identity)
   = ¬a ∧ (a ∨ x)            (assumption: a ∨ x = ⊤)
   = (¬a ∧ a) ∨ (¬a ∧ x)     (BA6: distributivity)
   = (a ∧ ¬a) ∨ (¬a ∧ x)     (BA2: commutativity)
   = ⊥ ∨ (¬a ∧ x)            (BA12: complement)
   = (¬a ∧ x) ∨ ⊥            (BA1: commutativity)
   = ¬a ∧ x                  (BA13: identity)
   = x ∧ ¬a                  (BA2: commutativity)
```

So we have: **¬a = x ∧ ¬a** ... (2)

From (1) and (2): **x = ¬a** ✓

---

## Proof of De Morgan's Law (d): ¬(a ∨ b) = ¬a ∧ ¬b

### Strategy

By the Uniqueness of Complement (Proposition 1.8(c)), to prove ¬(a ∨ b) = ¬a ∧ ¬b, we need to show:

1. (a ∨ b) ∨ (¬a ∧ ¬b) = ⊤
2. (a ∨ b) ∧ (¬a ∧ ¬b) = ⊥

---

### Part 1: (a ∨ b) ∨ (¬a ∧ ¬b) = ⊤

```
(a ∨ b) ∨ (¬a ∧ ¬b)
= ((a ∨ b) ∨ ¬a) ∧ ((a ∨ b) ∨ ¬b)     (BA5: distributivity)
= (a ∨ b ∨ ¬a) ∧ (a ∨ b ∨ ¬b)         (BA3: associativity)
= (a ∨ ¬a ∨ b) ∧ (a ∨ b ∨ ¬b)         (BA1: commutativity)
= ((a ∨ ¬a) ∨ b) ∧ (a ∨ (b ∨ ¬b))     (BA3: associativity)
= (⊤ ∨ b) ∧ (a ∨ ⊤)                   (BA11: complement)
= ⊤ ∧ ⊤                               (BA13: a ∨ ⊤ = ⊤)
= ⊤                                   (BA14: ⊤ ∧ ⊤ = ⊤)
```

✓ **Part 1 complete.**

---

### Part 2: (a ∨ b) ∧ (¬a ∧ ¬b) = ⊥

```
(a ∨ b) ∧ (¬a ∧ ¬b)
= ((a ∨ b) ∧ ¬a) ∧ ¬b                 (BA4: associativity)
= ((a ∧ ¬a) ∨ (b ∧ ¬a)) ∧ ¬b          (BA6: distributivity)
= (⊥ ∨ (b ∧ ¬a)) ∧ ¬b                 (BA12: complement)
= (b ∧ ¬a) ∧ ¬b                       (BA13: ⊥ ∨ x = x)
= b ∧ ¬a ∧ ¬b                         (BA4: associativity)
= b ∧ ¬b ∧ ¬a                         (BA1/BA2: commutativity)
= (b ∧ ¬b) ∧ ¬a                       (BA4: associativity)
= ⊥ ∧ ¬a                              (BA12: complement)
= ⊥                                   (BA14: ⊥ ∧ x = ⊥)
```

✓ **Part 2 complete.**

---

### Conclusion for (d)

Since (a ∨ b) ∨ (¬a ∧ ¬b) = ⊤ and (a ∨ b) ∧ (¬a ∧ ¬b) = ⊥, by the uniqueness of complement:

```
¬(a ∨ b) = ¬a ∧ ¬b  ✓
```

---

## Proof of De Morgan's Law (e): ¬(a ∧ b) = ¬a ∨ ¬b

### Strategy

Again, by the Uniqueness of Complement, to prove ¬(a ∧ b) = ¬a ∨ ¬b, we need to show:

1. (a ∧ b) ∨ (¬a ∨ ¬b) = ⊤
2. (a ∧ b) ∧ (¬a ∨ ¬b) = ⊥

---

### Part 1: (a ∧ b) ∨ (¬a ∨ ¬b) = ⊤

```
(a ∧ b) ∨ (¬a ∨ ¬b)
= ((a ∧ b) ∨ ¬a) ∨ ¬b                 (BA3: associativity)
= ((a ∨ ¬a) ∧ (b ∨ ¬a)) ∨ ¬b          (BA5: distributivity)
= (⊤ ∧ (b ∨ ¬a)) ∨ ¬b                 (BA11: complement)
= (b ∨ ¬a) ∨ ¬b                       (BA14: ⊤ ∧ x = x)
= b ∨ ¬a ∨ ¬b                         (BA3: associativity)
= b ∨ ¬b ∨ ¬a                         (BA1: commutativity)
= (b ∨ ¬b) ∨ ¬a                       (BA3: associativity)
= ⊤ ∨ ¬a                              (BA11: complement)
= ⊤                                   (BA13: ⊤ ∨ x = ⊤)
```

✓ **Part 1 complete.**

---

### Part 2: (a ∧ b) ∧ (¬a ∨ ¬b) = ⊥

```
(a ∧ b) ∧ (¬a ∨ ¬b)
= ((a ∧ b) ∧ ¬a) ∨ ((a ∧ b) ∧ ¬b)     (BA6: distributivity)
= (a ∧ b ∧ ¬a) ∨ (a ∧ b ∧ ¬b)         (BA4: associativity)
= (a ∧ ¬a ∧ b) ∨ (a ∧ b ∧ ¬b)         (BA1/BA2: commutativity)
= (⊥ ∧ b) ∨ (a ∧ ⊥)                   (BA12: complement)
= ⊥ ∨ ⊥                               (BA14: ⊥ ∧ x = ⊥)
= ⊥                                   (BA13: ⊥ ∨ ⊥ = ⊥)
```

✓ **Part 2 complete.**

---

### Conclusion for (e)

Since (a ∧ b) ∨ (¬a ∨ ¬b) = ⊤ and (a ∧ b) ∧ (¬a ∨ ¬b) = ⊥, by the uniqueness of complement:

```
¬(a ∧ b) = ¬a ∨ ¬b  ✓
```

---

## Alternative Proof Using Duality

### Duality Principle (Theorem 1.9)

If a formula is true in Boolean algebra, its **dual** is also true.

**Dual transformation:**
- ∨ ↔ ∧
- ⊤ ↔ ⊥
- Keep ¬ unchanged

### Applying Duality

Once we proved De Morgan's Law (d):
```
¬(a ∨ b) = ¬a ∧ ¬b
```

The dual is:
```
¬(a ∧ b) = ¬a ∨ ¬b
```

Which is exactly De Morgan's Law (e)! ✓

**Therefore, proving one De Morgan's law automatically proves the other by duality.**

---

## Verification with Truth Table (for intuition)

### De Morgan's Law (d): ¬(a ∨ b) = ¬a ∧ ¬b

| a | b | a∨b | ¬(a∨b) | ¬a | ¬b | ¬a∧¬b |
|---|---|-----|--------|----|----|-------|
| 0 | 0 |  0  |   1    | 1  | 1  |   1   |
| 0 | 1 |  1  |   0    | 1  | 0  |   0   |
| 1 | 0 |  1  |   0    | 0  | 1  |   0   |
| 1 | 1 |  1  |   0    | 0  | 0  |   0   |

✓ Columns match!

### De Morgan's Law (e): ¬(a ∧ b) = ¬a ∨ ¬b

| a | b | a∧b | ¬(a∧b) | ¬a | ¬b | ¬a∨¬b |
|---|---|-----|--------|----|----|-------|
| 0 | 0 |  0  |   1    | 1  | 1  |   1   |
| 0 | 1 |  0  |   1    | 1  | 0  |   1   |
| 1 | 0 |  0  |   1    | 0  | 1  |   1   |
| 1 | 1 |  1  |   0    | 0  | 0  |   0   |

✓ Columns match!

---

## Set-Theoretic Interpretation (Venn Diagram)

### De Morgan's Law (d): (A ∪ B)' = A' ∩ B'

```
    ┌─────────────────┐
    │    ┌───┐        │
    │ A  │ ∩ │   B    │
    │    └───┘        │
    │                 │
    │   Shaded:       │
    │   Everything    │
    │   except A∪B    │
    └─────────────────┘
```

The complement of the union equals the intersection of complements.

### De Morgan's Law (e): (A ∩ B)' = A' ∪ B'

The complement of the intersection equals the union of complements.

---

## Summary

| Law | Formula | Proof Method |
|-----|---------|--------------|
| **De Morgan (d)** | ¬(a ∨ b) = ¬a ∧ ¬b | Complement uniqueness |
| **De Morgan (e)** | ¬(a ∧ b) = ¬a ∨ ¬b | Complement uniqueness OR Duality |

### Key Proof Techniques Used

1. **Uniqueness of Complement (1.8(c))**: If x ∨ a = ⊤ and x ∧ a = ⊥, then x = ¬a
2. **Distributivity**: Essential for expanding expressions
3. **Complement axioms**: a ∨ ¬a = ⊤, a ∧ ¬a = ⊥
4. **Identity axioms**: a ∨ ⊥ = a, a ∧ ⊤ = a
5. **Duality Principle**: Proves (e) automatically from (d)

---

## Applications

1. **Logic**: ¬(P ∨ Q) ≡ ¬P ∧ ¬Q and ¬(P ∧ Q) ≡ ¬P ∨ ¬Q
2. **Set Theory**: (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ
3. **Digital Circuits**: NAND/NOR gate transformations
4. **Programming**: `!(a || b)` ≡ `!a && !b`

---

## References

- Section 1.2 - Boolean Algebra Axioms
- Proposition 1.8 - De Morgan's Laws
- Theorem 1.9 - Duality Principle
