# Apart_09 összefoglaló

## Hibatűrés és több adatközpont használata

A szöveg elején az oktató egy olyan architektúrát magyaráz, ahol több adatközpont együtt biztosítja a szolgáltatás működését.

- Ha az elsődleges adatközponttal probléma történik:
  - földrengés,
  - áramkimaradás,
  - egyéb meghibásodás,
  akkor egy másik adatközpont átveheti a szerepét.
- A `load balancing` réteg automatikusan át tudja irányítani a kéréseket.
- Ez a működés a magas rendelkezésre állás egyik alapvető eszköze.

A fő gondolat az, hogy a felhő nem egyetlen szerverről vagy egyetlen helyről szól, hanem elosztott, redundáns infrastruktúráról.

## Cold, warm és hot készenléti módok

Az oktató három különböző rendelkezésre állási szintet különböztet meg a tartalék rendszereknél.

- `Cold VM`
  - a virtuális gép nem fut,
  - csak az image van elmentve,
  - szükség esetén újra kell indítani.
- `Warm VM`
  - a virtuális gép már fut,
  - de az alkalmazás nem feltétlenül aktív rajta.
- `Hot VM`
  - ugyanaz az alkalmazás már fut rajta,
  - ugyanúgy készen áll, mint az elsődleges központban,
  - csak éppen normál esetben nem szolgál ki kéréseket.

A különbség főként az indulási időben és a készenléti költségben van.

- A `cold` a leglassabb, de olcsóbb.
- A `hot` a leggyorsabb, de erőforrásigényesebb.

## Adatszinkronizáció és hibatűrés

A `hot` modell csak akkor működik jól, ha az adatok is rendelkezésre állnak a másodlagos helyen.

- Ezért szinkronizálni kell az adatokat az adatközpontok között.
- Így a tartalék rendszer azonnal át tudja venni a működést.
- Ez különösen fontos hibatűrő rendszereknél.

Ez a rész azt emeli ki, hogy a rendelkezésre állás nemcsak szerverindítás kérdése, hanem adatkonzisztencia és folyamatos replikáció is kell hozzá.

## Csúcsterhelés kezelése felhővel

Ugyanez az architektúra nemcsak hibakezelésre, hanem terheléselosztásra is használható.

- Elképzelhető, hogy:
  - az elsődleges adatközpont helyi infrastruktúra,
  - a másodlagos pedig felhős kapacitás.
- Csúcsidőszakban a felhős oldal át tud venni extra kéréseket.
- A vállalat választhat:
  - `cold`
  - `warm`
  - `hot`
  tartalék erőforrások közül, attól függően, milyen gyors reakció szükséges.
- Amikor a csúcsidőszak véget ér:
  - ezek az erőforrások visszaállhatnak nyugalmi állapotba,
  - és csak a következő csúcsnál aktiválódnak újra.

Ez már nagyon tipikus hibrid felhős használati minta.

## Érzékeny adatok és hibrid működés

Az oktató egy harmadik felhasználási forgatókönyvet is említ, főleg érzékeny adatok esetére.

- Vannak intézmények, például:
  - kórházak,
  - más érzékeny adatokat kezelő szervezetek,
  amelyek nem engedhetik ki a nyers adatokat a felhőbe.
- Ilyenkor az alapadatokat helyben kell tárolni és feldolgozni.
- Ugyanakkor elképzelhető, hogy:
  - az adatok aggregált,
  - anonimizált
  változata már felvihető a felhőbe.
- Ez a felhős oldal használható például:
  - statisztikai elemzésre,
  - big data feldolgozásra,
  - nem kritikus, extra feladatokra.

Ez a modell jól mutatja, hogy a helyi és felhős infrastruktúra nem feltétlenül kizárják egymást, hanem kiegészíthetik egymást.

## A felhő a felhasználó és a szolgáltató szemszögéből

Az oktató ezután összegzi, hogy a felhasználó által látott szolgáltatási szintek csak a teljes rendszer egy részét jelentik.

- A felhasználó jellemzően az alábbi rétegeket látja:
  - infrastruktúra,
  - platform,
  - szoftver mint szolgáltatás.
- A szolgáltatónak viszont ennél sokkal többet kell kezelnie.
- A háttérben megjelennek például:
  - konfigurációs feladatok,
  - hordozhatóság,
  - rendszerüzemeltetés,
  - business support,
  - könyvelés és ügyfélkezelés,
  - erőforrás-menedzsment,
  - security,
  - privacy,
  - audit.

Ez a rész arra világít rá, hogy a felhőszolgáltató szerepe sokkal összetettebb annál, mint amit a végfelhasználó érzékel.

## Jogi és megfelelőségi követelmények

A szöveg hangsúlyozza, hogy a felhőszolgáltatók komoly jogi és szabályozási környezetben működnek.

- Folyamatos auditoknak kell megfelelniük.
- Fontos területek:
  - biztonság,
  - adatvédelem,
  - teljesítmény,
  - szabályozási megfelelés.
- Ha ezeknek nem felelnek meg, elveszíthetik a működési lehetőségüket.
- Bizonyos auditok azt is tanúsíthatják, hogy:
  - egészségügyi adatok tárolására is alkalmas a rendszer.

