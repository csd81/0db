# Northwind Control Center – Rendszerdokumentáció

**Verzió:** 1.0 &nbsp;|&nbsp; **Készült:** 2026. április &nbsp;|&nbsp; **Platform:** Python / Flask + Microsoft SQL Server

---

## 1. Rendszeráttekintés

A **Northwind Control Center** egy webalapú adminisztrációs és elemzési felület, amely a klasszikus Northwind mintaadatbázishoz (Microsoft SQL Server) csatlakozik. A rendszer hat funkcionális modult tartalmaz, és egyetlen Flask-alkalmazásként fut Linux környezetben.

### Technológiai verem

| Réteg | Technológia |
|---|---|
| Backend | Python 3.13, Flask 3.x |
| Adatbázis | Microsoft SQL Server (GCP Windows VM) |
| Kapcsolódás | pyodbc + ODBC Driver 18 for SQL Server |
| Frontend | Bootstrap 5.3, Bootstrap Icons, Chart.js, Cytoscape.js |
| ML / AI | scikit-learn (GradientBoostingRegressor), NumPy |

### Architektúra

Az alkalmazás a **service layer** mintát követi: az `app.py` csak az útvonalakat (route-okat) definiálja, az üzleti logika a `services/` könyvtár almodulaiba van kiszervezve (`query_service`, `ops_service`, `events_service`, `analytics_service`, `graph_service`, `ml_service`). Az adatbázis-kapcsolatot a `db.py` kezeli Flask alkalmazáskontextushoz kötve (`flask.g`), így minden HTTP kérésenként egy kapcsolat nyílik és zárul.

A konfigurációs adatok (szerver cím, hitelesítési adatok) a `.env` fájlból töltődnek be a `python-dotenv` csomagon keresztül, így a forráskódban nem szerepelnek érzékeny adatok.

---

## 2. Telepítés és indítás

### Előfeltételek

- Ubuntu 22.04 / 24.04 (vagy kompatibilis)
- Microsoft ODBC Driver 18 for SQL Server (telepítve)
- Python 3.10+ és pip / conda
- Hozzáférés a SQL Server példányhoz (TCP/1433 port nyitva)

### Környezeti konfiguráció (`.env`)

```
SECRET_KEY=<véletlenszerű string>
SQL_SERVER=<ip>,1433
SQL_DATABASE=Northwind
SQL_USERNAME=flask_user
SQL_PASSWORD=<jelszó>
SQL_DRIVER=ODBC Driver 18 for SQL Server
SQL_ENCRYPT=yes
SQL_TRUST_SERVER_CERT=yes
```

### Indítás

```bash
cd northwind-control-center
pip install -r requirements.txt
python app.py
```

Az alkalmazás a `0.0.0.0:5000` címen indul el, és a helyi hálózatból elérhető.

### Adatbázis-objektumok létrehozása

Az SQL Server oldalon a `sql/00_all.sql` szkriptet kell futtatni SSMS-ben (Windows Authentication alatt). Ez létrehozza az összes szükséges táblát, nézetet, triggert és tárolt eljárást.

---

## 3. Főoldal (Dashboard)

**URL:** `/`

A főoldal négy összefoglaló kártyán mutatja a rendszer aktuális állapotát:

- **Orders Today** – a mai nap rendeléseinek száma (az `OrderDate` alapján)
- **Low Stock Products** – az újrarendelési szint alá esett termékek száma
- **Pending Events** – a feldolgozásra váró események száma az `order_log` táblában
- **Failed Events** – hibásan végrehajtott események száma (piros jelzés, ha > 0)

Ha az adatbázis-kapcsolat sikertelen, a lap hibaüzenetet és a `.env` ellenőrzésére vonatkozó útmutatást jelenít meg. Ha az `order_log` tábla nem létezik (a 04-es SQL szkript nincs futtatva), sárga figyelmeztetés jelenik meg.

A lap alján gyors hivatkozások találhatók mind a hat modulhoz.

---

## 4. Query Studio

**URL:** `/query`

Az SQL lekérdezések közvetlen futtatására szolgáló modul. Főbb funkciói:

