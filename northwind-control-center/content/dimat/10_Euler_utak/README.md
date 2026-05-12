# 10. fejezet - Euler utak (Euler Paths)

## Tartalomjegyzék

- [10.1 Euler utak és körök definíciója](#101-euler-utak-és-körök-definíciója)
- [10.2 Euler-gráfok azonosítása](#102-euler-gráfok-azonosítása)
- [10.3 Euler tétele](#103-euler-tétele)
- [10.4 Euler út keresése](#104-euler-út-keresése)
- [10.5 Königsbergi hidak](#105-königsbergi-hidak)
- [10.6 Kínai postás probléma](#106-kínai-postás-probléma)
- [10.7 Fleury algoritmusa](#107-fleury-algoritmusa)
- [10.8 Alkalmazások](#108-alkalmazások)

---

## 10.1 Euler utak és körök definíciója

### Euler-út (10.1)

**Euler-út:** Olyan út, amely a gráf minden élét pontosan egyszer tartalmazza.

### Euler-kör (10.2)

**Euler-kör:** Olyan Euler-út, amely ugyanabba a csúcsba érkezik, ahonnan indult.

### Euler-gráf (10.3)

**Euler-gráf:** Olyan gráf, amely tartalmaz Euler-kört.

---

## 10.2 Euler-gráfok azonosítása

### Euler tétele (10.4)

**Tétel:** Egy összefüggő gráf pontosan akkor Euler-gráf, ha minden csúcsának foka páros.

---

## 10.3 Euler tétele

### Bizonyítás

**⇒ irány:** Ha van Euler-kör, minden fok páros.

**⇐ irány:** Ha minden fok páros, konstruálható Euler-kör.

---

## 10.4 Euler út keresése

### Félig Euler-gráfok

**Tétel:** Egy gráfban pontosan akkor van Euler-út (de nem kör), ha pontosan 2 páratlan fokú csúcs van.

---

## 10.5 Königsbergi hidak

### Történeti háttér

Euler 1736-ban oldotta meg a problémát, megalapozva a gráfelméletet.

### A gráf modell

4 csúcs (földrészek), 7 él (hidak).

Minden csúcs fokszáma páratlan → **nincs Euler-út**.

---

## 10.6 Kínai postás probléma

### Feladat

Egy postásnak minden utcán végig kell mennie, minimalizálva a teljes utat.

### Megoldás

Ha nem Euler-gráf, párosítsuk a páratlan fokú csúcsokat minimális súlyú utakkal.

---

## 10.7 Fleury algoritmusa

### Algoritmus

1. Kezdjünk egy csúcsból
2. Válasszunk olyan élt, ami nem híd (kivéve ha nincs más)
3. Ismételjük, amíg van él

---

## 10.8 Alkalmazások

- Utcaseprés
- Hálózatok tesztelése
- DNS szekvenálás
- Áramköri tervek

---

## Hivatkozások

- [E] Euler, L.: Solutio problematis ad geometriam situs pertinentis, 1736
- [BM] Bondy & Murty: Graph Theory

---

*Forrás: Dr. Szalkai István - Diszkrét matematika*
