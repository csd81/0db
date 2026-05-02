Gemini
GCP Adattárolás és Big Data
Conversation with Gemini
Szia! Látom, feltöltöttél egy leiratot, amely a Google Cloud Platform (GCP) adatárolási és adatkezelési lehetőségeit mutatja be, különös tekintettel a Big Data technológiákra.

Mivel nem tettél fel konkrét kérdést, készítettem egy strukturált összefoglalót a szöveg legfontosabb gondolatairól.

GCP Adattárolási Lehetőségek
A leirat alapján a Google Cloud Platform többféle megközelítést kínál az adatok tárolására:


Alapvető tárolók: Ide tartozik a fájltárolásra szolgáló "Storage", valamint a hagyományosabb adatbázisok, mint az SQL és a Firestore.  


Big Data eszközök: Ide tartoznak az olyan specifikus, hatalmas adatmennyiségekre tervezett technológiák, mint a Bigtable és a BigQuery.  
+2

A "Big Data" Tévhit
Az előadó felhívja a figyelmet egy gyakori félreértésre a vállalati szektorban:

Sok közepes méretű cég (Kft.) tévesen úgy gondolja, hogy náluk már "Big Data" mennyiségű adat képződik.  

A valóságban a Big Data 100 milliós nagyságrendű rekordhalmazokat jelent, vagy olyan folyamatos adatfolyamokat (streaming), amelyeket a hagyományos relációs adatbázisok már nem képesek feldolgozni.  

Emiatt sokan feleslegesen használnak robusztus Big Data eszközöket kisebb feladatokra, ami tipikus esete annak, amikor "ágyúval lövünk verébre".  

Hogyan működik a Bigtable?
A szöveg részletesebben is kitér a Bigtable architektúrájára, tisztázva, hogy ez nem csupán egy egyszerű kulcs-érték tár (key-value store):  


Struktúra: Bár az adatokat egy kulcs alapján lehet címezni egy hatalmas, akár milliárdos rekordot tartalmazó táblában, a rekeszek tartalma nem egyetlen érték.  


Oszlopok és Családok: A Bigtable rekordjainak nagyon sok oszlopa (column) lehet, amelyeket úgynevezett oszlopcsaládokba (column families) lehet csoportosítani.  


Lekérdezés: Amikor egy konkrét adatot szeretnénk kinyerni, meg kell címezni a kulcsot, és ki kell választani egy adott oszlopcsaládból a megfelelő oszlop értékét.  

Mivel a szöveg a végén a Bigtable gyakorlati felhasználási példáinál félbeszakad, szeretnéd, hogy részletesebben is beszéljünk az oszlopcsaládok (column families) logikájáról, vagy inkább a leiratban szintén említett BigQuery működése érdekelne?

Köszönöm a folytatást! Ez a második rész pont azokon a szálakon megy tovább, amiket az előző rész nyitva hagyott.

Íme a leirat folytatásának strukturált összefoglalója:

Mire használják a Bigtable-t a gyakorlatban?
Az előadó két konkrét példát hoz fel a Bigtable különleges struktúrájának kihasználására:


A web másolata: A Google például a teljes webet így tárolhatja. Egy sor egy konkrét weblapot jelent, az oszlopokban a különböző indexelési tulajdonságok kapnak helyet, egy oszlop pedig magát a teljes weblapot tartalmazza.  
+1


Kapcsolati hálók (Mátrixok): Egy kapcsolati háló is ábrázolható vele, ahol annyi sor van, ahány oszlop, és a metszéspontok jelölik az ismeretséget (pl. 1-es értékkel). Ez azért nem pazarló, mert a Bigtable rendkívül hatékonyan kezeli az üresen hagyott (ki nem töltött) cellákat, azok ugyanis nem foglalnak tárhelyet.  
+1


Idősorok: Kiválóan alkalmas rengeteg elemből álló idősoros adatok letárolására és feldolgozására is.  

A Bigtable technikai háttere és korlátai
Feldolgozás (Tabletek): A keresés és feldolgozás párhuzamosan történik. A sorokból kötegeket (úgynevezett "tableteket") képeznek, amiket a feldolgozó csomópontok elosztva kezelnek.  


