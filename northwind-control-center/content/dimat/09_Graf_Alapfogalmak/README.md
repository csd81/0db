# 9. fejezet - Gráf alapfogalmak (Graph Theory Basics)

## Tartalomjegyzék

- [9.1 Bevezetés](#91-bevezetés)
- [9.2 Nevezetes gráfok](#92-nevezetes-gráfok)
- [9.3 Elemi definíciók és összefüggések](#93-elemi-definíciók-és-összefüggések)
- [9.4 Utak, összefüggőség](#94-utak-összefüggőség)

---

## 9.1 Bevezetés

### Történeti háttér

- **1736**: Euler megoldja a königsbergi hidak problémáját (első gráfelméleti munka)
- **1936**: Kőnig Dénes "Gráfelmélet" könyve (alapmű)
- **1930**: Első dolgozat hipergráfokról

### Gráf definíció (1.2)

**Gráf:** $G = (V, E)$ ahol:
- $V \neq \emptyset$ = csúcsok (vertices) halmaza
- $E \subseteq [V]^2$ = élek (edges) halmaza

### Gráf típusok

| Típus | Definíció | Jelölés |
|-------|-----------|---------|
| **Egyszerű gráf** | Nincs hurokél és többszörös él | simple graph |
| **Multigráf** | Többszörös élek engedettek | multigraph |
| **Pszudográf** | Hurokél és többszörös él is | pseudograph |
| **Irányított gráf** | Élek irányítottak | digraph |
| **Hipergráf** | Élek több csúcsot kötnek | hypergraph |

### Speciális gráfok

| Típus | Leírás |
|-------|--------|
| **Számozott csúcsú** | $c: V \to \{1,\ldots,n\}$ injektív |
| **Súlyozott** | $w: E \to \mathbb{R}$ él súlyok |
| **Színezett** | $c: V \to \mathbb{N}$ csúcs színek |

---

## 9.2 Nevezetes gráfok

### Teljes gráf (1.11)

**$K_n$** = $n$ csúcsú teljes gráf
- $|V| = n$
- $E = [V]^2$ (minden lehetséges él behúzva)
- Élek száma: $\binom{n}{2} = \frac{n(n-1)}{2}$

### Páros gráf (1.12)

**Kétpólusú gráf:** $V = A \cup B$, $A \cap B = \emptyset$, élek csak $A$ és $B$ között

**Teljes páros gráf $K_{m,n}$:**
- $|A| = m$, $|B| = n$
- Minden lehetséges él behúzva
- Élek száma: $m \cdot n$

### Többpólusú gráf (1.13)

**$K_{m_1,\ldots,m_k}$** = teljes többpólusú gráf

**Turán gráf $T_{n}^{k}$:**
- $m_1 + \cdots + m_k = n$
- Pólusok méretei között eltérés ≤ 1

### Út és kör (1.14)

| Gráf | Jelölés | Leírás |
|------|---------|--------|
| **Út** | $P_n$ | $n$ hosszú egyszerű út ($n+1$ csúcs) |
| **Kör** | $C_n$ | $n$ hosszú kör ($n$ csúcs) |
| **Csillag** | $S_n$ | $n$ ágú csillag ($n+1$ csúcs) |
| **Szélkerék** | $W_n$ | $n$ ágú windmill ($2n+1$ csúcs) |

### Petersen gráf (1.14)

- 10 csúcs, 15 él
- 3-reguláris
- Fontos ellenpélda sok sejtéshez

---

## 9.3 Elemi definíciók és összefüggések

### Komplementer gráf (1.16a)

**$\overline{G} = (V, \overline{E})$** ahol $\overline{E} = [V]^2 \setminus E$

### Izomorfia (1.16b)

**$G \cong H$** ha létezik éltartó bijekció $f: V(G) \to V(H)$

### Fokszám (1.17)

**$d(v)$** = $v$-re illeszkedő élek száma (hurokélek kétszer!)

$$d(v) = \sum_{v \in e} m(e) + \sum_{v \in e, \text{ hurok}} m(e)$$

### Speciális csúcsok

| Típus | Definíció |
|-------|-----------|
| **Izolált** | $d(v) = 0$ |
| **Levél** | $d(v) = 1$ |
| **Reguláris** | Minden csúcs fokszáma egyenlő |
| **$k$-reguláris** | Minden csúcs fokszáma $k$ |

---

### Kézfogási tétel (1.20)

$$\sum_{v \in V} d(v) = 2|E|$$

**Következmények:**
1. Páratlan fokú csúcsok száma páros
2. Szénhidrogénekben ($C_nH_m$) mindig páros számú H atom van

---

### Részgráfok (1.23)

| Típus | Jelölés | Definíció |
|-------|---------|-----------|
| **Részgráf** | $H \subseteq G$ | $W \subseteq V$, $F \subseteq E$ |
| **Feszített részgráf** | $H \subseteq G$ | $W \subseteq V$, $F = E \cap [W]^2$ |
| **Feszítő részgráf** | - | $W = V$, $F \subseteq E$ |

---

## 9.4 Utak, összefüggőség

### Út definíciók (1.24-1.28)

| Típus | Definíció |
|-------|-----------|
| **Út/Séta** | $P = (v_0, \ldots, v_k)$, $\{v_i, v_{i+1}\} \in E$ |
| **Kör** | Út ahol $v_0 = v_k$ |
| **Egyszerű út** | Nincs csúcs- és élismétlődés |
| **Éldiszjunkt** | Nincs közös él |
| **Csúcsdiszjunkt** | Nincs közös csúcs |

### Út hossza (1.25)

- **Nem súlyozott:** $\ell(P) = k$ (élek száma)
- **Súlyozott:** $w(P) = \sum_{e \in P} w(e)$

---

### Összefüggőség (1.31-1.34)

**Összefüggő gráf:** Bármely két csúcs között van út

**Állítások:**
1. $G$ összefüggő ⇔ létezik $a \in V$ ahonnan minden csúcsba vezet út
2. Ha van út két csúcs között, van egyszerű út is
3. Ha összefüggő gráfban van kör, körből bármely él elhagyható (összefüggő marad)

---

### Komponensek (1.35)

**Összefüggő komponens:** Maximális összefüggő részgráf

**Tétel:** Gráf csúcsai ekvivalencia-osztályokra bomlanak a "van út közöttük" reláció szerint

---

## Összefoglaló táblázat

| Fogalom | Jelölés | Képlet/Definíció |
|---------|---------|------------------|
| Teljes gráf | $K_n$ | $\binom{n}{2}$ él |
| Páros gráf | $K_{m,n}$ | $m \cdot n$ él |
| Út | $P_n$ | $n+1$ csúcs, $n$ él |
| Kör | $C_n$ | $n$ csúcs, $n$ él |
| Csillag | $S_n$ | $n+1$ csúcs, $n$ él |
| Fokszámösszeg | - | $\sum d(v) = 2|E|$ |
| Komplementer | $\overline{G}$ | $\overline{E} = [V]^2 \setminus E$ |

---

## Kulcsfogalmak

| Fogalom | Jelentés |
|---------|----------|
| **Csúcs (Vertex)** | Gráf alapobjektuma |
| **Él (Edge)** | Két csúcsot összeköt |
| **Fokszám (Degree)** | Csúcsra illeszkedő élek száma |
| **Szomszédos** | Él köti össze őket |
| **Izomorfia** | Szerkezetileg azonos gráfok |
| **Összefüggő** | Bármely két csúcs között van út |
| **Komponens** | Maximális összefüggő részgráf |

---

## Hivatkozások

- [AB] Andrásfai Béla: Gráfelmélet
- [HaPé] Hajnal Péter: Gráfelmélet
- [BC] Claude Berge: Hipergráfok
- [RoKe] Rosen: Discrete Mathematics

---

*Forrás: Dr. Szalkai István - Diszkrét Matematika*
