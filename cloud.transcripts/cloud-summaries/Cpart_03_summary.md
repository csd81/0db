# Cpart_03 összefoglaló

## A Dataproc-gyakorlat célja

Ez a rész egy új gyakorlati blokk eleje, amelyben a hallgatók `Dataproc` klasztert hoznak létre a `Google Cloud`-ban.

- A cél egy működő `Hadoop`/`Spark`-kompatibilis klaszter felállítása.
- Erre később konkrét példaprogramokat fognak futtatni.
- Az oktató arra kéri a hallgatókat, hogy lépésről lépésre kövessék a leírást.

Ez a gyakorlat már közvetlenül a nagy adatos feldolgozórendszerek használatához kapcsolódik.

## API-k és jogosultságok

A klaszter létrehozása előtt több előfeltételnek is teljesülnie kell.

- Engedélyezni kell a szükséges `API`-kat.
- Meg kell adni a megfelelő jogosultságokat a rendszerkomponenseknek.
- Ha ezek hiányoznak, a klaszter nem fog elindulni.

Ez a rész ismét azt mutatja, hogy a felhőben a szolgáltatáshasználat sokszor adminisztratív és jogosultsági előkészítést is igényel.

## Régióválasztás a gyakorlatban

Az oktató itt külön kiemeli, hogy a dokumentációban ajánlott régió nem biztos, hogy működik.

- A példák gyakran amerikai régiókkal számolnak.
- A gyakorlatban azonban célszerű inkább európai régiót választani.
- Nem minden régió működik egyformán jól minden hallgatónál.

Ez konkrét gyakorlati tapasztalat arra, hogy a tutorialok és a valós működés nem mindig fedik egymást pontosan.

## A költségveszély Dataproc esetén

Az oktató erősen figyelmeztet a klaszterek költségére.

- Egy elfelejtett klaszter nagyon gyorsan fogyasztja a kreditet.
- Saját példát is említ arra, hogy rövid idő alatt jelentős összeg eltűnhet.
- A gyakorlat végén ezért kötelező a klaszter törlése.

Ez a rész különösen fontos, mert a `Dataproc` jóval drágább és összetettebb erőforrás lehet, mint egy egyszerű VM.

## Eltérő hozzáférési állapotok a hallgatóknál

Nem mindenkinek működik ugyanúgy a felhőelérés.

- Van, akinél a klaszterindítás sem megy.
- Van, akinek a hozzáférés vagy a kuponaktiválás akadt el.
- Az oktató azt javasolja, hogy ilyenkor a hallgatók párokban dolgozzanak.

Ez a rész jól mutatja az oktatási gyakorlat rugalmasságát: nem mindenkinél működik egyszerre minden, ezért együttműködésre van szükség.

## A job indításának elhalasztása

Az oktató külön kéri, hogy először csak a klaszter induljon el.

- A feladatot, vagyis a `job`-ot még ne indítsák el rögtön.
- Előbb legyen biztos, hogy maga a környezet működik.
- A feldolgozási logika megbeszélése csak ezután következik.

Ez jó mérnöki munkamódszer: először a platform legyen stabil, csak utána fusson rajta feladat.

## Összegzés

Az `Cpart_03.txt` fő témája a `Dataproc` klaszter létrehozásának gyakorlati előkészítése. A szöveg bemutatja az API-k és jogosultságok szerepét, a régióválasztás fontosságát, a klaszterek költségkockázatát és a hallgatók eltérő hozzáférési helyzeteit. A központi tanulság az, hogy nagy adatos felhős gyakorlatoknál a környezet felállítása önmagában is összetett feladat, és ennek sikeressége megelőzi a tényleges adatfeldolgozó jobok futtatását.
