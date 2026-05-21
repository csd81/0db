# 01. fejezet — Halmazok — Feladat-ellenőrzőlista

## 📋 Teljes feladatlista

Ezzel az ellenőrzőlistával követheted a 01. fejezet feladatainak előrehaladását.

---

## 🔵 Fejezeten belüli feladatok (HF = Házi Feladat)

### 1.1. § — Halmazok definíciója

- [x] **HF** — Értsd meg Cantor tételét: nincs univerzális halmaz
- [x] **HF** — Tanulmányozd a Russell-paradoxon indirekt bizonyítását
- [x] **HF** — Ismételd át a Zermelo-Fraenkel-axiómákat
- [x] **Tanulmány** — Naiv és axiomatikus halmazelmélet különbsége

---

### 1.2. § — Boole-algebrák

#### Alaptulajdonságok (BA1–BA14)

- [x] **HF** — Igazold a kommutativitást: $A \cup B = B \cup A$, $A \cap B = B \cap A$
- [x] **HF** — Igazold az asszociativitást: $A \cup (B \cup C) = (A \cup B) \cup C$
- [x] **HF** — Igazold a disztributivitást: $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$
- [x] **HF** — Igazold az elnyelést: $A \cup (A \cap B) = A$
- [x] **HF** — Igazold a komplemenst: $A \cup A' = I$, $A \cap A' = \emptyset$

---

#### Boole-algebra-példák

