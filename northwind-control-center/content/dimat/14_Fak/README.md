# 14. fejezet - Fák (Trees)

## Tartalomjegyzék

- [14.1 Fa definíciók](#141-fa-definíciók)
- [14.2 Fajták](#142-fajták)
- [14.3 Fákkal kapcsolatos fogalmak](#143-fákkal-kapcsolatos-fogalmak)
- [14.4 Fák száma](#144-fák-száma)
- [14.5 Feszítőfák](#145-feszítőfák)
- [14.6 Bináris fák](#146-bináris-fák)
- [14.7 Fák bejárása](#147-fák-bejárása)
- [14.8 Alkalmazások](#148-alkalmazások)

---

## 14.1 Fa definíciók

### Fa (14.1)

**Fa:** Összefüggő, körmentes gráf.

### Ekvivalens definíciók

1. Összefüggő, n-1 éllel
2. Körmentes, n-1 éllel
3. Bármely két csúcs között pontosan egy út van
4. Minimális összefüggő gráf

---

## 14.2 Fajták

### Gyökeres fa

Egy csúcs ki van emelve gyökérnek.

### Szabad fa

Nincs kitüntetett gyökér.

### Bináris fa

Minden csúcsnak legfeljebb 2 gyermeke van.

### k-áris fa

Minden csúcsnak legfeljebb k gyermeke van.

---

## 14.3 Fákkal kapcsolatos fogalmak

| Fogalom | Jelentés |
|---------|----------|
| Gyökér | Kitüntetett csúcs |
| Szülő | Egy szinttel feljebb |
| Gyermek | Egy szinttel lejjebb |
| Levél | Nincs gyermeke |
| Belső csúcs | Van gyermeke |
| Mélység | Gyökértől való távolság |
| Magasság | Legnagyobb mélység |

---

## 14.4 Fák száma

### Cayley tétele (14.2)

**Tétel:** n csúcsú címkézett fák száma: n^(n-2).

### Prüfer-kód

Bijekció fák és (n-2)-hosszú sorozatok között.

---

## 14.5 Feszítőfák

### Feszítőfa definíció

G összes csúcsát tartalmazó fa.

### Minimális feszítőfa (MST)

Legkisebb összsúlyú feszítőfa.

---

## 14.6 Bináris fák

### Teljes bináris fa

Minden szint teljesen kitöltött.

### Kitöltött bináris fa

Utolsó szint balra zárt.

### Catalan-számok

n csúcsú bináris fák száma: C_n = (1/(n+1))·C(2n,n).

---

## 14.7 Fák bejárása

### Preorder

Gyökér, Bal, Jobb

### Inorder

Bal, Gyökér, Jobb

### Postorder

Bal, Jobb, Gyökér

### Szint szerinti

Szélességi keresés

---

## 14.8 Alkalmazások

- Fájlrendszer hierarchia
- Döntési fák
- Bináris keresőfák
- Halom adatszerkezet
- Huffman-kódolás

---

## Hivatkozások

- [Cay] Cayley, A.: A theorem on trees, 1889
- [Knuth] Knuth, D.E.: The Art of Computer Programming, Vol. 1

---

*Forrás: Dr. Szalkai István - Diszkrét matematika*
