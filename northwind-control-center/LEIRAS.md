# Northwind Control Center — Alkalmazásleírás

## Bevezetés

A **Northwind Control Center** (NCC) egy oktatási célú, interaktív demóalkalmazás, amelyet az adatbázis-architektúra, a gráfelmélet és a földrajzi információs rendszerek (GIS) metszéspontjában fekvő témakörök szemléltetésére terveztünk. Az alkalmazás „Data-First" (adatközpontú) megközelítésű: a számításigényes feladatokat — gráfbejárás, max-flow számítás, replikációs protokollok szimulációja — a Python háttérszolgáltatások végzik el, míg a felhasználói felület valós idejű, vizuálisan gazdag eredményeket jelenít meg a böngészőben. Az elvont adatbázis-elméleti fogalmakat — tranzakciókezelés, replikációs stratégiák, hálózati folyamoptimalizálás — kézzel fogható, interaktív vizualizációkon keresztül teszi érthetővé mind hallgatók, mind szakmai közönség számára.

Az NCC hét egymástól független, mégis egységes dizájnrendszert követő demóból áll. Minden demó önálló Flask Blueprint-modulban él, saját háttérszolgáltatással, JavaScript-modullal és Jinja2-sablonnal, mégis egységes navigációs keretbe ágyazva jelenik meg.

---

## Technológiai stack

### Backend: Python és Flask

- **Flask** — Könnyűsúlyú RESTful API-átjáróként funkcionál. Minden demó saját Blueprint-modulban él (`blueprints/demos_bp.py`), tipikusan négy–öt végponttal: lapbetöltő, állapotlekérő (`/state`), indító (`/start`) és lépésenkénti vezérlők (`/step`, `/reset`). Éles telepítésnél Gunicorn vagy uWSGI munkások mögé helyezhető.

- **NetworkX** — Gráfelméleti számításokhoz. Az *Energy Flow* demóban Dinic-féle max-flow algoritmust futtat kétszer (gáz-, majd olajhálózat), és visszaadja a maradékkapacitás-alapú min-cut halmazt is. A *Global Infra Twin* topológiaszámításához és késleltetési mátrixához szintén ezt alkalmazzuk. A számítások szerveroldalon, reprodukálható lépésekben zajlanak — nem a böngészőben.

- **Pandas** — Adattranszformációhoz és az idősoros pillanatnézetek (timeline snapshot) lineáris interpolációjához. Az *Energy Flow* demóban a két rögzített pillanatfelvétel közötti hónapok kapacitásértékeit Pandas interpolálja, így a csúszka minden hónapjára pontos becsült adat áll rendelkezésre.

- **PyODBC / SQLAlchemy** — A Microsoft SQL Server Northwind mintaadatbázissal való kommunikációhoz. A routing demók városait és repülőtereit valós SQL-lekérdezések töltik be, a SQLAlchemy ORM adatbázis-agnosztikus lekérdezéseket biztosít, a PyODBC pedig alacsony szintű hozzáférést nyújt a tárolt eljárásokhoz és téradat-típusokhoz.

### Adatbázis: Microsoft SQL Server (Northwind)

Az SQL Server aktív résztvevő az üzleti logikában, nem puszta tárolóegység. A Northwind mintaadatbázis klasszikus kereskedelmi adatmodelljét (rendelések, termékek, ügyfelek, szállítók) téradatokkal és infrastruktúra-metaadatokkal bővítettük.

- **Téradatok (Spatial Data Types)** — A routing demók a csomópontokat `geography` típusú oszlopokban tárolják, lehetővé téve a haversine-alapú távolságszámítást SQL-szinten.
- **T-SQL és tárolt eljárások** — A replikációs demók és a rendelésfeldolgozás állapotátmenetei tárolt eljárásokra támaszkodnak; az állapotgép logikája az adatbázisban, nem az alkalmazásrétegben van definiálva.
- **SQL Server Agent** — A naplófájlok szállítását és a pillanatkép-generálást ütemezi; a Flask-végpontok triggerelhetnek Agent-jobokat, amelyek eredményét a `/state` végponton kérdezik le a frontendek.

### Frontend: JavaScript és vizualizációs könyvtárak

A felület nagy adatsűrűségű vizualizációra optimalizált — az egyes demók saját vizuális nyelvvel rendelkeznek (narancssárga–fekete energiaáramlás, lila–fekete algoritmuslabor, zöld–fekete infra-iker), egységes Bootstrap 5.3 alapon.

- **Leaflet.js** — 2D-s Mercator-vetítésű térképekhez. Egyéni `normalizeAntimeridian()` függvény kezeli az antimeridián-átlépő útvonalakat (pl. Panama → Japán LNG-szállítás); a tengeri útvonalak előre definiált közbülső pontok mentén kerülik el a szárazföldeket.
- **CesiumJS** — 3D-s glóbuszos nézet, lusta inicializálással (lazy init). A Cesium Entity API-t (`ColorMaterialProperty`, `arcType: GEODESIC`) alkalmazzuk polyline-megjelenítéshez; a glóbusz csak az első „3D" gombnyomásra töltődik be.
- **D3.js** — Adatvezérelt SVG-vizualizációkhoz (interaktív idővonalak, folyamatdiagramok).
- **Bootstrap 5.3 + Bootstrap Icons** — Egységes sötét téma (`#08090d` alapszín, `#f97316` kiemelőszín), kompakt sidebar-elemek, témaváltó Leaflet- és Cesium-rétegenként is átvezetett csempecserével.

