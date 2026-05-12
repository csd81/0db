# 8. fejezet - Partíciós problémák (Partition Problems)

## Tartalomjegyzék

- [8.1 Számok felbontása](#81-számok-felbontása)
- [8.2 Halmazpartíciók](#82-halmazpartíciók)
- [8.3 Összefoglalás](#83-összefoglalás)

---

## 8.1 Számok felbontása

### Definíció (8.1)

Egy $n \in \mathbb{N}$ szám **k-részre való partíciója**:
$$n = a_1 + a_2 + \cdots + a_k$$
ahol $a_1 \geq a_2 \geq \cdots \geq a_k \geq 1$ természetes számok.

**Jelölések:**
- $P(n, k)$ = $n$ szám $k$ részre való felosztásainak száma
- $P(n) = \sum_{k=1}^n P(n, k)$ = összes felosztás száma

### Fontos tulajdonságok

**8.2 Állítás (Korlátok):**
$$\frac{1}{n} \binom{n-1}{k-1} \leq P(n, k) \leq \frac{1}{k!} \binom{n-1}{k-1}$$

**8.3 Tétel (Rekurzió):**
$$P(n+k, k) = \sum_{i=1}^k P(n, i)$$

$$P(n, 1) = P(n, n) = 1$$

**8.4 Tétel (Dualitás):**
Az $n$ szám olyan felosztásainak száma, ahol a legnagyobb tag $m$, egyenlő $P(n, m)$-mel.

---

### Generátorfüggvény (8.5 Tétel)

**Euler eredménye (1740):**
$$\sum_{n=0}^{\infty} P(n) x^n = \prod_{i=1}^{\infty} \frac{1}{1 - x^i}$$

---

### Hardy-Ramanujan formula (8.6 Tétel)

**Aszimptotikus formula:**
$$P(n) \sim \frac{1}{4n\sqrt{3}} \exp\left(\pi \sqrt{\frac{2n}{3}}\right) \quad \text{ha } n \to \infty$$

---

### Partíciós számok táblázata

| n | P(n) | n | P(n) | n | P(n) |
|---|------|---|------|---|------|
| 0 | 1 | 10 | 42 | 20 | 627 |
| 1 | 1 | 11 | 56 | 21 | 792 |
| 2 | 2 | 12 | 77 | 22 | 1002 |
| 3 | 3 | 13 | 101 | 23 | 1255 |
| 4 | 5 | 14 | 135 | 24 | 1575 |
| 5 | 7 | 15 | 176 | 25 | 1958 |
| 6 | 11 | 16 | 231 | 26 | 2436 |
| 7 | 15 | 17 | 297 | 27 | 3010 |
| 8 | 22 | 18 | 385 | 28 | 3718 |
| 9 | 30 | 19 | 490 | 29 | 4565 |
| - | - | - | - | 30 | 5604 |

---

## 8.2 Halmazpartíciók

### Definíció (8.7)

Egy $H \neq \emptyset$ halmaz **k-adosztályú partíciója**: nemüres részhalmazok diszjunkt rendszere $\{A_1, \ldots, A_k\}$ ahol:
- $A_i \neq \emptyset$
- $A_i \cap A_j = \emptyset$ ($i \neq j$)
- $\bigcup_{i=1}^k A_i = H$

---

### Négy eset

| Eset | H elemei | Partíció elemei | Jelölés |
|------|----------|-----------------|---------|
| **a)** | Megkülönböztethetetlenek | Megkülönböztethetőek | $\binom{n+k-1}{k-1}$ |
| **b)** | Megkülönböztethetetlenek | Nem különböztetjük meg | $V(n,k)$ |
| **c)** | Megkülönböztethetőek | Megkülönböztethetőek | $S(n,k)$ |
| **d)** | Megkülönböztethetőek | Nem különböztetjük meg | $S_n^k$ (Stirling) |

---

### a) eset: Pénzváltási probléma

$$C_k^{(n, \text{ism})} = \binom{n+k-1}{k-1}$$

Ismétléses kombináció.

---

### c) eset: Szürjektív függvények

$$S(n, k) = \sum_{i=0}^k (-1)^i \binom{k}{i} (k-i)^n \quad \text{ha } n \geq k$$

Ez a szürjekciók száma (4. fejezet, logikai szitaformula).

---

### d) eset: Stirling és Bell számok

**Másodfajú Stirling számok:** $S_n^k$ = $n$ elemű halmaz $k$ nemüres, nem-számozott részre való partícióinak száma.

**Bell számok:** $B_n = \sum_{k=1}^n S_n^k$ = összes partíció száma.

---

### Stirling számok tulajdonságai (8.9 Állítás)

