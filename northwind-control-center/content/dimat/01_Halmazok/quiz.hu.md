# 01. fejezet — Halmazok — Feleletválasztós kvíz

## Útmutató
Válaszd ki **a legjobb** választ minden kérdéshez.

---

## Kérdések

### 1. Cantor tétele azt állítja, hogy:

A) Minden halmaznak van komplemense
B) Nincs olyan halmaz, amely a „világ" minden elemét tartalmazná
C) Minden Boole-algebra véges
D) A hatványhalmaz mindig nagyobb az eredeti halmaznál

<details>
<summary><strong>Megoldás</strong></summary>

**B) Nincs olyan halmaz, amely a „világ" minden elemét tartalmazná**

Cantor tétele indirekt bizonyítással (Russell-paradoxonon át) megmutatja, hogy nem létezhet univerzális halmaz.
</details>

---

### 2. Az alábbiak közül melyik NEM Boole-algebra-axióma?

A) $a \vee (a \wedge b) = a$
B) $a \vee a = a$
C) $a + (b + c) = (a + b) + c$
D) $a \vee \neg a = ⊤$

<details>
<summary><strong>Megoldás</strong></summary>

**C) $a + (b + c) = (a + b) + c$**

Ez aritmetikai (+) jelölést használ a Boole-algebra ($\vee$) helyett. A helyes axióma: $a \vee (b \vee c) = (a \vee b) \vee c$.
</details>

---

### 3. Boole-algebrában a $(a \vee b) \wedge ⊤ = a \vee b$ azonosság duálisa:

A) $(a \wedge b) \vee ⊥ = a \wedge b$
B) $(a \wedge b) \vee ⊤ = a \wedge b$
C) $(a \vee b) \wedge ⊥ = a \vee b$
D) $(a \wedge b) \vee a = a$

<details>
<summary><strong>Megoldás</strong></summary>

**A) $(a \wedge b) \vee ⊥ = a \wedge b$**

A dualitás elve szerint: $\vee \leftrightarrow \wedge$ és $⊤ \leftrightarrow ⊥$.
</details>

---

### 4. Hány eleme van egy 3 minőségileg független elemmel generált Boole-algebrának?

A) 8
B) 16
C) 256
D) 6

<details>
<summary><strong>Megoldás</strong></summary>

**C) 256**

Az 1.20. Következmény szerint $|B| = 2^{(2^m)} = 2^{(2^3)} = 2^8 = 256$, ha a generátorok függetlenek.
</details>

---

### 5. Az alábbiak közül melyik **valódi** Boole-algebra?

A) $(\mathbb{R}, +, \times)$ — valós számok az összeadással és szorzással
B) $(\{0, \tfrac{1}{2}, 1\}, \max, \min, 1-x)$ — háromérték logika
C) $(\{30 \text{ osztói}\}, \text{lnko}, \text{lkkt}, 30/x)$ — számelmélet
D) $(\mathbb{N}, +, \times)$ — természetes számok az összeadással és szorzással

<details>
<summary><strong>Megoldás</strong></summary>

**C) $(\{30 \text{ osztói}\}, \text{lnko}, \text{lkkt}, 30/x)$**

Ez Boole-algebrát alkot, izomorf $\mathcal{P}(\{2, 3, 5\})$-tel. A B csak kvázi-BA.
</details>

---

### 6. $A_1, A_2, \dots, A_n$ halmazok minőségileg függetlenek, ha:

A) Páronként diszjunktak
B) Uniójuk az alaphalmaz
C) A komplemensekkel képzett összes lehetséges metszet nem üres
D) Mind ugyanakkora a számossága

<details>
<summary><strong>Megoldás</strong></summary>

**C) A komplemensekkel képzett összes lehetséges metszet nem üres**

Formálisan: $A_1^{\varepsilon_1} \cap \cdots \cap A_n^{\varepsilon_n} \neq \emptyset$ minden $\vec\varepsilon \in \{+1, -1\}^n$ esetén.
</details>

---

### 7. $n$ minőségileg független halmazt tartalmazó alaphalmaz minimális mérete:

A) $n$
B) $2n$
C) $2^n$
D) $n^2$

<details>
<summary><strong>Megoldás</strong></summary>

