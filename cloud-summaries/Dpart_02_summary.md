# Dpart_02 összefoglaló

## Két alapvető függvénytípus

Ez a rész már a `cloud function` konkrét típusaival foglalkozik.

- Az egyik a `HTTP function`.
- A másik a `background function`.

Ez a felosztás az alapján történik, hogy milyen esemény indítja el a függvényt.

## HTTP függvények

Az `HTTP function` közvetlen webes kérésre reagál.

- Tipikusan frontend vagy API jellegű feladatokra való.
- Egy címre érkező kérés indítja el.
- A válasz közvetlenül a kliens felé megy vissza.

Ez a modell közel áll egy hagyományos webes végpont logikájához, csak menedzselt felhős formában.

## Background függvények

A `background function` nem HTTP-kérésből indul.

- Felhőn belüli események triggerelik.
- Például `Cloud Storage`, `Pub/Sub` vagy más szolgáltatási események.
- Ezek inkább backend jellegű feldolgozásokhoz alkalmasak.

Ez jól elkülöníti a felhasználói interakciókat a belső, aszinkron rendszerfolyamatoktól.

## Példa: storage esemény

Az oktató konkrét példát is mond.

- Ha egy bucketbe új fájl kerül,
  az eseményt generálhat.
- Ez elindíthat egy adatfeldolgozó függvényt.

Ez az egyik legegyszerűbb, de nagyon tipikus serverless munkafolyamat.

## Deploy és konfiguráció

A függvény használata több lépésből áll.

- Meg kell írni a kódot.
- Telepítéskor meg kell adni a futtatási környezetet.
- Meg kell mondani, milyen eseményre induljon.
- Később a futás monitorozható is.

Ez a rész kiemeli, hogy a függvényeknél a telepítés maga is konfigurációs lépés, nem pusztán fájlfeltöltés.

## Telepítési módok

Az oktató több telepítési lehetőséget is említ.

- `gcloud` parancssorból.
- Forráskód letöltése egy távoli repóból.
- Közvetlenül a böngészős konzolból.

A gyakorlati részben először a konzolos, vizuális megközelítést fogják használni.

## Függvényindító események

A szöveg kitér az első generációs `Cloud Functions` eseménykészletére is.

- A `HTTP` mellett több klasszikus eseménytípus elérhető.
- Ilyen a `Storage`, a `Pub/Sub`, a `Firestore`, a `Firebase` és más szolgáltatási trigger.

Ez a lista mutatja, hogy a függvények valóban sokféle felhős folyamat köztes elemeként használhatók.

## Összegzés

Az `Dpart_02.txt` fő témája a felhőfüggvények típusainak, telepítésének és triggerelésének gyakorlati bemutatása. A szöveg elkülöníti a `HTTP` és a `background` függvényeket, majd ismerteti a telepítési módokat és a tipikus eseményforrásokat. A központi tanulság az, hogy a `serverless` alkalmazások tervezésénél az indító esemény típusa alapvetően meghatározza a függvény szerepét és használati mintáját.
