# 1.3. Feladat — Minőségi függetlenség Boole-algebrákban

## A feladat

Az 1.3. szakasz 1.20. Következményéből:
> "Bár a minőségi függetlenséget csak halmazalgebrák esetén definiáltuk, tetszőleges Boole-algebrában ugyanúgy használhatjuk e fogalmat. (Újabb Házi Feladat, Kedves Olvasó!)"

**Feladat:** Mutassuk meg, hogy a minőségi függetlenség fogalma kiterjeszthető tetszőleges Boole-algebrára (nem csak halmazalgebrákra).

---

## Háttér

### Eredeti definíció (1.13) — halmazalgebrákra

$A_1, \dots, A_n \subseteq I$ **minőségileg függetlenek**, ha minden $\varepsilon_1, \dots, \varepsilon_n \in \{+1, -1\}$ esetén:

$$A_1^{\varepsilon_1} \cap \cdots \cap A_n^{\varepsilon_n} \neq \emptyset$$

ahol $A^{+1} = A$ és $A^{-1} = A'$ (komplemens).

### Általánosított definíció — tetszőleges Boole-algebrára

Legyen $\mathcal{B} = (B, \vee, \wedge, \neg, ⊤, ⊥)$ egy Boole-algebra.

Az $a_1, \dots, a_n \in B$ elemek **minőségileg függetlenek**, ha minden $\varepsilon_1, \dots, \varepsilon_n \in \{+1, -1\}$ esetén:

$$a_1^{\varepsilon_1} \wedge \cdots \wedge a_n^{\varepsilon_n} \neq ⊥$$

ahol:
- $a^{+1} = a$
- $a^{-1} = \neg a$ (komplemens)
- $⊥$ a $B$ nullelem-eleme

---

## Miért működik ez az általánosítás

### 1. Strukturális megfeleltetés

| Halmazalgebra | Általános Boole-algebra |
|---------------|------------------------|
| $\cap$ (metszet) | $\wedge$ (meet/AND) |
| $\emptyset$ (üres halmaz) | $⊥$ (nullelem) |
| $A'$ (komplemens) | $\neg a$ (komplemens) |
| $A_1 \cap \cdots \cap A_n \neq \emptyset$ | $a_1 \wedge \cdots \wedge a_n \neq ⊥$ |

### 2. Stone reprezentációs tétele

A **Stone-tétel (1.11)** szerint minden $\mathcal{B}$ Boole-algebra izomorf egy halmazalgebrával:

$$f: B \to \mathcal{P}(S) \quad (\text{valamilyen } S \text{ halmazra})$$

$$f(a \wedge b) = f(a) \cap f(b),\quad f(\neg a) = f(a)',\quad f(⊥) = \emptyset$$

Ezért $\mathcal{B}$-beli minőségi függetlenség pontosan megfelel $\mathcal{P}(S)$-beli minőségi függetlenségnek.

---

## Példa: Kétértékű logika

$\mathcal{B} = (\{0, 1\}, \vee, \wedge, \neg, 1, 0)$

Találhatunk-e minőségileg független elemeket?

### $n = 1$ esetén:
Kell: $a \neq 0$ és $\neg a \neq 0$

A $\{0, 1\}$-ban:
- Ha $a = 1$: $\neg a = 0$ ❌
- Ha $a = 0$: $a = 0$ ❌

**Eredmény:** A 2-elemű BA-ban nincs minőségileg független elem.

Ez összhangban van az 1.14(i) Állítással: $|B| \geq 2^n$ kell, vagyis $|B| \geq 2^1 = 2$, de a függetlenséghez **szigorúan több** kell.

### $n = 2$ egy 4-elemű BA-ban:

$\mathcal{B} = \mathcal{P}(\{x, y\}) = \{\emptyset, \{x\}, \{y\}, \{x,y\}\}$

Legyen $a_1 = \{x\}$, $a_2 = \{y\}$.

Ellenőrizzük mind a $2^2 = 4$ kombinációt:
```
ε = (+1, +1):  a₁ ∧ a₂ = {x} ∩ {y} = ∅ = ⊥  ❌
```

Ezek **NEM** függetlenek!

### Helyes konstrukció $n = 2$-re:

Legalább $2^n = 4$ elem kell az 1.14(i) szerint — de valójában $2^{(2^n)} = 16$ elem kell **2 független generátorhoz**.

$\mathcal{B} = \mathcal{P}(\{1, 2, 3, 4\})$ — 16 eleme van.

Legyen $a_1 = \{1, 2\}$, $a_2 = \{1, 3\}$.

Ellenőrizzük mind a kombinációkat:
```
(+1, +1): a₁ ∧ a₂ = {1,2} ∩ {1,3} = {1} ≠ ∅  ✓
(+1, -1): a₁ ∧ ¬a₂ = {1,2} ∩ {2,4} = {2} ≠ ∅  ✓
(-1, +1): ¬a₁ ∧ a₂ = {3,4} ∩ {1,3} = {3} ≠ ∅  ✓
(-1, -1): ¬a₁ ∧ ¬a₂ = {3,4} ∩ {2,4} = {4} ≠ ∅  ✓
```

**Sikerült!** $a_1$ és $a_2$ minőségileg függetlenek.

---

## Példa: Számelméleti BA ($N = 30$ osztói)

