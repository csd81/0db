# Bpart_08 összefoglaló

## A big data problémaköre

Ez a rész az infrastruktúra-kezelésről áttér a nagy adatmennyiségek feldolgozásának kérdésére.

- Nagy adatoknál nemcsak a számítás,
  hanem az adatmozgatás ideje is kritikus lehet.
- Sok esetben az `I/O` és a hálózati kommunikáció dominálja a teljes futási időt.

Az oktató ezzel megalapozza, hogy miért van szükség speciális feldolgozási modellekre.

## A 3V modell

A `big data` jelenséget a szöveg egy klasszikus háromtényezős modellel írja le.

- `Volume`: nagyon nagy mennyiségű adat.
- `Velocity`: gyorsan változó vagy gyorsan érkező adat.
- `Variety`: sokféle adatforma és struktúra.

Ha ez a három jellemző együtt jelenik meg, akkor a hagyományos adatkezelési megoldások gyakran már nem elegendők.

## Batch és stream feldolgozás

Az oktató két alapvető feldolgozási módot különböztet meg.

- A `batch` feldolgozásnál bemenő állományokból indulunk ki, és kimenő állományokat kapunk.
- A `stream` feldolgozásnál az adat folyamatosan érkezik és folyamatosan készül az eredmény.

Ez a különbség alapvetően meghatározza a programozási modellt és a rendszer felépítését is.

## A batch feldolgozás jelentősége

Ebben a szakaszban elsősorban a `batch` jellegű feldolgozás kerül előtérbe.

- Itt az adat előre rendelkezésre áll.
- A teljes adathalmazon kell futtatni a műveletet.
- A cél az, hogy ezt párhuzamosan és hatékonyan lehessen végrehajtani.

Ez a modell jól illeszkedik a klasszikus nagy adathalmazos elemzési feladatokhoz.

## Hadoop és Spark

Az oktató megemlíti a legismertebb elosztott feldolgozási környezeteket.

- A `Hadoop` az egyik korai, meghatározó rendszer.
- A `Spark` ennek későbbi, gyorsabb és hatékonyabb alternatívája.
- Mindkettő nagy, többgépes környezetben kezeli a statikus adathalmazokat.

Ez a rész a felhőn belüli nagy adatfeldolgozás ipari hátterét mutatja be.

## A MapReduce iránya

A szöveg hangsúlyozza, hogy a következő konkrét téma a `MapReduce` jellegű feldolgozási modell lesz.

- Ez egy egyszerűnek tűnő programozási séma.
- A lényege, hogy több gépen fut párhuzamosan.
- Nagy mennyiségű adat gyors feldolgozását teszi lehetővé.

Az oktató előre jelzi, hogy ehhez később gyakorlati anyagokat is kapnak majd a hallgatók.

## Alkalmazási területek

A rész felsorol néhány tipikus felhasználási területet is.

- `logelemzés`,
- `adatbányászat`,
- `gépi tanulás`,
- tudományos számítások.

Ezek közös jellemzője, hogy nagyon sok adatot kell kezelni és abból gyorsan kell mintázatokat vagy eredményeket kinyerni.

## Miért más az adatfeldolgozó klaszter?

Az oktató összehasonlítja a hagyományos párhuzamos számítási rendszereket a nagy adatos klaszterekkel.

- Tudományos számításoknál sokszor a számítás maga drága.
- Adatfeldolgozásnál viszont gyakran az adatmozgatás a szűk keresztmetszet.
- Ezért nem célszerű az adatot állandóan ide-oda küldözgetni.

Ez a különbség a rendszerarchitektúra egész logikáját meghatározza.

## A számítás odavitele az adathoz

A `Hadoop` egyik legfontosabb ötlete, hogy nem az adatot mozgatjuk a programhoz, hanem a programot visszük az adathoz.

- Az adat eleve szét van osztva a klaszter gépei között.
- Minden gép a helyben található adaton dolgozik.
- Így jelentősen csökkenthető a hálózati adatmozgatás.

Ez a szemléletváltás a modern nagy adatos rendszerek egyik alapelve.

## A klaszter szerkezete

A rész végén megjelenik a klaszter felépítése is.

- Van központi erőforrás-kezelés.
- A node-ok helyben hajtják végre a feladatokat.
- A menedzsment figyeli, melyik gép milyen állapotban van.

Ez előkészíti a következő rész részletesebb `MapReduce`-magyarázatát.

## Összegzés

Az `Bpart_08.txt` fő témája a `big data` feldolgozás szemléleti és architekturális alapjainak bemutatása. A szöveg tárgyalja a 3V modellt, a `batch` és `stream` feldolgozás különbségét, a `Hadoop` és a `Spark` szerepét, valamint azt az alapelvet, hogy nagy adathalmazoknál a számítást érdemes az adathoz vinni. A központi tanulság az, hogy a nagy adat kezelésében nemcsak a számítási teljesítmény, hanem az adatmozgatás minimalizálása is döntő fontosságú.
