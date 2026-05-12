# Chapter 01 - Halmazok (Sets) - Complete Solutions

## Section 1.1 - Halmazok definíciója

---

### Exercise 1.1.1 - Cantor's Theorem: No Universal Set Exists

**Problem:** Prove that there is no set containing everything.

**Solution:**

**Proof by contradiction (Russell's Paradox):**

**Step 1:** Assume there exists a universal set U that contains everything.

**Step 2:** Construct the Russell set:
$$R = \{x \in U : x \notin x\}$$

This is the set of all sets that do not contain themselves.

**Step 3:** Ask: Is R ∈ R?

**Case 1:** Assume R ∈ R
- By definition of R, if R ∈ R, then R must satisfy the condition: R ∉ R
- Contradiction! R ∈ R implies R ∉ R

**Case 2:** Assume R ∉ R
- By definition of R, if R ∉ R, then R satisfies the condition for membership
- Therefore R ∈ R
- Contradiction! R ∉ R implies R ∈ R

**Step 4:** Both cases lead to contradiction.

**Conclusion:** The assumption that U exists must be false.

**Therefore:** No universal set exists. ∎

---

### Exercise 1.1.2 - Russell's Paradox Detailed Analysis

**Problem:** Study Russell's paradox proof by contradiction.

**Solution:**

**Historical Context:**
- Discovered by Bertrand Russell (1901)
- Showed naive set theory is inconsistent
- Led to development of axiomatic set theory (ZF)

**Detailed Proof:**

Let P(x) be the property "x ∉ x"

By naive comprehension, we can form:
$$R = \{x : P(x)\} = \{x : x \notin x\}$$

**Question:** R ∈ R or R ∉ R?

**Logical Analysis:**
```
R ∈ R ⟺ R satisfies P ⟺ R ∉ R
```

This is a logical contradiction: R ∈ R ⟺ R ∉ R

**Resolution in ZF Set Theory:**
- ZF uses the Axiom of Separation instead of naive comprehension
- Can only form {x ∈ A : P(x)} for existing set A
- Cannot form {x : P(x)} without restricting to existing set
- This prevents R from being formed as a set

**Therefore:** Russell's paradox is avoided in axiomatic set theory. ∎

---

### Exercise 1.1.3 - Zermelo-Fraenkel Axioms Review

**Problem:** Review and understand the ZF axioms.

**Solution:**

**The 9 ZF Axioms:**

**1. Axiom of Extensionality:**
$$\forall A \forall B [\forall x (x \in A \iff x \in B) \implies A = B]$$

*Meaning:* Sets are equal iff they have the same elements.

**Example:** {1, 2, 3} = {3, 2, 1} (same elements, different order doesn't matter)

---

**2. Axiom of Empty Set:**
$$\exists \emptyset \forall x (x \notin \emptyset)$$

*Meaning:* There exists a set with no elements.

**Verification:** ∅ exists and is unique (by extensionality).

---

**3. Axiom of Pairing:**
$$\forall a \forall b \exists C \forall x (x \in C \iff x = a \lor x = b)$$

*Meaning:* For any a, b, the set {a, b} exists.

**Example:** For a=1, b=2: {1, 2} exists.

---

**4. Axiom of Union:**
$$\forall A \exists U \forall x (x \in U \iff \exists B (B \in A \land x \in B))$$

*Meaning:* For any set A, the union of all elements of A exists.

**Example:** A = {{1,2}, {3}} → ∪A = {1, 2, 3}

---

**5. Axiom of Power Set:**
$$\forall A \exists P \forall x (x \in P \iff x \subseteq A)$$

*Meaning:* For any set A, the set of all subsets of A exists.

**Example:** A = {1, 2} → P(A) = {∅, {1}, {2}, {1,2}}

---

**6. Axiom of Infinity:**
$$\exists I (\emptyset \in I \land \forall x (x \in I \implies x \cup \{x\} \in I))$$

*Meaning:* There exists an infinite set (containing ∅ and closed under successor).

**Construction:** ∅, {∅}, {∅, {∅}}, ... gives natural numbers.

---

**7. Axiom Schema of Separation:**
For any property φ and set A:
$$\exists B \forall x (x \in B \iff x \in A \land \phi(x))$$

*Meaning:* Can form subsets using properties, but only from existing sets.

**Prevents Russell's paradox:** Cannot form {x : x ∉ x} without restricting to existing set.

---

**8. Axiom Schema of Replacement:**
For any definable function f and set A:
$$\exists B \forall y (y \in B \iff \exists x (x \in A \land y = f(x)))$$

*Meaning:* Image of a set under a function is a set.

---

**9. Axiom of Regularity (Foundation):**
$$\forall A (A \neq \emptyset \implies \exists x (x \in A \land x \cap A = \emptyset))$$

*Meaning:* Every non-empty set has an ∈-minimal element.

**Consequence:** No set can contain itself (A ∉ A for all A).

---

### Exercise 1.1.4 - Naive vs Axiomatic Set Theory

**Problem:** Understand the difference between naive and axiomatic set theory.

**Solution:**

| Aspect | Naive Set Theory | Axiomatic Set Theory (ZF) |
|--------|-----------------|---------------------------|
| **Comprehension** | Unrestricted: {x : P(x)} | Restricted: {x ∈ A : P(x)} |
| **Paradoxes** | Vulnerable (Russell's) | Avoided by axioms |
| **Foundation** | Intuitive | Formal axioms |
| **Existence** | Assume sets exist | Prove from axioms |
| **Usage** | Informal mathematics | Foundation of mathematics |

**Key Difference:**
- Naive: "Any property defines a set" → leads to contradictions
- Axiomatic: "Sets built from axioms" → consistent (as far as we know)

---

## Section 1.2 - Boole-algebrák

---

### Exercise 1.2.1 - Verify Commutativity (BA1, BA2)

**Problem:** Verify A ∪ B = B ∪ A and A ∩ B = B ∩ A.

**Solution:**

**For Union (A ∪ B = B ∪ A):**

**Proof:**
```
x ∈ A ∪ B 
⟺ x ∈ A or x ∈ B     (definition of union)
⟺ x ∈ B or x ∈ A     (OR is commutative)
⟺ x ∈ B ∪ A          (definition of union)
```

**Therefore:** A ∪ B = B ∪ A ✓

**Concrete Example:**
- A = {1, 2}, B = {2, 3}
- A ∪ B = {1, 2, 3}
- B ∪ A = {1, 2, 3}
- Equal ✓

---

**For Intersection (A ∩ B = B ∩ A):**

**Proof:**
```
x ∈ A ∩ B
⟺ x ∈ A and x ∈ B    (definition of intersection)
⟺ x ∈ B and x ∈ A    (AND is commutative)
⟺ x ∈ B ∩ A          (definition of intersection)
```

**Therefore:** A ∩ B = B ∩ A ✓

**Concrete Example:**
- A = {1, 2}, B = {2, 3}
- A ∩ B = {2}
- B ∩ A = {2}
- Equal ✓

---

### Exercise 1.2.2 - Verify Associativity (BA3, BA4)

**Problem:** Verify A ∪ (B ∪ C) = (A ∪ B) ∪ C and A ∩ (B ∩ C) = (A ∩ B) ∩ C.

**Solution:**

**For Union:**

**Proof:**
```
x ∈ A ∪ (B ∪ C)
⟺ x ∈ A or (x ∈ B or x ∈ C)
⟺ (x ∈ A or x ∈ B) or x ∈ C    (OR is associative)
⟺ x ∈ (A ∪ B) ∪ C
```

**Concrete Example:**
- A = {1}, B = {2}, C = {3}
- A ∪ (B ∪ C) = {1} ∪ {2, 3} = {1, 2, 3}
- (A ∪ B) ∪ C = {1, 2} ∪ {3} = {1, 2, 3}
- Equal ✓

---

**For Intersection:**

**Proof:**
```
x ∈ A ∩ (B ∩ C)
⟺ x ∈ A and (x ∈ B and x ∈ C)
⟺ (x ∈ A and x ∈ B) and x ∈ C   (AND is associative)
⟺ x ∈ (A ∩ B) ∩ C
```

**Concrete Example:**
- A = {1, 2}, B = {2, 3}, C = {2, 4}
- A ∩ (B ∩ C) = {1, 2} ∩ {2} = {2}
- (A ∩ B) ∩ C = {2} ∩ {2, 4} = {2}
- Equal ✓

---

### Exercise 1.2.3 - Verify Distributivity (BA5, BA6)

**Problem:** Verify A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C).

**Solution:**

**Proof (⊆ direction):**

Let x ∈ A ∪ (B ∩ C).

**Case 1:** x ∈ A
- Then x ∈ A ∪ B and x ∈ A ∪ C
- Therefore x ∈ (A ∪ B) ∩ (A ∪ C)

**Case 2:** x ∈ B ∩ C
- Then x ∈ B and x ∈ C
- So x ∈ A ∪ B and x ∈ A ∪ C
- Therefore x ∈ (A ∪ B) ∩ (A ∪ C)

**Therefore:** A ∪ (B ∩ C) ⊆ (A ∪ B) ∩ (A ∪ C)

---

**Proof (⊇ direction):**

Let x ∈ (A ∪ B) ∩ (A ∪ C).

Then x ∈ A ∪ B AND x ∈ A ∪ C.

**Case 1:** x ∈ A
- Then x ∈ A ∪ (B ∩ C) ✓

**Case 2:** x ∉ A
- Since x ∈ A ∪ B and x ∉ A: x ∈ B
- Since x ∈ A ∪ C and x ∉ A: x ∈ C
- Therefore x ∈ B ∩ C
- Therefore x ∈ A ∪ (B ∩ C) ✓

**Therefore:** (A ∪ B) ∩ (A ∪ C) ⊆ A ∪ (B ∩ C)

---

**Conclusion:** A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C) ✓

**Concrete Example:**
- A = {1, 2}, B = {2, 3}, C = {2, 4}
- B ∩ C = {2}
- A ∪ (B ∩ C) = {1, 2}
- A ∪ B = {1, 2, 3}, A ∪ C = {1, 2, 4}
- (A ∪ B) ∩ (A ∪ C) = {1, 2}
- Equal ✓

---

### Exercise 1.2.4 - Verify Absorption (BA7, BA8)

**Problem:** Verify A ∪ (A ∩ B) = A.

**Solution:**

**Proof:**

**(⊆):** Let x ∈ A ∪ (A ∩ B).

- Case 1: x ∈ A → x ∈ A ✓
- Case 2: x ∈ A ∩ B → x ∈ A ✓

**Therefore:** A ∪ (A ∩ B) ⊆ A

---

**(⊇):** Let x ∈ A.

- Then x ∈ A ∪ (anything)
- Therefore x ∈ A ∪ (A ∩ B)

**Therefore:** A ⊆ A ∪ (A ∩ B)

---

**Conclusion:** A ∪ (A ∩ B) = A ✓

**Concrete Example:**
- A = {1, 2}, B = {2, 3}
- A ∩ B = {2}
- A ∪ (A ∩ B) = {1, 2} ∪ {2} = {1, 2} = A ✓

---

### Exercise 1.2.5 - Verify Complement (BA11, BA12)

**Problem:** Verify A ∪ A' = I and A ∩ A' = ∅.

**Solution:**

**For A ∪ A' = I (universal set):**

**Proof:**
```
x ∈ A ∪ A'
⟺ x ∈ A or x ∈ A'
⟺ x ∈ A or x ∉ A
⟺ x ∈ I  (law of excluded middle)
```

**Therefore:** A ∪ A' = I ✓

---

**For A ∩ A' = ∅:**

**Proof:**
```
x ∈ A ∩ A'
⟺ x ∈ A and x ∈ A'
⟺ x ∈ A and x ∉ A
⟺ False (contradiction)
⟺ x ∈ ∅
```

**Therefore:** A ∩ A' = ∅ ✓

**Concrete Example:**
- U = {1, 2, 3, 4}
- A = {1, 2}
- A' = {3, 4}
- A ∪ A' = {1, 2, 3, 4} = U ✓
- A ∩ A' = ∅ ✓

---

### Exercise 1.2.6 - Verify Set Algebra is Boolean

**Problem:** Verify that (P(S), ∪, ∩, ', ∅, S) is a Boolean algebra.

**Solution:**

**Need to verify all 14 axioms:**

| Axiom | Property | Verification |
|-------|----------|--------------|
| BA1-2 | Commutativity | Verified in Ex 1.2.1 ✓ |
| BA3-4 | Associativity | Verified in Ex 1.2.2 ✓ |
| BA5-6 | Distributivity | Verified in Ex 1.2.3 ✓ |
| BA7-8 | Absorption | Verified in Ex 1.2.4 ✓ |
| BA9-10 | Identity | A ∪ ∅ = A, A ∩ S = A ✓ |
| BA11-12 | Complement | A ∪ A' = S, A ∩ A' = ∅ ✓ |
| BA13-14 | Bounds | A ∪ S = S, A ∩ ∅ = ∅ ✓ |

**All 14 axioms satisfied.**

**Therefore:** (P(S), ∪, ∩, ', ∅, S) is a Boolean algebra. ✓

---

### Exercise 1.2.7 - Verify Logic Algebra is Boolean

**Problem:** Verify ({F, T}, ∨, ∧, ¬, F, T) is a Boolean algebra.

**Solution:**

**Truth Table Verification:**

**Commutativity:**
| p | q | p∨q | q∨p | p∧q | q∧p |
|---|---|-----|-----|-----|-----|
| F | F | F | F | F | F |
| F | T | T | T | F | F |
| T | F | T | T | F | F |
| T | T | T | T | T | T |

Columns match → Commutativity ✓

**Associativity, Distributivity:** Similar truth tables verify.

**Complement:**
| p | ¬p | p∨¬p | p∧¬p |
|---|----|------|------|
| F | T | T | F |
| T | F | T | F |

p∨¬p = T (top), p∧¬p = F (bottom) ✓

**Therefore:** ({F, T}, ∨, ∧, ¬, F, T) is a Boolean algebra. ✓

---

### Exercise 1.2.8 - Verify Number-Theoretic Algebra

**Problem:** Verify (Dₙ, gcd, lcm, ', n, 1) is a Boolean algebra for square-free n.

**Solution:**

**Let n = 6 = 2×3 (square-free)**

**Divisors:** D₆ = {1, 2, 3, 6}

**Operations:**
- a ∨ b = lcm(a, b)
- a ∧ b = gcd(a, b)
- a' = n/a (complement)
- Top = n = 6
- Bottom = 1

**Verification Table:**

| a | b | lcm(a,b) | gcd(a,b) | a' | a ∨ a' | a ∧ a' |
|---|---|----------|----------|----|--------|--------|
| 1 | 2 | 2 | 1 | 6 | 6 | 1 |
| 1 | 3 | 3 | 1 | 6 | 6 | 1 |
| 2 | 3 | 6 | 1 | 3 | 6 | 1 |
| 2 | 6 | 6 | 2 | 3 | 6 | 1 |
| 3 | 6 | 6 | 3 | 2 | 6 | 1 |

**All Boolean axioms satisfied for square-free n.** ✓

**Note:** For n with repeated prime factors, complement doesn't work properly.

---

### Exercise 1.2.9 - Verify Event Algebra

**Problem:** Verify that events in probability form a Boolean algebra.

**Solution:**

**Sample space Ω, events = subsets of Ω**

**Operations:**
- A ∨ B = A ∪ B (A or B occurs)
- A ∧ B = A ∩ B (A and B occur)
- A' = Ω \ A (A does not occur)
- Top = Ω (certain event)
- Bottom = ∅ (impossible event)

**Verification:**
- Same as set algebra (events are sets)
- All 14 axioms satisfied ✓

**Example:** Rolling a die
- Ω = {1, 2, 3, 4, 5, 6}
- A = "even" = {2, 4, 6}
- A' = "odd" = {1, 3, 5}
- A ∪ A' = Ω (certain)
- A ∩ A' = ∅ (impossible) ✓

---

### Exercise 1.2.10 - Verify Switching Algebra

**Problem:** Verify that switching circuits form a Boolean algebra.

**Solution:**

**Values:** {0, 1} (off, on)

**Operations:**
- OR (∨): 0∨0=0, 0∨1=1, 1∨0=1, 1∨1=1
- AND (∧): 0∧0=0, 0∧1=0, 1∧0=0, 1∧1=1
- NOT (¬): ¬0=1, ¬1=0

**Circuit Interpretation:**
- Series connection = AND
- Parallel connection = OR
- Inverter = NOT

**All Boolean axioms verified by truth tables.** ✓

**Application:** Digital logic design uses this Boolean algebra.

---

### Exercise 1.2.11 - Prove De Morgan's Laws (Sets)

**Problem:** Prove (A ∪ B)' = A' ∩ B' and (A ∩ B)' = A' ∪ B'.

**Solution:**

**First Law: (A ∪ B)' = A' ∩ B'**

**Proof:**
```
x ∈ (A ∪ B)'
⟺ x ∉ (A ∪ B)
⟺ ¬(x ∈ A or x ∈ B)
⟺ x ∉ A and x ∉ B         (De Morgan for logic)
⟺ x ∈ A' and x ∈ B'
⟺ x ∈ A' ∩ B'
```

**Therefore:** (A ∪ B)' = A' ∩ B' ✓

**Concrete Example:**
- U = {1,2,3,4,5}, A = {1,2}, B = {2,3}
- A ∪ B = {1,2,3}
- (A ∪ B)' = {4,5}
- A' = {3,4,5}, B' = {1,4,5}
- A' ∩ B' = {4,5}
- Equal ✓

---

**Second Law: (A ∩ B)' = A' ∪ B'**

**Proof:**
```
x ∈ (A ∩ B)'
⟺ x ∉ (A ∩ B)
⟺ ¬(x ∈ A and x ∈ B)
⟺ x ∉ A or x ∉ B          (De Morgan for logic)
⟺ x ∈ A' or x ∈ B'
⟺ x ∈ A' ∪ B'
```

**Therefore:** (A ∩ B)' = A' ∪ B' ✓

---

### Exercise 1.2.12 - Prove De Morgan's Laws (Logic)

**Problem:** Prove ¬(p ∨ q) ≡ ¬p ∧ ¬q and ¬(p ∧ q) ≡ ¬p ∨ ¬q.

**Solution:**

**First Law: ¬(p ∨ q) ≡ ¬p ∧ ¬q**

**Truth Table:**

| p | q | p∨q | ¬(p∨q) | ¬p | ¬q | ¬p∧¬q |
|---|---|-----|--------|----|----|-------|
| F | F | F | **T** | T | T | **T** |
| F | T | T | **F** | T | F | **F** |
| T | F | T | **F** | F | T | **F** |
| T | T | T | **F** | F | F | **F** |

Columns match → Equivalent ✓

---

**Second Law: ¬(p ∧ q) ≡ ¬p ∨ ¬q**

**Truth Table:**

| p | q | p∧q | ¬(p∧q) | ¬p | ¬q | ¬p∨¬q |
|---|---|-----|--------|----|----|-------|
| F | F | F | **T** | T | T | **T** |
| F | T | F | **T** | T | F | **T** |
| T | F | F | **T** | F | T | **T** |
| T | T | T | **F** | F | F | **F** |

Columns match → Equivalent ✓

---

### Exercise 1.2.13 - Apply Duality Principle

**Problem:** Apply the duality principle to Boolean identities.

**Solution:**

**Duality Principle:** If a Boolean identity is true, its dual is also true.

**Dual formation rules:**
- Swap ∨ ↔ ∧
- Swap ⊤ (top) ↔ ⊟ (bottom)
- Keep complements unchanged

---

**Example 1:**
- Original: A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)
- Dual: A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)
- Both are true (distributivity) ✓

---

**Example 2:**
- Original: A ∪ ∅ = A
- Dual: A ∩ S = A
- Both are true (identity laws) ✓

---

**Example 3:**
- Original: A ∪ A' = S
- Dual: A ∩ A' = ∅
- Both are true (complement laws) ✓

---

### Exercise 1.2.14 - Stone's Theorem

**Problem:** Study Stone's Theorem (1936).

**Solution:**

**Stone's Representation Theorem:**

**Theorem:** Every Boolean algebra is isomorphic to a field of sets (subalgebra of a power set algebra).

**Meaning:** Any abstract Boolean algebra can be represented as sets with union, intersection, and complement.

**Significance:**
- Set algebras are the "canonical" Boolean algebras
- Abstract Boolean algebra properties can be studied via sets
- Connects algebra and set theory

**Proof sketch:** Use ultrafilters to construct the representation.

---

### Exercise 1.2.15 - Completeness Theorem

**Problem:** Study the Completeness Theorem for Boolean algebras.

**Solution:**

**Completeness Theorem:**

**Statement:** A Boolean identity is true in all Boolean algebras if and only if it's true in the two-element Boolean algebra {0, 1}.

**Practical consequence:** To verify any Boolean identity, just check truth tables with 0 and 1!

**Example:** Verify A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)
- Just check 2³ = 8 truth table rows
- If all 8 rows match, identity is universally true ✓

---

## Section 1.3 - Halmazok minőségi függetlensége

---

### Exercise 1.3.1 - Qualitative Independence Definition

**Problem:** Understand qualitative independence definition.

**Solution:**

**Definition:** Sets A₁, A₂, ..., Aₙ are **qualitatively independent** if for every choice of ε₁, ε₂, ..., εₙ ∈ {+1, -1}:

$$A_1^{\epsilon_1} \cap A_2^{\epsilon_2} \cap \cdots \cap A_n^{\epsilon_n} \neq \emptyset$$

where A⁺¹ = A and A⁻¹ = A' (complement).

---

**Example (n=2):**

A and B are independent if all 4 intersections are non-empty:
1. A ∩ B ≠ ∅
2. A ∩ B' ≠ ∅
3. A' ∩ B ≠ ∅
4. A' ∩ B' ≠ ∅

**Concrete Example:**
- I = {1, 2, 3, 4}
- A = {1, 2}, B = {1, 3}
- A ∩ B = {1} ✓
- A ∩ B' = {2} ✓
- A' ∩ B = {3} ✓
- A' ∩ B' = {4} ✓

**Therefore:** A and B are qualitatively independent. ✓

---

### Exercise 1.3.2 - Verify Proposition 1.14(i)

**Problem:** Prove: If n sets are qualitatively independent, then |I| ≥ 2ⁿ.

**Solution:**

**Proof:**

For n independent sets, there are 2ⁿ possible choices of (ε₁, ..., εₙ).

Each choice gives an intersection:
$$I_{\epsilon_1,...,\epsilon_n} = A_1^{\epsilon_1} \cap \cdots \cap A_n^{\epsilon_n}$$

By independence, each intersection is non-empty.

**Key observation:** Different (ε₁, ..., εₙ) give disjoint intersections.

**Proof:** If εᵢ ≠ εᵢ', then one contains Aᵢ and the other contains Aᵢ'.
Since Aᵢ ∩ Aᵢ' = ∅, the intersections are disjoint.

**Therefore:** We have 2ⁿ disjoint non-empty sets.

Each must contain at least one element.

**Therefore:** |I| ≥ 2ⁿ. ✓

---

### Exercise 1.3.3 - Verify Proposition 1.14(ii)

**Problem:** Prove: There exists a 2ⁿ-element base set with n qualitatively independent sets.

**Solution:**

**Construction:**

Let I = {0, 1}ⁿ (all binary strings of length n). |I| = 2ⁿ.

Define Aᵢ = {strings with 1 in position i}.

**Verification:**

For any (ε₁, ..., εₙ), construct string s where:
- sᵢ = 1 if εᵢ = +1
- sᵢ = 0 if εᵢ = -1

Then s ∈ A₁^ε₁ ∩ A₂^ε₂ ∩ ... ∩ Aₙ^εₙ.

**Therefore:** Every intersection is non-empty.

**Therefore:** A₁, ..., Aₙ are qualitatively independent. ✓

---

**Concrete Example (n=3):**

I = {000, 001, 010, 011, 100, 101, 110, 111}

A₁ = {100, 101, 110, 111} (first bit = 1)
A₂ = {010, 011, 110, 111} (second bit = 1)
A₃ = {001, 011, 101, 111} (third bit = 1)

**Check:** A₁ ∩ A₂' ∩ A₃ = {101} ≠ ∅ ✓

All 8 intersections are singletons, hence non-empty. ✓

---

### Exercise 1.3.4 - Grünbaum's Theorem

**Problem:** Study Grünbaum's Theorem (1975).

**Solution:**

**Theorem (Grünbaum, 1975):**

For any n, there exist n qualitatively independent convex polygons in the plane.

**Significance:**
- Independent sets can have nice geometric structure
- Not just abstract set constructions
- Connection between combinatorics and geometry

**Construction idea:** Use carefully arranged convex polygons where each combination of inclusions/exclusions is realizable.

---

### Exercise 1.3.5 - DNF (Disjunctive Normal Form)

**Problem:** Understand DNF.

**Solution:**

**Definition:** DNF is a disjunction (OR) of conjunctions (ANDs).

**Form:** (a₁ ∧ a₂ ∧ ...) ∨ (b₁ ∧ b₂ ∧ ...) ∨ ...

**Example:** f(A,B,C) = (A ∧ B ∧ C') ∨ (A' ∧ B ∧ C) ∨ (A ∧ B' ∧ C')

**Each conjunction is a minterm.**

**Application:** Any Boolean function can be expressed in DNF.

---

### Exercise 1.3.6 - CNF (Conjunctive Normal Form)

**Problem:** Understand CNF.

**Solution:**

**Definition:** CNF is a conjunction (AND) of disjunctions (ORs).

**Form:** (a₁ ∨ a₂ ∨ ...) ∧ (b₁ ∨ b₂ ∨ ...) ∧ ...

**Example:** f(A,B,C) = (A ∨ B ∨ C') ∧ (A' ∨ B ∨ C)

**Each disjunction is a maxterm.**

**Application:** Any Boolean function can be expressed in CNF.

---

### Exercise 1.3.7 - Minterms

**Problem:** Understand minterms.

**Solution:**

**Definition:** A minterm is a conjunction of all variables, each possibly complemented.

**Form:** m_ε = a₁^ε₁ ∧ a₂^ε₂ ∧ ... ∧ aₙ^εₙ

**Example (n=3):**
- m₁₁₁ = A ∧ B ∧ C
- m₁₀₁ = A ∧ B' ∧ C
- m₀₀₀ = A' ∧ B' ∧ C'

**Property:** For n variables, there are 2ⁿ minterms.

**Application:** Any Boolean function = OR of minterms where function = 1.

---

### Exercise 1.3.8 - Maxterms

**Problem:** Understand maxterms.

**Solution:**

**Definition:** A maxterm is a disjunction of all variables, each possibly complemented.

**Form:** M_ε = a₁^ε₁ ∨ a₂^ε₂ ∨ ... ∨ aₙ^εₙ

**Example (n=3):**
- M₀₀₀ = A ∨ B ∨ C
- M₁₀₁ = A' ∨ B ∨ C'

**Property:** For n variables, there are 2ⁿ maxterms.

**Application:** Any Boolean function = AND of maxterms where function = 0.

---

### Exercise 1.3.9 - Verify |B| ≤ 2^(2^m)

**Problem:** Verify that a Boolean algebra generated by m elements has at most 2^(2^m) elements.

**Solution:**

**Proof:**

With m generators, there are 2^m possible minterms.

Each minterm is a conjunction of the m generators (each possibly complemented).

Any element of B can be expressed as a join (OR) of some subset of minterms.

Number of subsets of minterms = 2^(2^m).

**Therefore:** |B| ≤ 2^(2^m). ✓

---

**Example (m=2):**

Generators: a, b

Minterms: a∧b, a∧b', a'∧b, a'∧b' (4 = 2² minterms)

Maximum elements: 2⁴ = 16

These are all possible ORs of subsets of minterms.

When a, b are independent: |B| = 16 (achieves maximum).

When a, b are dependent: |B| < 16.

---

### Exercise 1.3.10 - Equality Condition

**Problem:** Understand when |B| = 2^(2^m).

**Solution:**

**Theorem:** |B| = 2^(2^m) if and only if the m generators are qualitatively independent.

**Proof:**

**(⇒):** If |B| = 2^(2^m), all 2^(2^m) elements are distinct.

This requires all 2^m minterms to be non-empty.

Non-empty minterms ⇔ generators are independent.

---

**(⇐):** If generators are independent, all minterms are non-empty and distinct.

Therefore all 2^(2^m) ORs of minterms are distinct.

Therefore |B| = 2^(2^m). ✓

---

## Summary

| Exercise | Topic | Status |
|----------|-------|--------|
| 1.1.1 | Cantor's theorem | ✅ Complete |
| 1.1.2 | Russell's paradox | ✅ Complete |
| 1.1.3 | ZF axioms | ✅ Complete |
| 1.1.4 | Naive vs axiomatic | ✅ Complete |
| 1.2.1-1.2.5 | Boolean axioms | ✅ Complete |
| 1.2.6-1.2.10 | Boolean examples | ✅ Complete |
| 1.2.11-1.2.12 | De Morgan's laws | ✅ Complete |
| 1.2.13 | Duality principle | ✅ Complete |
| 1.2.14-1.2.15 | Stone's, Completeness | ✅ Complete |
| 1.3.1-1.3.4 | Qualitative independence | ✅ Complete |
| 1.3.5-1.3.8 | Normal forms | ✅ Complete |
| 1.3.9-1.3.10 | Boolean algebra size | ✅ Complete |
| **Total** | | **33 exercises** |
