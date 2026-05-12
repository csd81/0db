# 16. fejezet - Izomorfia (Graph Isomorphism)

## Tartalomjegyzék

- [16.1 Izomorfia definíció](#161-izomorfia-definíció)
- [16.2 Izomorfia invariánsok](#162-izomorfia-invariánsok)
- [16.3 Izomorfia tesztelése](#163-izomorfia-tesztelése)
- [16.4 Automorfizmus](#164-automorfizmus)
- [16.5 Speciális gráfok izomorfia](#165-speciális-gráfok-izomorfia)
- [16.6 Izomorfia algoritmusok](#166-izomorfia-algoritmusok)
- [16.7 Alkalmazások](#167-alkalmazások)

---

## 16.1 Izomorfia definíció

### Gráfizomorfia (16.1)

**Definíció:** G₁ ≅ G₂ ha létezik f: V₁ → V₂ bijekció, amely tartja a szomszédságot:
$$\{u,v\} \in E_1 \iff \{f(u),f(v)\} \in E_2$$

### Ekvivalenciareláció

- Reflexív: G ≅ G
- Szimmetrikus: G₁ ≅ G₂ ⇒ G₂ ≅ G₁
- Tranzitív: G₁ ≅ G₂ és G₂ ≅ G₃ ⇒ G₁ ≅ G₃

---

## 16.2 Izomorfia invariánsok

### Invariánsok (nem változnak izomorfiánál)

| Invariáns | Jelölés |
|-----------|---------|
| Csúcsok száma | |V| |
| Élek száma | |E| |
| Fokszám-sorozat | (d₁, d₂, ..., dₙ) |
| Összefüggőség | - |
| Átmérő | diam(G) |
| Kromatikus szám | χ(G) |
| Körök jelenléte | - |
| Páros gráf | - |

---

## 16.3 Izomorfia tesztelése

### Nem-izomorfia bizonyítása

Elég egy invariánsban különbözni.

### Izomorfia bizonyítása

Konstruáljunk explicit izomorfizmust.

### Adjacencia mátrix módszer

A₂ = PᵀA₁P valamilyen P permutációs mátrixra.

---

## 16.4 Automorfizmus

### Definíció (16.2)

Automorfizmus: G → G izomorfizmus.

### Automorfizmus csoport

Aut(G) = összes automorfizmus, csoportot alkot.

### Példák

| Gráf | Aut(G) | Méret |
|------|--------|-------|
| Kₙ | Sₙ | n! |
| Pₙ | ℤ₂ | 2 |
| Cₙ | Dₙ | 2n |
| Kₘ,ₙ (m≠n) | Sₘ × Sₙ | m!·n! |

---

## 16.5 Speciális gráfok izomorfia

### Teljes gráfok

Minden Kₙ izomorf minden más Kₙ-nel.

### Út gráfok

Minden Pₙ izomorf minden más Pₙ-nel.

### Kör gráfok

Minden Cₙ izomorf minden más Cₙ-nel.

---

## 16.6 Izomorfia algoritmusok

### Brute-force

Minden permutáció kipróbálása: O(n!)

### Weisfeiler-Lehman

Szín-finomítás algoritmus.

### Babai tétele (2015)

Kvázipolinomiális algoritmus: exp(O((log n)^c))

---

## 16.7 Alkalmazások

- Kémiai szerkezet azonosítás
- Mintafelismerés
- Hálózat elemzés
- Kód ekvivalencia

---

## Hivatkozások

- [Kur] Kuratowski, C.: Sur le problème des courbes, 1930
- [Bab] Babai, L.: Graph Isomorphism in Quasipolynomial Time, 2015

---

*Forrás: Dr. Szalkai István - Diszkrét matematika*
