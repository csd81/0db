# Cpart_04 összefoglaló

## A Monte Carlo módszer bevezetése

Ez a rész a `Dataproc`-on futtatandó első példa matematikai hátterét magyarázza el: a `π` értékének közelítését véletlen pontok segítségével.

- Egy egységsugarú kör és egy befoglaló négyzet arányából indulnak ki.
- Ha sok véletlen pontot generálunk a négyzetben,
  akkor a körbe eső pontok aránya közelíti a `π/4` értéket.
- Innen a `π` közelítő értéke egyszerűen kiszámolható.

Ez a példa jól alkalmas párhuzamos feldolgozás bemutatására, mert nagyon sok egymástól független számítást igényel.

## A szekvenciális program logikája

Az oktató először egy hagyományos, egygépes gondolkodásmódot vázol fel.

- Véletlen `x` és `y` koordinátákat generálunk.
- Ellenőrizzük, hogy a pont a körön belülre esik-e.
- Ha igen, növeljük a találatok számát.
- A végén a találatok és az összes próbálkozás arányából számoljuk ki a közelítést.

Ez a rész azért fontos, mert megmutatja, miből indulunk ki, mielőtt a problémát elosztott feldolgozássá alakítjuk.

## A Spark-féle átírás

Ezután a feladat `Spark`-szerű adatfeldolgozó formát kap.

- Létrejön egy adatstruktúra, amely sok próbálkozást reprezentál.
- A `map` lépés minden elemhez eldönti, hogy a pont a körön belül van-e.
- A kimenet `1` vagy `0`.
- A `reduce` ezeket összeadja.

Ez jól mutatja, hogyan alakítható egy egyszerű matematikai algoritmus adathalmazokon végzett párhuzamos műveletté.

## Lambda-alapú feldolgozás

Az oktató röviden kitér a programozási formára is.

- A `map` és `reduce` lépések lambda-kifejezésekkel vannak definiálva.
- A `map` minden rekordot önállóan kezel.
- A `reduce` részeredményeket egyesít.

Ez a funkcionális stílus közel áll a modern elosztott feldolgozó keretrendszerek szemléletéhez.

## A job beküldése Dataprocra

A gyakorlat következő része a feladat tényleges elindítása a klaszteren.

- A `Dataproc` felületén új `job`-ot kell létrehozni.
- Mivel példaprogramról van szó, nem kell saját kódot építeni.
- Elég a megfelelő helyről megadni a futtatandó csomagot és paramétereket.

Ez már a tényleges felhős végrehajtás első kézzelfogható lépése.

## A demó bizonytalansága

Az órán természetesen itt is előfordulnak technikai nehézségek.

- A futás nem mindig indul elsőre hibátlanul.
- Az eredmény és a logok megjelenése sem mindig egyértelmű.
- Az oktató ennek ellenére igyekszik megmutatni a működési logikát.

Ez a rész jól érzékelteti, hogy a felhős demók és gyakorlatok sokszor nem tökéletesen simák, de a mögöttük álló modell ettől még jól megérthető.

## Összegzés

Az `Cpart_04.txt` fő témája a `π` közelítésének `Monte Carlo` jellegű példája mint párhuzamos feldolgozási feladat. A szöveg bemutatja a matematikai alapötletet, a szekvenciális megoldást, majd annak `Spark`-szerű `map`/`reduce` átírását. A központi tanulság az, hogy az egymástól független, tömegesen ismételhető számítások különösen jól illeszkednek az elosztott adatfeldolgozó rendszerekhez.
