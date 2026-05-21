# 1.2. Feladat — A valós számok NEM Boole-algebrát alkotnak

## A feladat

Igazoljuk, hogy a valós számok ℝ a szokásos összeadás (+) és szorzás (×) műveleteivel **nem** elégítik ki a Boole-algebra (BA1)–(BA14) axiómáit.

---

## Elemzés

Ellenőriznünk kell a Boole-algebra axiómáit a következő megfeleltetéssel:
- **H** = ℝ (valós számok)
- **∨** → + (összeadás)
- **∧** → × (szorzás)
- Be kell azonosítanunk: **¬** (komplemens), **⊤** (egységelem, top), **⊥** (nullelem, bottom)

---

## Az axiómák ellenőrzése

### ✅ (BA1) Kommutativitás — TELJESÜL
```
a + b = b + a  ✓
a × b = b × a  ✓
```

### ✅ (BA2) Asszociativitás — TELJESÜL
```
a + (b + c) = (a + b) + c  ✓
a × (b × c) = (a × b) × c  ✓
```

### ✅ (BA3) Disztributivitás — TELJESÜL
```
a × (b + c) = (a × b) + (a × c)  ✓  (a szorzás disztributív az összeadásra)
```
*Megjegyzés: Boole-algebrában mindkét irányú disztributivitás teljesül. ℝ-ben csak az egyik irány működik.*

### ❌ (BA4) Elnyelési tulajdonság — **NEM TELJESÜL**

A Boole-algebra megköveteli:
```
a ∨ (a ∧ b) = a    →    a + (a × b) = a  ❌
a ∧ (a ∨ b) = a    →    a × (a + b) = a  ❌
```

**Ellenpélda:** legyen a = 2, b = 3
```
2 + (2 × 3) = 2 + 6 = 8 ≠ 2  ❌
2 × (2 + 3) = 2 × 5 = 10 ≠ 2  ❌
```

### ❌ (BA5) Idempotencia — **NEM TELJESÜL**

A Boole-algebra megköveteli:
```
a ∨ a = a    →    a + a = a  ❌
a ∧ a = a    →    a × a = a  ❌
```

**Ellenpélda:** legyen a = 2
```
2 + 2 = 4 ≠ 2  ❌
2 × 2 = 4 ≠ 2  ❌
```

Csak a = 0 esetén teljesül (az összeadásra), illetve a ∈ {0, 1} esetén (a szorzásra).

### ❌ (BA6) Komplemens — **NEM TELJESÜL**

A Boole-algebra megköveteli, hogy minden a elemhez létezzen olyan ¬a, amelyre:
```
a ∨ ¬a = ⊤    →    a + (¬a) = ⊤
a ∧ ¬a = ⊥    →    a × (¬a) = ⊥
```

**A probléma:** ℝ-ben nincs olyan ¬a komplemens-művelet, amely mindkettőt kielégítené:
- Az összeadásra: $a + (\neg a) = $ valamilyen állandó ⊤
- A szorzásra: $a \times (\neg a) = $ valamilyen állandó ⊥

Ha ⊥ = 0 (additív egységelem):
```
a × (¬a) = 0  →  ¬a = 0/a = 0  (a ≠ 0 esetén)
De ekkor: a + 0 = a ≠ ⊤  ❌
```

Ha ⊥ = 1 (multiplikatív egységelem):
```
a + (¬a) = 1  →  ¬a = 1 - a
De ekkor: a × (1 - a) = a - a²  ≠ állandó  ❌
```

### ❌ (BA9)–(BA10) Egységelemek — **NEM TELJESÜL**

A Boole-algebra megköveteli ⊤ és ⊥ elemeket, amelyekre:
```
a ∨ ⊥ = a    →    a + ⊥ = a  →  ⊥ = 0  ✓
a ∧ ⊤ = a    →    a × ⊤ = a  →  ⊤ = 1  ✓

De ugyanakkor:
a ∨ ⊤ = ⊤    →    a + 1 = 1  ❌  (hamis bármely a ≠ 0-ra)
a ∧ ⊥ = ⊥    →    a × 0 = 0  ✓
```

---

## Összefoglaló táblázat

| Axióma | Tulajdonság | ℝ (+, ×)-szel |
|--------|-------------|---------------|
| BA1 | Kommutativitás | ✅ |
| BA2 | Asszociativitás | ✅ |
| BA3 | Disztributivitás | ⚠️ Részleges |
| BA4 | Elnyelési tulajdonság | ❌ |
| BA5 | Idempotencia | ❌ |
| BA6 | Komplemens | ❌ |
| BA9–BA10 | Egységelemek | ❌ |

---

## Konklúzió

**Az (ℝ, +, ×) struktúra NEM Boole-algebra**, mert több axiómát is megsért:
1. Az **elnyelési törvény** nem teljesül
2. Az **idempotencia** nem teljesül
3. Nincs **komplemens** művelet
4. Az **egységelemek tulajdonságai** nem állnak fenn

Az (ℝ, +, ×) struktúra valójában egy **test** (latinul *corpus*), ami teljesen más algebrai struktúra — más axiómarendszerrel.

---

## Mi *számít* Boole-algebrának számokon?

Összehasonlításul lásd az 1.7(e) példát a fejezetben:
- Legyen $N$ egy négyzetmentes szám
- $H = \{N \text{ osztói}\}$
- $a \vee b = \text{lnko}(a, b)$ (legnagyobb közös osztó)
- $a \wedge b = \text{lkkt}(a, b)$ (legkisebb közös többszörös)
- $\neg a = N / a$
- $⊤ = N$, $⊥ = 1$

Ez **valódi** Boole-algebrát alkot! ✓
