# Epart_01 összefoglaló

## A Bigtable logikai modellje

Ez a rész a `Bigtable` belső adatmodelljét magyarázza el.

- Az alapegység a tábla.
- A táblában sorok és oszlopok vannak.
- Minden sornak egyedi kulcsa van.

Az oktató kiemeli, hogy a sorkulcs nem egyszerű sorszám, hanem összetettebb azonosító is lehet.

## Oszlopcsaládok

A Bigtable egyik fontos szervezőelve az `oszlopcsalád`.

- Logikailag összetartozó oszlopok egy családba rendezhetők.
- Ennek a lekérdezési és teljesítménybeli oldalról is jelentősége van.

Ez közelebb viszi a modellt a nagy volumenű tárolás és gyors elérés közötti kompromisszumok világához.

## Több érték egy cellában

Az egyik legfontosabb különbség a klasszikus táblákhoz képest, hogy egyetlen cellában több érték is lehet.

- Egy sor és egy oszlop metszete nem feltétlenül egyetlen értéket jelent.
- Az értékekhez `időbélyeg` tartozik.
- Így ugyanazon cella története is tárolható.

Ez különösen alkalmassá teszi a rendszert idősoros adatok kezelésére.

## Ritka táblák működése

Az oktató példán keresztül is megmutatja a működést.

- Ha egy sor-oszlop metszetben nincs adat,
  a rendszer nem foglal helyet rá.
- Ha több érték van, azok időbélyeggel együtt jelennek meg.

Ez egyszerre hatékony helykezelést és időbeli követhetőséget ad.

## Összegzés

Az `Epart_01.txt` fő témája a `Bigtable` logikai adatmodellje. A szöveg bemutatja a sorokat, oszlopokat, oszlopcsaládokat és az időbélyeges cellaértékeket, valamint a ritka táblák helytakarékos működését. A központi tanulság az, hogy a Bigtable táblaképe csak első ránézésre hasonlít egy hagyományos adatbázistáblára; valójában sokkal inkább időbélyeges, kulcs-érték alapú adattároló modell.