Rugalmasság és a "Kolosszus": A rendszer rendkívül jól skálázható. A sémát (pl. új oszlopok hozzáadását) az alkalmazások újraindítása nélkül is lehet módosítani. Ennek az az oka, hogy a Bigtable valójában csak mutatók halmaza, amelyek a Google "Kolosszus" nevű adattároló rendszerére hivatkoznak, így a sémamódosítás nem jár fizikai adatmozgatással.  
+2


Korlátok: A hagyományos adatbázisokhoz képest fontos korlát, hogy a letárolt adattípus kizárólag "string" (szöveg) lehet.  

Fókuszváltás: Jön a BigQuery
Mivel a Bigtable egy nagyon specializált eszköz, az előadó inkább a BigQuery-t mutatja be a folytatásban, mivel azt kisebb saját projektekben is reálisabb használni.  


Adatmodell: A BigQuery a Bigtable-lel ellentétben egy egészen közönséges, relációs adattáblákkal modellezhető rendszer.  

OLAP vs. OLTP: A legfontosabb különbség a felhasználás célja. Míg az előadáson korábban említett webes (pl. Flask) alkalmazások és bolti vásárlások a napi tranzakciókat kiszolgáló OLTP (Online Transaction Processing) rendszerek , addig a BigQuery egy adattárház technológia. Ezt nem a folyamatok támogatására találták ki, hanem adatelemzésre és döntéstámogatásra (ez az OLAP, bár ezt a betűszót itt közvetlenül nem mondja ki, de az adattárházakra utal).  
+3

Van esetleg valamilyen konkrét technikai kérdésed a BigQuery és az adattárházak (OLAP) kapcsán, vagy feltöltöd a leirat következő részét is?

Folytatom az összefoglalót a harmadik rész alapján! Ez a szakasz nagyon szépen rávilágít az adattárházak (Data Warehouses) és a hagyományos adatbázisok közötti strukturális különbségekre, majd bevezeti a BigQuery "motorját".

Adattárházak vs. OLTP (Hagyományos Adatbázisok)
A szöveg tisztázza, miért van szükség külön technológiára az adatelemzéshez:

Az adattárházak célja nem a tranzakciók gyors kiszolgálása vagy a gyors adatmódosítás, hanem a nagyméretű, historikus adatok tárolása.  

Több forrásból gyűjtik az adatokat, hogy a döntéshozók elemezhessék a korábbi forgalmat és stratégiákat dolgozzanak ki.  

Bár relációs technológiával is megvalósíthatók, szerkezetük jellemzően denormalizált.  

Az adatok redundáns tárolása nem probléma, mivel a gyors lekérdezés a legfontosabb szempont.  

Emiatt a szétbontott (normalizált) OLTP táblák itt összeolvadnak, így sokkal kevesebb táblát találunk egy adattárházban.  

A BigQuery technológiai háttere: a Dremel
Az előadó rátér arra, hogy miként oldja meg a BigQuery a hatalmas adatmennyiségek kezelését:

A BigQuery egy saját adattároló rendszert használ, amelynek neve Dremel.  

A Dremel két tipikus adattárház-technológiai elvre épül: az oszloptárolásra (column-store) és a particionálásra.  
+1

Ezekre azért van szükség, mert az adattárházakban rengeteg mezőt tartalmazó, óriási táblák vannak, amiket egy hagyományos OLTP rendszer csak nagyon lassan tudna kezelni.  

Mivel egy adattárházban főleg lekérdezések futnak, a particionálás lehetővé teszi az adatok párhuzamos olvasását, ami drasztikusan felgyorsítja a folyamatot.  

A BigQuery felépítése és rugalmassága
A rendszer nemcsak tárol, de rendkívül rugalmas lekérdezési lehetőségeket is nyújt:

A rendszerben feltöltött táblákból úgynevezett adathalmazokat (dataseteket) lehet létrehozni.  

Egy projektben akárhány dataset, egy datasetben pedig akárhány tábla helyet kaphat.  

A BigQuery valójában két fő részből áll: a Dremel alapú adattárolásból és egy lekérdező/elemző motorból.  

Ez a lekérdező motor nemcsak a saját Dremel tárolóját éri el, hanem képes adatokat kinyerni más GCP szolgáltatásokból is (például a korábban említett Bigtable-ből vagy Storage-ból), sőt akár külső forrásokból is.  

