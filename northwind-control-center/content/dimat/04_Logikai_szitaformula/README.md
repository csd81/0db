# 4. fejezet - A logikai szitaformula (Inclusion-Exclusion Principle)

## Tartalomjegyzék

- [4.1 A formula](#41-a-formula)
- [4.2 Elcserélt levelek (Derangements)](#42-elcserélt-levelek)
- [4.3 Additív halmazfüggvények](#43-additív-halmazfüggvények)
- [4.4 Feladatok](#44-feladatok)

---

## 4.1 A formula

### Alapgondolat

Amikor halmazok unióját számoljuk, az átfedéseket (metszeteket) figyelembe kell venni:
- Többször számolt elemeket ki kell vonni
- Túl sokszor kivontakat vissza kell adni
- Ez a **"szitálás"** folyamata

### Két halmaz esete (4.1)

$$|A \cup B| = |A| + |B| - |A \cap B|$$

### Logikai szitaformula - Általános alak (4.2)

$$\left|\bigcup_{i=1}^{m} A_i\right| = \sum_{i=1}^{m} |A_i| - \sum_{1 \leq i < j \leq m} |A_i \cap A_j| + \sum_{1 \leq i < j < k \leq m} |A_i \cap A_j \cap A_k| - \cdots + (-1)^{m+1} \left|\bigcap_{i=1}^{m} A_i\right|$$

### Második változat (4.3) - Komplementer számítás

Ha $N = I \setminus \bigcup_{i=1}^{m} A_i$ (egyik tulajdonsággal sem rendelkezők):

$$|N| = |I| - \sum_{i=1}^{m} |A_i| + \sum_{i<j} |A_i \cap A_j| - \sum_{i<j<k} |A_i \cap A_j \cap A_k| + \cdots + (-1)^m \left|\bigcap_{i=1}^{m} A_i\right|$$

### Bizonyítás ötlete

Minden $x$ elemet pontosan **egyszer** számolunk meg:
- Ha $x$ pontosan $r$ halmazban van
- Jobb oldalon: $\binom{r}{1} - \binom{r}{2} + \binom{r}{3} - \cdots + (-1)^{r+1}\binom{r}{r} = 1$

---

## 4.2 Elcserélt levelek (Derangements)

### A probléma (4.5)

**Kérdés:** $n$ levelet hányféleképpen tehetünk $n$ címezett borítékba úgy, hogy **együk se kapja meg a saját levelét**?

### Megoldás (4.6)

Legyen:
- $I = S_n$ (összes permutáció, $|I| = n!$)
- $A_i$ = azok a permutációk, ahol az $i$-edik elem fixpont
- $N$ = fixpont nélküli permutációk (derangements)

**Szitaformula alkalmazása:**

$$D_n = n! - \binom{n}{1}(n-1)! + \binom{n}{2}(n-2)! - \binom{n}{3}(n-3)! + \cdots + (-1)^n\binom{n}{n}0!$$

$$\boxed{D_n = n! \sum_{k=0}^{n} \frac{(-1)^k}{k!}}$$

### Derangement értékek

| n | Dₙ |
|---|-----|
| 1 | 0 |
| 2 | 1 |
| 3 | 2 |
| 4 | 9 |
| 5 | 44 |
| 6 | 265 |
| 7 | 1,854 |
| 8 | 14,833 |
| 9 | 133,496 |
| 10 | 1,334,961 |

### Fontos tulajdonságok

#### 4.9 Állítás - Aszimptotikus viselkedés

$$\lim_{n \to \infty} \frac{D_n}{n!} = \frac{1}{e} \approx 0.367$$

$$D_n = \left\lfloor \frac{n!}{e} + \frac{1}{2} \right\rfloor$$

#### 4.10 Állítás - Rekurzív formula

$$D_n = n D_{n-1} + (-1)^n$$

vagy ekvivalensen:

$$D_n = (n-1)(D_{n-1} + D_{n-2})$$

### Általánosítás (Joó István tétele)

Ha $n$ ember mindegyike $m$-féle tárgyat ad le, és senki sem kaphat ` több azonos típusút:

$$\lim_{n \to \infty} P(n, m, \ell) = e^{-m}$$

---

## 4.3 Additív halmazfüggvények

### Definíciók

#### Halmazalgebra (4.13)

$\mathcal{A} \subseteq \mathcal{P}(X)$ halmazalgebra, ha zárt a halmazműveletekre:
- $A, B \in \mathcal{A} \Rightarrow A \cup B, \overline{A} \in \mathcal{A}$

#### σ-algebra

Ha megszámlálható unióra is zárt.

#### Additív halmazfüggvény / Mérték (4.14)

$\mu: \mathcal{A} \to \mathbb{R}^+$ additív, ha diszjunkt $A, B$-re:

$$\mu(A \cup B) = \mu(A) + \mu(B)$$

### Példák mértékekre (4.15)

| Mérték | Jelölés | Példa |
|--------|---------|-------|
| (a) Számosság | $|A|$ | Véges halmazok elemszáma |
| (b) Terület | $T(A)$ | Síkidomok területe |
| (c) Térfogat | $V(A)$ | Testek térfogata |
| (d) Súly | $m(A)$ | Homogén lemezek súlya |
| (e) Valószínűség | $P(A)$ | Események valószínűsége |
| (f) Integrál | $\int_A f$ | Pozitív függvény integrálja |
| (g) Sűrűség | $d(A)$ | Számelméleti sűrűség |

### Tulajdonságok (4.16)

1. **$\mu(\emptyset) = 0$**
2. **Véges additivitás:** $\mu(A_1 \cup \cdots \cup A_m) = \sum \mu(A_i)$ (diszjunktakra)
3. **Monotonitás:** $A \subseteq B \Rightarrow \mu(A) \leq \mu(B)$
4. **Inklúzió-exklúzió:** $\mu(A \cup B) = \mu(A) + \mu(B) - \mu(A \cap B)$

### Szitaformula általános mértékekre

**4.18 Tétel:**

$$\mu\left(\bigcup_{i=1}^{m} A_i\right) = \sum_{i} \mu(A_i) - \sum_{i<j} \mu(A_i \cap A_j) + \sum_{i<j<k} \mu(A_i \cap A_j \cap A_k) - \cdots$$

**4.19 Tétel (komplementer):**

$$\mu(N) = \mu(I) - \sum_{i} \mu(A_i) + \sum_{i<j} \mu(A_i \cap A_j) - \cdots + (-1)^m \mu\left(\bigcap_{i=1}^{m} A_i\right)$$

---

## 4.4 Feladatok

### 4.1 - Három nyelv
67 hallgató, 47 angol, 35 német, 23 mindkettő, 20 francia, 12 angol+francia, 11 német+francia, 5 mindhárom.
**Megoldás:** 6 hallgató nem beszél egyet sem.

### 4.2 - Pontos egy fixpont
5 levél, pontosan 1 kapja meg sajátját.
**Megoldás:** $5 \cdot D_4 = 45$

### 4.3 - Legalább egy tárgy
$r$ tárgyat szétosztani $n+p$ ember között, első $n$ ember legalább 1-et kap.
**Megoldás:** $\sum_{i=0}^{n} (-1)^i \binom{n}{i} (n+p-i)^r$

### 4.4 - Derangement rekurzió
Bizonyítsuk: $D_n = n D_{n-1} + (-1)^n$

### 4.5 - Szürjektív függvények
$|B| = m \to |A| = n$ szürjekciók száma:
$$S(m,n) = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n-i)^m$$

### 4.6 - Játékok osztása
6 játékot 4 gyereknek, mindenki legalább egyet.
**Megoldás:** $S(6,4) = 1560$

### 4.8 - Relatív prímek
$M$-nél nem nagyobb, $n$-hez relatív prím számok száma.
**Euler φ-függvény:** $\phi(n) = n \prod_{p|n} \left(1 - \frac{1}{p}\right)$

### 4.9 - Alternáló binomiális összeg
$$\sum_{i=0}^{n} (-1)^{n-i} \binom{n}{i} i^k = \begin{cases} 0 & \text{ha } k < n \\ n! & \text{ha } k = n \end{cases}$$

---

## Képletek összefoglalója

### Derangement
$$D_n = n! \sum_{k=0}^{n} \frac{(-1)^k}{k!} \approx \frac{n!}{e}$$

### Szitaformula (általános)
$$\left|\bigcup_{i=1}^{m} A_i\right| = \sum_{\emptyset \neq J \subseteq [m]} (-1)^{|J|-1} \left|\bigcap_{j \in J} A_j\right|$$

### Szürjekciók száma
$$S(m,n) = \sum_{i=0}^{n} (-1)^i \binom{n}{i} (n-i)^m$$

### Euler φ-függvény
$$\phi(n) = n \prod_{p|n} \left(1 - \frac{1}{p}\right)$$

---

## Hivatkozások

- [BP] Balogh József, Pete Gábor: Egy ötlet: A szita formula
- [HHM] Harris-Hirst-Mossinghoff: Combinatorics and Graph Theory
- [J] Joó István: Egy elemi kombinatorikai probléma
- [L] Lovász László: Combinatorial Problems and Exercises

---

*Forrás: Dr. Szalkai István - Diszkrét Matematika*
