# 12. fejezet - Graf mátrixok (Graph Matrices)

## Tartalomjegyzék

- [12.1 Adjacencia mátrix](#121-adjacencia-mátrix)
- [12.2 Incidencia mátrix](#122-incidencia-mátrix)
- [12.3 Laplace mátrix](#123-laplace-mátrix)
- [12.4 Mátrixok és gráf tulajdonságok](#124-mátrixok-és-gráf-tulajdonságok)
- [12.5 Spektrális gráfelmélet](#125-spektrális-gráfelmélet)
- [12.6 Alkalmazások](#126-alkalmazások)

---

## 12.1 Adjacencia mátrix

### Definíció (12.1)

A gráf adjacencia mátrixa A, ahol:
$$A_{ij} = \begin{cases} 1 & \text{ha } i \sim j \\ 0 & \text{különben} \end{cases}$$

### Tulajdonságok

- Szimmetrikus (irányítatlan gráfoknál)
- (Aᵏ)ᵢⱼ = k hosszúságú utak száma i-ből j-be

---

## 12.2 Incidencia mátrix

### Definíció (12.2)

B n×m mátrix, ahol:
$$B_{ij} = \begin{cases} 1 & \text{ha csúcs i illeszkedik élre j} \\ 0 & \text{különben} \end{cases}$$

---

## 12.3 Laplace mátrix

### Definíció (12.3)

L = D - A, ahol D a fokmátrix.

### Tulajdonságok

- Sorösszegek = 0
- Pozitív szemidefinit
- Sajátértékek információt hordoznak

---

## 12.4 Mátrixok és gráf tulajdonságok

### Feszítőfák száma

Mátrix-fa tétel: L bármely cofaktora = feszítőfák száma.

### Izomorfia tesztelés

A₁ és A₂ permutáció-hasonlók ⇔ G₁ ≅ G₂.

---

## 12.5 Spektrális gráfelmélet

### Gráf spektrum

A sajátértékek halmaza.

### Alkalmazások

- Gráfok osztályozása
- Fürtözés
- Hálózatok elemzése

---

## 12.6 Alkalmazások

- PageRank algoritmus
- Közösségdetektálás
- Képszegmentálás

---

## Hivatkozások

- [GRS] Godsil & Royle: Algebraic Graph Theory
- [Chu] Chung: Spectral Graph Theory

---

*Forrás: Dr. Szalkai István - Diszkrét matematika*
