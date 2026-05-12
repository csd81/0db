# 5. fejezet - Rekurzív sorozatok (Recursive Sequences)

## Tartalomjegyzék

- [5.0 Alapfogalmak](#50-alapfogalmak)
- [5.1 Iterációs módszer](#51-iterációs-módszer)
- [5.2 Lineáris rekurziók](#52-lineáris-rekurziók)
- [5.3 Klasszikus módszer](#53-klasszikus-módszer)
- [Nevezetes sorozatok](#nevezetes-sorozatok)

---

## 5.0 Alapfogalmak

### Rekurzív összefüggés (5.0)

$$a_n = F(a_{n-1}, a_{n-2}, \ldots, n)$$

**k-adrendű rekurzió:** Ha $a_n$ csak $a_{n-1}, \ldots, a_{n-k}$-tól függ.

**Kezdeti érték probléma:** $a_1 = A_1, \ldots, a_k = A_k$

### Példa: Fibonacci sorozat (5.2)

**Probléma:** Hány nyúlpár lesz az $n$-edik hónapban?

**Rekurzió:**
$$f_n = f_{n-1} + f_{n-2}, \quad n > 2$$
$$f_1 = f_2 = 1$$

**Explicit képlet (Binet-formula):**
$$f_n = \frac{1}{\sqrt{5}}\left[\left(\frac{1+\sqrt{5}}{2}\right)^n - \left(\frac{1-\sqrt{5}}{2}\right)^n\right]$$

---

## 5.1 Iterációs módszer

### Módszer

Helyettesítsük vissza a rekurziót önmagába:
$$\begin{aligned}
a_n &= F(a_{n-1}, a_{n-2}, \ldots, n) \\
&= F(F(a_{n-2}, \ldots), a_{n-2}, \ldots) \\
&= \cdots
\end{aligned}$$

### Példa: Hanoi tornyai (5.3)

**Rekurzió:**
$$h_{n+1} = 2h_n + 1, \quad h_1 = 1$$

**Iteráció:**
$$\begin{aligned}
h_n &= 2h_{n-1} + 1 \\
&= 2(2h_{n-2} + 1) + 1 = 4h_{n-2} + 2 + 1 \\
&= 4(2h_{n-3} + 1) + 2 + 1 = 8h_{n-3} + 4 + 2 + 1 \\
&= \cdots \\
&= 2^{n-1}h_1 + 2^{n-2} + \cdots + 2 + 1 \\
&= 2^{n-1} + (2^{n-1} - 1) \\
&= 2^n - 1
\end{aligned}$$

**Megoldás:** $\boxed{h_n = 2^n - 1}$

**Legend:** 64 korong esetén $2^{64}-1 \approx 586$ milliárd év!

---

## 5.2 Lineáris rekurziók

### Definíció (5.4)

**k-adrendű lineáris rekurzió:**
$$a_n = d_1(n)a_{n-1} + d_2(n)a_{n-2} + \cdots + d_k(n)a_{n-k} + b_n$$

- **Homogén:** $b_n = 0$ minden $n$-re
- **Inhomogén:** $b_n \neq 0$
- **Állandó együtthatós:** $d_i(n) = d_i$ (konstans)

### Algebrai struktúra (5.5-5.7 Tétel)

**Homogén megoldások tere:**
- $k$-dimenziós altér
- Bázis: $k$ lineárisan független megoldás

**Inhomogén általános megoldás:**
$$\text{Inhomogén általános} = \text{Homogén általános} + \text{Partikuláris}$$

$$S^{\text{Inh}} = S^{\text{Hom}} + s^{\text{Part}}_n$$

---

## 5.3 Klasszikus módszer

### Állandó együtthatós homogén rekurziók

**Rekurzió:**
$$a_n = d_1 a_{n-1} + d_2 a_{n-2} + \cdots + d_k a_{n-k}$$

### Karakterisztikus egyenlet

Keressük a megoldást $a_n = cq^n$ alakban:

$$q^k - d_1 q^{k-1} - d_2 q^{k-2} - \cdots - d_k = 0$$

### Megoldás szerkezete

#### 1. Különböző gyökök

Ha $q_1, q_2, \ldots, q_k$ különböző gyökök:

$$a_n = c_1 q_1^n + c_2 q_2^n + \cdots + c_k q_k^n$$

#### 2. Többszörös gyökök

Ha $q_i$ gyök $m_i$ multiplicitással:

$$a_n = (c_{i1} + c_{i2}n + c_{i3}n^2 + \cdots + c_{i,m_i}n^{m_i-1})q_i^n$$

### Példa: Fibonacci (másodrendű)

**Karakterisztikus egyenlet:**
$$q^2 - q - 1 = 0$$

**Gyökök:**
$$q_{1,2} = \frac{1 \pm \sqrt{5}}{2}$$

**Általános megoldás:**
$$f_n = c_1\left(\frac{1+\sqrt{5}}{2}\right)^n + c_2\left(\frac{1-\sqrt{5}}{2}\right)^n$$

**Kezdeti értékekből:** $c_1 = \frac{1}{\sqrt{5}}, c_2 = -\frac{1}{\sqrt{5}}$

---

## Nevezetes sorozatok

### Fibonacci sorozat

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|----|
| $f_n$ | 1 | 1 | 2 | 3 | 5 | 8 | 13 | 21 | 34 | 55 |

**Tulajdonságok:**
- $f_{n+1}/f_n \to \phi = \frac{1+\sqrt{5}}{2}$ (aranymetszés)
- $\sum_{i=1}^n f_i = f_{n+2} - 1$
- $f_n^2 + f_{n+1}^2 = f_{2n+1}$

### Hanoi sorozat

$$h_n = 2^n - 1$$

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $h_n$ | 1 | 3 | 7 | 15 | 31 | 63 | 127 | 255 |

### Faktoriális

$$n! = n \cdot (n-1)!$$

### Mértani sorozat

$$a_n = a_1 \cdot r^{n-1}$$

### Számtani sorozat

$$a_n = a_1 + (n-1)d$$

---

## Vandermonde determináns

### 5.9 Állítás

$$\det\begin{pmatrix}
1 & q_1 & q_1^2 & \cdots & q_1^{t-1} \\
1 & q_2 & q_2^2 & \cdots & q_2^{t-1} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & q_t & q_t^2 & \cdots & q_t^{t-1}
\end{pmatrix} = \prod_{1 \leq i < j \leq t}(q_j - q_i)$$

### Következmény (5.10)

Ha $q_1, \ldots, q_t$ különbözők, akkor a $(q_i^n)$ sorozatok lineárisan függetlenek.

---

## Összefoglaló táblázat

| Rekurzió típusa | Megoldás módszere |
|-----------------|-------------------|
| Elsőrendű lineáris | Iteráció vagy képlet |
| Állandó együtthatós | Karakterisztikus egyenlet |
| Inhomogén | Homogén + partikuláris |
| Változó együtthatós | Generátorfüggvény (köv. fejezet) |

---

## Képletek összefoglalója

### Általános megoldás (különböző gyökök)

$$a_n = c_1 q_1^n + c_2 q_2^n + \cdots + c_k q_k^n$$

### Általános megoldás (többszörös gyökök)

$$a_n = \sum_{i=1}^t\left(\sum_{j=0}^{m_i-1} c_{ij} n^j\right)q_i^n$$

### Fibonacci (Binet)

$$f_n = \frac{\phi^n - \psi^n}{\sqrt{5}}, \quad \phi = \frac{1+\sqrt{5}}{2}, \psi = \frac{1-\sqrt{5}}{2}$$

### Hanoi

$$h_n = 2^n - 1$$

---

## Hivatkozások

- [M] Mickens: Journal of Difference Equations
- [JDE] Journal of Difference Equations
- [Sz1], [Sz2] Szalkai cikkei

---

*Forrás: Dr. Szalkai István - Diszkrét Matematika*
