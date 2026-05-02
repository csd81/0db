# Bpart_00 összefoglaló

## A gyakorlati óra kiindulópontja

A szöveg elején az oktató azzal kezdi, hogy végre megérkezett a `Google Cloud` kredit, ezért a mai alkalom egyik legfontosabb feladata ennek az üzembe helyezése lesz.

- A terv szerint:
  - először egy rövid elméleti áttekintés következik,
  - utána folytatják a korábbi anyagot,
  - majd gyakorlati feladatokkal dolgoznak tovább.
- Az oktató hangsúlyozza, hogy ez az áttekintés azért kell, hogy mindenki értse, milyen környezetben fognak dolgozni.

Ez a rész tehát a gyakorlati munka előkészítése: a cél nem pusztán a szolgáltatások felsorolása, hanem egy alapvető tájékozódási keret felépítése.

## A Google Cloud mint globális infrastruktúra

Az első érdemi téma az, hogy a `Google` globális felhőszolgáltatóként működik, és ezt a világ különböző pontjain elhelyezkedő adatközpontok hálózata biztosítja.

- A térképen látható pontok az adatközpontokat jelölik.
- A zöld pontok olyan helyeket mutatnak, amelyek még építés alatt állnak.
- Az oktató kiemeli, hogy ezeknek a helyszíneknek neve van, és a felhő használatakor ezeket nekünk is ismernünk kell.

A lényeg itt az, hogy a felhő nem valami elvont rendszer, hanem konkrét földrajzi helyekhez kötött infrastruktúra, amelyből a felhasználónak választania kell.

## Régiók kiválasztása

A szöveg külön foglalkozik azzal, hogy a hallgatók melyik földrajzi régiót válasszák majd a munkához.

- Az amerikai adatközpontokat nem javasolja.
- Inkább európai régiók használatát ajánlja.
- Különösen javasolt:
  - német régió,
  - holland régió.
- Ennek fő oka a földrajzi közelség és a várhatóan gyorsabb kapcsolat.

Az oktató szerint alapvetően több európai régió is megfelelő lehet, de érdemes a fizikailag közelebbi helyeket előnyben részesíteni.

## Régiók és zónák szerepe

Az egyik legfontosabb technikai magyarázat a `régió` és a `zóna` megkülönböztetése.

- Egy régió egy adott földrajzi helyhez kötött adatközponti környezetet jelent.
- Egy régión belül több zóna található.
- A zónák olyanok, mint különálló termek vagy egységek.
- Ennek fő célja a `redundancia` és a `hibatűrés`.

Ha egy zónában probléma történik, a többi tovább működhet. Ez a felhő egyik fontos megbízhatósági alapelve.

## Miért fontos a zóna az erőforrásoknál?

Az oktató hangsúlyozza, hogy a hallgatók projektjeiben az erőforrások valójában zónaszinten jelennek meg.

- A számítási erőforrások,
- a lemezek,
- és más infrastrukturális elemek
  jellemzően egy adott zónához kötődnek.

Ezért a gyakorlatban nem elég csak annyit tudni, hogy melyik régióban dolgozunk, hanem a pontos zónát is meg kell adni. Ha ez hiányzik, a rendszer nem fog megfelelően működni.

## Globális, regionális és zónaszintű erőforrások

A szöveg kitér arra is, hogy a felhőben nem minden erőforrás ugyanahhoz a földrajzi szinthez kapcsolódik.

- `Globális` erőforrások például:
  - operációs rendszer image-ek,
  - snapshotok,
  - bizonyos hálózati beállítások.
- `Regionális` erőforrás lehet például:
  - statikus IP-cím.
- Sok más erőforrás viszont `zónaszintű`.

Ez a felosztás fontos lesz a későbbi infrastruktúra-kezelésben, mert meg kell érteni, hogy egy adott elem milyen hatókörben létezik.

## A mai gyakorlati fókusz: virtuális gép és storage

Az oktató világosan kijelöli, hogy ezen az alkalmon mely szolgáltatások lesznek a legfontosabbak.

- A fő téma a `virtuális gép`, vagyis a `Compute Engine`.
- Emellett foglalkoznak a `Storage` szolgáltatással is.
- Mindez persze attól függ, hogy a kredit aktiválása rendben működik-e.

Ez azt mutatja, hogy a mai óra az infrastruktúra-szintű szolgáltatások alapvető használatára koncentrál.

## A szolgáltatási modellek áttekintése

A szöveg másik fontos része a felhőszolgáltatások szintjeinek áttekintése.

- Az oktató három fő kategóriát említ:
  - `infrastruktúra mint szolgáltatás`,
  - `platform mint szolgáltatás`,
  - `szoftver mint szolgáltatás`.
- Ezen belül többféle szolgáltatási terület is létezik:
  - számítás,
  - adattárolás,
  - hálózat,
  - adatfeldolgozás.

Az a fontos gondolat, hogy ugyanazon a területen belül is több absztrakciós szint létezhet.

## Példák a szolgáltatási szintekre

Az oktató példát is ad arra, hogyan jelennek meg ezek a különböző szintek a gyakorlatban.

- A `Compute Engine` tipikusan infrastruktúra-szintű szolgáltatás.
- Egy kutatókörnyezet vagy magasabb szintű futtatási közeg már platformszintű lehet.
- A szerver nélküli futtatás pedig a szoftverszolgáltatási logikához áll közelebb.

Ez a rész segít abban, hogy a hallgatók ne csak termékneveket lássanak, hanem megértsék azok helyét a szolgáltatási hierarchiában.

## A dokumentáció szerepe

A szöveg végén az oktató több hivatkozást is említ, és külön felhívja a figyelmet arra, hogy a `Google Cloud` dokumentációjában nem mindig könnyű eligazodni.

- A linkek referenciaanyagként szolgálnak.
- Ezek célja, hogy a hallgatók később vissza tudjanak térni a megfelelő leírásokhoz.
- Házi feladatként is megjelenik, hogy mindenki nézzen utána, melyik termék melyik szolgáltatási szinthez tartozik.

Ez a rész azt hangsúlyozza, hogy a felhőhasználathoz nem elég csak a gyakorlati kattintgatás: a dokumentáció önálló használata is alapvető készség.

## Összegzés

A `Bpart_00.txt` fő témája egy bevezető áttekintés a `Google Cloud` működési logikájáról a gyakorlati feladatok előtt. A szöveg központi elemei a globális infrastruktúra, a régiók és zónák szerepe, valamint az, hogy a felhőben használt erőforrások különböző földrajzi szintekhez kötődhetnek. Emellett az oktató kijelöli a mai gyakorlati fókuszt is, amely elsősorban a `Compute Engine` és a `Storage`, miközben elhelyezi ezeket az infrastruktúra, platform és szoftver mint szolgáltatás tágabb rendszerében.
