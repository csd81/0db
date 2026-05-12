# 15. fejezet - Feszítőfák (Spanning Trees)

## Tartalomjegyzék

- [15.1 Feszítőfa definíció](#151-feszítőfa-definíció)
- [15.2 Minimális feszítőfa](#152-minimális-feszítőfa)
- [15.3 Kruskal algoritmus](#153-kruskal-algoritmus)
- [15.4 Prim algoritmus](#154-prim-algoritmus)
- [15.5 Fák száma](#155-fák-száma)
- [15.6 Alkalmazások](#156-alkalmazások)

---

## 15.1 Feszítőfa definíció

### Feszítőfa (15.1)

**Feszítőfa:** Olyan részgráf, amely:
1. Tartalmazza G összes csúcsát
2. Fa (összefüggő, körmentes)

### Tétel (15.2)

Minden összefüggő gráfnak van feszítőfája.

### Élek száma

n csúcsú feszítőfának pontosan n-1 éle van.

---

## 15.2 Minimális feszítőfa

### Definíció (15.3)

Súlyozott gráfban a legkisebb összsúlyú feszítőfa.

### Vágási tulajdonság (15.4)

Egy vágás minimális súlya éle benne van az MST-ben.

### Kör tulajdonság (15.5)

Egy kör maximális súlya éle NINCS benne az MST-ben.

---

## 15.3 Kruskal algoritmus

### Algoritmus (15.6)

1. Élek súly szerint rendezve
2. Vegyük a legkisebb élt, ha nem alkot kört
3. Ismételjük, amíg n-1 élünk van

### Komplexitás

O(E log E)

### Adatszerkezet

Union-Find (Disjoint Set Union)

---

## 15.4 Prim algoritmus

### Algoritmus (15.7)

1. Kezdjünk egy tetszőleges csúcsból
2. Mindig a legkisebb súlyú, fát elérő élt válasszuk
3. Ismételjük, amíg minden csúcsot hozzáadtunk

### Komplexitás

- Bináris kupaccal: O((V+E) log V)
- Fibonacci kupaccal: O(E + V log V)

---

## 15.5 Fák száma

### Mátrix-fa tétel (15.8)

Feszítőfák száma = Laplace-mátrix bármely cofaktora.

### Cayley formula

Kₙ-nek n^(n-2) feszítőfája van.

---

## 15.6 Alkalmazások

- Hálózati tervezés
- Fürtözés
- TSP közelítés
- Képszegmentálás

---

## Hivatkozások

- [Krus] Kruskal, J.B.: On the shortest spanning subtree, 1956
- [Prim] Prim, R.C.: Shortest connection networks, 1957
- [Cay] Cayley, A.: A theorem on trees, 1889

---

*Forrás: Dr. Szalkai István - Diszkrét matematika*
