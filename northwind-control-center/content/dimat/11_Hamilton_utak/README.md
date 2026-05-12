# 11. fejezet - Hamilton utak (Hamilton Paths)

## Tartalomjegyzék

- [11.1 Hamilton utak és körök definíciója](#111-hamilton-utak-és-körök-definíciója)
- [11.2 Szükséges feltételek](#112-szükséges-feltételek)
- [11.3 Elégséges feltételek](#113-elégséges-feltételek)
- [11.4 A bezárás módszere](#114-a-bezárás-módszere)
- [11.5 Algoritmusok](#115-algoritmusok)
- [11.6 Alkalmazások](#116-alkalmazások)

---

## 11.1 Hamilton utak és körök definíciója

### Hamilton-út (11.1)

**Hamilton-út:** Olyan út, amely a gráf minden csúcsát pontosan egyszer tartalmazza.

### Hamilton-kör (11.2)

**Hamilton-kör:** Olyan Hamilton-út, amely ugyanabba a csúcsba érkezik, ahonnan indult.

### Hamilton-gráf (11.3)

**Hamilton-gráf:** Olyan gráf, amely tartalmaz Hamilton-kört.

---

## 11.2 Szükséges feltételek

### Összefüggőség

Ha G Hamilton-gráf, akkor G összefüggő.

### Nincs vágási csúcs

Ha G Hamilton-gráf, akkor G-nek nincs vágási csúcsa.

### Általános feltétel (11.4)

Ha G Hamilton-gráf, akkor minden S ⊆ V-re: c(G-S) ≤ |S|.

---

## 11.3 Elégséges feltételek

### Dirac tétele (11.5, 1952)

**Tétel:** Ha G n ≥ 3 csúcsú egyszerű gráf és δ(G) ≥ n/2, akkor G Hamilton-gráf.

---

### Ore tétele (11.6, 1960)

**Tétel:** Ha G n ≥ 3 csúcsú egyszerű gráf és minden nem szomszédos u,v-re: d(u) + d(v) ≥ n, akkor G Hamilton-gráf.

---

### Pósa tétele (11.7, 1962)

Fokszám-sorozaton alapuló erősebb feltétel.

---

## 11.4 A bezárás módszere

### Bondy-Chvátal tétel (11.8)

A gráf lezártja megőrzi a Hamilton-tulajdonságot.

---

## 11.5 Algoritmusok

### Brute-force

Minden permutáció kipróbálása: O(n!)

### Backtracking

Visszalépéses keresés.

### Posá forgatás-bővítés

Speciális technika Hamilton-utak keresésére.

---

## 11.6 Alkalmazások

### Utazó ügynök probléma (TSP)

Minimális költségű Hamilton-kör keresése súlyozott gráfban.

### Ütemezés

Feladatok sorrendjének optimalizálása.

---

## Hivatkozások

- [D] Dirac, G.A.: Some theorems on abstract graphs, 1952
- [O] Ore, O.: Note on Hamilton circuits, 1960
- [Karp] Karp, R.M.: Reducibility among combinatorial problems, 1972

---

*Forrás: Dr. Szalkai István - Diszkrét matematika*