### Mentett lekérdezések
A `dbo.saved_queries` táblában előre tárolt lekérdezések legördülő menüből betölthetők. A mentett lekérdezések neve, SQL szövege, leírása és csak olvasható jelzője kerül eltárolásra. A 02-es SQL szkript kilenc előre definiált lekérdezéssel tölti fel a táblát (pl. havi forgalom, készlethiány, vevő-statisztikák).

### Lekérdezés futtatása
A szövegmezőbe tetszőleges T-SQL utasítás írható. A futtatás előtt megadható:

- **Isolation level** – `READ COMMITTED`, `READ UNCOMMITTED`, `REPEATABLE READ`, `SERIALIZABLE` közül választható, ezzel demonstrálható az izolációs szintek hatása
- **Read-only mode** – bekapcsolt állapotban az alkalmazás megtagadja az `INSERT`, `UPDATE`, `DELETE`, `DROP` kulcsszavakat tartalmazó lekérdezéseket
- **Export to CSV** – az eredmény letölthető CSV formátumban

Az eredmény táblázatos formában jelenik meg a futási idővel (milliszekundumban) együtt. Hiba esetén az SQL Server hibaüzenete kerül megjelenítésre. Minden lekérdezés-futtatás naplózódik a `dbo.query_execution_log` táblában (lekérdezés szövege, felhasználó, időbélyeg, futási idő, sorok száma, esetleges hiba).

---

## 5. Operations (Üzemeltetési műszerfal)

**URL:** `/operations`

A SQL Server példány üzemeltetési állapotát öt panelen mutatja be:

### Adatbázis-méret
A `sys.database_files` és `sys.databases` rendszernézetekből lekérdezett fájlinformációk: adatfájl és naplófájl mérete MB-ban, szabad hely, automatikus növekedés.

### Mentések (Backups)
Az `msdb.dbo.backupset` táblából az utolsó 10 biztonsági mentés: típus (teljes / differenciális / tranzakciónapló), méret, kezdési idő, időtartam.

### SQL Agent feladatok
Az `msdb.dbo.sysjobs` és `msdb.dbo.sysjobactivity` nézetekből a konfigurált feladatok neve, állapota és utolsó futásának eredménye. Ide tartozik a `ProcessNorthwindOrderEvents` feladat is, ha be van konfigurálva.

### Sorstatisztika
A Northwind adatbázis összes felhasználói táblájának sorszáma az `sys.dm_db_partition_stats` dinamikus nézet alapján.

### Alacsony készlet
A `ReorderLevel` alá esett, nem megszüntetett termékek listája a hiány mértékével.

---

## 6. Events (Laza csatolás monitor)

**URL:** `/events`

Ez a modul az adatbázisban implementált **aszinkron eseményfeldolgozási mintát** (loose coupling) vizualizálja és kezeli.

### A minta működése

1. Az `Orders` táblán lévő `dbo.tr_log_order` trigger minden INSERT és UPDATE után bejegyzést ír a `dbo.order_log` táblába (`event_type`: `new_order`, `address_changed` vagy `order_updated`, `status`: 0 = várakozik).
2. A `dbo.sp_process_order_events` tárolt eljárás a `status = 0` állapotú eseményeket sorban feldolgozza: levonja az eladott mennyiséget az `UnitsInStock` mezőből (negatívba nem megy), és az esemény státuszát `2` (sikeres) vagy `3` (hibás) értékre állítja.
3. Az eljárást SQL Agent job hívja percenként (`ProcessNorthwindOrderEvents`), de kézzel is elindítható a felületen a **Process Now** gombbal.
4. Hibás (status = 3) esemény esetén az egyes soroknál megjelenik egy **Retry** gomb, amely az eseményt visszaállítja `0` (várakozó) állapotba, így a következő feldolgozási körben újrapróbálkozás történik (`dbo.sp_retry_order_event`).

### Megjelenített adatok

- Összefoglaló kártyák: Pending / Processing / Success / Failed események száma
- Az utolsó 100 esemény részletes listája: azonosító, típus, rendelés ID, állapot, létrehozás ideje, feldolgozás kezdete/vége, hibaüzenet

---

## 7. Analytics (Elemzési műszerfal)

**URL:** `/analytics`

