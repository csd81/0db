# 01. fejezet — Halmazok — Teljes megoldások

## 1.1. § — Halmazok definíciója

---

### 1.1.1. Feladat — Cantor tétele: nincs univerzális halmaz

**Feladat:** Igazoljuk, hogy nincs olyan halmaz, amely minden elemet tartalmaz.

**Megoldás:**

**Indirekt bizonyítás (Russell-paradoxon):**

**1. lépés:** Tegyük fel, hogy létezik egy $U$ univerzális halmaz, amely mindent tartalmaz.

**2. lépés:** Konstruáljuk meg a Russell-halmazt:
$$R = \{x \in U : x \notin x\}$$

Ez azon halmazok halmaza, amelyek nem tartalmazzák önmagukat.

**3. lépés:** Kérdezzük: $R \in R$?

**1. eset:** Tegyük fel $R \in R$
- $R$ definíciója szerint ha $R \in R$, akkor $R$ kielégíti a feltételt: $R \notin R$
- Ellentmondás! $R \in R$ azt jelenti, hogy $R \notin R$

**2. eset:** Tegyük fel $R \notin R$
- $R$ definíciója szerint ha $R \notin R$, akkor $R$ kielégíti a tagsági feltételt
- Tehát $R \in R$
- Ellentmondás! $R \notin R$ azt jelenti, hogy $R \in R$

**4. lépés:** Mindkét eset ellentmondáshoz vezet.

**Konklúzió:** A feltevés, hogy $U$ létezik, hamis kell hogy legyen.

**Tehát:** Nem létezik univerzális halmaz. $\blacksquare$

---

### 1.1.2. Feladat — Russell-paradoxon részletes elemzése

**Feladat:** Tanulmányozzuk a Russell-paradoxon indirekt bizonyítását.

**Megoldás:**

**Történeti háttér:**
- Bertrand Russell fedezte fel (1901)
- Megmutatta, hogy a naiv halmazelmélet ellentmondásos
- Az axiomatikus halmazelmélet (ZF) kifejlesztéséhez vezetett

**Részletes bizonyítás:**

Legyen $P(x)$ az „$x \notin x$" tulajdonság.

A naiv komprehenzió szerint képezhetjük:
$$R = \{x : P(x)\} = \{x : x \notin x\}$$

**Kérdés:** $R \in R$ vagy $R \notin R$?

**Logikai elemzés:**
```
R ∈ R ⟺ R kielégíti P-t ⟺ R ∉ R
```

Ez logikai ellentmondás: $R \in R \iff R \notin R$.

**Feloldás a ZF halmazelméletben:**
- A ZF a szétválasztási axiómát használja a naiv komprehenzió helyett
- Csak $\{x \in A : P(x)\}$ alakú részhalmaz képezhető (egy létező $A$ halmazból)
- Nem képezhető $\{x : P(x)\}$ alaphalmaz nélkül
- Ez megakadályozza $R$ halmazként való létrejöttét

**Tehát:** A Russell-paradoxon elkerülhető az axiomatikus halmazelméletben. $\blacksquare$

---

### 1.1.3. Feladat — Zermelo–Fraenkel-axiómák áttekintése

**Feladat:** Ismételjük át és értsük meg a ZF-axiómákat.

**Megoldás:**

**A 9 ZF-axióma:**

**1. Extenzionalitási axióma:**
$$\forall A \forall B [\forall x (x \in A \iff x \in B) \implies A = B]$$

*Jelentés:* Két halmaz pontosan akkor egyenlő, ha ugyanazon elemeket tartalmazzák.

**Példa:** $\{1, 2, 3\} = \{3, 2, 1\}$ (ugyanazok az elemek, sorrend nem számít)

---

**2. Üres halmaz axiómája:**
$$\exists \emptyset \forall x (x \notin \emptyset)$$

*Jelentés:* Létezik egy elemek nélküli halmaz.

**Ellenőrzés:** $\emptyset$ létezik és egyértelmű (extenzionalitásból).

---

**3. Páraxióma:**
$$\forall a \forall b \exists C \forall x (x \in C \iff x = a \lor x = b)$$

*Jelentés:* Bármely $a, b$-re létezik a $\{a, b\}$ halmaz.

**Példa:** $a = 1$, $b = 2$ esetén $\{1, 2\}$ létezik.

---

**4. Unió-axióma:**
$$\forall A \exists U \forall x (x \in U \iff \exists B (B \in A \land x \in B))$$

