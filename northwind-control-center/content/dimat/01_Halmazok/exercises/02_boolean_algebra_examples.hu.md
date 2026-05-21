# 1.7. Feladat — Boole-algebra-példák igazolása

## A feladat

Igazoljuk, hogy az 1.7. szakaszban szereplő mindegyik példa valóban Boole-algebra (izomorf egy halmazalgebrával).

---

## 1.7(a) Halmazalgebra ✓

**Definíció:**
- $H = \mathcal{P}(I)$ ($I$ hatványhalmaza)
- $\vee = \cup$ (unió)
- $\wedge = \cap$ (metszet)
- $\neg = $ komplemens ($'$)
- $⊤ = I$ (alaphalmaz)
- $⊥ = \emptyset$ (üres halmaz)

**Ellenőrzés:** Ez a **kanonikus Boole-algebra** — az (BA1)–(BA14) axiómák a halmazműveletek definíciójából triviálisan következnek.

---

## 1.7(b) Hatványhalmaz rész-Boole-algebrája ✓

**Definíció:**
- $X \subseteq \mathcal{P}(I)$ zárt a halmazműveletekre
- $I \in X$, $\emptyset \in X$
- $A, B \in X \Rightarrow A \cup B, A \cap B, A' \in X$

**Ellenőrzés:** Mivel $X$ örökli $\mathcal{P}(I)$ műveleteit és zárt rájuk, az axiómák automatikusan teljesülnek.

---

## 1.7(c) Kétértékű logika ✓

**Definíció:**
- $H = \{h, i\} = \{\text{hamis}, \text{igaz}\} = \{0, 1\}$
- $\vee = $ "vagy" (OR)
- $\wedge = $ "és" (AND)
- $\neg = $ "nem" (NOT)
- $⊤ = i$ (igaz/1)
- $⊥ = h$ (hamis/0)

### Igazságtáblázatos ellenőrzés

**Kommutativitás (BA1):**
| a | b | a∨b | b∨a | a∧b | b∧a |
|---|---|-----|-----|-----|-----|
| 0 | 0 |  0  |  0  |  0  |  0  |
| 0 | 1 |  1  |  1  |  0  |  0  |
| 1 | 0 |  1  |  1  |  0  |  0  |
| 1 | 1 |  1  |  1  |  1  |  1  |

**Asszociativitás (BA2):** $(a \vee b) \vee c = a \vee (b \vee c)$ ✓ (mind a 8 esetre ellenőrizhető)

**Disztributivitás (BA3):**
```
a ∨ (b ∧ c) = (a ∨ b) ∧ (a ∨ c)  ✓
a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c)  ✓
```

**Elnyelési tulajdonság (BA4):**
```
a ∨ (a ∧ b) = a  ✓
a ∧ (a ∨ b) = a  ✓
```

**Idempotencia (BA5):**
```
a ∨ a = a  ✓
a ∧ a = a  ✓
```

**Komplemens (BA6):**
| a | ¬a | a∨¬a | a∧¬a |
|---|----|------|------|
| 0 |  1 |  1=⊤ |  0=⊥ |
| 1 |  0 |  1=⊤ |  0=⊥ |

**Egységelemek (BA9–BA10):**
```
a ∨ ⊥ = a ∨ 0 = a  ✓
a ∧ ⊤ = a ∧ 1 = a  ✓
a ∨ ⊤ = a ∨ 1 = 1 = ⊤  ✓
a ∧ ⊥ = a ∧ 0 = 0 = ⊥  ✓
```

**Izomorfia a halmazalgebrával:**
```
h (0) ↔ ∅
i (1) ↔ {x}  (egyelemű halmaz)
```

---

## 1.7(d) Háromérték logika (kvázi-BA) ⚠️

**Definíció:**
- $H = \{h, k, i\} = \{0, \tfrac{1}{2}, 1\}$
- $a \vee b = \max(a, b)$
- $a \wedge b = \min(a, b)$
- $\neg a = 1 - a$

**Ellenőrzés:**

✅ **Kommutativitás, asszociativitás:** A min/max tulajdonságaiból következnek.

✅ **Disztributivitás:**
```
max(a, min(b,c)) = min(max(a,b), max(a,c))  ✓
min(a, max(b,c)) = max(min(a,b), min(a,c))  ✓
```

✅ **Idempotencia:**
```
max(a,a) = a  ✓
min(a,a) = a  ✓
```

❌ **Komplemens NEM teljesül:**
```
a ∨ ¬a = max(a, 1-a) ≠ 1  (a = ½ esetén)
max(½, 1-½) = max(½, ½) = ½ ≠ 1  ❌

a ∧ ¬a = min(a, 1-a) ≠ 0  (a = ½ esetén)
min(½, 1-½) = min(½, ½) = ½ ≠ 0  ❌
```

**Konklúzió:** Ez csak **kvázi-Boole-algebra** (nem valódi BA).

---

## 1.7(e) Számelméleti BA (osztók) ✓

**Definíció:**
- $N$ = négyzetmentes szám (pl. $N = 30 = 2 \cdot 3 \cdot 5$)
- $H = \{N \text{ osztói}\}$
- $a \vee b = \operatorname{lnko}(a, b)$ (legnagyobb közös osztó)
- $a \wedge b = \operatorname{lkkt}(a, b)$ (legkisebb közös többszörös)
- $\neg a = N/a$
- $⊤ = N$
- $⊥ = 1$

### Példa: $N = 30$

$H = \{1, 2, 3, 5, 6, 10, 15, 30\}$

**Ellenőrzés:**

✅ **Kommutativitás:**
```
lnko(a,b) = lnko(b,a)  ✓
lkkt(a,b) = lkkt(b,a)  ✓
```

✅ **Asszociativitás:**
```
lnko(a, lnko(b,c)) = lnko(lnko(a,b), c)  ✓
lkkt(a, lkkt(b,c)) = lkkt(lkkt(a,b), c)  ✓
```

✅ **Disztributivitás:**
```
lnko(a, lkkt(b,c)) = lkkt(lnko(a,b), lnko(a,c))  ✓
lkkt(a, lnko(b,c)) = lnko(lkkt(a,b), lkkt(a,c))  ✓
```

✅ **Elnyelési tulajdonság:**
```
lnko(a, lkkt(a,b)) = a  ✓  (mert a | lkkt(a,b))
lkkt(a, lnko(a,b)) = a  ✓  (mert lnko(a,b) | a)
```

✅ **Idempotencia:**
```
lnko(a,a) = a  ✓
lkkt(a,a) = a  ✓
```

✅ **Komplemens:**
```
a ∨ ¬a = lnko(a, N/a) = 1 = ⊥  ✓  (mert N négyzetmentes)
a ∧ ¬a = lkkt(a, N/a) = N = ⊤  ✓  (mert lnko(a, N/a) = 1)
```

✅ **Egységelemek:**
```
lnko(a, 1) = a   ❓  Vigyázat: lnko ↔ ⊥ így ⊥-szel egyesítve → a (de itt ⊥=1, és lnko(a,1)=1, ami ⊥, nem a) — a halmaz-megfeleltetésben lnko a ∩ szerepét tölti be, lkkt a ∪-ét; lásd a halmaz-izomorfiát alább.
```

Pontosabban a megfeleltetés: $\vee = $ lnko felelne meg $\cap$-nak, de itt a definícióban $\vee = $ **lnko**. Helyes interpretáció: $\vee$ a halmazok metszete, $\wedge$ az uniója, így $⊥ = N$ (mindent fed) és $⊤ = 1$ (üres halmaz). A halmaz-izomorfia ezt teszi világossá:

**Izomorfia a halmazalgebrával:**

$N = p_1 \cdot p_2 \cdots p_n$ (négyzetmentes) esetén minden osztó egy prím-részhalmaznak felel meg:
```
d ↔ {pᵢ : pᵢ | d}

N=30=2·3·5 esetén:
  1  ↔ ∅
  2  ↔ {2}
  3  ↔ {3}
  5  ↔ {5}
  6  ↔ {2,3}
  10 ↔ {2,5}
  15 ↔ {3,5}
  30 ↔ {2,3,5}

lnko ↔ ∩
lkkt ↔ ∪
N/a  ↔ komplemens
```

---

## 1.7(f) Eseményalgebra (valószínűségszámítás) ✓

**Definíció:**
- $\Omega = $ eseménytér
- $H = \mathcal{P}(\Omega)$ (összes esemény)
- $A \vee B = A \cup B$ (események összege)
- $A \wedge B = A \cap B$ (események szorzata)
- $\neg A = A'$ (ellentett esemény)
- $⊤ = \Omega$ (biztos esemény)
- $⊥ = \emptyset$ (lehetetlen esemény)

**Ellenőrzés:** Pontosan ugyanaz, mint 1.7(a) — *ez egy halmazalgebra!*

---

## 1.7(g) Kapcsoló-/csapalgebra ✓

**Definíció:**
- $H = \{0, 1\}$ (zárt/nyitott, ki/be)
- Soros kapcsolás: $a \wedge b = a \cdot b$ (AND)
- Párhuzamos kapcsolás: $a \vee b = a + b - ab$ (OR, vagy egyszerűen max)
- $\neg a = 1 - a$ (inverz kapcsoló)

**Ellenőrzés:** Pontosan ugyanaz, mint 1.7(c) — *izomorf a kétértékű logikával!*

**Fizikai értelmezés:**
```
Soros:        Áram folyik ⟺ MINDKÉT kapcsoló zárt (AND)
Párhuzamos:   Áram folyik ⟺ LEGALÁBB EGY kapcsoló zárt (OR)
Inverz:       Normál nyitott ↔ Normál zárt (NOT)
```

---

## 1.7(h) Színkeverés (kvázi-BA) ⚠️

**Definíció:**
- $H = \{$ lehetséges színek $\}$
- $\vee = $ additív keverés (fény)
- $\wedge = $ szubtraktív keverés (festék)
- $\neg a = $ kiegészítő szín
- $⊤ = $ fehér
- $⊥ = $ fekete

**Megjegyzés:** Ez egy **analóg** struktúra, de szigorúan nem Boole-algebra a következők miatt:
- Folytonos színtér (végtelen sok elem)
- A kiegészítő színek nem elégítik ki pontosan a BA-axiómákat
- A keverés nem tökéletesen asszociatív/disztributív

---

## Összefoglaló táblázat

| Példa | Boole-algebra? | Izomorf vele |
|-------|---------------|--------------|
| (a) Halmazalgebra | ✅ Igen | $\mathcal{P}(I)$ |
| (b) Rész-algebra | ✅ Igen | $\mathcal{P}(I)$ rész-halmaza |
| (c) Kétértékű logika | ✅ Igen | $\mathcal{P}(\{x\}) \cong \{\emptyset, \{x\}\}$ |
| (d) Háromérték logika | ⚠️ Kvázi-BA | — |
| (e) Számelméleti (osztók) | ✅ Igen | $\mathcal{P}(\{N \text{ prímjei}\})$ |
| (f) Eseményalgebra | ✅ Igen | $\mathcal{P}(\Omega)$ |
| (g) Kapcsolóalgebra | ✅ Igen | $\mathcal{P}(\{x\}) \cong \{0, 1\}$ |
| (h) Színkeverés | ⚠️ Analóg | — |

---

## Kulcs-felismerés (Stone-tétel)

A **Stone-féle reprezentációs tétel (1.11)** szerint minden Boole-algebra *izomorf* egy halmazalgebrával. Ez a feladat azt demonstrálja, hogy első ránézésre nagyon különbözőnek tűnő struktúrák (logika, számok, kapcsolók, események) <em>matematikailag ugyanaz az objektum</em>!
