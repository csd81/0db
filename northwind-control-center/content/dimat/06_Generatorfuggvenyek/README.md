# 6. fejezet - Generátorfüggvények (Generating Functions)

## Tartalomjegyzék

- [6.0 Alapfogalmak](#60-alapfogalmak)
- [6.1 Lineáris rekurziók](#61-lineáris-rekurziók)
- [6.2 Newton binomiális sora](#62-newton-binomiális-sora)
- [6.3 Nemlineáris rekurziók](#63-nemlineáris-rekurziók)
- [6.4 Exponenciális generátorfüggvények](#64-exponenciális-generátorfüggvények)

---

## 6.0 Alapfogalmak

### Generátorfüggvény definíció (6.0)

Az $(a_n)_{n=0}^{\infty}$ sorozat **generátorfüggvénye**:

$$F(x) = \sum_{n=0}^{\infty} a_n x^n$$

**Fontos:** Az $a_n$ együttható az $x^n$ tag együtthatója!

### Megjegyzések

1. **Index = kitevő:** A sorozat $n$-edik tagja az $x^n$ együtthatója
2. **Konvergencia:** Feltesszük, hogy a sor konvergens 0 egy környezetében
3. **Eltolás:** Ha $b_n = a_{n-1}$, akkor $G(x) = xF(x)$
4. **Történet:** Moivre, Euler, Laplace fejlesztették ki

---

## 6.1 Lineáris rekurziók

### Fibonacci sorozat (6.3 példa)

**Rekurzió:** $f_n = f_{n-1} + f_{n-2}$, $f_0 = 0, f_1 = 1$

**Generátorfüggvény levezetése:**

$$\begin{aligned}
\sum_{n=2}^{\infty} f_n x^n &= \sum_{n=2}^{\infty} f_{n-1} x^n + \sum_{n=2}^{\infty} f_{n-2} x^n \\
F(x) - f_0 - f_1 x &= x(F(x) - f_0) + x^2 F(x) \\
F(x) - x &= xF(x) + x^2 F(x) \\
F(x)(1 - x - x^2) &= x \\
F(x) &= \frac{x}{1 - x - x^2}
\end{aligned}$$

**Parciális törtekre bontás:**

$$F(x) = \frac{1}{\sqrt{5}}\left(\frac{1}{1 - \phi x} - \frac{1}{1 - \psi x}\right)$$

ahol $\phi = \frac{1+\sqrt{5}}{2}$, $\psi = \frac{1-\sqrt{5}}{2}$

**Sorbafejtés:**

$$F(x) = \frac{1}{\sqrt{5}}\sum_{n=0}^{\infty}(\phi^n - \psi^n)x^n$$

**Explicit képlet (Binet):**

$$f_n = \frac{\phi^n - \psi^n}{\sqrt{5}}$$

---

### Hanoi tornyai (6.4 példa)

**Rekurzió:** $h_{n+1} = 2h_n + 1$, $h_0 = 0$

**Generátorfüggvény:**

$$\begin{aligned}
\sum_{n=0}^{\infty} h_{n+1} x^{n+1} &= 2x \sum_{n=0}^{\infty} h_n x^n + x \sum_{n=0}^{\infty} x^n \\
H(x) &= 2x H(x) + \frac{x}{1-x} \\
H(x)(1 - 2x) &= \frac{x}{1-x} \\
H(x) &= \frac{x}{(1-x)(1-2x)}
\end{aligned}$$

**Parciális törtek:**

$$H(x) = \frac{1}{1-2x} - \frac{1}{1-x}$$

**Explicit képlet:**

$$h_n = 2^n - 1$$

---

### 6.5 Módszer - Általános eljárás

**k-adrendű lineáris inhomogén rekurzió:**

$$a_n = d_1 a_{n-1} + d_2 a_{n-2} + \cdots + d_k a_{n-k} + b_n$$

**Lépések:**
1. Szorozzuk meg mindkét oldalt $x^n$-nel
2. Összegezzünk $n \geq k$-ra
3. Fejezzük ki $F(x)$-szel
4. Oldjuk meg az algebrai egyenletet $F(x)$-re
5. Bontsuk parciális törtekre
6. Fejtsük sorba az együtthatókhoz

---

### 6.6 Tétel - Racionális generátorfüggvények

**Állítás:** $(a_n)$ generátorfüggvénye pontosan akkor racionális törtfüggvény (ahol $x=0$ nem gyök), ha $(a_n)$ kielégít egy állandó együtthatójú homogén lineáris rekurziót.

$$F(x) = \frac{p(x)}{q(x)} \iff a_n = d_1 a_{n-1} + \cdots + d_k a_{n-k}$$

---

## 6.2 Newton binomiális sora

### Általánosított binomiális tétel (3.4)

$$(a + x)^\alpha = \sum_{n=0}^{\infty} \binom{\alpha}{n} a^{\alpha-n} x^n$$

ahol $|x| < |a|$ és

$$\binom{\alpha}{n} = \frac{\alpha(\alpha-1)\cdots(\alpha-n+1)}{n!}$$

### Speciális esetek

**Negatív kitevő:**
$$(1-x)^{-k} = \sum_{n=0}^{\infty} \binom{n+k-1}{k-1} x^n$$

**Félegész kitevő:**
$$(1-x)^{-1/2} = \sum_{n=0}^{\infty} \binom{2n}{n} \frac{x^n}{4^n}$$

---

## 6.3 Nemlineáris rekurziók

### Catalan számok

**Rekurzió:**
$$C_0 = 1, \quad C_{n+1} = \sum_{i=0}^{n} C_i C_{n-i}$$

**Generátorfüggvény:**

$$C(x) = \sum_{n=0}^{\infty} C_n x^n$$

A rekurzióból:
$$C(x) = 1 + x C(x)^2$$

**Megoldás:**
$$C(x) = \frac{1 - \sqrt{1-4x}}{2x}$$

**Explicit képlet:**
$$C_n = \frac{1}{n+1}\binom{2n}{n}$$

**Értékek:** 1, 1, 2, 5, 14, 42, 132, 429, ...

**Alkalmazások:**
- Zárójelezések száma
- Bináris fák száma
- Hegyláncok

---

## 6.4 Exponenciális generátorfüggvények

### Definíció

**Exponenciális generátorfüggvény:**

$$E(x) = \sum_{n=0}^{\infty} a_n \frac{x^n}{n!}$$

### Alkalmazás

Permutációk számolásánál hasznos, ahol a faktoriálisok természetesen megjelennek.

### Kapcsolat a szokásos generátorfüggvénnyel

Ha $F(x) = \sum a_n x^n$ és $E(x) = \sum a_n \frac{x^n}{n!}$, akkor bizonyos transzformációkkal átalakíthatók egymásba.

---

## Összefoglaló táblázat

| Sorozat | Rekurzió | Generátorfüggvény | Explicit |
|---------|----------|-------------------|----------|
| Fibonacci | $f_n = f_{n-1} + f_{n-2}$ | $\frac{x}{1-x-x^2}$ | $\frac{\phi^n - \psi^n}{\sqrt{5}}$ |
| Hanoi | $h_n = 2h_{n-1} + 1$ | $\frac{x}{(1-x)(1-2x)}$ | $2^n - 1$ |
| Mértani | $a_n = r a_{n-1}$ | $\frac{a_0}{1-rx}$ | $a_0 r^n$ |
| Catalan | $C_{n+1} = \sum C_i C_{n-i}$ | $\frac{1-\sqrt{1-4x}}{2x}$ | $\frac{1}{n+1}\binom{2n}{n}$ |

---

## Kulcstechnikák

### 1. Generátorfüggvény felírása
- Szorzás $x^n$-nel
- Összegzés megfelelő indexre
- $F(x)$ kifejezése

### 2. Parciális törtekre bontás
- Nevező gyöktényezőkre bontása
- Együtthatók meghatározása

### 3. Sorbafejtés
- Mértani sor: $\frac{1}{1-x} = \sum x^n$
- Newton binomiális sor
- Ismert sorfejtések felhasználása

### 4. Együtthatók leolvasása
- $[x^n]F(x) = a_n$

---

## Hivatkozások

- [Sa] Sárközy András: Generátorfüggvények
- [W] Wilf: Generatingfunctionology
- [SzIs;97] Szalkai: Feladatgyűjtemény

---

*Forrás: Dr. Szalkai István - Diszkrét Matematika*
