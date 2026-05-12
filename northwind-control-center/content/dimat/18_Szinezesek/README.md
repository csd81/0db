# 18. fejezet - Színezések (Graph Colorings)

## Tartalomjegyzék

- [18.1 Csúcsszínezés](#181-csúcsszínezés)
- [18.2 Élszínezés](#182-élszínezés)
- [18.3 Síkgráfok színezése](#183-síkgráfok-színezése)
- [18.4 Kritikus gráfok](#184-kritikus-gráfok)
- [18.5 Színezési algoritmusok](#185-színezési-algoritmusok)
- [18.6 Alkalmazások](#186-alkalmazások)

---

## 18.1 Csúcsszínezés

### Megfelelő színezés (18.1)

Szomszédos csúcsok különböző színűek.

### Kromatikus szám

χ(G) = minimális színek száma.

### Példák

| Gráf | χ(G) |
|------|------|
| Kₙ | n |
| Páros | 2 |
| Cₙ (páros) | 2 |
| Cₙ (páratlan) | 3 |
| Fa | 2 |

---

## 18.2 Élszínezés

### Kromatikus index

χ'(G) = minimális színek száma élszínezéshez.

### Vizing tétele (18.2)

$$\Delta(G) \leq \chi'(G) \leq \Delta(G) + 1$$

### Osztályok

- 1. osztály: χ' = Δ
- 2. osztály: χ' = Δ + 1

### Kőnig tétele

Páros gráfok 1. osztályúak.

---

## 18.3 Síkgráfok színezése

### Ötszín-tétel

Minden síkgráf 5-színezhető.

### Négyszín-tétel

Minden síkgráf 4-színezhető.

---

## 18.4 Kritikus gráfok

### k-kritikus gráf (18.3)

χ(G) = k, de minden valódi részgráfja (k-1)-színezhető.

### Tulajdonságok

δ(G) ≥ χ(G) - 1 kritikus gráfokra.

---

## 18.5 Színezési algoritmusok

### Mohó algoritmus

Csúcsok sorban, legkisebb elérhető szín.

### Welsh-Powell

Fokszám szerint csökkenő sorrend.

### DSatur

Telítettségi fok alapján választ.

---

## 18.6 Alkalmazások

### Ütemezés

Vizsgák időpontjainak kiosztása.

### Regiszter-allokáció

Fordítóprogramok optimalizálása.

### Frekvencia-kiosztás

Mobilhálózatok.

### Sudoku

9×9-es gráf 9-színezése.

---

## Brooks tétele

### Tétel (18.4)

Ha G nem Kₙ és nem páratlan kör, akkor:
$$\chi(G) \leq \Delta(G)$$

---

## Hivatkozások

- [Bro] Brooks, R.L.: On colouring the nodes of a network, 1941
- [Viz] Vizing, V.G.: On an estimate of the chromatic class, 1964
- [AH] Appel & Haken: Every planar map is four colorable, 1976

---

*Forrás: Dr. Szalkai István - Diszkrét matematika*
