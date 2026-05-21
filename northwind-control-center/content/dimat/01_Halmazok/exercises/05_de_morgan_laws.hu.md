# Feladat — De Morgan-azonosságok bizonyítása a BA-axiómákból

## A feladat

Az 1.2. szakasz 1.8. Állításából:

Bizonyítsuk be a De Morgan-azonosságokat csak a Boole-algebra (BA1)–(BA14) axiómáit használva:

```
(d) ¬(a ∨ b) = ¬a ∧ ¬b
(e) ¬(a ∧ b) = ¬a ∨ ¬b
```

---

## Boole-algebra-axiómák (BA1)–(BA14)

Hivatkozásul:

| Axióma | Név | Képlet |
|--------|-----|--------|
| (BA1) | Kommutativitás (∨) | $a \vee b = b \vee a$ |
| (BA2) | Kommutativitás (∧) | $a \wedge b = b \wedge a$ |
| (BA3) | Asszociativitás (∨) | $a \vee (b \vee c) = (a \vee b) \vee c$ |
| (BA4) | Asszociativitás (∧) | $a \wedge (b \wedge c) = (a \wedge b) \wedge c$ |
| (BA5) | Disztributivitás (∨) | $a \vee (b \wedge c) = (a \vee b) \wedge (a \vee c)$ |
| (BA6) | Disztributivitás (∧) | $a \wedge (b \vee c) = (a \wedge b) \vee (a \wedge c)$ |
| (BA7) | Elnyelés (∨) | $a \vee (a \wedge b) = a$ |
| (BA8) | Elnyelés (∧) | $a \wedge (a \vee b) = a$ |
| (BA9) | Idempotencia (∨) | $a \vee a = a$ |
| (BA10) | Idempotencia (∧) | $a \wedge a = a$ |
| (BA11) | Komplemens (∨) | $a \vee \neg a = ⊤$ |
| (BA12) | Komplemens (∧) | $a \wedge \neg a = ⊥$ |
| (BA13) | Egységelem (∨) | $a \vee ⊥ = a$, $a \vee ⊤ = ⊤$ |
| (BA14) | Egységelem (∧) | $a \wedge ⊤ = a$, $a \wedge ⊥ = ⊥$ |

---

## Kulcs-lemma: a komplemens egyértelműsége

### 1.8(c) Állítás

**Állítás:** Ha $a \vee x = ⊤$ és $a \wedge x = ⊥$, akkor $x = \neg a$.

**Bizonyítás:**

Tegyük fel, hogy $a \vee x = ⊤$ és $a \wedge x = ⊥$.

Be kell látnunk, hogy $x = \neg a$.

```
x = x ∧ ⊤                    (BA14: egységelem)
  = x ∧ (a ∨ ¬a)             (BA11: komplemens)
  = (x ∧ a) ∨ (x ∧ ¬a)       (BA6: disztributivitás)
  = (a ∧ x) ∨ (x ∧ ¬a)       (BA2: kommutativitás)
  = ⊥ ∨ (x ∧ ¬a)             (feltétel: a ∧ x = ⊥)
  = (x ∧ ¬a) ∨ ⊥             (BA1: kommutativitás)
  = x ∧ ¬a                   (BA13: egységelem)
```

Tehát: **$x = x \wedge \neg a$** ... (1)

Hasonlóan $\neg a$-ra:

```
¬a = ¬a ∧ ⊤                  (BA14: egységelem)
   = ¬a ∧ (a ∨ x)            (feltétel: a ∨ x = ⊤)
   = (¬a ∧ a) ∨ (¬a ∧ x)     (BA6: disztributivitás)
   = (a ∧ ¬a) ∨ (¬a ∧ x)     (BA2: kommutativitás)
   = ⊥ ∨ (¬a ∧ x)            (BA12: komplemens)
   = (¬a ∧ x) ∨ ⊥            (BA1: kommutativitás)
   = ¬a ∧ x                  (BA13: egységelem)
   = x ∧ ¬a                  (BA2: kommutativitás)
```

Tehát: **$\neg a = x \wedge \neg a$** ... (2)

(1) és (2)-ből: **$x = \neg a$** ✓

---

## (d) De Morgan-azonosság bizonyítása: $\neg(a \vee b) = \neg a \wedge \neg b$

### Stratégia

A komplemens egyértelműsége (1.8(c)) szerint $\neg(a \vee b) = \neg a \wedge \neg b$ bizonyításához elég megmutatni:

1. $(a \vee b) \vee (\neg a \wedge \neg b) = ⊤$
2. $(a \vee b) \wedge (\neg a \wedge \neg b) = ⊥$

---