**(i) Rekurzió:**
$$S_n^{k+1} = S_{n-1}^k + k \cdot S_n^k$$

**(ii) Explicit formula:**
$$S_n^k = \frac{1}{k!} \sum_{i=0}^k (-1)^i \binom{k}{i} (k-i)^n$$

**(iii) Összegzési identitás:**
$$\sum_{k=1}^n (-1)^{k-1} (k-1)! S_n^k = 0$$

**(iv) Alternáló összeg:**
$$\sum_{k=1}^n (-1)^{k-1} k! S_n^k = (-1)^{n-1}$$

**(v) Polinom identitás:**
$$\sum_{i=1}^n S_n^i (x-1)(x-2)\cdots(x-i+1) = x^n$$

**(vi) Generátorfüggvény:**
$$\sum_{n=k}^{\infty} S_n^k \frac{x^n}{n!} = \frac{(e^x - 1)^k}{k!}$$

**(vii) Exponenciális generátorfüggvény:**
$$\sum_{n=k}^{\infty} S_n^k \frac{x^n}{n!} = \frac{(e^x - 1)^k}{k!}$$

---

### Bell számok tulajdonságai (8.10 Állítás)

**Rekurzió:**
$$B_{n+1} = \sum_{k=0}^n \binom{n}{k} B_k, \quad B_0 = 1$$

**Bell polinomok (8.11 Tétel):**
$$B_n = p_n(1)$$
ahol $p_1(x) = 1$ és $p_{k+1} = (x+1)p_k + x p_k'(x)$

**Exponenciális generátorfüggvény:**
$$\sum_{n=0}^{\infty} B_n \frac{x^n}{n!} = e^{e^x - 1}$$

---

### Bell számok táblázata

| n | Bₙ |
|---|-----|
| 0 | 1 |
| 1 | 1 |
| 2 | 2 |
| 3 | 5 |
| 4 | 15 |
| 5 | 52 |
| 6 | 203 |
| 7 | 877 |
| 8 | 4140 |
| 9 | 21147 |
| 10 | 115975 |

---

## 8.3 Összefoglalás

### Partíciós problémák típusai

| # | Leírás | Formula |
|---|--------|---------|
| 1 | $n$ elem $k$ számozott részbe (üres engedett) | $k^n$ |
| 2 | $n$ elem $k$ számozott részbe (üres nem) | $S(n,k) = \sum (-1)^i \binom{k}{i}(k-i)^n$ |
| 3 | $n$ elem $k$ nem-számozott részbe (üres nem) | $S_n^k = S(n,k)/k!$ |
| 4 | $n$ azonos tárgy $k$ nemüres számozott részbe | $\binom{n-1}{k-1}$ |
| 5 | $n$ azonos tárgy $k$ számozott részbe (üres is) | $\binom{n+k-1}{k-1}$ |
| 6 | $n$ azonos tárgy $k$ részbe, min. $q$ elemű | $\binom{n-k(q-1)-1}{k-1}$ |
| 7 | $n$ azonos tárgy $k$ nem-számozott részbe | $p_k(n)$ |
| 8 | $n$ elem $k$ rendezett részbe (üres is) | $k(k+1)\cdots(k+n-1)$ |
| 9 | $n$ elem $k$ nem-számozott rendezett részbe | $n! \binom{n-1}{k-1} / k!$ |

---

## Képletek összefoglalója

### Partíciók száma

| Típus | Formula |
|-------|---------|
| Szám partíciók | $P(n) \sim \frac{1}{4n\sqrt{3}} e^{\pi\sqrt{2n/3}}$ |
| Stirling (másodfajú) | $S_n^k = \frac{1}{k!}\sum_{i=0}^k (-1)^i \binom{k}{i}(k-i)^n$ |
| Bell számok | $B_{n+1} = \sum_{k=0}^n \binom{n}{k} B_k$ |

### Generátorfüggvények

| Sorozat | Generátorfüggvény |
|---------|-------------------|
| $P(n)$ | $\prod_{i=1}^{\infty} \frac{1}{1-x^i}$ |
| $S_n^k$ | $\frac{(e^x-1)^k}{k!}$ |
| $B_n$ | $e^{e^x-1}$ |

---

## Hivatkozások

- [HaPé] Hajnal Péter: Diszkrét matematika
- [ViN] Vilenkin: Kombinatorika
- [ToIo] Tomescu: Problems in Combinatorics
- [HHM] Harris-Hirst-Mossinghoff: Combinatorics and Graph Theory
- [P Sz] Pólya-Szegő: Válogatott feladatok az analízisből

---

*Forrás: Dr. Szalkai István - Diszkrét Matematika*