Ez megmutatja, hogy a felhő nemcsak technológiai, hanem erősen jogi és üzleti terület is.

## EU-s adatkezelés és digitális szuverenitás

Az oktató kitér az európai adatkezelési trendekre is.

- Az `EU` egyre inkább abba az irányba halad, hogy az adatok ne hagyják el az unió területét.
- Megjelentek olyan adatközponti modellek, ahol:
  - minden alkalmazott EU-állampolgár,
  - az adatközpontnak nincs kapcsolata Európán kívüli központokkal.
- Ez részben az adatszuverenitásról szól.
- Cél lehet például:
  - az európai adatok európai kézben tartása,
  - külső országok hozzáférésének korlátozása,
  - érzékeny adatok jobb védelme.

Ez a rész már inkább jogi és politikai dimenziót ad a felhő témájához.

## Mire fókuszál majd a kurzus?

Az oktató egyértelművé teszi, hogy a tárgyban nem a teljes szolgáltatói háttérrendszert fogják tanulni.

- A kurzus fókusza marad:
  - a szolgáltatási szinteken,
  - a használati modelleken,
  - a programozott vezérlésen,
  - és azon, hogyan lehet kisebb programokat futtatni ezeken a rendszereken.
- Vagyis inkább:
  - felhasználói,
  - fejlesztői,
  - alkalmazási
  nézőpontból tárgyalják a felhőt.

Ez egy fontos keretezés: a cél nem adatközpontot üzemeltetni tanulni, hanem felhőszolgáltatásokat érteni és használni.

## Fejlesztők mint felhasználók

A szöveg végén az oktató kitér arra is, hogy nemcsak végfelhasználók, hanem fejlesztők is a felhő célcsoportjai.

- Egy fejlesztő ma már a teljes munkafolyamatát elvégezheti a felhőben.
- A felhő támogatást adhat:
  - repozitóriumokhoz,
  - fejlesztéshez,
  - teszteléshez,
  - adattároláshoz,
  - analitikához,
  - integrációhoz.
- Az üzleti rendszerekben különösen fontos az integráció:
  - meglévő rendszerek összekötése,
  - adatok és folyamatok összekapcsolása.

Ez a rész azt hangsúlyozza, hogy a felhő már nemcsak futtatási hely, hanem teljes fejlesztési és üzemeltetési ökoszisztéma.

## A számonkérés pontosítása

A hallgatói kérdésekből a számonkérésről is pontosabb kép rajzolódik ki.

- A félév végén egy `elméleti ZH` lesz.
- Ez nem hosszú esszé jellegű dolgozat lesz.
- Inkább:
  - több kérdésből áll majd,
  - egy-egy kérdésre rövidebb, fél-egy oldalas válaszokat várnak.
- A cél annak felmérése, hogy a hallgatók:
  - értik-e a főbb felhős fogalmakat,
  - átlátják-e a technológiai hátteret,
  - rendelkeznek-e általános informatikai tájékozottsággal a témában.
- `Programírás` nem lesz része az írásbeli számonkérésnek.

Ez a rész fontos gyakorlati információ a vizsgafelkészüléshez.

## A jegyzet szerepe

Az oktató megerősíti, hogy a feltöltött jegyzet lefedi az elméleti anyagot.

- A jegyzet körülbelül `118 oldalas`.
- Ez tartalmazza az elméleti hátteret.
- Az órákon nem biztos, hogy minden benne levő részt részletesen elmondanak.
- Emiatt a hallgatóknak:
  - önállóan is olvasniuk kell,
  - előrehaladhatnak a jegyzetben,
  - kérdezhetnek, ha valami kimarad vagy nem világos.

A kurzus tehát tudatosan épít az önálló tanulásra.

## Következő alkalom és további anyagok

A záró rész a következő lépésekre vonatkozik.

- A következő alkalom `március 7-én` lesz, online.
- Az oktató feltölti:
  - a diákat,
  - háttéranyagokat a gridről,
  - szolgáltatásorientáltságról,
  - és más kapcsolódó témákról.
- Kéri, hogy ezeket addig a hallgatók nézzék át.
- A könyvből különösen:
  - a `2. fejezet`,
  - és akár a `3. fejezet`
  is ajánlott.

A terv szerint a következő alkalommal már a `Google Cloud` hozzáférések beállítása és az első gyakorlati lépések következnek.

## Összegzés

Az `Apart_09.txt` lezárja a bevezető alkalmat. Egyrészt tovább részletezi a felhő gyakorlati használatának mintáit, például a több adatközpontos hibatűrést, a csúcsterhelés-kezelést és a hibrid működést érzékeny adatok esetén. Másrészt rávilágít arra, hogy a felhő mögött komoly üzemeltetési, jogi és auditkövetelmények állnak. A végén a kurzus menetének gyakorlati részletei is tisztázódnak: a számonkérés elméleti ZH lesz, a jegyzet központi szerepet kap, a következő alkalom pedig már a Google Cloud gyakorlati használata felé lép tovább.