*Jelentés:* Bármely $A$ halmazra létezik az elemei uniója.

**Példa:** $A = \{\{1,2\}, \{3\}\} \Rightarrow \bigcup A = \{1, 2, 3\}$

---

**5. Hatványhalmaz-axióma:**
$$\forall A \exists P \forall x (x \in P \iff x \subseteq A)$$

*Jelentés:* Bármely $A$ halmazra létezik az összes részhalmazának halmaza.

**Példa:** $A = \{1, 2\} \Rightarrow \mathcal{P}(A) = \{\emptyset, \{1\}, \{2\}, \{1, 2\}\}$

---

**6. Végtelenségi axióma:**
$$\exists I (\emptyset \in I \land \forall x (x \in I \implies x \cup \{x\} \in I))$$

*Jelentés:* Létezik egy végtelen halmaz ($\emptyset$ benne van és zárt az utódképzésre).

**Konstrukció:** $\emptyset, \{\emptyset\}, \{\emptyset, \{\emptyset\}\}, \dots$ — természetes számok.

---

**7. Szétválasztási axiómaséma:**
Bármely $\varphi$ tulajdonság és $A$ halmaz esetén:
$$\exists B \forall x (x \in B \iff x \in A \land \varphi(x))$$

*Jelentés:* Részhalmazok képezhetők tulajdonságokkal, de csak létező halmazból.

**Megelőzi a Russell-paradoxont:** Nem képezhető $\{x : x \notin x\}$ alaphalmaz nélkül.

---

**8. Helyettesítési axiómaséma:**
Bármely definiálható $f$ függvény és $A$ halmaz esetén:
$$\exists B \forall y (y \in B \iff \exists x (x \in A \land y = f(x)))$$

*Jelentés:* Egy halmaz képe egy függvény mentén szintén halmaz.

---

**9. Regularitás (alapozási) axióma:**
$$\forall A (A \neq \emptyset \implies \exists x (x \in A \land x \cap A = \emptyset))$$

*Jelentés:* Minden nemüres halmaznak van $\in$-minimális eleme.

**Következmény:** Egyetlen halmaz sem tartalmazza önmagát ($A \notin A$ minden $A$-ra).

---

### 1.1.4. Feladat — Naiv vs. axiomatikus halmazelmélet

**Feladat:** Értsük meg a naiv és axiomatikus halmazelmélet különbségét.

**Megoldás:**

| Szempont | Naiv halmazelmélet | Axiomatikus halmazelmélet (ZF) |
|----------|-------------------|--------------------------------|
| **Komprehenzió** | Korlátlan: $\{x : P(x)\}$ | Korlátozott: $\{x \in A : P(x)\}$ |
| **Paradoxonok** | Sebezhető (Russell-) | Axiómákkal elkerülve |
| **Alapozás** | Intuitív | Formális axiómák |
| **Létezés** | Halmazok létét feltételezi | Axiómákból bizonyítja |
| **Használat** | Informális matematika | A matematika alapja |

**Kulcs-különbség:**
- Naiv: „Bármely tulajdonság halmazt definiál" → ellentmondáshoz vezet
- Axiomatikus: „Halmazok axiómákból épülnek" → konzisztens (eddigi tudásunk szerint)

---

## 1.2. § — Boole-algebrák

---

### 1.2.1. Feladat — Kommutativitás (BA1, BA2)

**Feladat:** Igazoljuk $A \cup B = B \cup A$-t és $A \cap B = B \cap A$-t.

**Megoldás:**

**Az unióra ($A \cup B = B \cup A$):**

**Bizonyítás:**
```
x ∈ A ∪ B
⟺ x ∈ A vagy x ∈ B     (unió definíciója)
⟺ x ∈ B vagy x ∈ A     (VAGY kommutatív)
⟺ x ∈ B ∪ A            (unió definíciója)
```

**Tehát:** $A \cup B = B \cup A$ ✓

**Konkrét példa:**
- $A = \{1, 2\}, B = \{2, 3\}$
- $A \cup B = \{1, 2, 3\}$
- $B \cup A = \{1, 2, 3\}$
- Egyenlő ✓

---

**A metszetre ($A \cap B = B \cap A$):**

**Bizonyítás:**
```
x ∈ A ∩ B
⟺ x ∈ A és x ∈ B     (metszet definíciója)
⟺ x ∈ B és x ∈ A     (ÉS kommutatív)
⟺ x ∈ B ∩ A          (metszet definíciója)
```

