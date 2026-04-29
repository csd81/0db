# Cpart_05 összefoglaló

## A Dataproc klaszter működésének megfigyelése

Ez a rész már a futó `Dataproc` klaszter megfigyeléséről szól.

- Látszik a vezérlő és a worker node-ok szerkezete.
- Megjelennek a klaszterhez tartozó hardver- és futási információk.
- A hallgatók így nemcsak elindítják a környezetet, hanem annak belső szerkezetét is látják.

Ez a megfigyelési lépés segít összekötni az elméleti klaszterfogalmat a konkrét felhős megvalósítással.

## A π-példa kódjának értelmezése

Az oktató ismét visszatér a példakód első részére.

- Meghatározzák, hány adatponttal dolgozzon a rendszer.
- Ebből jön létre egy Spark-kompatibilis rekordhalmaz.
- Ezt a halmazt alakítja át a `map`, majd összegzi a `reduce`.

Ez azt hangsúlyozza, hogy a párhuzamos adatfeldolgozás sokszor egyszerű műveletekből épül fel, csak nagyon nagy elemszámon.

## Második példa: word count Hadoopon

A következő demonstráció egy klasszikus `word count` feladat `Hadoop MapReduce` formában.

- Szükség van egy bemeneti `words.txt` állományra.
- A feladat a szavak előfordulásainak összeszámolása.
- A kód a klasszikus `Mapper` és `Reducer` osztályokra épül.

Ez a példa közvetlen kapcsolatot teremt a korábban elméletben tárgyalt `MapReduce` modell és a valódi futtatás között.

## A mapper működése

A `mapper` feladata a részeredmények előállítása.

- Beolvassa a szöveget.
- Kiszedi az egyes szavakat.
- Minden szóhoz egy `1` értéket rendel.

Ez ugyanaz a logika, amelyet korábban már elméleti példaként is láttunk.

## A reducer működése

A `reducer` a részeredmények összegzését végzi.

- Egy adott szóhoz több érték érkezik.
- Ezeket össze kell adni.
- Az eredmény a szó teljes előfordulási száma.

Az oktató itt ismét hangsúlyozza, hogy a két fázis között a rendszer fájlrendszeren keresztül koordinálja az adatmozgást.

## Kód, bucket és futtatás

A `Hadoop`-példa futtatásához további gyakorlati lépések is kellenek.

- A kódot vagy a csomagot el kell juttatni a klaszterhez.
- Kell egy `bucket`, amely tartalmazza a bemeneti adatot.
- Ide fog kerülni a kimeneti eredmény is.

Ez jól mutatja, hogy az elosztott feldolgozásnál a kód, a tárolás és a végrehajtás együtt alkot rendszert.

## Gcloud és alternatív nyelvek

Az oktató megjegyzi, hogy a feladat nem csak a bemutatott formában hajtható végre.

- A `gcloud` parancssal is be lehet küldeni a jobot.
- A logika más nyelven, például `Python`-ban is hasonló lenne.
- A `Java` itt elsősorban illusztrációs és hagyományos példa.

Ez ismét azt mutatja, hogy az alapelv fontosabb, mint az adott nyelv vagy szintaxis.

## Összegzés

Az `Cpart_05.txt` fő témája a `Dataproc` klaszteren futtatott két klasszikus nagy adatos példa: a `π` közelítése Sparkkal és a `word count` Hadoop `MapReduce`-szal. A szöveg részletesen bemutatja a `mapper` és `reducer` logikáját, valamint azt, hogy a bemeneti adatok, a bucketek és a futtatási környezet hogyan kapcsolódnak össze. A központi tanulság az, hogy a korábban elméletben tárgyalt minták nagyon közvetlenül jelennek meg a gyakorlatban is.