**C) $2^n$**

Az 1.14(i) Állítás szerint: $|I| \geq 2^n$ az $n$ minőségileg független halmazra.
</details>

---

### 8. A De Morgan-azonosság a Boole-algebrában:

A) $\neg(a \vee b) = \neg a \vee \neg b$
B) $\neg(a \wedge b) = \neg a \wedge \neg b$
C) $\neg(a \vee b) = \neg a \wedge \neg b$
D) $a \vee (b \wedge c) = (a \vee b) \wedge (a \vee c)$

<details>
<summary><strong>Megoldás</strong></summary>

**C) $\neg(a \vee b) = \neg a \wedge \neg b$**

A másik De Morgan-azonosság: $\neg(a \wedge b) = \neg a \vee \neg b$. A D pedig a disztributivitás.
</details>

---

### 9. A kétértékű $\{0, 1\}$ Boole-algebrában mennyi $1 \vee (1 \wedge 0)$?

A) 0
B) 1
C) nem értelmezett
D) $\tfrac{1}{2}$

<details>
<summary><strong>Megoldás</strong></summary>

**B) 1**

Az elnyelési törvény szerint: $a \vee (a \wedge b) = a$, tehát $1 \vee (1 \wedge 0) = 1$.

Vagy közvetlenül: $1 \vee (1 \wedge 0) = 1 \vee 0 = 1$.
</details>

---

### 10. A $⊤$ DNF-je 2 generátorral hány mintermből áll?

A) 2
B) 4
C) 8
D) 0

<details>
<summary><strong>Megoldás</strong></summary>

**B) 4**

$m = 2$ generátor esetén $⊤ = \bigvee_{\text{all } \vec\varepsilon} m_{\vec\varepsilon}$ — összesen $2^m = 2^2 = 4$ minterm.
</details>

---

### 11. A Stone-féle reprezentációs tétel azt állítja, hogy:

A) Minden Boole-algebra véges
B) Minden Boole-algebra izomorf egy halmazalgebrával
C) Minden halmazalgebra izomorf egy szám-algebrával
D) Minden Boole-algebrának pontosan $2^n$ eleme van

<details>
<summary><strong>Megoldás</strong></summary>

**B) Minden Boole-algebra izomorf egy halmazalgebrával**

Pontosabban: izomorf egy hatványhalmaz-algebra rész-algebrájával.
</details>

---

### 12. Melyik tulajdonság NEM teljesül $(\mathbb{R}, +, \times)$-ben?

A) Kommutativitás
B) Asszociativitás
C) Disztributivitás
D) Elnyelési törvény ($a + (a \times b) = a$)

<details>
<summary><strong>Megoldás</strong></summary>

**D) Elnyelési törvény ($a + (a \times b) = a$)**

Ellenpélda: $2 + (2 \times 3) = 2 + 6 = 8 \neq 2$.

Pontosan ezért $(\mathbb{R}, +, \times)$ **nem** Boole-algebra.
</details>

---

### 13. $a$ komplemense egy Boole-algebrában az alábbiakat elégíti ki:

A) $a \vee \neg a = ⊥$
B) $a \wedge \neg a = ⊤$
C) $a \vee \neg a = ⊤$ és $a \wedge \neg a = ⊥$
D) $\neg(\neg a) = a$ csak halmazokra

<details>
<summary><strong>Megoldás</strong></summary>

**C) $a \vee \neg a = ⊤$ és $a \wedge \neg a = ⊥$**

Ezek a (BA11) és (BA12) komplemens-axiómák.

Ráadásul $\neg(\neg a) = a$ MINDEN Boole-algebrában teljesül (involúció).
</details>

---

### 14. $N = 30 = 2 \cdot 3 \cdot 5$ esetén mennyi $\neg 6$ az osztó-Boole-algebrában?

A) 5
B) 15
C) 1
D) 30

<details>
<summary><strong>Megoldás</strong></summary>

**A) 5**

Az osztó-BA-ban: $\neg a = N/a = 30/6 = 5$.

Ellenőrzés: $\operatorname{lnko}(6, 5) = 1 = ⊥$ ✓ és $\operatorname{lkkt}(6, 5) = 30 = ⊤$ ✓
</details>

---

