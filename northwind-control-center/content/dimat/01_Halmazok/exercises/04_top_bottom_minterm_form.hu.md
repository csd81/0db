# Feladat — ⊤ és ⊥ kifejezése minterm/maxterm-alakban

## A feladat

Az 1.3. szakaszban, az 1.17. Állítás után:
> "No jó, még ⊤-t és ⊥-t is elő kell állítanunk (1.2) alakú kifejezésként, de ez már semmiség az előző házifeladatokhoz képest..."

**Feladat:** Írjuk fel a $⊤$ (egységelem) és $⊥$ (nullelem) elemeket diszjunktív normálformában (DNF) mintermek segítségével.

---

## Háttér

### Minterm-definíció (1.4)

Az $\{a_1, \dots, a_m\}$ generátorok esetén egy **minterm**:

$$m_{\vec\varepsilon} = a_1^{\varepsilon_1} \wedge a_2^{\varepsilon_2} \wedge \cdots \wedge a_m^{\varepsilon_m}$$

ahol $\vec\varepsilon = (\varepsilon_1, \dots, \varepsilon_m) \in \{+1, -1\}^m$ és:
- $a^{+1} = a$
- $a^{-1} = \neg a$

### DNF-képlet (1.2)

Bármely $x \in B$ elem felírható:

$$x = \bigvee_{\vec\varepsilon \in S_x} m_{\vec\varepsilon}$$

ahol $S_x \subseteq \{+1, -1\}^m$ az indexek egy részhalmaza.

---

## Megoldás: ⊥ (nullelem)

### Állítás:
$$⊥ = \bigvee_{\vec\varepsilon \in \emptyset} m_{\vec\varepsilon}$$

Azaz **⊥ az üres diszjunkció** ($S_⊥ = \emptyset$).

### Ellenőrzés:

A Boole-algebrában az üres diszjunkció definíció szerint $⊥$ (ahogy az aritmetikában az üres összeg = 0).

**Bizonyítás:** bármely $x \in B$-re:
```
x ∨ ⊥ = x  (egységelem-tulajdonság)
```

Ha $⊥ = \bigvee_{\vec\varepsilon \in \emptyset} m_{\vec\varepsilon}$, akkor bármely $D$ DNF-kifejezésre:
```
D ∨ (⋁_{∅} m_ε) = D ∨ ⊥ = D
```

Ez összhangban áll a DNF-reprezentációval. ✓

### Alternatív szemlélet:

Mivel a mintermek **páronként diszjunktak**:
```
m_ε ∧ m_δ = ⊥  ha ε ≠ δ
```

Az üres "join" (egyetlen minterm sincs kiválasztva) természetesen $⊥$-t ad.

---

## Megoldás: ⊤ (egységelem)

### Állítás:
$$⊤ = \bigvee_{\vec\varepsilon \in \{+1, -1\}^m} m_{\vec\varepsilon}$$

Azaz **⊤ az ÖSSZES $2^m$ minterm diszjunkciója** ($S_⊤ = \{+1, -1\}^m$).

### Bizonyítás:

**1. lépés:** A mintermek partícionálják az algebrát.

Bármely $x \in B$ elemre minden $a_i$ generátorra pontosan az egyik teljesül:
- $x \leq a_i$ ($x$ "benne van" $a_i$-ben)
- $x \leq \neg a_i$ ($x$ "benne van" a komplemensben)

Ezért minden nem-nulla elem pontosan egy minterm-mel ad nem-nulla meet-et.

**2. lépés:** Minden minterm join-ja $⊤$.

Legyen $T = \bigvee_{\vec\varepsilon} m_{\vec\varepsilon}$.

Be kell látnunk, hogy $T = ⊤$, vagyis $\neg T = ⊥$.

$$\begin{aligned}
\neg T &= \neg\!\left(\bigvee_{\vec\varepsilon} m_{\vec\varepsilon}\right) \\
       &= \bigwedge_{\vec\varepsilon} \neg m_{\vec\varepsilon} \qquad \text{(De Morgan)} \\
       &= \bigwedge_{\vec\varepsilon} \neg(a_1^{\varepsilon_1} \wedge \cdots \wedge a_m^{\varepsilon_m}) \\
       &= \bigwedge_{\vec\varepsilon} (\neg a_1^{\varepsilon_1} \vee \cdots \vee \neg a_m^{\varepsilon_m}) \\
       &= \bigwedge_{\vec\varepsilon} (a_1^{-\varepsilon_1} \vee \cdots \vee a_m^{-\varepsilon_m})
\end{aligned}$$

Minden $\vec\varepsilon$-ra az $(a_1^{-\varepsilon_1} \vee \cdots \vee a_m^{-\varepsilon_m})$ tag legalább egy literálú.

Az ÖSSZES $\vec\varepsilon$-ra vett konjunkció azt jelenti, hogy minden lehetséges literál-kombináció előfordul, és a konjunkciójuk $⊥$.

Tehát: $\neg T = ⊥$, ami azt jelenti, hogy $T = ⊤$. ✓

---

## Konkrét példák

### Példa 1: $m = 1$ (egy generátor)

Generátorok: $\{a\}$

Mintermek:
```
m_(+1) = a
m_(-1) = ¬a
```

**⊥ DNF-ben:**
```
⊥ = ⋁_{∅} m_ε  (üres diszjunkció)
```

**⊤ DNF-ben:**
```
⊤ = m_(+1) ∨ m_(-1) = a ∨ ¬a  ✓  (kizárt harmadik elve)
```