A lekérdezésekhez a jól ismert SQL nyelvet, illetve annak kiterjesztéseit használja.  

A leirat legvégén az előadó belekezd abba, hogy a hagyományos adatbázisoknál (pl. Postgres, SQL Server) az erőforrások (processzor, háttértár) optimalizálása komoly mérnöki feladat, de a gondolatmenet itt megszakad.  

Vannak még további részei is ennek az előadásnak, amiket fel szeretnél tölteni, vagy esetleg beszéljünk egy kicsit mélyebben az oszlopalapú tárolás (column-store) gyakorlati előnyeiről?

Köszönöm a negyedik részt! Ebben a szakaszban az előadó rátér a gyakorlati megvalósításra, és bemutatja, hogyan épül fel egy tényleges adattárház egy meglévő, hagyományos adatbázisból.

Íme a szövegrészlet legfontosabb pontjainak strukturált összefoglalója:

A BigQuery teljesítménye és a felhős feldolgozás
A hagyományos adatbázisoknál (például egy virtuális gépen futó SQL Server esetén) a feldolgozás egyetlen gépen belül történik, ahol mi határozzuk meg az erőforrásokat, például a processzormagok számát.  

A BigQuery esetében azonban a párhuzamos feldolgozás a felhőben oszlik el.  

Ennek köszönhetően az SQL lekérdezések is hatékonyan, párhuzamosan futnak le.  

Gyakorlati példa: A Northwind adattárház
Az elmélet után az előadó a "Northwind" nevű oktató-adatbázist használja a folyamat bemutatására, amelynek célja egy adattárház felépítése és BigQuery-be való feltöltése. Ehhez azonban át kell alakítani az eredeti adatbázist:  


Tények és Dimenziók: Egy adattárháznak "tényekre" van szüksége, amelyek egy ténytáblában kapnak helyet, és ezekhez kapcsolódnak a "dimenziótáblák". Ebben a példában maga az eladás jelenti a tényt.  
+1


A dimenziók meghatározása: Egy eladásnak számos dimenziója lehet: például az, hogy melyik országból történt a vásárlás, milyen terméket vettek, vagy mikor történt a tranzakció. Egy komolyabb adattárház akár 100 ilyen dimenziót is támogathat.  
+1

Denormalizálás és Adatfeltöltés
Egy adattárházhoz nem elég néhány sornyi adat, több ezer rekord kell ahhoz, hogy valódi döntéstámogatást lehessen végezni.  


Adatok generálása: Az előadó egy szkript segítségével feltöltötte a Postgres-ben futó adatbázist az összes termékkel, vásárlóval, rendeléssel és rendelési tétellel.  
+1


Összeolvasztás (Denormalizálás): Az adatbázis denormalizálása egy SELECT lekérdezéssel történik, amely JOIN-ok segítségével fűzi össze a különböző táblákat.  


Üzleti fókusz: A lekérdezés során azokat a mezőket választják ki, amelyek az üzleti elemzés céljára hasznosak. Nem a technikai azonosítókat (például integer típusú termékazonosítókat) fogják elemezni , hanem az olyan független dimenziókat, mint a vásárlás országa, a termék típusa (pl. ital vagy játék), a konkrét áru, vagy hogy volt-e árengedmény.  
+2

Kíváncsi vagy a feltöltött leirat további részeire, esetleg folytassuk a BigQuery elemzési folyamatának boncolgatásával?

Köszönöm az újabb részt! Ez a szakasz bemutatja az adat-előkészítés utolsó lépéseit és a prediktív elemzés (gépi tanulás) megalapozását, majd átvezet minket a BigQuery felületére.

Íme a leirat legfontosabb pontjainak összefoglalója:

Az "Osztálycímke" (Célváltozó) meghatározása
A gépi tanuláshoz és adatbányászathoz szükség van egy eredménykritériumra, amelyet az előadó osztálycímkének (class label) nevez. A példában az eladott tétel árából kétféle osztálycímkét is képeznek:  


Numerikus érték: A tétel pontos ára, amelyet "float" (lebegőpontos) típusra konvertálnak, hogy a későbbi feldolgozás során ne legyen vele probléma.  