$\mathcal{B} = \{1, 2, 3, 5, 6, 10, 15, 30\}$ az lnko, lkkt műveletekkel.

- $⊥ = 1$ (nullelem)
- $⊤ = 30$ (egységelem)
- $\neg a = 30 / a$

### Próbáljunk $n = 3$ független elemet:

Az 1.14. Állítás szerint kell $|H| \geq 2^3 = 8$. Pontosan 8 elemünk van! ✓

Legyenek:
- $a_1 = 2$ (a $\{2\}$ prímnek felel meg)
- $a_2 = 3$ (a $\{3\}$ prímnek felel meg)
- $a_3 = 5$ (a $\{5\}$ prímnek felel meg)

Néhány kombináció (lnko-t használva $\wedge$-ként):
```
(+1, +1, +1): lnko(2, 3, 5) = 1 = ⊥  ❌
```

Ezek **NEM** függetlenek!

### A nehézség

A problémát az okozza, hogy a 8-elemű algebrát 3 *atomi* prím generálja — nincs elég "hely" 3 független elemnek. A *valódi* 3-függetlenség kb. $2^{2^3} = 256$ elemet igényelne.

**Kulcsfontosságú:** Az $N = p_1 p_2 \cdots p_n$ négyzetmentes szám osztóinak BA-ja izomorf $\mathcal{P}(\{p_1, \dots, p_n\})$-nal, ami $2^n$ elemű. $n$ független elemhez $2^{(2^n)}$ elemű BA kell!

---

## Az 1.14. Állítás — általánosított bizonyítás

### (i) Alsó korlát: $|B| \geq 2^n$

**Bizonyítás:** Minőségileg független $a_1, \dots, a_n$ esetén mind a $2^n$ kombináció:

$$a_1^{\varepsilon_1} \wedge \cdots \wedge a_n^{\varepsilon_n} \neq ⊥$$

különböző és nem-nulla. Ezek páronként diszjunktak (páronkénti meet-jük $⊥$):

$$(a_1^{\varepsilon_1} \wedge \cdots \wedge a_n^{\varepsilon_n}) \wedge (a_1^{\delta_1} \wedge \cdots \wedge a_n^{\delta_n}) = ⊥$$

ha $\vec\varepsilon \neq \vec\delta$ (mert valamely $i$-re $\varepsilon_i \neq \delta_i$, ami $a_i \wedge \neg a_i = ⊥$-t ad).

Véges Boole-algebrában diszjunkt nem-nulla elemek mind különbözőek, így legalább $2^n$ különböző elem kell. $\square$

### (ii) Létezés: konstrukció tetszőleges $n$-re

**Bizonyítás:** Vegyük $B = \mathcal{P}(\{0, 1\}^n)$-t (az összes $n$-bites sorozat hatványhalmazát).

Definiáljuk: $a_i = \{x \in \{0, 1\}^n : x_i = 1\}$ ($i$-edik bit 1-es a sorozatokban).

Ekkor bármely $\vec\varepsilon \in \{+1, -1\}^n$-re:

$$a_1^{\varepsilon_1} \wedge \cdots \wedge a_n^{\varepsilon_n} = \{\vec\varepsilon\}$$

(egyelemű halmaz), ami nem üres. ✓

A Stone-tétel értelmében ez a konstrukció működik **tetszőleges** $\geq 2^{(2^n)}$ elemű Boole-algebrában. $\square$

---

## Alkalmazás: 1.20. Következmény

**Állítás:** Ha $\mathcal{B}$-t $m$ elem generálja, akkor $|B| \leq 2^{(2^m)}$.

**Egyenlőség** pontosan akkor áll fenn, ha a generátorelemek minőségileg függetlenek.

### Bizonyítás-vázlat

1. **Felső korlát:** Minden elemnek van DNF-je legfeljebb $2^m$ mintermmel, minden minterm az $m$ generátor egy kombinációja. Összesen: $2^{(2^m)}$ lehetséges DNF.

2. **Egyenlőségi feltétel:** Ha a generátorok függetlenek, mind a $2^{(2^m)}$ DNF különböző.

3. **Általánosítás tetszőleges BA-ra:** A Stone-tétel értelmében $B \cong $ valamilyen halmazalgebra, ahol a bizonyítás azonos módon megy.

---

## Összefoglaló

| Fogalom | Halmazalgebra | Általános Boole-algebra |
|---------|---------------|------------------------|
| Függetlenség | $A_1^{\varepsilon_1} \cap \cdots \neq \emptyset$ | $a_1^{\varepsilon_1} \wedge \cdots \neq ⊥$ |
| Üres halmaz | $\emptyset$ | $⊥$ |
| Metszet | $\cap$ | $\wedge$ |
| Komplemens | $A'$ | $\neg a$ |
| Min. méret | $2^n$ | $2^n$ |
| Konstrukció | Bináris reprezentáció | Ugyanaz (Stone-on át) |

**Kulcs-felismerés:** A Stone reprezentációs tétel lehetővé teszi, hogy minden halmazelméleti fogalmat átültessünk tetszőleges Boole-algebrába!

---

## Hivatkozások

- 1.3. § — Minőségi függetlenség definíciója
- 1.11. Tétel — Stone reprezentációs tétele
- 1.14. Állítás — Független halmazok korlátai
- 1.20. Következmény — Végesen generált Boole-algebrák mérete
