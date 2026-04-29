# Cpart_06 összefoglaló

## Gyakorlati nehézségek és lassú futások

Ez a rész még a `Dataproc`-gyakorlat lezárásához kapcsolódik.

- Nem mindenkinél indul vagy fejeződik be gyorsan a feladat.
- Az eredmények kiolvasása sem mindig egyértelmű.
- Az oktató emiatt fokozatosan átvezet a következő nagy témára.

Ez jól mutatja, hogy a nagy adatos felhőgyakorlatoknál a futási idő és az eredmények elérése önmagában is tanulási kérdés.

## Miért nem elég a batch feldolgozás?

A következő központi kérdés az, hogy mi történik akkor, ha az adat folyamatosan változik.

- A `batch` feldolgozásnál feltételezzük, hogy az egész adat egyszerre rendelkezésre áll.
- Sok valós helyzetben ez nem igaz.
- Vannak olyan alkalmazások, ahol az adatra azonnal reagálni kell.

Ezzel kezdődik a `stream processing` indokolása.

## Valós idejű példák

Az oktató több olyan területet említ, ahol folyamatos adatsorral kell dolgozni.

- `szenzoradatok`,
- környezetfigyelés,
- közlekedési kamerák,
- `önvezető autók`.

Ezeknél nem lehet megvárni egy teljes nap vagy nagy adathalmaz beérkezését, mert a reakciónak gyakorlatilag azonnalinak kell lennie.

## A memória korlátja

Nemcsak az időbeliség miatt kell más modell.

- Nagy adatnál sokszor nem fér be minden memória.
- Ilyenkor sem lehet egyszerre, egyben kezelni az egész halmazt.
- Az adatot szeletekben kell feldolgozni.

Ez a rész fontos, mert megmutatja: a streamszerű feldolgozás néha nemcsak „valós idejű”, hanem egyszerűen erőforrás-korlátok miatt szükséges.

## Batchből stream-szerű gondolkodás

Az oktató rámutat, hogy ha egy nagy adathalmazt szeletekben kezelünk, az sok szempontból streamhez hasonló működést eredményez.

- Nem az egész adatot látjuk egyszerre.
- Részletekben jönnek a feldolgozható elemek.
- A rendszernek folyamatosan újra és újra kell dolgoznia.

Ez átmenetet képez a batch és a stream világ között.

## Összegzés

Az `Cpart_06.txt` fő témája az átmenet a `batch` feldolgozásból a `stream processing` felé. A szöveg hangsúlyozza, hogy sok valós alkalmazásban az adatok folyamatosan érkeznek, azonnali reakció szükséges, illetve a teljes adathalmaz egyszerre nem is férne memóriába. A központi tanulság az, hogy a nagy adatos rendszereknél a folyamatos vagy szeletelt adatfeldolgozás nem kivétel, hanem sokszor alapkövetelmény.