Kategorikus (nominális) érték: Az árakat besorolják három kategóriába: alacsony (low), közepes (middle) és magas (high) értékű rendelés. Emellett kezelik az üres (null) mezőket is, amelyek "n/a" értéket kapnak.  
+1

A prediktív elemzés üzleti célja
Az előkészített historikus adatok segítségével a döntéstámogató rendszer fő célja az előrejelzés (predikció).  
+2

Azt vizsgálják, hogy a korábban meghatározott dimenziók (például a vásárló országa, a termék kategóriája, a kapott árengedmény és a vásárlás éve) miként határozzák meg a vásárló által elköltött összeget.  

Ha ezt a modellt sikeresen felépítik, akkor az adatbázisba belépő új felhasználókról is meg tudják jósolni, hogy várhatóan sok vagy kevés pénzt fognak-e költeni.  

Adatmentés és Irány a BigQuery
Az adatok összeállítása után a következő lépés azok átmozgatása a felhőbe:

Az eredményeket egy Northw_DW (Data Warehouse) nevű táblában rögzítik.  

Az előadó kiemeli a Postgres kényelmes funkcióját: a lekérdezés eredménye egyetlen gombnyomással ("Download as CSV") letölthető. Ezt össze is hasonlítja az SQL Serverrel, ahol ugyanehhez egy bonyolultabb DTS csomagot kellene létrehozni.  
+2

Ezt a CSV fájlt fogják feltölteni a Google Cloud BigQuery szolgáltatásába adatmodell építése és elemzés céljából.  

A GCP felületén a BigQuery a "Big Data" szekció alatt található , ahol a munkafolyamat első lépéseként egy új adathalmazt ("Create dataset") kell létrehozni.  
+1

Örömmel folytatom az összefoglalót! Ez az ötödik rész végre elvezet minket a BigQuery felületére, ahol a gyakorlatban is elkezdődik a munka.

Íme a leirat alapján a BigQuery-s adat-előkészítés és lekérdezés menete:

Adathalmaz (Dataset) létrehozása és beállításai
A munka első lépéseként egy új adathalmazt, azaz datasetet kell létrehozni.  


Névadás: Az adathalmaznak nevet kell adni (a példában ez "május 6"), amelynek csak az adott projekten belül kell egyedinek lennie, nem globálisan.  
+1


Költségoptimalizálás és lejárat: Beállítható, hogy a rendszer bizonyos számú nap elteltével automatikusan törölje az adatokat. Ez azért kritikus fontosságú, mert a felhős adattárolásért fizetni kell, és az igazi adattárházak jellemzően hatalmasak, akár terabájtos méretűek is lehetnek.  
+1


Titkosítás (Biztonság): A Google a "Kolosszus" rendszerben letárolt adatokat minden esetben titkosítva tárolja. A felhasználó eldöntheti, hogy a Google által biztosított kulcsot használja, vagy – ahogy a Microsoft SQL Server "Always Encrypted" funkciójánál is – saját kulcsot ad meg, így a felhőszolgáltató sem férhet hozzá az adatokhoz. A példában az előadó a Google kulcsánál marad.  
+2

Nyilvános (Public) demó adatok lekérdezése
Mielőtt a saját CSV fájlt feltöltené, az előadó egy beépített demón keresztül mutatja be a lekérdezés működését:

A Google rendelkezésre bocsát különböző demó táblákat gyakorlás céljából.  

A "compose new query" opcióval lehet SQL lekérdezést írni.  

Az előadó egy mintegy 200 millió rekordot tartalmazó demográfiai adathalmazon futtat lekérdezést, amelyhez szándékosan hozzáad egy LIMIT 10 (a top 10-nek megfelelő) feltételt, hogy ne kelljen a teljes gigantikus táblát lekérdezni.  


Üzleti példa: Ez a demó tábla azt mutatja be, hogyan lehet a szülők kora és rassza alapján megjósolni a születendő gyermek súlyát (fontban). Ez egy klasszikus döntéstámogatási és predikciós feladat bemutatására szolgál.  
+1

