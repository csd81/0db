# Dpart_06 összefoglaló

## Storage trigger hozzáadása

Ez a rész az első `HTTP` függvény továbbfejlesztésével foglalkozik.

- A cél most már nem közvetlen HTTP-hívás,
  hanem egy `Cloud Storage` eseményre induló működés.
- A hallgatók a meglévő függvényhez próbálnak `storage` triggert kapcsolni.

Ez már átvezet a klasszikus backend, eseményvezérelt serverless mintába.

## Bucket létrehozása és kiválasztása

Ahhoz, hogy a storage esemény működjön, szükség van egy megfelelő bucketre.

- Ha nincs bucket, újat kell létrehozni.
- Ha vannak korábbi, már nem szükséges bucketek, azokat érdemes törölni.
- A kiválasztott bucket lesz az eseményforrás.

Ez ismét megmutatja, hogy a felhőszolgáltatások közötti kapcsolat konkrét erőforrásokra épül.

## Jogosultsági problémák

A demo során gyorsan kiderül, hogy a triggereléshez megfelelő jogosultságok is kellenek.

- A `Compute Engine` vagy kapcsolódó service account jogosultságot igényelhet.
- A bucketnél külön engedélyezni kell bizonyos hozzáféréseket.
- Ha ez nincs jól beállítva, a trigger nem menthető vagy nem fog működni.

Ez tipikus felhős valóság: a technikai logika mellett az IAM-beállítások is kritikusak.

## Finalize esemény

Az oktató a `finalized` típusú storage-eseményt választja.

- Ez akkor keletkezik, amikor egy objektum véglegesen bekerül a bucketbe.
- Ideális bemenete egy feldolgozó függvénynek.

Ez a leggyakoribb storage-triggerelt serverless minta egyike.

## Logok és monitorozás

A feltöltés után a függvény futását a logokban vizsgálják.

- Látható, hogy megérkezett a `storage` esemény.
- A rendszer felismeri az eseménytípust és a bucketből érkező fájlt.
- A demo itt még részben HTTP-s logikára épül, ezért nem teljesen tiszta a feldolgozás.

Ez azonban jól szemlélteti, hogy az eseményvezérelt működés valóban elindult.

## Átmenet a Pub/Sub felé

A rész végén az oktató áttér a `Pub/Sub` szolgáltatásra.

- Emlékeztet a korábban említett `Kafka`-szerű topiklogikára.
- A `Pub/Sub` lesz az eszköz a függvények közötti lazán csatolt kommunikációra.

Ez fontos építőkocka lesz a következő, összetettebb workflow-példákhoz.

## Összegzés

Az `Dpart_06.txt` fő témája az első storage-eseményre reagáló serverless megoldás létrehozása és a hozzá kapcsolódó jogosultsági, triggerelési kérdések bemutatása. A szöveg megmutatja, hogy a `Cloud Storage` könnyen lehet eseményforrás, de a tényleges működéshez pontos bucket- és IAM-beállítások is szükségesek. A központi tanulság az, hogy a serverless architektúrák egyszerűnek tűnnek, de a szolgáltatások összekötéséhez precíz felhős konfiguráció kell.