Öt interaktív Chart.js diagramot tartalmaz, amelyek az adatokat AJAX-on keresztül töltik be a `/analytics/data/<chart_name>` JSON végpontokról. A diagramok az oldal betöltésekor párhuzamosan lekérik az adatokat, és azonnal megjelenítik azokat.

| Diagram | Leírás |
|---|---|
| **Monthly Revenue** | Havi forgalom vonaldiagram, 1996–1998 |
| **Revenue by Category** | Kategóriánkénti bevétel kördiagram (Beverages, Confections, stb.) |
| **Top 10 Products** | A 10 legtöbbet értékesített termék vízszintes oszlopdiagramon |
| **Orders by Country** | Rendelések száma vevő-ország szerint (bar chart) |
| **Shipping Status** | Szállítási állapot megoszlása (szállított / szállítás alatt / késésben) |

A diagramok a Northwind alaptáblákon futó aggregációs lekérdezésekre épülnek (nem nézeteken), így mindig az aktuális adatot tükrözik.

---

## 8. Graph Explorer (Gráf feltáró)

**URL:** `/graph`

A SQL Server 2017-ben bevezetett **gráftábla** (NODE / EDGE) funkcionalitást bemutató modul. Négy előre definiált lekérdezés közül lehet választani:

### Relációs lekérdezések (nem igényelnek gráftáblákat)

- **Employee Hierarchy** – Az alkalmazottak hierarchiája a `Employees.ReportsTo` önhivatkozó kulcs alapján. Cytoscape.js-sel hálózati gráfként is megjeleníthető (Load Visualization gomb).
- **Product Co-occurrence** – Melyek a leggyakrabban együtt rendelt termékpárok? Ugyanazon rendelésen belüli közös előfordulás alapján, TOP 40 pár.

### Gráf MATCH lekérdezések (igénylik a gráftáblákat)

A `06_graph.sql` szkript öt gráftáblát tölt fel:
- **NODE:** `g_orders`, `g_products`, `g_customers`
- **EDGE:** `g_order_contains` (rendelés → termék, mennyiség és érték attribútumokkal), `g_customer_places` (vevő → rendelés)

- **Sales by Product & Year (graph MATCH)** – Termékenkénti éves bevétel a `MATCH(o-(e)->p)` szintaxissal, a gráf él-táblán aggregálva.
- **Customer → Product Paths** – Melyik vevő mit rendelt, a gráf útvonal-traversalon keresztül lekérdezve.

Az eredmény minden esetben táblázatos formában jelenik meg. Az Employee Hierarchy lekérdezésnél ezen felül egy interaktív gráfvizualizáció is elérhető Cytoscape.js segítségével.

---

## 9. Insights / ML (Gépi tanulás és anomáliadetekció)

**URL:** `/insights`

Három gépi tanulási és statisztikai elemzési funkciót tartalmaz három fülön.

### 9.1 Order Value Prediction (Rendelési érték előrejelzés)

**Algoritmus:** `GradientBoostingRegressor` (scikit-learn)

**Tanítási folyamat** (Train Model gomb):
1. A `dbo.[Order Details]`, `Orders`, `Products`, `Categories`, `Customers` táblákból lekérdezi az összes rendeléstételt (kb. 2155 sor a Northwind adatbázisban).
2. Jellemzők: termékkategória (label-kódolt), vevő országa (label-kódolt), egységár, kedvezmény, rendelési év.
3. Cél: tétel értéke = `UnitPrice × Quantity × (1 − Discount)`.
4. 80/20 arányú tanítási/tesztelési felosztás után illeszti a modellt, és kiszámítja az R² értéket a teszthalmazon.
5. A modell memóriában marad (szerver újraindításig); a tanítás időbélyege, mintaszám, R² és jellemző-fontossági értékek a felületen megjelennek.

**Előrejelzés** (Predict gomb):
- A felhasználó megadja: kategória, ország, egységár, kedvezmény (0–0,25), év
- A modell visszaad egy becsült értéket euróban, és L / M / H osztályba sorolja a 33. és 67. percentilis küszöbök alapján

Ha az előrejelzéshez megadott ország nem szerepelt a tanítási adatokban, a rendszer figyelmeztet, és a leggyakoribb país-kódot használja tartalékként.

### 9.2 Inventory Risk Scoring (Készletkockázat-pontozás)

**Módszer:** Szabályalapú kockázati pontozás