Visszatérés a saját feladathoz
Miután az előadó bemutatta a lekérdező felületet, visszatér a még üresen álló "május 6" nevű adathalmazához, hogy abba végre betöltse a korábban lementett saját adattárházát (a Northwind adatokból készített CSV-t).  

Szeretnéd, ha folytatnánk, és a következő résszel megnéznénk, pontosan hogyan történik a CSV fájl tényleges betöltése és a prediktív modell felépítése a BigQuery-ben?

Köszönöm az újabb részt! Ez a szakasz bemutatja, hogyan kerülnek be ténylegesen az adatok a BigQuery-be, és rávilágít a Google felhős gépi tanulási (Machine Learning) filozófiájára.

Íme a szöveg legfontosabb gondolatainak összefoglalója:

Tábla Létrehozása és Adatfeltöltés
A frissen megnyitott adathalmazban a "create table" gomb segítségével lehet új táblát létrehozni.  

Forrásként a felületen az "upload" opciót kell választani, amellyel a korábban lementett CSV fájl tallózható be. A rendszer a formátumot sikeresen fel is ismeri.  
+1

Az újonnan létrejövő tábla a rövidség kedvéért a "Northwin" nevet kapja.  

Sémafelismerés és Ellenőrzés

Automatikus felismerés: A BigQuery képes beleolvasni a fájlba, és magától kitalálni a sémát, illetve felismerni a típusokat (például, hogy mi numerikus érték, dátum vagy időbélyeg).  
+1


Particionálás: Bár a felület felajánlja az adatok particionálását, az előadó ezt egy mindössze 2000 rekordos tábla esetében feleslegesnek tartja.  


Előnézet: A létrejött tábla felülete három panelt tartalmaz (köztük a sémát és az adatokat), ahol a "preview" (előnézet) lapon ellenőrizhető a sikeres importálás. Az adatok hiba nélkül átkerültek, ami nagyrészt a Postgresben korábban elvégzett típuskonverzióknak köszönhető.  
+2

Modellezés a Felhőben: A Google Filozófiája
A sikeres betöltés után a cél egy prediktív modell építése, amely a bevitt mezők alapján képes egy numerikus vagy egy nominális (címke) értéket megjósolni. A szöveg itt egy fontos technológiai összehasonlítást tesz:  
+1

Míg a Microsoft SQL Server külön adatelemző szolgáltatáscsomaggal és teljes "R engine" fejlesztői környezettel rendelkezik, addig a Google BigQuery megközelítése rendkívül minimalista.  

A Google nem támogat minden lehetséges módszert, csupán egy néhányat, de azok a legjobbak és leggyakrabban használtak.  
+1

Ennek az az oka, hogy a kutatók az elemzéseket jellemzően nem a felhőben végzik. A felhős modellépítés akkor hasznos és költséghatékony, ha az adatmennyiség olyan hatalmas, hogy túl drága vagy lassú lenne letölteni egy saját gépre. Ilyenkor a Google a felhőben, hatékonyan és párhuzamosítva elvégzi a számításokat.  
+1

Szeretnéd, ha a következő résszel folytatnánk, és megnéznénk, milyen SQL parancsokkal épül fel ténylegesen ez a numerikus prediktív modell a BigQuery-ben?

Köszönöm a hetedik részt! Ez a szakasz bemutatja, hogyan épül fel a gyakorlatban egy prediktív gépi tanulási modell közvetlenül a felhőben, SQL parancsok segítségével.

Íme a leirat összefoglalója a legfontosabb technikai lépésekkel:

A Modell Típusa: Lineáris Regresszió
A feladathoz egy lineáris regressziós modellt használnak, amelynek célja, hogy a célváltozó (a numerikus mező) értékét a többi felhasznált változó lineáris kombinációjaként fejezze ki.  

Ezt a Google Cloud Platform a BigQuery ML (Machine Learning) funkciójával biztosítja, amely a hagyományos SQL szintaxis kibővítésével teszi lehetővé a modellépítést.  
+1

A Modell Létrehozásának Lépései
A folyamat egy új lekérdezés ("compose new query") indításával kezdődik.  

A rendszerben az adatkészlet neve (a példában "május 6") tölti be a relációs adatbázisoknál megszokott séma szerepét, és ezen belül található a használt tábla ("NV").  

