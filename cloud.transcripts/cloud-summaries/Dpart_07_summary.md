# Dpart_07 összefoglaló

## A Pub/Sub szerepe

Ez a rész a `Google Pub/Sub` szolgáltatás bevezetésével foglalkozik.

- Ez egy publish-subscribe alapú üzenet- és eseménytovábbító rendszer.
- Függvények és más felhőszolgáltatások között lehet vele kommunikálni.
- Kifejezetten jól illeszkedik eseményvezérelt architektúrákhoz.

Az oktató ezt úgy vezeti be, mint a korábbi `Kafka`-jellegű gondolkodás felhős megfelelőjét.

## Managed, skálázható szolgáltatás

A `Pub/Sub` is tipikus menedzselt felhőszolgáltatás.

- Automatikusan skálázódik.
- Nem kell a háttérben futó infrastruktúrával foglalkozni.
- Biztonságos és nyelvfüggetlen módon használható.

Ez jól illeszkedik a serverless szemlélethez: az alkalmazáslogikára koncentrálunk, nem az üzenetközvetítő klaszter üzemeltetésére.

## Topic mint központi fogalom

Az egész rendszer középpontjában a `topic` áll.

- A publisher egy topicra küld üzenetet.
- A subscriber egy topicra iratkozik fel.
- A topic így egy logikai közvetítő csatorna.

Az oktató ezt várakozási sorhoz vagy központi adattovábbító ponthoz hasonlítja.

## Push és pull kézbesítés

Két fő kézbesítési mód létezik.

- A `pull` esetén a kliens kérdezi le, jött-e új üzenet.
- A `push` esetén a szolgáltatás küldi ki automatikusan az adatot.

Ez fontos különbség, mert más infrastruktúrát és más működési mintát feltételez.

## Acknowledge és megbízhatóság

Az üzenetkezelés egyik kulcseleme a visszajelzés.

- A fogyasztónak jeleznie kell, hogy megkapta és feldolgozta az üzenetet.
- Addig az üzenet a rendszerben perzisztensen tárolódik.
- Ez csökkenti az üzenetvesztés esélyét.

Ez a rész az üzenetszintű megbízhatóság alapmechanizmusát mutatja be.

## Különböző kommunikációs minták

A Pub/Sub nemcsak egy-egy pont közti kommunikációra használható.

- `many-to-one`,
- `one-to-many`,
- `many-to-many`
  minták is kialakíthatók.

Ez teszi alkalmassá bonyolultabb eseménygráfok és többfogyasztós rendszerek kialakítására.

## Összegzés

Az `Dpart_07.txt` fő témája a `Google Pub/Sub` működésének alapmodellje. A szöveg bemutatja a topic, publisher és subscriber szerepét, a `push` és `pull` kézbesítést, az `acknowledge` fontosságát, valamint a különféle kommunikációs topológiákat. A központi tanulság az, hogy a serverless rendszerek valódi összetettségét gyakran nem a függvények önmagukban, hanem az ezeket összekötő esemény- és üzenetkezelési réteg adja.