### Példa 2: $m = 2$ (két generátor)

Generátorok: $\{a, b\}$

Mintermek:
```
m_(+,+) = a ∧ b
m_(+,-) = a ∧ ¬b
m_(-,+) = ¬a ∧ b
m_(-,-) = ¬a ∧ ¬b
```

**⊥ DNF-ben:**
```
⊥ = (üres diszjunkció)
```

**⊤ DNF-ben:**
```
⊤ = (a ∧ b) ∨ (a ∧ ¬b) ∨ (¬a ∧ b) ∨ (¬a ∧ ¬b)
```

**Ellenőrzés:**
```
(a ∧ b) ∨ (a ∧ ¬b) = a ∧ (b ∨ ¬b) = a ∧ ⊤ = a
(¬a ∧ b) ∨ (¬a ∧ ¬b) = ¬a ∧ (b ∨ ¬b) = ¬a ∧ ⊤ = ¬a

Tehát: a ∨ ¬a = ⊤  ✓
```

### Példa 3: $m = 3$ (három generátor)

Generátorok: $\{a, b, c\}$

**⊤ DNF-ben:**
```
⊤ = (a∧b∧c) ∨ (a∧b∧¬c) ∨ (a∧¬b∧c) ∨ (a∧¬b∧¬c)
  ∨ (¬a∧b∧c) ∨ (¬a∧b∧¬c) ∨ (¬a∧¬b∧c) ∨ (¬a∧¬b∧¬c)
```

Mind a $2^3 = 8$ minterm diszjunkciója.

---

## CNF-reprezentáció (konjunktív normálforma)

Dualitásból $⊤$ és $⊥$ CNF-ben is felírható **maxtermek** segítségével.

### Maxterm-definíció:
$$M_{\vec\eta} = a_1^{\eta_1} \vee a_2^{\eta_2} \vee \cdots \vee a_m^{\eta_m}$$

### ⊤ CNF-ben:
$$⊤ = \bigwedge_{\vec\eta \in \emptyset} M_{\vec\eta} \quad (\text{üres konjunkció})$$

### ⊥ CNF-ben:
$$⊥ = \bigwedge_{\vec\eta \in \{+1, -1\}^m} M_{\vec\eta}$$

**Példa ($m = 2$):**
```
⊥ = (a ∨ b) ∧ (a ∨ ¬b) ∧ (¬a ∨ b) ∧ (¬a ∨ ¬b)
```

**Ellenőrzés:**
```
(a ∨ b) ∧ (a ∨ ¬b) = a ∨ (b ∧ ¬b) = a ∨ ⊥ = a
(¬a ∨ b) ∧ (¬a ∨ ¬b) = ¬a ∨ (b ∧ ¬b) = ¬a ∨ ⊥ = ¬a

Tehát: a ∧ ¬a = ⊥  ✓
```

---

## Összefoglaló táblázat

| Elem | DNF (mintermekkel) | CNF (maxtermekkel) |
|------|-------------------|-------------------|
| **⊥** (nullelem) | $\bigvee_{\vec\varepsilon \in \emptyset} m_{\vec\varepsilon}$ (üres) | $\bigwedge_{\text{all } \vec\eta} M_{\vec\eta}$ |
| **⊤** (egységelem) | $\bigvee_{\text{all } \vec\varepsilon} m_{\vec\varepsilon}$ | $\bigwedge_{\vec\eta \in \emptyset} M_{\vec\eta}$ (üres) |

### Tagok száma

| Elem | DNF-tagok | CNF-tagok |
|------|-----------|-----------|
| $⊥$ | 0 | $2^m$ |
| $⊤$ | $2^m$ | 0 |

---

## Kulcs-felismerések

1. **Üres műveletek:**
   - Üres diszjunkció ($\vee$) = $⊥$ (mint üres összeg = 0)
   - Üres konjunkció ($\wedge$) = $⊤$ (mint üres szorzat = 1)

2. **Partíció-tulajdonság:** A mintermek $⊤$ partícióját alkotják:
   - Páronként diszjunktak: $m_{\vec\varepsilon} \wedge m_{\vec\delta} = ⊥$ ha $\vec\varepsilon \neq \vec\delta$
   - Az összes minterm join-ja: $\bigvee_{\text{all}} m_{\vec\varepsilon} = ⊤$

3. **Egyértelműség:** Minden elemnek **egyértelmű** DNF-reprezentációja van (sorrendtől eltekintve), ha a generátorok minőségileg függetlenek.

4. **Dualitás:** $⊤$ DNF ↔ $⊥$ CNF (és fordítva) a dualitás elve szerint.

---

## Alkalmazás: 1.20. Következmény

Ez a feladat befejezi az 1.20. Következmény bizonyítását:

> Ha $\mathcal{B}$-t $m$ elem generálja, akkor $|B| \leq 2^{(2^m)}$.

**Indoklás:** Minden elem $\bigvee_{\vec\varepsilon \in S} m_{\vec\varepsilon}$ alakú DNF, ahol $S \subseteq \{+1, -1\}^m$.

- $2^m$ lehetséges minterm van
- $2^{(2^m)}$ lehetséges $S$ részhalmaz van
- Tehát legfeljebb $2^{(2^m)}$ különböző elem létezik

A korlátot akkor érjük el, ha a generátorok minőségileg függetlenek. ✓

---

## Hivatkozások

- 1.3. § — DNF/CNF definíciói
- 1.19. Definíció — Normálformák
- 1.17. Állítás — Generált algebrák szerkezete
- 1.20. Következmény — Méretkorlátok