### 15. Az üres diszjunkció $\bigvee_{\vec\varepsilon \in \emptyset} m_{\vec\varepsilon}$ értéke:

A) $⊤$
B) $⊥$
C) nem értelmezett
D) az algebrától függ

<details>
<summary><strong>Megoldás</strong></summary>

**B) $⊥$**

Az üres diszjunkció (mint az üres összeg) a $\vee$ egységelemével egyenlő, ami $⊥$.

Hasonlóan az üres konjunkció $⊤$.
</details>

---

### 16. Az alábbiak közül melyik egy minterm az $\{a, b\}$ generátorokra?

A) $a \vee b$
B) $a \wedge b$
C) $\neg a \vee \neg b$
D) $(a \wedge b) \vee (\neg a \wedge \neg b)$

<details>
<summary><strong>Megoldás</strong></summary>

**B) $a \wedge b$**

Egy minterm az összes generátor konjunkciója (mindegyik vagy negálva vagy nem).

Az $\{a, b\}$ esetén a 4 minterm: $a \wedge b$, $a \wedge \neg b$, $\neg a \wedge b$, $\neg a \wedge \neg b$.
</details>

---

### 17. A dualitás elve lehetővé teszi:

A) Két tétel bizonyítását egyetlen bizonyítással
B) DNF ↔ CNF konverziót
C) A komplemensek könnyű megtalálását
D) A fentiek mindegyikét

<details>
<summary><strong>Megoldás</strong></summary>

**D) A fentiek mindegyikét**

A dualitás elve hatékony eszköz, amely duális tételeket automatikusan generál.
</details>

---

### 18. Az eseményalgebrában (valószínűségszámítás) $⊤$ jelentése:

A) Az üres esemény
B) A biztos esemény (eseménytér)
C) Egy lehetetlen esemény
D) Egy komplemens-esemény

<details>
<summary><strong>Megoldás</strong></summary>

**B) A biztos esemény (eseménytér)**

A valószínűségszámításban: $⊤ = \Omega$ (eseménytér), $⊥ = \emptyset$ (lehetetlen esemény).
</details>

---

### 19. Egy 4-elemű alaphalmazban hány minőségileg független halmaz létezhet?

A) 1
B) 2
C) 3
D) 4

<details>
<summary><strong>Megoldás</strong></summary>

**B) 2**

Az 1.14. Állítás szerint $|I| \geq 2^n$, vagyis $4 \geq 2^n$, azaz $n \leq 2$.

Maximum 2 független halmaz lehet.
</details>

---

### 20. A (BA1)–(BA14) Boole-algebra-axiómák:

A) Függetlenek (egyik sem vezethető le a többiből)
B) Teljesek (minden igaz formula bizonyítható)
C) Ellentmondás-mentesek
D) A fentiek mindegyike

<details>
<summary><strong>Megoldás</strong></summary>

**D) A fentiek mindegyike**

A Boole-algebra-axiómarendszer független, teljes (1.12. Tétel) és ellentmondás-mentes.
</details>

---

## Pontszám-értelmezés

| Helyes | Érdemjegy | Értékelés |
|--------|-----------|-----------|
| 18–20 | 5 (Jeles) | Az 1. fejezet teljes elsajátítása! |
| 15–17 | 4 (Jó) | Szilárd ismeretek |
| 11–14 | 3 (Közepes) | Át kell ismételni a kulcsfogalmakat |
| 6–10 | 2 (Elégséges) | A fejezetet újra tanulmányozni |
| 0–5 | 1 (Elégtelen) | Át kell olvasni és többet gyakorolni |

---

## Gyors-hivatkozás

| Téma | Kérdések |
|------|----------|
| Halmazelméleti alapok | 1, 7, 19 |
| Boole-algebra-axiómák | 2, 9, 12, 13, 20 |
| Dualitás | 3, 17 |
| Méret / szerkezet | 4, 10, 15, 16 |
| Példák | 5, 14, 18 |
| Minőségi függetlenség | 6, 7, 19 |
| De Morgan-azonosságok | 8 |
| Stone-tétel | 11 |

---

*A 01. fejezetből generálva: Halmazok*
*Forrás: Dr. Szalkai István — Diszkrét Matematika*