### 1. rész: $(a \vee b) \vee (\neg a \wedge \neg b) = ⊤$

```
(a ∨ b) ∨ (¬a ∧ ¬b)
= ((a ∨ b) ∨ ¬a) ∧ ((a ∨ b) ∨ ¬b)     (BA5: disztributivitás)
= (a ∨ b ∨ ¬a) ∧ (a ∨ b ∨ ¬b)         (BA3: asszociativitás)
= (a ∨ ¬a ∨ b) ∧ (a ∨ b ∨ ¬b)         (BA1: kommutativitás)
= ((a ∨ ¬a) ∨ b) ∧ (a ∨ (b ∨ ¬b))     (BA3: asszociativitás)
= (⊤ ∨ b) ∧ (a ∨ ⊤)                   (BA11: komplemens)
= ⊤ ∧ ⊤                               (BA13: a ∨ ⊤ = ⊤)
= ⊤                                   (BA14: ⊤ ∧ ⊤ = ⊤)
```

✓ **1. rész kész.**

---

### 2. rész: $(a \vee b) \wedge (\neg a \wedge \neg b) = ⊥$

```
(a ∨ b) ∧ (¬a ∧ ¬b)
= ((a ∨ b) ∧ ¬a) ∧ ¬b                 (BA4: asszociativitás)
= ((a ∧ ¬a) ∨ (b ∧ ¬a)) ∧ ¬b          (BA6: disztributivitás)
= (⊥ ∨ (b ∧ ¬a)) ∧ ¬b                 (BA12: komplemens)
= (b ∧ ¬a) ∧ ¬b                       (BA13: ⊥ ∨ x = x)
= b ∧ ¬a ∧ ¬b                         (BA4: asszociativitás)
= b ∧ ¬b ∧ ¬a                         (BA1/BA2: kommutativitás)
= (b ∧ ¬b) ∧ ¬a                       (BA4: asszociativitás)
= ⊥ ∧ ¬a                              (BA12: komplemens)
= ⊥                                   (BA14: ⊥ ∧ x = ⊥)
```

✓ **2. rész kész.**

---

### Konklúzió (d)-re

Mivel $(a \vee b) \vee (\neg a \wedge \neg b) = ⊤$ és $(a \vee b) \wedge (\neg a \wedge \neg b) = ⊥$, a komplemens egyértelműsége alapján:

$$\neg(a \vee b) = \neg a \wedge \neg b \quad \checkmark$$

---

## (e) De Morgan-azonosság bizonyítása: $\neg(a \wedge b) = \neg a \vee \neg b$

### Stratégia

A komplemens egyértelműsége alapján szintén elég megmutatni:

1. $(a \wedge b) \vee (\neg a \vee \neg b) = ⊤$
2. $(a \wedge b) \wedge (\neg a \vee \neg b) = ⊥$

---

### 1. rész: $(a \wedge b) \vee (\neg a \vee \neg b) = ⊤$

```
(a ∧ b) ∨ (¬a ∨ ¬b)
= ((a ∧ b) ∨ ¬a) ∨ ¬b                 (BA3: asszociativitás)
= ((a ∨ ¬a) ∧ (b ∨ ¬a)) ∨ ¬b          (BA5: disztributivitás)
= (⊤ ∧ (b ∨ ¬a)) ∨ ¬b                 (BA11: komplemens)
= (b ∨ ¬a) ∨ ¬b                       (BA14: ⊤ ∧ x = x)
= b ∨ ¬a ∨ ¬b                         (BA3: asszociativitás)
= b ∨ ¬b ∨ ¬a                         (BA1: kommutativitás)
= (b ∨ ¬b) ∨ ¬a                       (BA3: asszociativitás)
= ⊤ ∨ ¬a                              (BA11: komplemens)
= ⊤                                   (BA13: ⊤ ∨ x = ⊤)
```

✓ **1. rész kész.**

---

### 2. rész: $(a \wedge b) \wedge (\neg a \vee \neg b) = ⊥$

```
(a ∧ b) ∧ (¬a ∨ ¬b)
= ((a ∧ b) ∧ ¬a) ∨ ((a ∧ b) ∧ ¬b)     (BA6: disztributivitás)
= (a ∧ b ∧ ¬a) ∨ (a ∧ b ∧ ¬b)         (BA4: asszociativitás)
= (a ∧ ¬a ∧ b) ∨ (a ∧ b ∧ ¬b)         (BA1/BA2: kommutativitás)
= (⊥ ∧ b) ∨ (a ∧ ⊥)                   (BA12: komplemens)
= ⊥ ∨ ⊥                               (BA14: ⊥ ∧ x = ⊥)
= ⊥                                   (BA13: ⊥ ∨ ⊥ = ⊥)
```

