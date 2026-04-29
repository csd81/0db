# Dpart_00 összefoglaló

## A mai téma: felhőfüggvények

Ez a rész egy új nagy témát nyit meg: a `cloud function` vagy felhőfüggvény alapú fejlesztést.

- Nem hagyományos programnyelvi függvényekről van szó.
- A cél az, hogy felhőben futó, eseményvezérelt komponensekből építsünk alkalmazásokat.
- Ezzel a kurzus a számítási technológiák magasabb absztrakciós szintjére lép.

Az oktató szerint ezzel lezárható a felhő számítási oldalának egyik fontos blokkja.

## A monolit alkalmazások problémája

A bevezetés egy hagyományos alkalmazásfejlesztési modellből indul ki.

- Sok rendszer egyetlen nagy alkalmazásként készül el.
- Ha változtatni kell valamin, gyakran az egész forráskódhoz hozzá kell nyúlni.
- Ahogy nő a rendszer, az architektúra könnyen összekuszálódik.

Ez különösen nagy rendszereknél vezet nehéz bővíthetőséghez és rossz karbantarthatósághoz.

## Skálázási nehézségek

A másik alapvető probléma a skálázhatóság.

- Egy szerveralkalmazás különböző részeit eltérő gyakorisággal használják.
- Bizonyos funkciók sokkal nagyobb terhelést kapnak, mint mások.
- Nehéz pontosan oda skálázni, ahol valóban szükség van rá.

Ez a hagyományos szerveroldali rendszereknél gyakran több példány, load balancer és összetett infrastruktúra bevezetéséhez vezet.

## A szerver nélküli szemlélet

Az oktató innen vezeti be a `serverless` gondolatot.

- Ez nem azt jelenti, hogy nincs szerver.
- Hanem azt, hogy a fejlesztőnek nem kell közvetlenül a szerverekkel foglalkoznia.
- A cél az infrastruktúra-kezelés elrejtése.

Ez a szemlélet összhangban van a felhő egyik alapígéretével: minél kevesebb operatív beavatkozással lehessen alkalmazásokat futtatni.

## A cloud function mint extrém modularitás

A felhőfüggvények mögött az a gondolat áll, hogy a modularitást a végletekig visszük.

- Egy-egy funkció önálló felhőben futó egység lehet.
- Ha egy részletet módosítani kell, sokszor elég csak azt az egy függvényt cserélni.
- Új funkciókat is könnyebb beszúrni eseményvezérelt módon.

Ez a modell radikálisan csökkentheti a teljes rendszer újrafordításának és újratelepítésének igényét.

## Összegzés

Az `Dpart_00.txt` fő témája a `cloud function` és a `serverless` fejlesztési szemlélet motivációja. A szöveg bemutatja a monolit alkalmazások karbantarthatósági és skálázási problémáit, majd ezekre válaszként vezeti be a felhőfüggvények moduláris, eseményvezérelt modelljét. A központi tanulság az, hogy a felhő egyik legnagyobb ereje nem pusztán az erőforrásbőség, hanem az, hogy újfajta szoftverarchitektúrákat tesz lehetővé.
