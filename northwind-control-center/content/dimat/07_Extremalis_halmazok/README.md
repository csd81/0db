# 7. fejezet - Extremális halmazrendszerek (Extremal Set Systems)

## Tartalomjegyzék

- [7.1 Sperner tétele](#71-sperner-tétele)
- [7.2 Erdős-DeBruijn, Ryser és Fisher tételei](#72-erdős-debruijn-ryser-és-fisher-tételei)
- [7.3 Erdős-Ko-Rado tétele](#73-erdős-ko-rado-tétele)
- [7.4 Egyéb eredmények](#74-egyéb-eredmények)
- [7.5 Szimplexek](#75-szimplexek)

---

## 7.1 Sperner tétele

### Sperner-tulajdonság (7.1)

Egy $\mathcal{F} = \{A_1, \ldots, A_m\}$ halmazrendszer **Sperner-tulajdonságú**, ha:
$$A_i \not\subseteq A_j \quad \text{ha } i \neq j$$

Azaz egyik halmaz sem tartalmazza a másikat.

### Sperner tétele (7.1 Tétel, 1928)

Ha $|S| = n$ és $\{A_1, \ldots, A_m\}$ Sperner-tulajdonságú halmazrendszer $S$-en, akkor:
$$m \leq \binom{n}{\lfloor n/2 \rfloor}$$

**A becslés éles!** A maximumot az összes $\lfloor n/2 \rfloor$-elemű részhalmaz adja.

### Példa

**n = 4:** $\binom{4}{2} = 6$

A 2-elemű részhalmazok: $\{1,2\}, \{1,3\}, \{1,4\}, \{2,3\}, \{2,4\}, \{3,4\}$

Egyik sem tartalmazza a másikat, és nem adható meg több ilyen halmaz!

### Bizonyítás (Lubell)

**Lánc:** $X_1 \subset X_2 \subset \cdots \subset X_t$

- $n$-hosszúságú láncok száma: $n!$
- $k$-elemű $A_i$ legfeljebb $k!(n-k)!$ láncban szerepel
- Sperner-tulajdonság miatt különböző $A_i$ különböző láncokban vannak

$$n! \geq \sum_{i=1}^m k_i!(n-k_i)! \geq m \cdot \lfloor n/2 \rfloor! \lceil n/2 \rceil!$$

$$m \leq \frac{n!}{\lfloor n/2 \rfloor! \lceil n/2 \rceil!} = \binom{n}{\lfloor n/2 \rfloor}$$

### Általánosítások

**7.3 Tétel:** Ha minden $|A_i| \leq k \leq n/2$, akkor $m \leq \binom{n}{k}$

**7.4 Tétel (Lubell, 1969):**
$$\sum_{i=1}^m \frac{1}{\binom{n}{|A_i|}} \leq 1$$

---

## 7.2 Erdős-DeBruijn, Ryser és Fisher tételei

### Erdős-DeBruijn tétel (7.5 Tétel)

Ha $|A_i \cap A_j| = 1$ minden $i \neq j$ esetén, akkor:
$$m \leq n$$

**Egyenlőség esetén három lehetőség:**
- (a) Projektív sík szerkezet
- (b) Csillagszerkezet (minden halmaz tartalmaz egy közös elemet)
- (c) Véges geometria

### Gallai tétele (7.6 Tétel)

**Geometriai alkalmazás:**
- $m$ pont a síkban (nem egy egyenesen) $\Rightarrow$ legalább $m$ egyenest határoznak meg
- Duális: $m$ egyenes (nem egy ponton át) $\Rightarrow$ legalább $m$ metszéspont

### Ryser tétele (7.7 Tétel)

Ha $|A_i \cap A_j| = t$ (állandó) minden $i \neq j$ esetén, akkor:
$$m \leq n$$

**Bizonyítás (lineáris algebrai módszer):**
- Rendeljük hozzá minden $A_i$-hez a karakterisztikus vektorát $a_i \in \mathbb{R}^n$
- Megmutatjuk: $a_1, \ldots, a_m$ lineárisan függetlenek
- Ezért $m \leq n$

### Fisher tétele (7.9 Tétel)

Ha $|A_i| = k$ (állandó) és $|A_i \cap A_j| = t$ minden $i \neq j$ esetén, akkor:
$$m \leq n$$

**Alkalmazás:** Statisztika (kísérlettervezés)

---

## 7.3 Erdős-Ko-Rado tétele

### EKR tétel (7.10 Tétel, 1961)

Ha $|A_i| \leq k \leq n/2$ és $A_i \cap A_j \neq \emptyset$ minden $i \neq j$ esetén (metsző halmazrendszer), akkor:
$$m \leq \binom{n-1}{k-1}$$

**A becslés éles!**

### Éles konstrukció

Rögzítsünk egy elemet $x_0 \in S$. Legyen:
$$\mathcal{F} = \{A \subseteq S : |A| = k, x_0 \in A\}$$

Minden halmaz tartalmazza $x_0$-t, tehát páronként metszik egymást.

**Példa:** $n = 5, k = 2$
$$m \leq \binom{4}{1} = 4$$

Konstrukció: $\{1,2\}, \{1,3\}, \{1,4\}, \{1,5\}$ (mind tartalmazza az 1-est)

---

## 7.4 Egyéb eredmények

### Ray-Chaudhuri-Wilson tétel (7.12 Tétel, 1975)

Ha $|A_i| = k$ és $|A_i \cap A_j| \in L = \{r_1, \ldots, r_s\}$ minden $i \neq j$ esetén, akkor:
$$m \leq \binom{n}{s}$$

### Babai-Frankl tétel (7.13 Tétel, 1988)

Ha még $\gcd(r_1, \ldots, r_s) \nmid k$, akkor:
$$m \leq n$$

### Róka Sándor tételei

**7.14 Tétel (1992):** Szimmetrikus differenciára:
$$|A_i \triangle A_j| \in L \Rightarrow m \leq \binom{n}{s}$$

**7.15 Tétel (1993):** Háromszoros metszetre:
$$|A_i \cap A_j \cap A_k| \leq 1 \Rightarrow m \leq \frac{1}{3}n(n-1)$$

**7.17 Tétel (1997):** Független metszőrendszerek:
$$c_1 \log_2 n \leq m \leq c_2 n^2$$

### Tuza Zsolt tétele (7.18 Tétel, 1987)

Kölcsönös metszetmentes párokra vonatkozó korlátok.

---

## 7.5 Szimplexek

### Kémiai alkalmazás

**Probléma:** Összes minimális reakcióegyenlet felírása adott vegyületek között.

**Modell:**
- Vegyületek: $A_1, \ldots, A_m \in \mathbb{R}^n$ (összetétel vektorok)
- Reakció: $\sum_{j \in S} x_j A_j = 0$ (lineáris kombináció = 0)
- Minimális reakció: Bármely vegyületet elhagyva már nincs reakció

### Szimplex definíció (7.19)

$C = \{b_j : j \in S\} \subseteq \mathbb{R}^n$ **szimplex**, ha:
- $C$ lineárisan összefüggő
- Bármely valódi részhalmaz lineárisan független

### Alkalmazás

- Minimális reakciók = szimplexek keresése
- Lineáris algebra + kombinatorika = kémiai reakcióhálózatok elemzése

---

## Összefoglaló táblázat

| Tétel | Feltétel | Korlát |
|-------|----------|--------|
| **Sperner** | $A_i \not\subseteq A_j$ | $\binom{n}{\lfloor n/2 \rfloor}$ |
| **Erdős-DeBruijn** | $|A_i \cap A_j| = 1$ | $n$ |
| **Ryser** | $|A_i \cap A_j| = t$ | $n$ |
| **Fisher** | $|A_i| = k, |A_i \cap A_j| = t$ | $n$ |
| **Erdős-Ko-Rado** | $A_i \cap A_j \neq \emptyset, |A_i| \leq k$ | $\binom{n-1}{k-1}$ |
| **Ray-Chaudhuri-Wilson** | $|A_i \cap A_j| \in L, |L| = s$ | $\binom{n}{s}$ |

---

## Kulcsfogalmak

| Fogalom | Definíció |
|---------|-----------|
| **Sperner-tulajdonság** | Egyik halmaz sem tartalmazza a másikat |
| **Metsző halmazrendszer** | Bármely két halmaz metszete nemüres |
| **t-metsző** | Bármely két halmaz metszete pontosan t elemű |
| **Szimplex** | Lineárisan összefüggő, de valódi részhalmazai függetlenek |
| **Lánc** | $X_1 \subset X_2 \subset \cdots \subset X_t$ |

---

## Hivatkozások

- [Sp] Sperner, 1928
- [L] Lubell, 1969
- [BF] Babai László, Frankl Péter
- [RW] Ray-Chaudhuri, Wilson, 1975
- [R1-R3] Róka Sándor cikkei
- [Sz1-Sz2] Szalkai cikkei szimplexekről

---

*Forrás: Dr. Szalkai István - Diszkrét Matematika*
