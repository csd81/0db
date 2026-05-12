# 2. fejezet - Elemi leszámlálások (Elementary Counting)

## Tartalomjegyzék

- [2.1 Általános módszerek](#21-általános-módszerek)
- [2.2 Teljes indukció](#22-teljes-indukció)
- [2.3 Permutációk, variációk, kombinációk](#23-permutációk-variációk-kombinációk)
- [Stirling-formula](#stirling-formula)

---

## 2.1 Általános módszerek

### A kombinatorika alapelvei (2.1)

Három fő szabály:
1. **Mindent** összeszámoltunk?
2. **Semmit** sem számoltunk kétszer?
3. **Csak a halmaz elemeit** számoltuk meg?

> "A kombinatorika az összeszámlálás művészete"

### I. Módszer - Összeszámlálás két alapmódszere (2.2)

| Eset | Módszer | Képlet |
|------|---------|--------|
| **a) Diszjunkt halmazok** | Összeadás | n₁ + n₂ + ... + nₖ |
| **b) Független összetevők** | Szorzás | n₁ × n₂ × ... × nₖ |

**Példa (a):** Buszjegy lyukasztás 3×3 mezőben, legfeljebb 3 lyuk:
- 1 lyuk: $\binom{9}{1} = 9$
- 2 lyuk: $\binom{9}{2} = 36$
- 3 lyuk: $\binom{9}{3} = 84$
- **Összesen:** 9 + 36 + 84 = **129**

**Példa (b):** Francia kártya (52 lap), 5 lap osztása, pontosan 1 pár:
- 13 figura × $\binom{4}{2}$ színek × $\binom{12}{3}$ maradék × $4^3$ színek
- **Összesen:** 13 × 6 × 220 × 64 = **1,098,240**

### II. Módszer - Bijekciók (2.4)

A keresett halmaz és egy könnyebben számolható halmaz között kölcsönösen egyértelmű megfeleltetést keresünk.

**Példa (2.5):** Hány részhalmaza van egy n-elemű halmaznak?

**Megoldás:** 
- Minden részhalmaz kódolható n-jegyű bináris számmal
- 0 = nincs benne, 1 = benne van
- Összesen: **2ⁿ** részhalmaz

**Feladat (2.6):** Hány függvény van A → B?
- Ha |A| = n, |B| = m: **mⁿ** függvény

---

## 2.2 Teljes indukció

### A módszer (2.7)

**1. Kezdőlépés:** Ellenőrizzük Φ(n₀) értékét

**2. Indukciós lépés:** Bizonyítsuk be:
```
Ha Φ(n) igaz, akkor Φ(n+1) is igaz
```

### Indukció Tétele (2.8)

Ha:
1. Φ(n₀) igaz (kezdőlépés)
2. ∀n ≥ n₀: Φ(n) ⇒ Φ(n+1) (indukciós lépés)

Akkor: ∀n ≥ n₀: Φ(n) igaz

### Történeti megjegyzések

| Matematikus | Hozzájárulás |
|-------------|--------------|
| Francesco Maurolico (1494-1575) | Első használata (n² összeg) |
| Blaise Pascal (1623-1662) | Első pontos leírás |
| Giuseppe Peano (1858-1932) | Axiómarendszer |
| Gottlob Frege (1848-1925) | Helyesség igazolása |
| Gerhard Gentzen (1909-1945) | Ellentmondásmentesség |

### Példa: Háromszög-egyenlőtlenség (2.9)

**Állítás:** ∀z₁,...,zₙ ∈ ℂ:
```
|z₁ + ... + zₙ| ≤ |z₁| + ... + |zₙ|
```

**Bizonyítás:**
- n₀ = 1: triviális
- n = 2: háromszög-egyenlőtlenség
- Indukció: n+1 esetre bizonyítva

---

## 2.3 Permutációk, variációk, kombinációk

### Faktoriális (2.10)

```
n! = 1 × 2 × ... × n
0! = 1
(n+1)! = (n+1) × n!
```

---

### 2.3.1 Permutációk

**Definíció (2.12):** n elem sorbarendezéseinek száma

| Típus | Jelölés | Képlet |
|-------|---------|--------|
| **Ismétlés nélküli** | Pₙ | **n!** |
| **Ismétléses** | Pₙ^(k₁,...,kₛ) | **n! / (k₁! × ... × kₛ!)** |

ahol k₁ + ... + kₛ = n (elemek típusai)

**Példa ismétlésesre:** "MISSISSIPPI" betűi:
- 11 betű: M=1, I=4, S=4, P=2
- P = 11! / (1! × 4! × 4! × 2!) = **34,650**

### Polinomiális együttható (2.14)

```
(n choose k₁,...,kₛ) = n! / (k₁! × ... × kₛ!)
```

---

### 2.3.2 Variációk és Kombinációk

#### Kulcsfontosságú különbség!

| | **Variáció** | **Kombináció** |
|---|--------------|----------------|
| **Sorrend** | LÉNYEGES | LÉNYEGTELEN |
| **Jelölés** | Vₙᵏ | Cₙᵏ vagy (n choose k) |

#### Összefoglaló táblázat

| Típus | Sorrend? | Visszatevés? | Képlet |
|-------|----------|--------------|--------|
| **Variáció (ism. nélküli)** | Igen | Nincs | Vₙᵏ = n!/(n-k)! |
| **Variáció (ismétléses)** | Igen | Van | Vₙᵏ^(ism) = nᵏ |
| **Kombináció (ism. nélküli)** | Nem | Nincs | Cₙᵏ = (n choose k) = n!/(k!(n-k)!) |
| **Kombináció (ismétléses)** | Nem | Van | Cₙᵏ^(ism) = (n+k-1 choose k) |

#### Részletes képletek

**1. Variáció (ismétlés nélküli) - 2.18**
```
Vₙᵏ = n × (n-1) × ... × (n-k+1) = n!/(n-k)!
```
*Példa:* 10 versenyző, első 3 hely: V₁₀³ = 10×9×8 = **720**

**2. Variáció (ismétléses) - 2.19**
```
Vₙᵏ^(ism) = nᵏ
```
*Példa:* 6-os lottó, 3 szám sorrenddel: 6³ = **216**

**3. Kombináció (ismétlés nélküli) - 2.20**
```
Cₙᵏ = (n choose k) = n! / (k! × (n-k)!)
```
*Példa:* 10 versenyzőből 3 kiválasztása (sorrend nem számít): C₁₀³ = **120**

**4. Kombináció (ismétléses) - 2.21**
```
Cₙᵏ^(ism) = (n+k-1 choose k)
```
*Példa:* 6 fagylaltból 3 gombóc (ismétlődhet): C₆³^(ism) = (8 choose 3) = **56**

---

### Összefüggések

**Variáció és kombináció kapcsolata:**
```
Vₙᵏ = Cₙᵏ × k!
```
(Mert minden kiválasztott k-elemű halmazt k!-féleképpen sorba rendezhetünk)

**Binomiális együttható szimmetria:**
```
(n choose k) = (n choose n-k)
```

**Rekurzív összefüggés (Pascal):**
```
(n choose k) = (n-1 choose k-1) + (n-1 choose k)
```

---

## Stirling-formula

### Stirling-formula (n! becslése)

Nagy n értékekre:
```
n! ≈ √(2πn) × (n/e)ⁿ
```

Pontosabb alak:
```
√(2πn) × (n/e)ⁿ < n! < √(2πn) × (n/e)ⁿ × e^(1/(12n))
```

### Alkalmazások

- Nagy faktoriálisok becslése
- Permutációk számának közelítése
- Valószínűségszámítás

**Példa:** 100! ≈ 9.33 × 10¹⁵⁷

---

## Gyakorló feladatok

### 1. Alapelvek
- Hány 3-jegyű szám képezhető 1,2,3,4,5 számjegyekből?
- Hányféleképpen ülhet 5 ember egy padon?

### 2. Indukció
- Bizonyítsuk: 1 + 2 + ... + n = n(n+1)/2
- Bizonyítsuk: 1² + 2² + ... + n² = n(n+1)(2n+1)/6

### 3. Permutációk
- Hányféleképpen állítható sorba ABCDE?
- Hányféleképpen a MAMA szó betűi?

### 4. Variációk
- Hány 4-jegyű rendszám készíthető 10 számjegyből?
- Hányféleképpen választható ki 10 emberből 3 különböző díj?

### 5. Kombinációk
- Hányféleképpen húzható 5 lap 52-ből?
- Hányféleképpen osztható ki 3 egyforma díj 10 ember között?

---

## Hivatkozások

- [HHM] Harris-Hirst-Mossinghoff: Combinatorics and Graph Theory
- [P] Pólya: On the number of certain lattice polygons
- [PR] Pólya-Read: Combinatorial Methods in the Theory of Chemical Enumeration

---

*Forrás: Dr. Szalkai István - Diszkrét Matematika*