Minden aktív (nem megszüntetett) termékre kiszámítja a következő pontszámot:

```
score = 0,6 × max(0, (reorder_level − stock) / reorder_level)
      + 0,4 × min(sales_30d / (stock + on_order), 1)
```

- Az első tag a **készlethiány aránya**: mennyivel van a készlet a rendelési szint alatt
- A második tag a **forgási sebesség**: az elmúlt 30 nap eladásai a rendelkezésre álló készlethez képest (az adatbázis maximális rendelési dátumától visszaszámolva, hogy a 1996–1998-as adatokon is működjön)

**Kockázati szintek:** High ≥ 0,55 &nbsp;|&nbsp; Medium ≥ 0,25 &nbsp;|&nbsp; Low < 0,25

A lista a pontszám szerint csökkenő sorrendben jelenik meg, progress-bar vizualizációval és szín-kódolással (piros / sárga / zöld).

### 9.3 Anomaly Detection (Anomáliadetekció)

**Módszer:** Statisztikai küszöbérték-alapú jelzés (NumPy)

A `dbo.[Order Details]` összes tételére három szabályt alkalmaz:

| Szabály | Küszöb | Súlyosság |
|---|---|---|
| Magas tétel érték | > 95. percentilis | High / Medium / Low a szórástól függően |
| Szokatlan kedvezmény | > átlag + 2σ (és > 0) | High / Medium / Low |
| Magas szállítási díj | > 95. percentilis | High / Medium / Low |

Egy tételen több szabály is teljesülhet egyidejűleg; a súlyossági szint a teljesült szabályok számától és erejétől függ. Az eredmény legfeljebb 150 anomáliatételt mutat, súlyosság szerint csökkenő sorrendben, a „Reasons" oszlopban az összes teljesült szabállyal.

---

## 10. Adatbázis-objektumok összefoglalója

| Objektum | Típus | Modul |
|---|---|---|
| `dbo.saved_queries` | Tábla | Query Studio |
| `dbo.query_execution_log` | Tábla | Query Studio |
| `dbo.order_log` | Tábla | Events |
| `dbo.tr_log_order` | Trigger | Events |
| `dbo.sp_process_order_events` | Tárolt eljárás | Events |
| `dbo.sp_retry_order_event` | Tárolt eljárás | Events |
| `dbo.vw_event_status_summary` | Nézet | Events |
| `dbo.vw_event_log_recent` | Nézet | Events |
| `dbo.vw_db_file_sizes` | Nézet | Operations |
| `dbo.vw_low_stock` | Nézet | Operations |
| `dbo.vw_revenue_by_month` | Nézet | Analytics |
| `dbo.vw_revenue_by_category` | Nézet | Analytics |
| `dbo.vw_top_products` | Nézet | Analytics |
| `dbo.g_orders` | NODE tábla | Graph Explorer |
| `dbo.g_products` | NODE tábla | Graph Explorer |
| `dbo.g_customers` | NODE tábla | Graph Explorer |
| `dbo.g_order_contains` | EDGE tábla | Graph Explorer |
| `dbo.g_customer_places` | EDGE tábla | Graph Explorer |
| `dbo.vw_ml_order_features` | Nézet | Insights |
| `dbo.vw_inventory_risk_features` | Nézet | Insights |
| `dbo.vw_order_anomaly_candidates` | Nézet | Insights |

---

## 11. Biztonság és hozzáférés-kezelés

Az alkalmazás a `flask_user` SQL Server felhasználóval csatlakozik, amelynek jogosultságai a Northwind adatbázisra korlátozódnak (`db_datareader`, `db_datawriter`, `EXECUTE` a tárolt eljárásokon). Az SQL Server kapcsolat TLS titkosítással (`SQL_ENCRYPT=yes`) történik.

A Query Studio read-only módja szerver oldalon nem kényszerített (a szűrés alkalmazásszinten történik); a `flask_user` jogosultságainak megfelelő szűkítése ajánlott éles környezetben. A webes felület jelenleg hitelesítés nélkül elérhető — éles üzembe helyezés előtt Flask-Login vagy hasonló megoldás integrálása szükséges.

---

*Northwind Control Center – MSc Haladó Adatbázisok és Felhő (2025/2026)*
