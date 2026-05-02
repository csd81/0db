# Dpart_01 összefoglaló

## A felhőfüggvények előnyei

Ez a rész részletesebben fejti ki, miért tekinti az oktató erős ötletnek a `cloud function` modellt.

- A rendszer nagyon modulárissá válik.
- Egy meglévő funkció módosításához elég lehet egyetlen függvényt cserélni.
- Új funkciók könnyen beszúrhatók eseményvezérelt formában.

Az oktató szerint ez nem minden feladathoz ideális, de bizonyos problémákra rendkívül elegáns megoldást ad.

## Forráskód és futtatókörnyezet

A szöveg kitér arra is, hogyan kerül a kód a felhőbe.

- Szkriptnyelveknél a kódot egyszerűen feltöltjük.
- Fordítandó nyelveknél a telepítés során történik meg a build.
- A végén futtatásra kész állapot kerül a felhőbe.

Ez a modell eltávolítja a fejlesztőt a szerverek kézi előkészítésétől és a közvetlen üzemeltetéstől.

## Skálázhatóság függvényszinten

Az egyik legfontosabb előny a skálázás egyszerűsége.

- Ha egy függvényt sokszor hívnak meg,
  a rendszer automatikusan több példányt indíthat belőle.
- Nem kell az egész alkalmazást teljes egészében skálázni.
- A skálázás így közvetlenül a terhelt funkcióra koncentrálható.

Ez sokkal finomabb erőforráskezelést tesz lehetővé, mint a monolit alkalmazásoknál.

## Nyelvi támogatás

Az oktató kiemeli, hogy ma már szinte minden fontos nyelv támogatott.

- `JavaScript`,
- `Python`,
- `Java`,
- `Go`,
- `C#`,
- sőt akár `C++` is.

Korábban elsősorban interpretált nyelvek voltak jellemzők, de mára ez jelentősen kibővült.

## Az eseményvezérelt működés vázlata

A szöveg egy absztrakt ábrán keresztül mutatja be a működést.

- Bal oldalon különböző szolgáltatások vagy programok eseményt generálnak.
- Ezek elindítanak egy függvényt.
- A függvény feldolgoz valamit, majd akár további eseményeket generálhat.

Ez azt jelenti, hogy a teljes alkalmazás egy gráfként is felfogható, ahol a csomópontok függvények, az élek pedig események.

## Tipikus alkalmazási területek

A rész néhány gyakorlati példát is felsorol.

- Backend üzleti logika.
- Rendszerintegráció.
- Mobilbackend.
- Webalkalmazások.
- `IoT` és szenzoradatok feldolgozása.

Az oktató azt is hangsúlyozza, hogy stream jellegű feldolgozás is megvalósítható ilyen függvényláncokkal.

## Összegzés

Az `Dpart_01.txt` fő témája a felhőfüggvények gyakorlati előnyeinek és tipikus használati módjainak bemutatása. A szöveg tárgyalja a moduláris módosíthatóságot, a függvényszintű skálázást, a nyelvi támogatást és az eseményvezérelt alkalmazásgráf gondolatát. A központi tanulság az, hogy a `serverless` modell nem csupán kényelmi eszköz, hanem egészen új tervezési mintákat tesz lehetővé.