---

## Demók leírása

### 1. Global Infra Twin — Globális infrastruktúra-iker

Több mint 80 aktív felhőrégió (AWS, GCP, Azure) digitális ikermodelljét jeleníti meg a világtérképen — koordinátákkal, régiók közötti késleltetési mátrixszal és CDN-jelenlét-pontokkal (PoP). A NetworkX valós idejű topológiaszámítást végez: megmutatja, hogy egy régió kiesése esetén hogyan változik a hálózat összekötöttsége és az optimális kiszolgálási útvonal.

### 2. Graph City Router — Városútvonal-kereső

Northwind-városok és repülőterek gráfján futtat legrövidebb útvonal-keresést, figyelembe véve a távolságot, a kompjárat-büntetést (`FERRY_PENALTY = 1.5`) és az A\* heurisztika epszilon-paraméterét (`ASTAR_EPSILON = 1.5`). A Dijkstra és az A\* eredményét párhuzamosan mutatja meg, szemléltetve a sebesség–pontosság kompromisszumot: az epsilon növelésével az A\* gyorsabb, de kissé szuboptimális útvonalat adhat.

### 3. Energy Flow — Globális energiaáramlás

A legösszetettebb demó. A globális kőolaj- és földgázhálózatot max-flow / min-cut algoritmussal modellezi: 88 csomópont, 141 él, kettős áruosztály (olaj: ezer hordó/nap, gáz: milliárd m³/év). A havi időcsúszka 2021 januárjától 2026 májusáig 65 pillanatfelvételt fed le; a geopolitikai sokkok (Északi Áramlat-szabotázs, húszi válság, Hormuzi-blokád) automatikusan átírják a kapacitásokat. A szűk keresztmetszetek 0–100%-os csúszkákkal kézzel is állíthatók. Legfontosabb pedagógiai üzenet: a kereszt-áru-kapcsolódás — a Hormuzi-szoros lezárása Katar LNG-exportját is megbénítja, így az európai gázhiány is megjelenik, holott csak egy olaj-keresztmetszetet változtattunk.

### 4. Snapshot Replication — Pillanatkép-replikáció

Az adatbázist egy adott pillanatban „lefényképezi", és a teljes pillanatképet eljuttatja az előfizetői adatbázisba a *kiadó → terjesztő → előfizető* pipeline-on. Az animáció lépésről lépésre követhető, a sorok átvitelének állapotával és a késleltetési mutatóval együtt. Szemlélteti, mikor érdemes ezt a replikációs formát választani: statikus riportoláshoz, ahol napi egyszeri, teljes frissítés elegendő.

### 5. Log Shipping — Naplófájl-szállítás

Katasztrófa-elhárítási (DR) fókuszú demó. A tranzakciós naplófájlok rendszeres mentését, átvitelét és `NORECOVERY` módú visszaállítását animálja az elsődleges kiszolgálóról a meleg tartalékra. A vizualizáció számszerűsíti az adatveszteség-ablakot (RPO), és egyértelművé teszi a különbséget az aszinkron Log Shipping és a szinkron tükrözés között — utóbbi nulla RPO-t garantál, de magasabb hálózati terhelés árán.

### 6. Merge Replication — Összefésülő replikáció

Kétirányú szinkronizáció: az adatot mind a kiadó, mind az előfizető oldalán lehet módosítani, az SQL Server „utolsó írás nyer" elven fésüli össze a változtatásokat, az ütközéseket ütközési naplóban rögzítve. Különösen hasznos időszakosan csatlakozó, terepen működő rendszerek esetén (raktáros kéziszámítógépek, területi laptopok), ahol a kapcsolat nem folyamatos és mindkét fél írhat az adatbázisba.

### 7. Order Fulfillment — Rendelésfeldolgozás

Egy rendelés teljes életciklusát követi nyomon öt fázison át: befogadás → fizetés → komissiózás → csomagolás → kiszállítás. Minden állapotátmenet atomikus tárolt eljárással történik, garantálva, hogy két párhuzamos felhasználó soha ne igényelhesse egyszerre az utolsó raktáron lévő terméket. Az ACID-tranzakciókezelés értékajánlatát illusztrálja: adatintegritás nagy konkurencia mellett is, explicit zárolás nélkül.

---

## Összefoglalás

A Northwind Control Center megmutatja, hogy a **Microsoft SQL Server** adatintegritása és a **Python** analitikai teljesítménye együttesen képes megbirkózni a digitális iker típusú kihívásokkal. Az alkalmazás egyben működő referencia-architektúra is: Blueprint-alapú modularitás, lusta Cesium-inicializálás, antimeridián-normalizáló kartográfia és adatbázisban definiált állapotgépek — mind azt illusztrálják, hogy a professzionális szoftvertervezési elvek oktatási kontextusban is következetesen alkalmazhatók. Az NCC végső üzenete: az adatbázis nem „fekete doboz", hanem programozható, aktív komponens, amely üzleti logikát, téradatot és replikációs protokollokat egységes keretben képes nyújtani.
