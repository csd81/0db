# Bpart_02 összefoglaló

## A cloud storage további költségei

Ez a rész a `Cloud Storage` használatához kapcsolódó költségeket folytatja.

- Nemcsak a tárolásnak van ára,
  hanem a műveleteknek és az adatforgalomnak is.
- Az első műveleti és forgalmi mennyiségek részben ingyenesek lehetnek.
- A hálózati kommunikáció azonban később fizetőssé válik.

Az oktató ezzel azt hangsúlyozza, hogy a felhőben az adat nemcsak „ott van”, hanem a hozzá kapcsolódó hozzáférési és mozgatási műveletek is pénzbe kerülnek.

## Tárolási osztályok használati gyakoriság szerint

A szöveg részletesen tárgyalja a különböző storage-osztályokat.

- A `standard` tárolás folyamatosan, azonnal elérhető.
- A `nearline` ritkább, nagyjából havi hozzáférésre való.
- A `coldline` még ritkább, több hónapos hozzáférési ciklusra alkalmas.
- Az `archive` archiválási célú, nagyon ritka eléréssel.

Minél ritkábban akarjuk használni az adatot, annál olcsóbb lehet a tárolás.

## Miért olcsóbb az archivált adat?

Az oktató megmagyarázza a költségkülönbség technikai hátterét is.

- A gyakran elérendő adatot gyors, online tárolókon kell tartani.
- Az archivált adat lehet sokkal lassabb médián.
- Ilyenkor a visszaolvasás is több időt vesz igénybe.

Ez jól mutatja, hogy a tárolási osztályok mögött valós infrastrukturális különbségek vannak.

## Példaarchitektúra: médiafeldolgozás

A rész egyik szemléletes példája egy médiastreamelő rendszer.

- A médiafájlok a `Storage`-ban vannak.
- Egy `Compute Engine` példány végzi a feldolgozást vagy kódolást.
- Az eredmény egy másik rendszerhez kerül továbbításra.

Ez a példa azt mutatja meg, hogy a felhő szolgáltatásai tipikusan külön „dobozokként” működnek, amelyeket össze kell kapcsolni.

## A szolgáltatások dobozos architektúrája

A szöveg fontos szemléleti eleme, hogy a felhő komponensekből épül fel.

- Egy-egy szolgáltatás egy meghatározott feladatot végez.
- Az alkalmazások ezek összekapcsolásával jönnek létre.
- A rendszertervezés lényege sokszor éppen az, hogy az adat a megfelelő komponensek között haladjon végig.

Ez a felhő egyik alapvető architekturális gondolata.

## A storage ára hosszú távon

Az oktató konkrét példákkal hasonlítja össze a felhős és helyi adattárolás költségeit.

- Kis méretnél a költség még kezelhetőnek tűnik.
- Több terabájtnál azonban a havi díj gyorsan jelentőssé válik.
- Helyi merevlemezekhez képest a felhős tárolás sokszor jóval drágábbnak látszik.

Ugyanakkor a felhő ezért cserébe megbízhatóságot, replikációt, mentést és üzemeltetési garanciát ad.

## A nagy mennyiségű adat feltöltésének problémája

A rész végén az oktató kiemeli, hogy a nagy adatmennyiségek kezelése nemcsak pénzkérdés.

- Már maga a `feltöltési idő` is komoly akadály lehet.
- Több tíz vagy száz terabájt feljuttatása nagyon sok időbe telhet.
- Ez a gyakorlatban sokszor legalább akkora probléma, mint maga a tárolási költség.

Ez a gondolat előrevetíti a nagy adatmennyiségek felhős kezelésének valódi gyakorlati nehézségeit.

## Átmenet a gyakorlati részre

A szöveg második felében lezárul az elméleti bevezető, és megkezdődik a gyakorlati munka.

- Az első feladat a `Google Cloud` kredit aktiválása.
- A hallgatóknak egy adott linken keresztül kell elindítaniuk az érvényesítést.
- A rendszer az egyetemi email-cím alapján ellenőrzi a jogosultságot.

Ezzel megkezdődik a tényleges belépés a felhőplatform használatába.

## Összegzés

Az `Bpart_02.txt` fő témája a `Cloud Storage` költség- és használati modelljének lezárása, majd az átmenet a gyakorlati kreditaktiválási folyamathoz. A szöveg bemutatja a storage-osztályokat, a hosszú távú költségeket, a komponensalapú felhőarchitektúrát és a nagy adatmennyiség feltöltésének problémáját. A rész végén az elméletből a gyakorlati belépés felé mozdul a hangsúly, a Google Cloud kredit érvényesítésének első lépéseivel.
