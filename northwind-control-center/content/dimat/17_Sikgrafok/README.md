# 17. fejezet - Síkgráfok (Planar Graphs)

## Tartalomjegyzék

- [17.1 Síkgráf definíció](#171-síkgráf-definíció)
- [17.2 Euler-formula](#172-euler-formula)
- [17.3 Kuratowski-tétel](#173-kuratowski-tétel)
- [17.4 Síkgráf színezés](#174-síkgráf-színezés)
- [17.5 Dualitás](#175-dualitás)
- [17.6 Síkgráfok felismerése](#176-síkgráfok-felismerése)
- [17.7 Alkalmazások](#177-alkalmazások)

---

## 17.1 Síkgráf definíció

### Síkgráf (17.1)

**Síkbgráf:** Olyan gráf, amely lerajzolható a síkba élek keresztezése nélkül.

### Síkba ágyazott gráf

Egy konkrét keresztezésmentes rajz.

### Lapok

A sík tartományai, amelyeket élek határolnak.

---

## 17.2 Euler-formula

### Euler tétele (17.2)

Összefüggő síkgráfra:
$$V - E + F = 2$$

ahol F a lapok száma (beleértve a külsőt).

### Következmények

**Egyszerű síkgráfokra (V ≥ 3):**
$$E \leq 3V - 6$$

**Háromszögmentes síkgráfokra:**
$$E \leq 2V - 4$$

### Alkalmazás

K₅ és K₃,₃ nem síkgráfok bizonyítása.

---

## 17.3 Kuratowski-tétel

### Felosztás (17.3)

Él helyettesítése úttal.

### Kuratowski tétele (17.4)

**Tétel:** G pontosan akkor síkgráf, ha nem tartalmaz K₅ vagy K₃,₃ felosztást.

---

## 17.4 Síkgráf színezés

### Ötszín-tétel (17.5)

Minden síkgráf 5-színezhető.

### Négyszín-tétel (17.6)

Minden síkgráf 4-színezhető.

**Bizonyítás:** Appel & Haken (1976), számítógéppel segített.

---

## 17.5 Dualitás

### Duális gráf (17.7)

G* csúcsai = G lapjai
G* élei = G élein mennek át

### Tulajdonságok

| G | G* |
|---|----|
| |V| | |F| |
| |E| | |E| |
| |F| | |V| |

---

## 17.6 Síkgráfok felismerése

### Hopcroft-Tarjan algoritmus

O(V) időben eldönti a síkbarajzolhatóságot.

---

## 17.7 Alkalmazások

- Áramköri tervek
- Térképszínezés
- Földrajzi információs rendszerek
- Gráfrajzolás

---

## Hivatkozások

- [Eul] Euler, L.: Elementa doctrinae solidorum, 1750
- [AH] Appel & Haken: Every planar map is four colorable, 1976
- [HT] Hopcroft & Tarjan: Efficient planarity testing, 1974

---

*Forrás: Dr. Szalkai István - Diszkrét matematika*
