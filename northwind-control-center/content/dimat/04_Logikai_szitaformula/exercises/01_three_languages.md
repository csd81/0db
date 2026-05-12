# Exercise 4.1 - Three Languages Problem

## Problem Statement

In a faculty of 67 students:
- 47 speak English
- 35 speak German
- 23 speak both English and German
- 20 speak French
- 12 speak English and French
- 11 speak German and French
- 5 speak all three languages

**Question:** How many students speak none of the three languages?

---

## Solution using Inclusion-Exclusion

### Given Information

Let:
- $E$ = students who speak English, $|E| = 47$
- $G$ = students who speak German, $|G| = 35$
- $F$ = students who speak French, $|F| = 20$

Intersections:
- $|E \cap G| = 23$
- $|E \cap F| = 12$
- $|G \cap F| = 11$
- $|E \cap G \cap F| = 5$

Total students: $|I| = 67$

### Step 1: Apply Inclusion-Exclusion Formula

Number of students who speak **at least one** language:

$$|E \cup G \cup F| = |E| + |G| + |F| - |E \cap G| - |E \cap F| - |G \cap F| + |E \cap G \cap F|$$

Substituting values:

$$|E \cup G \cup F| = 47 + 35 + 20 - 23 - 12 - 11 + 5$$

$$|E \cup G \cup F| = 102 - 46 + 5 = 61$$

### Step 2: Find Complement

Students who speak **none** of the languages:

$$|N| = |I| - |E \cup G \cup F| = 67 - 61 = 6$$

---

## Answer

$$\boxed{6 \text{ students speak none of the three languages}}$$

---

## Verification

Let's verify by counting each region in the Venn diagram:

### Region breakdown:

| Region | Description | Count |
|--------|-------------|-------|
| $E \cap G \cap F$ | All three | 5 |
| $E \cap G \setminus F$ | English & German only | $23 - 5 = 18$ |
| $E \cap F \setminus G$ | English & French only | $12 - 5 = 7$ |
| $G \cap F \setminus E$ | German & French only | $11 - 5 = 6$ |
| $E \setminus (G \cup F)$ | English only | $47 - 18 - 7 - 5 = 17$ |
| $G \setminus (E \cup F)$ | German only | $35 - 18 - 6 - 5 = 6$ |
| $F \setminus (E \cup G)$ | French only | $20 - 7 - 6 - 5 = 2$ |
| None | No language | ? |

### Sum of all regions:

$$5 + 18 + 7 + 6 + 17 + 6 + 2 + \text{None} = 67$$

$$61 + \text{None} = 67$$

$$\text{None} = 6$$ ✓

---

## Alternative Method: Direct Formula

Using the complement form of inclusion-exclusion (Theorem 4.3):

$$|N| = |I| - \sum |A_i| + \sum |A_i \cap A_j| - |A_1 \cap A_2 \cap A_3|$$

$$|N| = 67 - (47 + 35 + 20) + (23 + 12 + 11) - 5$$

$$|N| = 67 - 102 + 46 - 5$$

$$|N| = 67 - 61 = 6$$ ✓

---

## Key Insight

The inclusion-exclusion principle ensures we count each student exactly once:
- Students in exactly 1 set: counted 1 - 0 + 0 = 1 time
- Students in exactly 2 sets: counted 2 - 1 + 0 = 1 time
- Students in exactly 3 sets: counted 3 - 3 + 1 = 1 time

---

## General Formula for 3 Sets

For any three sets $A$, $B$, $C$:

$$|A \cup B \cup C| = |A| + |B| + |C| - |A \cap B| - |A \cap C| - |B \cap C| + |A \cap B \cap C|$$

And the complement (none of the properties):

$$|I \setminus (A \cup B \cup C)| = |I| - |A \cup B \cup C|$$

---

*Exercise 4.1 from Chapter 04 - A logikai szitaformula*
