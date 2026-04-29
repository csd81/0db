# Cpart_02 összefoglaló

## Összegzés az eddigi felhős szintekről

Ez a rész lezárja az addig tárgyalt felhős feldolgozási szinteket.

- Elindultak a `virtuális gépektől`.
- Áttértek a `storage` használatára.
- Utána a klaszteralapú `Dataproc`- és `MapReduce`-szerű feldolgozás következett.
- Most pedig egy még magasabb szintű, `Dataflow`-jellegű modell jelenik meg.

Az oktató ezzel tudatosan mutatja meg a felhő absztrakciós lépcsőit.

## Az absztrakció emelkedése

A szöveg egyik legfontosabb gondolata az, hogy egyre kevésbé a hardverrel foglalkozunk.

- Először még közvetlenül virtuális gépeket kezeltünk.
- Később már klasztert hoztunk létre.
- A `Dataflow` szintjén viszont már inkább csak a feldolgozási gráfot írjuk le.

Ez az a pont, ahol a felhő valódi ígérete láthatóvá válik: a fejlesztő egyre kevésbé foglalkozik az infrastruktúra részleteivel.

## A futtatás elrejtése

Az oktató külön hangsúlyozza, hogy magasabb szinten a rendszer futtatását már a platform végzi.

- A programozó nem azt mondja meg, melyik gépen mi történjen.
- Ehelyett a logikát küldi be a szolgáltatásba.
- A háttérben a platform elvégzi a szükséges futtatási és skálázási feladatokat.

Ez a `platform mint szolgáltatás` szemlélet lényege.

## Figyelmeztetés a költségekre

A rész végén még egyszer előkerül az operatív fegyelem.

- A létrehozott klasztereket törölni kell.
- Ha valami futva marad, az fogyasztja a kreditet.
- A felhőhasználat egyik alapelve továbbra is az, hogy semmi ne maradjon fölöslegesen aktív állapotban.

Ez megint összeköti a magas szintű technológiát a nagyon is gyakorlati költségkezeléssel.

## Átvezetés a következő alkalomra

Az oktató jelzi, hogy a következő órákon tovább mennek a magasabb szintű feldolgozási modellek felé.

- A `MapReduce` után a `stream processing` következik.
- Később `cloud functions`, `serverless` és analitikai témák is elő fognak kerülni.
- A kurzus íve az alap infrastruktúrától az adatfeldolgozásig vezet.

Ez a rész jól összerendezi az addigi szétszórt témákat.

## Ismétlés a MapReduce-ról

Mivel új alkalom kezdődik, az oktató röviden visszafoglalja a `MapReduce` alapgondolatát is.

- Van egy `map` fázis, amely részekre bont és átalakít.
- Van egy `reduce` fázis, amely összegzi a részeredményeket.
- Ez főként `batch` típusú, véges adathalmazok feldolgozására alkalmas.

Ez a visszatekintés előkészíti a következő gyakorlati feladatot is.

## Összegzés

Az `Cpart_02.txt` fő témája az eddig tanult felhős feldolgozási szintek összefoglalása és az új alkalom átvezetése. A szöveg azt hangsúlyozza, hogy a hallgatók a virtuális gépektől fokozatosan jutottak el a klasztereken át a magasabb szintű `Dataflow`-jellegű feldolgozásig. A központi tanulság az, hogy a felhő egyik legfontosabb értéke az absztrakció fokozatos emelése: a fejlesztő egyre kevésbé a hardverrel, és egyre inkább a feldolgozási logikával foglalkozik.