- [x] **HF** — Igazold a halmazalgebrát (hatványhalmaz $\cup, \cap, '$-vel)
- [x] **HF** — Igazold a logika-algebrát ($\{\text{hamis}, \text{igaz}\}$ VAGY, ÉS, NEM-mel)
- [x] **HF** — Igazold a számelméleti algebrát (osztók lnko, lkkt-vel)
- [x] **HF** — Igazold az eseményalgebrát (valószínűségszámítás)
- [x] **HF** — Igazold a kapcsolóalgebrát (áramkör-elmélet)

---

#### Fontos tételek

- [x] **HF** — Bizonyítsd a De Morgan-azonosságokat:
  - $\neg(a \vee b) = \neg a \wedge \neg b$
  - $\neg(a \wedge b) = \neg a \vee \neg b$

- [x] **HF** — Alkalmazd a dualitás elvét (1.9):
  - Cseréld fel $\vee \leftrightarrow \wedge$ és $⊤ \leftrightarrow ⊥$ az igaz állításokban

- [x] **Tanulmány** — Stone-tétel (1.11, 1936):
  - Minden Boole-algebra izomorf egy halmazalgebrával

- [x] **Tanulmány** — Teljességi tétel (1.12):
  - Minden formula vagy minden Boole-algebrában igaz, vagy mindegyikben hamis

---

### 1.3. § — Halmazok minőségi függetlensége

#### Definíció és tulajdonságok

- [x] **HF** — Értsd meg a minőségi függetlenség (1.13) definícióját:
  - $A_1^{\varepsilon_1} \cap \cdots \cap A_n^{\varepsilon_n} \neq \emptyset$ minden $\varepsilon_1, \dots, \varepsilon_n \in \{+1, -1\}$ esetén

- [x] **HF** — Igazold az 1.14(i) Állítást:
  - Ha $n$ halmaz független, akkor $|I| \geq 2^n$

- [x] **HF** — Igazold az 1.14(ii) Állítást:
  - Létezik $2^n$-elemű alaphalmaz $n$ független részhalmazzal

- [x] **Tanulmány** — Grünbaum-tétel (1.15, 1975):
  - Bármely $n$-re léteznek minőségileg független konvex sokszögek a síkon

---

#### Normálformák

- [x] **HF** — Értsd meg a DNF-et (diszjunktív normálforma):
  - Konjunkciók diszjunkciója

- [x] **HF** — Értsd meg a CNF-et (konjunktív normálforma):
  - Diszjunkciók konjunkciója

- [x] **HF** — Értsd meg a mintermeket:
  - $m_{\vec\varepsilon} = a_1^{\varepsilon_1} \wedge \cdots \wedge a_m^{\varepsilon_m}$

- [x] **HF** — Értsd meg a maxtermeket:
  - $M_{\vec\eta} = a_1^{\eta_1} \vee \cdots \vee a_m^{\eta_m}$

---

#### 1.20. Következmény

- [x] **HF** — Igazold: ha $\mathcal{B}$-t $m$ elem generálja:
  - $|B| \leq 2^{(2^m)}$

- [x] **HF** — Értsd meg az egyenlőségi feltételt:
  - Egyenlőség pontosan akkor, ha a generátorok minőségileg függetlenek

---

## 🔴 Formális feladatok (1.4. § — Feladatok)

### 1.1. Feladat — Halmazműveletek
- [x] Igazold az alapvető halmaz-azonosságokat
- [x] Bizonyítsd elem-módszerrel

### 1.2. Feladat — Boole-algebra-tulajdonságok
- [x] Igazold a BA-axiómákat konkrét példákra
- [x] Bizonyíts tulajdonságokat az axiómákból

### 1.3. Feladat — De Morgan-azonosságok
- [x] Bizonyítsd halmazokra
- [x] Bizonyítsd logikára

### 1.4. Feladat — Dualitás elve
- [x] Alkalmazd adott formulákra
- [x] Igazold a duális állításokat

### 1.5. Feladat — Minőségi függetlenség
- [x] Konstruálj független családokat
- [x] Igazold a függetlenségi feltételt

### 1.6. Feladat — Mintermek és maxtermek
- [x] Fejezz ki függvényeket DNF-ben
- [x] Fejezz ki függvényeket CNF-ben

### 1.7. Feladat — Boole-algebra mérete
- [x] Számítsd ki a maximum méretet $m$ generátorra
- [x] Igazold a $2^{(2^m)}$ korlátot

### 1.8. Feladat — Alkalmazások
- [x] Alkalmazd logikai áramkörökre
- [x] Alkalmazd valószínűségszámításra

---

## 📚 Hivatkozott külső feladatok

### Szalkai [SzIs;97] feladatgyűjteményéből
- [ ] Halmazelméleti fejezet
- [ ] Boole-algebra-feladatok

### Hajnal–Hamburger [HH]-ból
- [ ] Halmazelméleti feladatok
- [ ] Boole-algebra-problémák

### Halmos [HS]-ből
- [ ] Elemi halmazelméleti problémák

---

## 📊 Előrehaladás-követő

| Kategória | Összes | Teljesítve | Százalék |
|-----------|--------|------------|----------|
| Fejezeten belüli HF | 25 | 25 | 100% |
| Formális feladatok 1.1–1.8 | 8 | 8 | 100% |
| Külső feladatok | 0 | 0 | 0% |
| **ÖSSZESEN** | **33** | **33** | **100%** |

---

## 🎯 Tanulási tippek

1. **Kezdd:** Alapvető halmazműveletekkel és Venn-diagramokkal
2. **Sajátítsd el:** A Boole-algebra-axiómákat (BA1–BA14)
3. **Értsd meg:** A dualitás elvét — cseréld fel a műveleteket
4. **Gyakorold:** A De Morgan-azonosságokat különböző kontextusokban
5. **Kulcs-technika:** Elem-módszer halmaz-bizonyításokhoz

---

## ⏱️ Becsült idő

| Feladat | Idő |
|---------|-----|
| Fejezet elolvasása | 2–3 óra |
| Fejezeten belüli HF | 3–4 óra |
| Formális feladatok 1.1–1.8 | 3–4 óra |
| Külső feladatok | 2–3 óra |
| **Összesen** | **10–14 óra** |

---

## 📝 Memorizálandó kulcsfontosságú képletek

```
□ De Morgan: (A ∪ B)' = A' ∩ B', (A ∩ B)' = A' ∪ B'
□ Dualitás: cseréld ∪↔∩, ∅↔I
□ Függetlenség: |I| ≥ 2ⁿ n független halmazra
□ Boole-méret: |B| ≤ 2^(2^m) m generátorra
□ DNF: ÉS-ek VAGY-a
□ CNF: VAGY-ok ÉS-e
```

---

## Boole-algebra-példák összefoglalója

| Példa | Elemek | Műveletek | Egységelem | Nullelem |
|-------|--------|-----------|------------|----------|
| Halmazalgebra | $\mathcal{P}(S)$ | $\cup, \cap, '$ | $S$ | $\emptyset$ |
| Logika | $\{H, I\}$ | $\vee, \wedge, \neg$ | $I$ | $H$ |
| Osztók | $D(n)$ | lnko, lkkt | $n$ | $1$ |
| Események | Események | $\cup, \cap$, komplemens | $\Omega$ | $\emptyset$ |

---

*A 01. fejezetből generálva: Halmazok*
*Forrás: Dr. Szalkai István — Diszkrét matematika*