✓ **2. rész kész.**

---

### Konklúzió (e)-re

Mivel $(a \wedge b) \vee (\neg a \vee \neg b) = ⊤$ és $(a \wedge b) \wedge (\neg a \vee \neg b) = ⊥$, a komplemens egyértelműsége alapján:

$$\neg(a \wedge b) = \neg a \vee \neg b \quad \checkmark$$

---

## Alternatív bizonyítás dualitással

### Dualitás elve (1.9. Tétel)

Ha egy formula igaz a Boole-algebrában, akkor a **duálisa** is igaz.

**Duális transzformáció:**
- $\vee \leftrightarrow \wedge$
- $⊤ \leftrightarrow ⊥$
- $\neg$ változatlan

### A dualitás alkalmazása

Miután bebizonyítottuk a (d) De Morgan-azonosságot:
$$\neg(a \vee b) = \neg a \wedge \neg b$$

A duálisa:
$$\neg(a \wedge b) = \neg a \vee \neg b$$

Ami pontosan a (e) De Morgan-azonosság! ✓

**Tehát egyik De Morgan-azonosság bizonyításával a másik automatikusan adódik a dualitás-elvből.**

---

## Ellenőrzés igazságtáblával (intuícióhoz)

### (d): $\neg(a \vee b) = \neg a \wedge \neg b$

| a | b | a∨b | ¬(a∨b) | ¬a | ¬b | ¬a∧¬b |
|---|---|-----|--------|----|----|-------|
| 0 | 0 |  0  |   1    | 1  | 1  |   1   |
| 0 | 1 |  1  |   0    | 1  | 0  |   0   |
| 1 | 0 |  1  |   0    | 0  | 1  |   0   |
| 1 | 1 |  1  |   0    | 0  | 0  |   0   |

✓ Az oszlopok egyeznek!

### (e): $\neg(a \wedge b) = \neg a \vee \neg b$

| a | b | a∧b | ¬(a∧b) | ¬a | ¬b | ¬a∨¬b |
|---|---|-----|--------|----|----|-------|
| 0 | 0 |  0  |   1    | 1  | 1  |   1   |
| 0 | 1 |  0  |   1    | 1  | 0  |   1   |
| 1 | 0 |  0  |   1    | 0  | 1  |   1   |
| 1 | 1 |  1  |   0    | 0  | 0  |   0   |

✓ Az oszlopok egyeznek!

---

## Halmazelméleti interpretáció (Venn-diagram)

### (d): $(A \cup B)' = A' \cap B'$

```
    ┌─────────────────┐
    │    ┌───┐        │
    │ A  │ ∩ │   B    │
    │    └───┘        │
    │                 │
    │   Festett:      │
    │   minden, ami   │
    │   nincs A∪B-ben │
    └─────────────────┘
```

Az unió komplemense egyenlő a komplemensek metszetével.

### (e): $(A \cap B)' = A' \cup B'$

A metszet komplemense egyenlő a komplemensek uniójával.

---

## Összefoglaló

| Azonosság | Képlet | Bizonyítási módszer |
|-----------|--------|---------------------|
| **De Morgan (d)** | $\neg(a \vee b) = \neg a \wedge \neg b$ | Komplemens egyértelműsége |
| **De Morgan (e)** | $\neg(a \wedge b) = \neg a \vee \neg b$ | Komplemens egyértelműsége VAGY dualitás |

### Fő bizonyítási technikák

1. **Komplemens egyértelműsége (1.8(c)):** ha $x \vee a = ⊤$ és $x \wedge a = ⊥$, akkor $x = \neg a$
2. **Disztributivitás:** kifejezések átalakításához
3. **Komplemens axiómák:** $a \vee \neg a = ⊤$, $a \wedge \neg a = ⊥$
4. **Egységelem-axiómák:** $a \vee ⊥ = a$, $a \wedge ⊤ = a$
5. **Dualitás elve:** (d)-ből automatikusan adja (e)-t

---

## Alkalmazások

1. **Logika:** $\neg(P \vee Q) \equiv \neg P \wedge \neg Q$ és $\neg(P \wedge Q) \equiv \neg P \vee \neg Q$
2. **Halmazelmélet:** $(A \cup B)^c = A^c \cap B^c$
3. **Digitális áramkörök:** NAND/NOR kapuk átalakítása
4. **Programozás:** `!(a || b)` ≡ `!a && !b`

---

## Hivatkozások

- 1.2. § — Boole-algebra-axiómák
- 1.8. Állítás — De Morgan-azonosságok
- 1.9. Tétel — Dualitás elve
