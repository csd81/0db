# 13. fejezet - Útkereső algoritmusok (Pathfinding Algorithms)

## Tartalomjegyzék

- [13.1 Legrövidebb út problémák](#131-legrövidebb-út-problémák)
- [13.2 Dijkstra algoritmusa](#132-dijkstra-algoritmusa)
- [13.3 Bellman-Ford algoritmus](#133-bellman-ford-algoritmus)
- [13.4 Floyd-Warshall algoritmus](#134-floyd-warshall-algoritmus)
- [13.5 Szélességi keresés](#135-szélességi-keresés)
- [13.6 Mélységi keresés](#136-mélységi-keresés)
- [13.7 A* algoritmus](#137-a-algoritmus)
- [13.8 Alkalmazások](#138-alkalmazások)

---

## 13.1 Legrövidebb út problémák

### Egy forrásból minden csúcsba

Adott: G = (V, E), súlyfüggvény w: E → ℝ, forrás s.

Keresett: δ(s, v) minden v ∈ V-re.

### Összes csúcspár

Keresett: δ(u, v) minden u, v ∈ V-re.

---

## 13.2 Dijkstra algoritmusa

### Algoritmus (13.1)

1. Inicializálás: d[s] = 0, többi = ∞
2. Prioritássor használata
3. Mindig a legközelebbi csúcsot dolgozzuk fel
4. Élek relaxálása

### Komplexitás

- Bináris kupaccal: O((V+E) log V)
- Fibonacci kupaccal: O(E + V log V)

### Korlátok

Csak nem-negatív súlyokkal működik!

---

## 13.3 Bellman-Ford algoritmus

### Algoritmus (13.2)

1. Inicializálás
2. |V|-1 iteráció: minden él relaxálása
3. Negatív kör ellenőrzése

### Komplexitás

O(VE)

### Előny

Kezeli a negatív súlyokat is!

---

## 13.4 Floyd-Warshall algoritmus

### Algoritmus (13.3)

Dinamikus programozás összes csúcspárra.

### Komplexitás

O(V³)

### Használat

Sűrű gráfoknál, amikor minden pár kell.

---

## 13.5 Szélességi keresés (BFS)

### Algoritmus

Sor használata, rétegenkénti bejárás.

### Komplexitás

O(V+E)

### Alkalmazás

Legrövidebb út súlyozatlan gráfokban.

---

## 13.6 Mélységi keresés (DFS)

### Algoritmus

Verem használata (rekurzív vagy iteratív).

### Élosztályozás

- Fa-él
- Vissza-él
- Előre-él
- Kereszt-él

---

## 13.7 A* algoritmus

### Algoritmus

Dijkstra + heurisztika.

### Feltétel

A heurisztika legyen megengedő (soha nem becsül túl).

---

## 13.8 Alkalmazások

- GPS navigáció
- Hálózati útválasztás
- Játék AI
- Robotika

---

## Hivatkozások

- [Dij] Dijkstra, E.W.: A note on two problems in connexion with graphs, 1959
- [BF] Bellman, R.: On a routing problem, 1958
- [FW] Floyd, R.W.: Algorithm 97: Shortest path, 1962

---

*Forrás: Dr. Szalkai István - Diszkrét matematika*
