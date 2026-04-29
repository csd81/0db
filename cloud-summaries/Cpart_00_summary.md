# Cpart_00 összefoglaló

## A streamfeldolgozó rendszerek összehasonlításának szempontjai

Ez a rész már nem a korábbi batch jellegű adatfeldolgozásról szól, hanem arról, hogy különböző `stream processing` rendszerek között hogyan lehet választani.

- Nem elég azt nézni, hogy egy rendszer „divatos-e”.
- Fontos kérdés, hogy hosszú távon is életképes-e.
- Számít, hogy iparban elterjedt, tesztelt és megbízható megoldásról van-e szó.

Az oktató itt arra figyelmeztet, hogy technológiai döntéseknél nem csak a pillanatnyi népszerűséget kell nézni.

## Throughput és latency

A szöveg két alapvető teljesítménymutatót emel ki.

- A `throughput` azt mutatja meg, hogy adott idő alatt mennyi adatot vagy üzenetet tud feldolgozni a rendszer.
- A `latency` pedig azt, hogy egy beérkező adat után mennyi idő múlva születik eredmény.

Ez a két szempont gyakran ellentmond egymásnak: ami nagyon nagy áteresztőképességre van optimalizálva, annál gyakran nő a késleltetés is.

## Hibatűrés és programozási modell

Az oktató szerint a választásnál a megbízhatóság legalább olyan fontos, mint a sebesség.

- Fontos kérdés, hogy a rendszer `hibatűrő-e`.
- Az sem mindegy, hogyan valósítja meg ezt a hibatűrést.
- Emellett a programozási modell is lényeges:
  - `micro-batch`,
  - valódi `stream`,
  - deklaratív vagy komponálható leírás.

Ez a rész azt hangsúlyozza, hogy a fejlesztői élmény és az üzemeltetési tulajdonságok együtt határozzák meg egy rendszer értékét.

## Bevezetés a Beam szemléletbe

Innen a szöveg átfordul egy konkrétabb példába, a `Beam`-szerű programozási modell felé.

- Megjelenik a `PCollection`, vagyis egy adathalmaz vagy adatsor reprezentációja.
- A `Transform` egy feldolgozási lépést jelent.
- Az adat egyik állapotból egy másikba megy át a transzformációkon keresztül.

Ez a modell már nem közvetlenül hardverben vagy klaszterekben gondolkodik, hanem adatfolyamok és transzformációk láncolatában.

## Bounded és unbounded adat

Az oktató kétféle adatforrást különböztet meg.

- A `bounded` adat véges méretű.
- Az `unbounded` adat folyamatosan érkezik, tehát nincs természetes vége.

Ez a különbség alapvető a streamfeldolgozás megértéséhez, mert más programozási és futtatási logikát igényel.

## A pipeline felépítése

A szöveg röviden a `pipeline` alaplogikáját is bemutatja.

- Beolvasunk adatot valahonnan.
- Erre egymás után `apply` hívásokkal különféle feldolgozó lépéseket rakunk.
- A végén a `run` indítja el a teljes feldolgozást.

Ez a deklaratív stílus azt jelenti, hogy a programozó nem a végrehajtás részleteit írja le, hanem a feldolgozás szerkezetét.

## Összegzés

Az `Cpart_00.txt` fő témája a streamfeldolgozó rendszerek kiválasztásának szempontjai és a `Beam`-jellegű adatfolyam-programozás bevezetése. A szöveg bemutatja a `throughput`, a `latency`, a hibatűrés és a programozási modell jelentőségét, majd átvezet a `PCollection`- és `Transform`-alapú pipeline-szemlélethez. A központi tanulság az, hogy a modern adatfeldolgozásban egyre inkább deklaratív adatfolyamokban kell gondolkodni, nem pusztán gépekben vagy egyedi programokban.