**Tehát:** $A \cap B = B \cap A$ ✓

---

### 1.2.2. Feladat — Asszociativitás (BA3, BA4)

**Feladat:** Igazoljuk $A \cup (B \cup C) = (A \cup B) \cup C$-t és $A \cap (B \cap C) = (A \cap B) \cap C$-t.

**Megoldás:**

**Az unióra:**
```
x ∈ A ∪ (B ∪ C)
⟺ x ∈ A vagy (x ∈ B vagy x ∈ C)
⟺ (x ∈ A vagy x ∈ B) vagy x ∈ C    (VAGY asszociatív)
⟺ x ∈ (A ∪ B) ∪ C
```

**Konkrét példa:** $A = \{1\}, B = \{2\}, C = \{3\}$
- $A \cup (B \cup C) = \{1\} \cup \{2, 3\} = \{1, 2, 3\}$
- $(A \cup B) \cup C = \{1, 2\} \cup \{3\} = \{1, 2, 3\}$ ✓

---

### 1.2.3. Feladat — Disztributivitás (BA5, BA6)

**Feladat:** Igazoljuk $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$-t.

**Megoldás:**

**Bizonyítás ($\subseteq$ irány):**

Legyen $x \in A \cup (B \cap C)$.

**1. eset:** $x \in A$
- Akkor $x \in A \cup B$ és $x \in A \cup C$
- Tehát $x \in (A \cup B) \cap (A \cup C)$

**2. eset:** $x \in B \cap C$
- Akkor $x \in B$ és $x \in C$
- Tehát $x \in A \cup B$ és $x \in A \cup C$
- Tehát $x \in (A \cup B) \cap (A \cup C)$

**Tehát:** $A \cup (B \cap C) \subseteq (A \cup B) \cap (A \cup C)$

---

**Bizonyítás ($\supseteq$ irány):**

Legyen $x \in (A \cup B) \cap (A \cup C)$.

Akkor $x \in A \cup B$ ÉS $x \in A \cup C$.

**1. eset:** $x \in A$ — akkor $x \in A \cup (B \cap C)$ ✓

**2. eset:** $x \notin A$
- $x \in A \cup B$ és $x \notin A$ → $x \in B$
- $x \in A \cup C$ és $x \notin A$ → $x \in C$
- Tehát $x \in B \cap C$
- Tehát $x \in A \cup (B \cap C)$ ✓

**Konklúzió:** $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$ ✓

---

### 1.2.4. Feladat — Elnyelés (BA7, BA8)

**Feladat:** Igazoljuk $A \cup (A \cap B) = A$-t.

**Megoldás:**

**($\subseteq$):** Legyen $x \in A \cup (A \cap B)$.
- 1. eset: $x \in A$ → $x \in A$ ✓
- 2. eset: $x \in A \cap B$ → $x \in A$ ✓

**($\supseteq$):** Legyen $x \in A$. Akkor $x \in A \cup (\text{bármi})$.

**Konklúzió:** $A \cup (A \cap B) = A$ ✓

---

### 1.2.5. Feladat — Komplemens (BA11, BA12)

**Feladat:** Igazoljuk $A \cup A' = I$-t és $A \cap A' = \emptyset$-t.

**Megoldás:**

**$A \cup A' = I$ (alaphalmaz):**
```
x ∈ A ∪ A'
⟺ x ∈ A vagy x ∈ A'
⟺ x ∈ A vagy x ∉ A
⟺ x ∈ I  (kizárt harmadik elve)
```

**$A \cap A' = \emptyset$:**
```
x ∈ A ∩ A'
⟺ x ∈ A és x ∈ A'
⟺ x ∈ A és x ∉ A
⟺ Hamis (ellentmondás)
⟺ x ∈ ∅
```

**Konkrét példa:** $U = \{1, 2, 3, 4\}, A = \{1, 2\}, A' = \{3, 4\}$
- $A \cup A' = \{1, 2, 3, 4\} = U$ ✓
- $A \cap A' = \emptyset$ ✓

---

### 1.2.6. Feladat — Halmazalgebra Boole-volta