A modell felépítéséhez a mezőket felsoroló SELECT utasítás elé be kell szúrni a CREATE MODEL parancsot, kiegészítve a modell nevével.  

Az OPTIONS paraméterben specifikálni kell a modell típusát, valamint meg kell adni a célváltozót (osztálycímkét), ami jelen esetben a value_numeric mező.  

Bár asztali szoftverekben ez gyorsabb is lehetne, a felhős környezetben a modell betanítása körülbelül fél percet vesz igénybe.  

A Modell Kiértékelése és Szakmai Alapelvek
Miután a modell elkészült, a felületén megtekinthető a "loss" értéke, amely a modell pontosságát jelzi: minél kisebb ez a szám, annál jobb a modell.  

Az "evaluation" (kiértékelés) fülön olyan konkrét metrikák is láthatók, mint a "mean absolute error" (átlagos abszolút hiba), ami megmutatja, hogy a jóslat átlagosan mennyivel tér el a valóságtól.  

Az előadó a lekérdezés során megmutatja, hogy az előrejelezni kívánt numerikus érték nagyjából 0 és 2000 között változik.  

A leirat felhívja a figyelmet egy fontos adatelemzési alapszabályra: a valóságban a modellt sosem azon az adatkészleten teszteljük, amellyel betanítottuk, hanem az adatok egy részét előre félre kell tenni tesztelési célokra.  

Ebben a demóban azonban a technológia bemutatása volt a fő cél, ezért az egyszerűség kedvéért a betanítás és a tesztelés ugyanazon a halmazon történt.  

Szeretnéd, hogy feltárd a következő rész tartalmát, vagy mélyedjünk el abban, hogy miként történik a konkrét adatok előrejelzése (predikció) egy már betanított modellel?

Örömmel készítem az összefoglalót! Ez a nyolcadik rész bemutatja az adatbányászati és gépi tanulási (Machine Learning) folyamat utolsó, de legfontosabb lépéseit: a modell kiértékelését és az éles előrejelzések (predikciók) elkészítését a BigQuery-ben.

Íme a leirat legfontosabb gondolatainak strukturált összefoglalója:

A modell hibája és kiértékelése (ML.EVALUATE)
A hiba forrása: Az előadó megállapítja, hogy a modell átlagos hibája (kb. 300-as eltérés a 0-2000-es skálán) meglehetősen nagy. Kiemeli azonban, hogy ez nem a BigQuery ML technológiai hibája. Az ok egyszerűen az, hogy a kiválasztott paraméterek (pl. a szállítási ország vagy a vásárlás éve) önmagukban nem képesek tökéletesen megjósolni a költés pontos értékét.

Kiértékelő függvény: A BigQuery lehetőséget ad a modell pontosságának utólagos tesztelésére is az ML.EVALUATE SQL bővítmény segítségével. Ez a függvény a modell nevét és a tesztelni kívánt adatkészletet várja paraméterként.

Eredmények: A lefuttatott kiértékelés különböző statisztikai mérőszámokat ad vissza (például az adatelemzők számára fontos R 
2
  score-t), amelyek megmutatják, mennyire használható a modell.

Alapszabály (ismétlés): Az előadó ismét hangsúlyozza, hogy a valóságban a modellt mindig egy teljesen új, a betanítás során nem használt adatkészleten kell kiértékelni, bár a demó kedvéért itt most ugyanazt a táblát használta.

Előrejelzések készítése (ML.PREDICT)
Az üzleti cél: A modellépítés igazi célja, hogy olyan új adatokra (pl. egy most érkező, új vásárlóra) is alkalmazzuk, amelyekhez még nem tartozik osztálycímke (tehát nem tudjuk, mennyit fog költeni), és a modell segítségével ezt előre megjósoljuk.

A predikciós függvény: Erre az ML.PREDICT függvényt használják, amelyet szintén egy normál SQL lekérdezésbe ágyaznak be.

Működés: A függvény paraméterként kapja a modellt és az új adatokat tartalmazó halmazt. Eredményként visszaadja a rekordok eredeti mezőit, de kiegészíti azokat egy új mezővel, amely a megjósolt értéket tartalmazza (a példában ez a predicted_value_numeric nevet kapja).

