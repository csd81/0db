# 3. fejezet - Binomiális és polinomiális együtthatók

## Tartalomjegyzék

- [3.1 Binomiális és polinomiális tételek](#31-binomiális-és-polinomiális-tételek)
- [3.2 A binomiális együtthatók tulajdonságai](#32-a-binomiális-együtthatók-tulajdonságai)
- [3.3 Összegezési módszerek](#33-összegezési-módszerek)
- [3.4 Rugalmas pénzérmék](#34-rugalmas-pénzérmék)

---

## 3.1 Binomiális és polinomiális tételek

### Newton binomiális tétele (3.1)

Tetszőleges $a, b \in \mathbb{C}$ és $n \in \mathbb{N}$ esetén:

$$\boxed{(a + b)^n = \sum_{i=0}^{n} \binom{n}{i} a^i b^{n-i}}$$

**Bizonyítás (kombinatorikus):**
- $(a+b)^n = (a+b)(a+b)\cdots(a+b)$ (n tényező)
- Minden zárójelből választunk $a$-t vagy $b$-t
- $a^i b^{n-i}$ pontosan $\binom{n}{i}$-féleképpen alakul ki

### Newton-Leibniz formula (3.2)

Függvények szorzatának n-edik deriváltja:

$$(f \cdot g)^{(n)} = \sum_{i=0}^{n} \binom{n}{i} f^{(i)} \cdot g^{(n-i)}$$

### Általánosított binomiális együttható (3.3)

Tetszőleges $\alpha \in \mathbb{C}$ és $n \in \mathbb{N}$ esetén:

$$\binom{\alpha}{n} = \frac{\alpha(\alpha-1)\cdots(\alpha-n+1)}{n!}$$

### Newton binomiális sora (3.4)

Tetszőleges $x, a \in \mathbb{C}$, $|x| < |a|$ és $\alpha \in \mathbb{R}$ esetén:

$$(a + x)^\alpha = \sum_{i=0}^{\infty} \binom{\alpha}{i} a^{\alpha-i} x^i$$

### Polinomiális tétel (3.5)

Többtagú hatványai:

$$(a_1 + a_2 + \cdots + a_s)^n = \sum_{\substack{k_1+\cdots+k_s=n \\ k_i \geq 0}} \binom{n}{k_1, k_2, \ldots, k_s} a_1^{k_1} a_2^{k_2} \cdots a_s^{k_s}$$

ahol $\binom{n}{k_1, \ldots, k_s} = \frac{n!}{k_1! k_2! \cdots k_s!}$ a **polinomiális együttható**.

---

## 3.2 A binomiális együtthatók tulajdonságai

### Alapvető azonosságok (3.9)

| Tulajdonság | Képlet |
|-------------|--------|
| (i) Szélső értékek | $\binom{n}{0} = \binom{n}{n} = 1$ |
| (ii) Egyessel | $\binom{n}{1} = \binom{n}{n-1} = n$ |
| (iii) Szimmetria | $\binom{n}{k} = \binom{n}{n-k}$ |
| (iv) Nulla | $\binom{n}{k} = 0$ ha $k > n$ |

### Pascal-szabály (3.10)

$$\boxed{\binom{n}{k-1} + \binom{n}{k} = \binom{n+1}{k}}$$

**Kombinatorikus bizonyítás:** n régi + 1 új elemből k-t választunk:
- Az új elemet is választjuk: $\binom{n}{k-1}$ lehetőség
- Az új elemet nem választjuk: $\binom{n}{k}$ lehetőség

### Pascal-háromszög

```
n=0:        1
n=1:       1 1
n=2:      1 2 1
n=3:     1 3 3 1
n=4:    1 4 6 4 1
n=5:   1 5 10 10 5 1
```

### Vandermonde-konvolúció (3.11)

$$\sum_{i=0}^{k} \binom{n}{i} \binom{m}{k-i} = \binom{n+m}{k}$$

### Felső összegzés (3.12)

$$\sum_{i=k}^{n} \binom{i}{k} = \binom{n+1}{k+1}$$

### Monotonitás (3.13)

Rögzített $n$ esetén $\binom{n}{i}$:
- $0 \leq i \leq \frac{n}{2}$: szigorúan növekvő
- $\frac{n}{2} \leq i \leq n$: szigorúan csökkenő

**Maximum:** $\binom{n}{n/2} \approx \frac{2^n}{\sqrt{\pi n/2}}$ (Stirling-formula)

---

## 3.3 Összegezési módszerek

### Binomiális együtthatók összegei (3.14)

| Összeg | Eredmény |
|--------|----------|
| $\sum_{i=0}^{n} \binom{n}{i}$ | $2^n$ |
| $\sum_{i=0}^{n} (-1)^i \binom{n}{i}$ | $0$ |

**Bizonyítás:** $(1+1)^n$ és $(1-1)^n$ a binomiális tételből

### Szorzatos összegek (3.15)

| Összeg | Eredmény |
|--------|----------|
| $\sum_{i=0}^{n} i \binom{n}{i}$ | $n \cdot 2^{n-1}$ |
| $\sum_{i=0}^{n} \frac{1}{i+1} \binom{n}{i}$ | $\frac{2^{n+1}-1}{n+1}$ |

**Módszer:** $(1+x)^n$ deriválása/integrálása, majd $x=1$ helyettesítés

---

### Hatványok összege

#### Binomiális polinomok (3.16)

$$\binom{x}{j} = \frac{x(x-1)\cdots(x-j+1)}{j!}$$

#### Tétel (3.17)

Minden $k \in \mathbb{N}$ esetén létezik egy $(k+1)$-edfokú $P_k(n)$ polinom, hogy:

$$\sum_{i=1}^{n} i^k = P_k(n)$$

#### Ismert összegképletek

| k | $\sum_{i=1}^{n} i^k$ |
|---|---------------------|
| 0 | $n$ |
| 1 | $\frac{n(n+1)}{2}$ |
| 2 | $\frac{n(n+1)(2n+1)}{6}$ |
| 3 | $\left[\frac{n(n+1)}{2}\right]^2$ |
| 4 | $\frac{n(n+1)(2n+1)(3n^2+3n-1)}{30}$ |

---

## 3.4 Rugalmas pénzérmék

### Szimuláció definíciója (3.18)

$p$ **szimulálja** $q$-t, ha található olyan $n$ és $E \subseteq \{f, i\}^n$, hogy $p$ valószínűségű érmét $n$-szer feldobva:

$$P(\text{eredmény} \in E) = q$$

### Tétel (3.19)

Minden véges $F \subset \mathbb{Q} \cap [0,1]$ halmazhoz létezik olyan $p \in [0,1]$, amely egyszerre szimulálja $F$ minden elemét.

### Megoldatlan problémák (3.20)

- Szimulálhatók-e egyszerre $\frac{1}{\sqrt{2}}$ és $\frac{1}{\sqrt{3}}$?
- Szimulálhatók-e $\frac{1}{e}$ és $\frac{1}{e+1}$?

---

## Képletek összefoglalója

### Binomiális együttható definíciói

$$\binom{n}{k} = \frac{n!}{k!(n-k)!} = \frac{n(n-1)\cdots(n-k+1)}{k!}$$

### Fontosabb azonosságok

| Név | Képlet |
|-----|--------|
| Pascal | $\binom{n}{k-1} + \binom{n}{k} = \binom{n+1}{k}$ |
| Szimmetria | $\binom{n}{k} = \binom{n}{n-k}$ |
| Vandermonde | $\sum_{i=0}^{k} \binom{n}{i}\binom{m}{k-i} = \binom{n+m}{k}$ |
| Felső összeg | $\sum_{i=k}^{n} \binom{i}{k} = \binom{n+1}{k+1}$ |

### Összegképletek

| Összeg | Zárt alak |
|--------|-----------|
| $\sum \binom{n}{i}$ | $2^n$ |
| $\sum (-1)^i\binom{n}{i}$ | $0$ |
| $\sum i\binom{n}{i}$ | $n2^{n-1}$ |
| $\sum \binom{i}{k}$ | $\binom{n+1}{k+1}$ |

---

## Hivatkozások

- [G] Gould: Combinatorial Identities (1972) - félezer azonosság!
- [HaPé] Hajnal Péter: Diszkrét matematika
- [ViN] Vilenkin: Kombinatorika
- [SzV1], [SzV2] Szalkai-Velleman: Flexible coins cikkek

---

*Forrás: Dr. Szalkai István - Diszkrét Matematika*