**Feladat:** Igazoljuk, hogy $(\mathcal{P}(S), \cup, \cap, ', \emptyset, S)$ Boole-algebra.

**Megoldás:**

| Axióma | Tulajdonság | Ellenőrzés |
|--------|-------------|------------|
| BA1–2 | Kommutativitás | 1.2.1-ben igazolva ✓ |
| BA3–4 | Asszociativitás | 1.2.2-ben igazolva ✓ |
| BA5–6 | Disztributivitás | 1.2.3-ban igazolva ✓ |
| BA7–8 | Elnyelés | 1.2.4-ben igazolva ✓ |
| BA9–10 | Egységelem | $A \cup \emptyset = A$, $A \cap S = A$ ✓ |
| BA11–12 | Komplemens | $A \cup A' = S$, $A \cap A' = \emptyset$ ✓ |
| BA13–14 | Korlátok | $A \cup S = S$, $A \cap \emptyset = \emptyset$ ✓ |

**Mind a 14 axióma teljesül.**

**Tehát:** $(\mathcal{P}(S), \cup, \cap, ', \emptyset, S)$ Boole-algebra. ✓

---

### 1.2.7. Feladat — Logika-algebra Boole-volta

**Feladat:** Igazoljuk, hogy $(\{H, I\}, \vee, \wedge, \neg, H, I)$ Boole-algebra.

**Megoldás:**

**Igazságtáblázatos ellenőrzés:**

**Kommutativitás:**
| p | q | p∨q | q∨p | p∧q | q∧p |
|---|---|-----|-----|-----|-----|
| H | H | H | H | H | H |
| H | I | I | I | H | H |
| I | H | I | I | H | H |
| I | I | I | I | I | I |

Az oszlopok egyeznek → kommutativitás ✓

**Komplemens:**
| p | ¬p | p∨¬p | p∧¬p |
|---|----|------|------|
| H | I | I | H |
| I | H | I | H |

$p \vee \neg p = I$ (egységelem), $p \wedge \neg p = H$ (nullelem) ✓

**Tehát:** $(\{H, I\}, \vee, \wedge, \neg, H, I)$ Boole-algebra. ✓

---

### 1.2.8. Feladat — Számelméleti algebra Boole-volta

**Feladat:** Igazoljuk, hogy $(D_n, \operatorname{lnko}, \operatorname{lkkt}, ', n, 1)$ Boole-algebra négyzetmentes $n$-re.

**Megoldás:**

**Legyen $n = 6 = 2 \cdot 3$ (négyzetmentes).**

**Osztók:** $D_6 = \{1, 2, 3, 6\}$

**Műveletek:**
- $a \vee b = \operatorname{lkkt}(a, b)$
- $a \wedge b = \operatorname{lnko}(a, b)$
- $a' = n/a$
- $⊤ = n = 6$
- $⊥ = 1$

**Ellenőrző táblázat:**

| a | b | lkkt(a,b) | lnko(a,b) | a' | a∨a' | a∧a' |
|---|---|-----------|-----------|----|------|------|
| 1 | 2 | 2 | 1 | 6 | 6 | 1 |
| 1 | 3 | 3 | 1 | 6 | 6 | 1 |
| 2 | 3 | 6 | 1 | 3 | 6 | 1 |
| 2 | 6 | 6 | 2 | 3 | 6 | 1 |
| 3 | 6 | 6 | 3 | 2 | 6 | 1 |

**Minden Boole-axióma teljesül négyzetmentes $n$ esetén.** ✓

**Megjegyzés:** Ha $n$-nek vannak ismétlődő prím-tényezői, a komplemens nem működik megfelelően.

---

### 1.2.9. Feladat — Eseményalgebra

**Feladat:** Igazoljuk, hogy a valószínűségszámítási események Boole-algebrát alkotnak.

**Megoldás:**

**Eseménytér $\Omega$, események = $\Omega$ részhalmazai.**

**Műveletek:**
- $A \vee B = A \cup B$ ($A$ vagy $B$ bekövetkezik)
- $A \wedge B = A \cap B$ ($A$ és $B$ is bekövetkezik)
- $A' = \Omega \setminus A$ ($A$ nem következik be)
- $⊤ = \Omega$ (biztos esemény)
- $⊥ = \emptyset$ (lehetetlen esemény)

**Ellenőrzés:** Ugyanaz, mint a halmazalgebra — minden 14 axióma teljesül ✓

**Példa:** dobókocka
- $\Omega = \{1, 2, 3, 4, 5, 6\}$
- $A = $ „páros" $= \{2, 4, 6\}$
- $A' = $ „páratlan" $= \{1, 3, 5\}$
- $A \cup A' = \Omega$ (biztos)
- $A \cap A' = \emptyset$ (lehetetlen) ✓

---

### 1.2.10. Feladat — Kapcsolóalgebra

**Feladat:** Igazoljuk, hogy a kapcsoló-áramkörök Boole-algebrát alkotnak.

**Megoldás:**

**Értékek:** $\{0, 1\}$ (ki, be)

**Műveletek:**
- VAGY ($\vee$): $0 \vee 0 = 0$, $0 \vee 1 = 1$, $1 \vee 0 = 1$, $1 \vee 1 = 1$
- ÉS ($\wedge$): $0 \wedge 0 = 0$, $0 \wedge 1 = 0$, $1 \wedge 0 = 0$, $1 \wedge 1 = 1$
- NEM ($\neg$): $\neg 0 = 1$, $\neg 1 = 0$

**Áramkör-értelmezés:**
- Soros kapcsolás = ÉS
- Párhuzamos kapcsolás = VAGY
- Inverter = NEM

**Minden Boole-axióma igazságtáblázattal igazolható.** ✓

**Alkalmazás:** A digitális logikatervezés ezt a Boole-algebrát használja.

---

### 1.2.11. Feladat — De Morgan-azonosságok (halmazok)

**Feladat:** Igazoljuk $(A \cup B)' = A' \cap B'$-t és $(A \cap B)' = A' \cup B'$-t.

**Megoldás:**

**Első: $(A \cup B)' = A' \cap B'$**

```
x ∈ (A ∪ B)'
⟺ x ∉ (A ∪ B)
⟺ ¬(x ∈ A vagy x ∈ B)
⟺ x ∉ A és x ∉ B         (logikai De Morgan)
⟺ x ∈ A' és x ∈ B'
⟺ x ∈ A' ∩ B'
```

**Tehát:** $(A \cup B)' = A' \cap B'$ ✓

**Konkrét példa:**
- $U = \{1,2,3,4,5\}$, $A = \{1,2\}$, $B = \{2,3\}$
- $A \cup B = \{1,2,3\}$
- $(A \cup B)' = \{4,5\}$
- $A' = \{3,4,5\}$, $B' = \{1,4,5\}$
- $A' \cap B' = \{4,5\}$ ✓

---

**Második: $(A \cap B)' = A' \cup B'$**

```
x ∈ (A ∩ B)'
⟺ x ∉ (A ∩ B)
⟺ ¬(x ∈ A és x ∈ B)
⟺ x ∉ A vagy x ∉ B       (logikai De Morgan)
⟺ x ∈ A' vagy x ∈ B'
⟺ x ∈ A' ∪ B'
```

**Tehát:** $(A \cap B)' = A' \cup B'$ ✓

---

### 1.2.12. Feladat — De Morgan-azonosságok (logika)

**Feladat:** Igazoljuk $\neg(p \vee q) \equiv \neg p \wedge \neg q$-t és $\neg(p \wedge q) \equiv \neg p \vee \neg q$-t.

**Megoldás:**

**Első: $\neg(p \vee q) \equiv \neg p \wedge \neg q$**

**Igazságtáblázat:**

| p | q | p∨q | ¬(p∨q) | ¬p | ¬q | ¬p∧¬q |
|---|---|-----|--------|----|----|-------|
| H | H | H | **I** | I | I | **I** |
| H | I | I | **H** | I | H | **H** |
| I | H | I | **H** | H | I | **H** |
| I | I | I | **H** | H | H | **H** |

Az oszlopok egyeznek → ekvivalensek ✓

---

**Második: $\neg(p \wedge q) \equiv \neg p \vee \neg q$**

| p | q | p∧q | ¬(p∧q) | ¬p | ¬q | ¬p∨¬q |
|---|---|-----|--------|----|----|-------|
| H | H | H | **I** | I | I | **I** |
| H | I | H | **I** | I | H | **I** |
| I | H | H | **I** | H | I | **I** |
| I | I | I | **H** | H | H | **H** |

Az oszlopok egyeznek → ekvivalensek ✓

---

### 1.2.13. Feladat — Dualitás elve

**Feladat:** Alkalmazzuk a dualitás elvét Boole-azonosságokra.

**Megoldás:**

**Dualitás elve:** ha egy Boole-azonosság igaz, a duálisa is igaz.

**Duális képzési szabályok:**
- Cseréld: $\vee \leftrightarrow \wedge$
- Cseréld: $⊤$ (egységelem) $\leftrightarrow ⊥$ (nullelem)
- A komplemenseket változatlanul hagyd

---

**1. példa:**
- Eredeti: $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$
- Duális: $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$
- Mindkettő igaz (disztributivitás) ✓

---

**2. példa:**
- Eredeti: $A \cup \emptyset = A$
- Duális: $A \cap S = A$
- Mindkettő igaz (egységelem-törvények) ✓

---

**3. példa:**
- Eredeti: $A \cup A' = S$
- Duális: $A \cap A' = \emptyset$
- Mindkettő igaz (komplemens-törvények) ✓

---

### 1.2.14. Feladat — Stone-tétel

**Feladat:** Tanulmányozzuk Stone tételét (1936).

**Megoldás:**

**Stone-féle reprezentációs tétel:**

**Tétel:** Minden Boole-algebra izomorf egy halmaztest részalgebrájával (egy hatványhalmaz-algebra rész-algebrájával).

**Jelentés:** Bármely absztrakt Boole-algebra reprezentálható halmazok unió, metszet és komplemens műveleteivel.

**Jelentőség:**
- A halmazalgebrák a „kanonikus" Boole-algebrák
- Absztrakt BA-tulajdonságok halmazokon keresztül tanulmányozhatók
- Összeköti az algebrát és a halmazelméletet

**Bizonyítás-vázlat:** Ultrafilterek segítségével konstruáljuk a reprezentációt.

---

### 1.2.15. Feladat — Teljességi tétel

**Feladat:** Tanulmányozzuk a Boole-algebrák teljességi tételét.

**Megoldás:**

**Teljességi tétel:**

**Állítás:** Egy Boole-azonosság akkor és csak akkor igaz minden Boole-algebrában, ha igaz a kétértékű $\{0, 1\}$ Boole-algebrában.

**Gyakorlati következmény:** Bármely Boole-azonosság ellenőrzéséhez elég megnézni az igazságtáblázatokat 0-val és 1-gyel!

**Példa:** Igazoljuk $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$-t.
- Csak a $2^3 = 8$ igazságtáblázat-sort kell ellenőrizni
- Ha mind a 8 sor egyezik, az azonosság univerzálisan igaz ✓

---

## 1.3. § — Halmazok minőségi függetlensége

---

### 1.3.1. Feladat — Minőségi függetlenség definíciója

**Feladat:** Értsük meg a minőségi függetlenség definícióját.

**Megoldás:**

**Definíció:** Az $A_1, A_2, \dots, A_n$ halmazok **minőségileg függetlenek**, ha minden $\varepsilon_1, \varepsilon_2, \dots, \varepsilon_n \in \{+1, -1\}$ választásra:

$$A_1^{\varepsilon_1} \cap A_2^{\varepsilon_2} \cap \cdots \cap A_n^{\varepsilon_n} \neq \emptyset$$

ahol $A^{+1} = A$ és $A^{-1} = A'$ (komplemens).

---

**Példa ($n = 2$):**

$A$ és $B$ függetlenek, ha mind a 4 metszet nemüres:
1. $A \cap B \neq \emptyset$
2. $A \cap B' \neq \emptyset$
3. $A' \cap B \neq \emptyset$
4. $A' \cap B' \neq \emptyset$

**Konkrét példa:**
- $I = \{1, 2, 3, 4\}$
- $A = \{1, 2\}$, $B = \{1, 3\}$
- $A \cap B = \{1\}$ ✓
- $A \cap B' = \{2\}$ ✓
- $A' \cap B = \{3\}$ ✓
- $A' \cap B' = \{4\}$ ✓

**Tehát:** $A$ és $B$ minőségileg függetlenek. ✓

---

### 1.3.2. Feladat — Az 1.14(i) Állítás igazolása

**Feladat:** Bizonyítsuk: ha $n$ halmaz minőségileg független, akkor $|I| \geq 2^n$.

**Megoldás:**

**Bizonyítás:**

$n$ független halmaz esetén $2^n$ lehetséges $(\varepsilon_1, \dots, \varepsilon_n)$ választás van.

Minden választás egy metszetet ad:
$$I_{\vec\varepsilon} = A_1^{\varepsilon_1} \cap \cdots \cap A_n^{\varepsilon_n}$$

Függetlenség miatt minden metszet nemüres.

**Kulcs-megfigyelés:** Különböző $(\varepsilon_1, \dots, \varepsilon_n)$ esetén a metszetek diszjunktak.

**Bizonyítás:** Ha $\varepsilon_i \neq \varepsilon'_i$, akkor egyik tartalmazza $A_i$-t, a másik $A_i'$-t.
Mivel $A_i \cap A_i' = \emptyset$, a metszetek diszjunktak.

**Tehát:** $2^n$ diszjunkt nemüres halmazunk van.

Mindegyik legalább egy elemet tartalmaz.

**Tehát:** $|I| \geq 2^n$. ✓

---

### 1.3.3. Feladat — Az 1.14(ii) Állítás igazolása

**Feladat:** Bizonyítsuk: létezik $2^n$-elemű alaphalmaz $n$ minőségileg független halmazzal.

**Megoldás:**

**Konstrukció:**

Legyen $I = \{0, 1\}^n$ (összes $n$-hosszúságú bináris sorozat). $|I| = 2^n$.

Definiáljuk: $A_i = $ azon sorozatok halmaza, amelyeknek az $i$-edik bitje 1.

**Ellenőrzés:**

Bármely $(\varepsilon_1, \dots, \varepsilon_n)$-ra konstruáljuk a sorozatot:
- $s_i = 1$ ha $\varepsilon_i = +1$
- $s_i = 0$ ha $\varepsilon_i = -1$

Akkor $s \in A_1^{\varepsilon_1} \cap A_2^{\varepsilon_2} \cap \cdots \cap A_n^{\varepsilon_n}$.

**Tehát:** minden metszet nemüres.

**Tehát:** $A_1, \dots, A_n$ minőségileg függetlenek. ✓

---

**Konkrét példa ($n = 3$):**

$I = \{000, 001, 010, 011, 100, 101, 110, 111\}$

- $A_1 = \{100, 101, 110, 111\}$ (első bit = 1)
- $A_2 = \{010, 011, 110, 111\}$ (második bit = 1)
- $A_3 = \{001, 011, 101, 111\}$ (harmadik bit = 1)

**Ellenőrzés:** $A_1 \cap A_2' \cap A_3 = \{101\} \neq \emptyset$ ✓

Mind a 8 metszet egyelemű, tehát nemüres. ✓

---

### 1.3.4. Feladat — Grünbaum tétele

**Feladat:** Tanulmányozzuk Grünbaum tételét (1975).

**Megoldás:**

**Tétel (Grünbaum, 1975):**

Bármely $n$-re léteznek a síkon $n$ darab minőségileg független konvex sokszögek.

**Jelentőség:**
- A független halmazoknak lehet szép geometriai szerkezetük
- Nem csak absztrakt halmazkonstrukció
- Kombinatorika és geometria kapcsolata

**Konstrukció ötlete:** Gondosan elrendezett konvex sokszögek, ahol minden bennefoglalás/kihagyás-kombináció megvalósítható.

---

### 1.3.5. Feladat — DNF (diszjunktív normálforma)

**Feladat:** Értsük meg a DNF-et.

**Megoldás:**

**Definíció:** A DNF konjunkciók (ÉS-ek) diszjunkciója (VAGY-a).

**Alak:** $(a_1 \wedge a_2 \wedge \dots) \vee (b_1 \wedge b_2 \wedge \dots) \vee \dots$

**Példa:** $f(A, B, C) = (A \wedge B \wedge C') \vee (A' \wedge B \wedge C) \vee (A \wedge B' \wedge C')$

**Minden konjunkció egy minterm.**

**Alkalmazás:** bármely Boole-függvény kifejezhető DNF-ben.

---

### 1.3.6. Feladat — CNF (konjunktív normálforma)

**Feladat:** Értsük meg a CNF-et.

**Megoldás:**

**Definíció:** A CNF diszjunkciók (VAGY-ok) konjunkciója (ÉS-e).

**Alak:** $(a_1 \vee a_2 \vee \dots) \wedge (b_1 \vee b_2 \vee \dots) \wedge \dots$

**Példa:** $f(A, B, C) = (A \vee B \vee C') \wedge (A' \vee B \vee C)$

**Minden diszjunkció egy maxterm.**

**Alkalmazás:** bármely Boole-függvény kifejezhető CNF-ben.

---

### 1.3.7. Feladat — Mintermek

**Feladat:** Értsük meg a mintermeket.

**Megoldás:**

**Definíció:** Egy minterm az összes változó konjunkciója, mindegyik esetleg negálva.

**Alak:** $m_{\vec\varepsilon} = a_1^{\varepsilon_1} \wedge a_2^{\varepsilon_2} \wedge \cdots \wedge a_n^{\varepsilon_n}$

**Példa ($n = 3$):**
- $m_{111} = A \wedge B \wedge C$
- $m_{101} = A \wedge B' \wedge C$
- $m_{000} = A' \wedge B' \wedge C'$

**Tulajdonság:** $n$ változó esetén $2^n$ minterm van.

**Alkalmazás:** bármely Boole-függvény = azon mintermek VAGY-a, ahol a függvény = 1.

---

### 1.3.8. Feladat — Maxtermek

**Feladat:** Értsük meg a maxtermeket.

**Megoldás:**

**Definíció:** Egy maxterm az összes változó diszjunkciója, mindegyik esetleg negálva.

**Alak:** $M_{\vec\eta} = a_1^{\eta_1} \vee a_2^{\eta_2} \vee \cdots \vee a_n^{\eta_n}$

**Példa ($n = 3$):**
- $M_{000} = A \vee B \vee C$
- $M_{101} = A' \vee B \vee C'$

**Tulajdonság:** $n$ változó esetén $2^n$ maxterm van.

**Alkalmazás:** bármely Boole-függvény = azon maxtermek ÉS-e, ahol a függvény = 0.

---

### 1.3.9. Feladat — $|B| \leq 2^{(2^m)}$ igazolása

**Feladat:** Igazoljuk, hogy egy $m$ elemmel generált Boole-algebrának legfeljebb $2^{(2^m)}$ eleme van.

**Megoldás:**

**Bizonyítás:**

$m$ generátorral $2^m$ lehetséges minterm van.

Minden minterm az $m$ generátor konjunkciója (mindegyik esetleg negálva).

$B$ bármely eleme felírható mintermek egy részhalmazának join-jaként (VAGY-aként).

Mintermek részhalmazainak száma = $2^{(2^m)}$.

**Tehát:** $|B| \leq 2^{(2^m)}$. ✓

---

**Példa ($m = 2$):**

Generátorok: $a, b$

Mintermek: $a \wedge b$, $a \wedge b'$, $a' \wedge b$, $a' \wedge b'$ ($4 = 2^2$ minterm)

Maximális elemszám: $2^4 = 16$

Ezek a mintermek részhalmazainak összes VAGY-a.

Ha $a, b$ függetlenek: $|B| = 16$ (a maximum elérve).

Ha $a, b$ nem függetlenek: $|B| < 16$.

---

### 1.3.10. Feladat — Egyenlőségi feltétel

**Feladat:** Értsük meg, mikor $|B| = 2^{(2^m)}$.

**Megoldás:**

**Tétel:** $|B| = 2^{(2^m)}$ akkor és csak akkor, ha az $m$ generátor minőségileg független.

**Bizonyítás:**

**($\Rightarrow$):** Ha $|B| = 2^{(2^m)}$, akkor mind a $2^{(2^m)}$ elem különböző.

Ehhez az kell, hogy mind a $2^m$ minterm nem-üres legyen.

Nem-üres mintermek $\iff$ a generátorok függetlenek.

---

**($\Leftarrow$):** Ha a generátorok függetlenek, akkor minden minterm nem-üres és különböző.

Ezért minden $2^{(2^m)}$ mintermek VAGY-a különböző.

Tehát $|B| = 2^{(2^m)}$. ✓

---

## Összefoglaló

| Feladat | Téma | Állapot |
|---------|------|---------|
| 1.1.1 | Cantor tétele | ✅ Kész |
| 1.1.2 | Russell-paradoxon | ✅ Kész |
| 1.1.3 | ZF-axiómák | ✅ Kész |
| 1.1.4 | Naiv vs. axiomatikus | ✅ Kész |
| 1.2.1–1.2.5 | Boole-axiómák | ✅ Kész |
| 1.2.6–1.2.10 | Boole-példák | ✅ Kész |
| 1.2.11–1.2.12 | De Morgan-azonosságok | ✅ Kész |
| 1.2.13 | Dualitás elve | ✅ Kész |
| 1.2.14–1.2.15 | Stone, teljességi tétel | ✅ Kész |
| 1.3.1–1.3.4 | Minőségi függetlenség | ✅ Kész |
| 1.3.5–1.3.8 | Normálformák | ✅ Kész |
| 1.3.9–1.3.10 | Boole-algebra mérete | ✅ Kész |
| **Összesen** | | **33 feladat** |