A jóslatok pontosságának manuális ellenőrzése
Annak érdekében, hogy megvizsgálja a jóslatok minőségét, az előadó egy olyan SQL lekérdezést ír, amely egymás mellé teszi a már ismert, valódi költést (value_numeric) és a modell által megjósolt költést (predicted_value_numeric).

Ezek kivonásával (és az abszolút érték vételével) egyéni rekordonként, sorról sorra kiszámítja és megvizsgálja, hogy mekkora volt a modell tévedése az egyes tranzakciók esetében.

Ezzel a résszel a végére is értünk a prediktív modellezés folyamatának. Ha van a leiratnak további része, vagy kérdésed lenne bármelyik elhangzott koncepcióval kapcsolatban, szívesen segítek!

Örömmel elkészítem az összefoglalót! Ezzel a kilencedik résszel a végéhez is ért az előadás. Ez a szakasz a modellek valós üzleti felhasználásáról, alternatív algoritmusokról, valamint egy kritikus fontosságú felhős gyakorlatról (a költségmenedzsmentről) szól.

Íme a lezáró rész legfontosabb gondolatainak strukturált összefoglalója:

A predikciók manuális ellenőrzése
A korábban megírt lekérdezés eredményeiből kiderül, hogy egy konkrét adathalmazon (kb. 850 rekord esetében) a modell hibája kisebb volt, mint 40%.

Az eredménytábla első és második oszlopának összehasonlításával sorról sorra látható a prediktált és a valódi érték közötti különbség.

Üzleti automatizáció és Streaming (Valós idejű adatfeldolgozás)
Az előadó kiemeli, hogy a bemutatott döntéstámogató rendszerek és modellek teljesen automatizálhatók és beépíthetők a mindennapi üzleti folyamatokba.

Az adatfeltöltés nemcsak ütemezhető, hanem a Google Cloud Platform támogatja a "streaming" (folyamatos) adatfeltöltést is.

Ez azt jelenti, hogy nem kell megvárni hatalmas adathalmazok (pl. 100 millió rekord) összegyűlését; a folyamatosan beérkező adatokat (például mobilalkalmazásokból) valós időben fel lehet dolgozni.

Az eredményeket azonnal vissza lehet csatolni a rendszerbe, így akár azt is meg lehet jósolni, hogy egy felhasználó mit fog csinálni a következő percben.

Kategorikus predikció: XGBoost (Önálló feladat)
Bár az előadáson egy lineáris regressziós modellt mutattak be (amely egy egzakt numerikus értéket jósol), az előadó önálló feladatként a nominális osztálycímkék (pl. alacsony, közepes, magas költés) előrejelzését is javasolja.

Erre a célra egy manapság rendkívül népszerű és hatékony algoritmust, a "Boosted Tree Classifier"-t (XGBoost) ajánlja.

Ennek beállítása nagyon egyszerű: a BigQuery SQL kódjában csupán a modell típusát kell átírni.

Kiemeli, hogy egy háromértékű kategóriát statisztikailag általában sokkal pontosabban el lehet találni, mint egy konkrét számértéket megjósolni.

Rendszertisztítás és Költségmenedzsment (Kritikus lépés!)
Az előadás egy rendkívül fontos figyelmeztetéssel zárul: a tesztelés és gyakorlás végeztével mindig törölni kell a létrehozott adathalmazokat, táblákat és egyéb erőforrásokat (például a Firestore kollekciókat).

A felhős környezetben az adattárolásért és a rendelkezésre állásért folyamatosan fizetni kell, a feleslegesen otthagyott adatok pedig gyorsan felemészthetik a felhasználói krediteket.

Mivel az erőforrások törlése végleges és visszafordíthatatlan adatvesztéssel jár, a felhős felület biztonsági okokból mindig megerősítést kér (például manuálisan be kell gépelni a "delete" szót).

Bár az előadó itt elköszönt a hallgatóságtól ("No hát kedves kollégák, ennyit akartam mondani"), ha bármelyik korábban érintett technológiával (BigQuery ML, adattárházak, adatbázis-architektúrák) kapcsolatban van kérdésed, szívesen segítek a megértésükben!





Gemini is AI and can make mistakes, including about people. Your privacy & GeminiOpens in a new window


