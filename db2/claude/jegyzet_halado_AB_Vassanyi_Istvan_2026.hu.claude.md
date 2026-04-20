## 1. Az alapvető adatbázis-készségek áttekintése

   Üdvözlet. A kurzus néhány bemutatójában a Northwind minta relációs adatbázist és a Microsoft
   SQL Server 2022 technológiát használjuk. A Northwind adatbázist egy fogyóeszközökkel
   kereskedő kis cég támogatására tervezték. Tartalmaz készletnyilvántartást és rendeléskezelő
   táblákat. A táblák és fájlok nevei magukért beszélnek.

### Modellezés

Az OLTP-adatbázisok relációs modellezésének alapjait a Northwind példáján tekintjük át:
`Customers`, `Employees`, `Orders`, `Order Details`, `Products`, `Categories`,
`Territories`.

- A kiindulópont a koncepcionális modell, vagyis a domainmodell vagy az
  entitáskapcsolati modell, amelyet a használati esetekből vezetünk le. A cél a logikai
  adatbázismodell kialakítása.

- A relációs modell egyszerűsége miatt a hagyományos üzleti folyamatok támogatásának
  leggyakoribb megközelítése.
  A Northwind adatbázis dumpja innen tölthető le:
  https://www.microsoft.com/en-us/download/details.aspx?id=23654
  A kurzusban az eredeti adatbázist úgy módosítottuk, hogy egy `territory_id` idegen kulcsot
  adtunk a `Customers` táblához, valamint egy extra `Salary` mezőt az `Employees` táblához.

- Az entitásokat, attribútumokat, előfordulásokat és azonosítókat a relációs modellben táblák,
  mezők, rekordok és elsődleges kulcsok formájában valósítjuk meg. A kulcsok több mezőből is
  állhatnak.

- Egyetlen cellában csak egy érték lehet, ezért a redundancia és az inkonzisztencia nem
  megengedett a harmadik normál formában (3NF).

- A 3NF jellemzői:
  
  - Minden táblának van egy elsődleges kulcsa, amely több mezőből is állhat, és amelytől az
    összes többi mező funkcionálisan függ.
  - Kompozit, vagyis többmezős kulcsok esetén az összes nem kulcsmező a teljes kulcstól függ,
    nem csak annak egy részétől, vagyis nincs részleges függés.
  - A nem kulcsmezők a kulcson kívül más mező(k)től nem függnek, vagyis nincs tranzitív függés
    egy táblán belül.

- Minden tábla kapcsolódik más táblákhoz.

- Az 1:N, vagyis az egy a sokhoz kapcsolatokat idegen kulcsokkal valósítjuk meg
  (például `Orders.EmployeeID`).

- Az N:M, vagyis a sok a sokhoz kapcsolatokat kapcsolótáblákkal valósítjuk meg
  (például `EmployeeTerritories`).

- Az 1:1 kapcsolat nem szerepel a Northwind adatbázisban.
  
  - Egy normál 1:1 kapcsolat lehetne például egy `CompanyCar` tábla, ha egy alkalmazottnak
    legfeljebb egy céges autója lehet.
  - Egy specializációs típusú 1:1 kapcsolat lehetne például egy `ExciseProducts` tábla a
    jövedéki termékek extra mezőivel, például `ExciseDutyAmount`, `RegBarCode` stb.

- Az összekapcsoló táblák általában összetett kulcsokkal rendelkeznek. Kulcsot csak akkor
  generálunk, ha külső hivatkozásra van szükség.

- Az OLTP-séma kapcsolati struktúrája feltárja az adatbázist használó alkalmazás kulcsfontosságú
  tranzakcióit.

- A törzstáblák a séma szélén, a tranzakciós táblák pedig a középpontban találhatók. Az előbbiek
  kicsik és ritkán változnak, az utóbbiak nagyok és gyakran módosulnak.

- Egy jól megtervezett grafikus felhasználói felület is követi ezt a szerkezetet:
  
  - rejtett vagy csak olvasható mező: kulcs
  - szerkeszthető szövegmezők: a kulcstól függő attribútumok
  - legördülő vagy kombinált listák: hivatkozások törzstáblákra
  - jelölőnégyzet kiegészítő szövegmezővel: specializáció
  - legördülő táblák vagy listák: 1:N kapcsolatok

További olvasnivalók a modellezésről:

- https://www.safaribooksonline.com/library/view/relational-theoryfor/9781449365431/ch01.html
- http://www.blackwasp.co.uk/RelationalDBConcepts.aspx
- https://www.tutorialspoint.com/ms_sql_server/index.htm

GYAKORLAT: a minta adatbázis létrehozása és bővítése

- Telepítsd az MS SQL Server 2016 vagy újabb verzióját, indítsd el az adatbázis-szolgáltatást, és csatlakozz hozzá
  az MS Management Studio-val.
- Futtasd a Northwind adatbázist, készíts kiírást, és tekintsd át a táblákat a grafikus felhasználói felület eszközeivel
- Rajzolj a fenti diagramhoz hasonló logikai adatbázismodell-diagramot
- Add hozzá az Alkalmazottak.Bérezés és a Vevők.terület_azonosítója mezőket
- Tervezd meg és valósítsd meg az adatbázis kiterjesztését a következő forgatókönyv modellezéséhez.
  Munkatársainkat rendszeres képzésekre küldjük, ahol különféle ismereteket sajátítanak el.
  A képzéseket szerződött harmadik fél cégek szervezik. Van egy listánk
  szükséges készségek (például „B fokú üzleti prezentáció” vagy „számviteli alapismeretek” stb.).
  minden foglalkoztatási kategóriát (például „értékesítési menedzser”, lásd Alkalmazottak.Megnevezés), amelyet meg kell tenniük
  munkaviszonyuk kezdetétől számított 10 éven belül megtanulják. Minden edzéshez mi
  tárolja az időtartamot (kezdési és befejezési dátum), a helyszínt, a szervező céget, a készségeket
  tanított, résztvevők, képzési állapotuk (például „beiratkozott”, „kezdett”, „befejezett”,
  „elvetélt”) és vizsgaeredményeiket külön-külön a különböző készségek esetében. Tekintettel a
  tréningeket szervező cégeknél tároljuk a cégünk által fizetett díjakat a
  képzések minden évben.
- (Add hozzá az új táblákat az adatbázisdiagramhoz, és adj meg néhány tesztadatot)
- MEGOLDÁS: train_tables.sql2

### Lekérdezés

- Áttekintjük a Structured Query Language (SQL) lekérdezés alapjait, mint például a kijelölés, csoportosítás,
  csatlakozás. Példa lekérdezések:
  
  - Az egyes rendelések értéke
  - Minden egyes termékre éves szinten eladott minimális és maximális mennyiség
  - Melyik alkalmazott adta el a legtöbb darabot a legnépszerűbb termékből 1998-ban?

- Minden rendelés értéke
  
  ```sql
  select o.orderid, o.orderdate,
         str(sum((1-discount)*unitprice*quantity), 15, 2) as order_value,
         sum(quantity) as no_of_pieces,
         count(d.orderid) as no_of_items
  from orders o inner join [order details] d on o.orderid=d.orderid
  group by o.orderid, o.orderdate
  order by sum((1-discount)*unitprice*quantity) desc
  ```

- Évesen termékenként eladott mennyiség
  
  ```sql
  select p.ProductID, p.ProductName, year(o.orderdate), SUM(quantity) as quantity
  from orders o inner join [order details] d on o.orderid=d.orderid
  inner join Products p on p.ProductID=d.ProductID
  group by p.ProductID, p.ProductName, year(o.orderdate)
  order by p.ProductName
  ```

- Melyik alkalmazott adta el a legtöbb darabot a legnépszerűbb termékből 1998-ban?
  
  ```sql
  select top 1 u.titleofcourtesy+' '+u.lastname+' '+u.firstname+' ('+u.title+')',
         sum(quantity) as pieces_sold,
         pr.productname as productname
  from orders o inner join [order details] d on o.orderid=d.orderid
  inner join employees u on u.employeeid=o.employeeid
  inner join products pr on pr.productid=d.productid
  where year(o.orderdate)=1998
    and d.productid = (
      select top 1 p.productid
      from products p left outer join [order details] d on p.productid=d.productid
      group by p.productid
      order by count(*) desc
    )
  group by u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname,
           pr.ProductID, pr.productname
  order by sum(quantity) desc
  ```

- További példákért és az SQL-lekérdezések szisztematikus áttekintéséért lásd a Függeléket

- További olvasnivalók a lekérdezésről:
  
  - https://docs.microsoft.com/en-us/sql/t-sql/queries/queries

GYAKORLAT: az első gyakorlatban megvalósított táblák segítségével valósítsd meg a következő lekérdezéseket

- Mik a hiányzó képességek Mrs. Peacock számára?
- Vannak a jövőben olyan foglalkozások, amelyeken továbbra is részt kell venni Peacock-nak?
- Mi az első és az utolsó képzés dátuma és az edzések átlagos időtartama napokban?
- Melyik alkalmazott rendelkezik a legtöbb készségekkel, ha a vizsga eredménye „elbukott”?
- Mennyi a teljes díja minden olyan képzésért, amelyen a legképzettebb munkatársunk
  (lásd fent) részt vett?
- Mely szükséges készségekkel nem foglalkoztak még egyetlen tréningen sem?
- MEGOLDÁS: train_solution.sql

### Programozás

- Az SQL mellett a procedurális tranzakciós logika a TSQL szkriptnyelvben is megvalósítható, és a szerver oldalon futtatható és tárolható
  - A szerveroldali üzleti logika előnyei és hátrányai
    ✓ Egyszerű architektúra
    ✓ Technológiai semlegesség
    ✓ Adatbiztonság
    ✓ Kezelhetőség
    ✓ Hatékonyság

✓ Olvasható kód
 Alacsony szint
 Gyenge szoftvertechnológiai támogatás
 Drága méretezhetőség

- A lényeg az, hogy az üzleti logika egyszerű, halmazalapú része
  a nagy mennyiségű strukturált adattal végzett műveletek végrehajtása és kezelése a legjobban
  az adatbázis-kiszolgálón tárolt eljárások, függvények, triggerek és jobok formájában.
  Az üzleti logika eljárásilag kifinomult részeit, amelyek magas szintű, objektumorientált programozási környezetet igényelnek, implementálni kell egy alkalmazáson
  szerver.

- A szerver oldali programozhatóság elemei

- Speciális SQL kulcsszavak a vezérlési folyamathoz: `DECLARE`, `SET`, `BEGIN/END`,
  `IF/ELSE`, `WHILE/BREAK/CONTINUE`, `RETURN`, `WAITFOR/DELAY/TIME`, `GOTO`

- Hibakezelés: `TRY/CATCH/THROW/RAISERROR`

- A programozhatóságot támogató objektumok: `PROCEDURE` / `FUNCTION` / `TRIGGER`

- Tranzakciós támogatás: `BEGIN/COMMIT/ROLLBACK TRANSACTION`

- `CREATE`

Az alábbiakban egy egyszerű példa látható egy T-SQL scriptre és annak tárolt eljárásos
megfelelőjére. Egy hasonló felhasználó által definiált függvény egy `SELECT` utasításban is
használható.

```sql
--a simple script that demonstrates the elements of T-SQL
--megkeresünk egy alkalmazottat, és ha pontosan egy találat van,
--10%-kal megemeljük az alkalmazott fizetését
set nocount on
declare @name nvarchar(20), @address nvarchar(max), @res_no int, @emp_id int
set @name='Fuller'
select @res_no=count(*) from Employees where LastName like @name + '%'
if @res_no=0 print 'No matching record.'
else if @res_no>1 print 'More than one matching record.'
else begin --egyetlen találat
select @address=Country+', '+City+' '+Address, @emp_id=EmployeeID
from Employees where LastName like @name
print 'Employee ID: ' + cast(@emp_id as varchar(10)) + ', address: ' + @address
update Employees set salary=1.1*salary where EmployeeID=@emp_id
print 'Salary increased.'
end
go
--csomagold be tárolt eljárásba
create procedure sp_increase_salary @name nvarchar(40)
as
set nocount on
declare @address nvarchar(max), @res_no int, @emp_id int
select @res_no=count(*) from Employees where LastName like @name + '%'
if @res_no=0 print 'No matching record.'
else if @res_no>1 print 'More than one matching record.'
else begin --egyetlen találat
select @address=Country+', '+City+' '+Address, @emp_id=EmployeeID
from Employees where LastName like @name
print 'Employee ID: ' + cast(@emp_id as varchar(10)) + ', address: ' + @address
update Employees set salary=1.1*salary where EmployeeID=@emp_id
print 'Salary increased.'
end
go
--test
```

```sql
select Salary from Employees where LastName like 'Fuller%'
exec sp_increase_salary 'Fuller'
select Salary from Employees where LastName like 'Fuller%'
--skaláris függvény, amely visszaadd egy személy fizetését, vagy 0-t, ha nem
found
go
create function fn_salary (@name nvarchar(40)) returns money as
begin
declare @salary money, @res_no int
select @res_no=count(*) from Employees where LastName like @name + '%'
if @res_no <> 1 set @salary=0
else select @salary=Salary from Employees where LastName like @name + '%'
return @salary
end
go
--teszt
select [your user name].fn_salary('Fuller') as salary
```

- Vedd figyelembe, hogy egy tárolt eljárás több rekordkészletet is visszaadhat, ha több SELECT-et tartalmaz
  állítások változó hozzárendelés nélkül. Értékkel átadott paraméterek a példában látható módon
  fent INPUT típusú paraméterek találhatók. A tárolt eljárások skaláris értékeket is visszaadhatnak az OUTPUT paraméterekben (a példában nem láthatók). A tárolt eljárások más tárolt eljárásokat vagy függvényeket is hívhatnak, ezért használhatók összetett üzleti logika megvalósítására a DB szerveren.

- A felhasználó által definiált függvény abban különbözik a tárolt eljárástól, hogy egyetlen visszatérési értéke van, amely lehet skaláris (például pénz) vagy tábla. Egy függvény utolsó utasításának `RETURN`-nek kell lennie. A felhasználó által definiált függvények előnye a tárolt eljárásokkal szemben az, hogy a függvény meghívható egy SELECT utasításon belül, mint bármely más beépített SQL függvény, például a `DATEDIFF`, így sokat ad a statikus SQL lekérdezések rugalmasságához.

- GYAKORLAT

- A képzési lekérdezések segítségével hozz létre egy tárolt eljárást, amely visszaadd a hiányzó készségeket
  paraméterként átadott alkalmazottnévhez. A tárolt eljárásnak vissza kell térnie a
  tábla egyetlen mezővel, amely a hiányzó készségeket tartalmazza. Ha a munkavállaló nem lehet
  azonosítva, hibaüzenetet ad vissza, és nincs tábla.

- A betanítási lekérdezések segítségével hozz létre egy tábla értékű függvényt, amely visszaadd a hiányzót
  készségek egy munkavállalói azonosítóhoz, tábla formájában. Tipp: használd a „visszatérési táblát” a függvényben
  specifikáció.
  A valósághűbb üzleti folyamat bemutatása érdekében itt van egy példa a szkript elkészítéséhez
  egy új Northwind rendelés, amely egyetlen rendelési tételt tartalmaz. A forgatókönyv szerint a cég
  iroda sürgős rendelést kap egy kedves vásárlótól telefonon. Egy ilyen folyamat
  tipikus üzleti tranzakció.

```sql
--változók
declare @prod_name varchar(20), @quantity int, @cust_id nchar(5) --a szöveges
customer id over the phone
declare @status_message nvarchar(100), @status int --az üzleti folyamat eredménye
declare @res_no int --találatok száma
declare @prod_id int, @order_id int --azonosítók
declare @stock int --meglévő készlet
declare @cust_balance money --vevőegyenleg
declare @unitprice money --termék egységára
-- parameters
set @prod_name = 'boston'
set @quantity = 10
set @cust_id = 'AROUT'
```

```sql
begin try
select @res_no = count(*) from products where productname like '%' + @prod_name +
'%'
if @res_no <> 1 begin
set @status = 1
set @status_message = 'ERROR: Ambiguous Product name.';
end else begin
--ha pontosan egy terméket találunk, lekérdezzük az azonosítót és a készletet
select @prod_id = productID, @stock = unitsInStock from products where
productName like '%' + @prod_name + '%'
--elég-e a készlet?
if @stock < @quantity begin
set @status = 2
set @status_message = 'ERROR: Stock is insufficient.'
end else begin
--van-e elég fedezete a vevőnek?
select @cust_balance = balance from customers where customerid =
@cust_id
--ha nincs találat, az @cust_balance értéke NULL lesz
--legfeljebb egy találat lehet
select @unitprice = unitPrice from products where productID =
@prod_id --nincs kedvezmény
if @cust_balance < @quantity*@unitprice or @cust_balance is null
begin
set @status = 3
set @status_message = 'ERROR: Customer not found or balance
insufficient.'
end else begin
-- no more checks, we start the transaction (3 steps)
--1. csökkentjük az egyenleget
update customers set balance = balance-(@quantity*@unitprice) where
customerid=@cust_id
--2. új rekord az Orders és Order Details táblákba
insert into orders (customerID, orderdate) values (@cust_id,
getdate()) --orderid: identity
set @order_id = @@identity --az utolsó identity eredménye
insert [order details] (orderid, productid, quantity,
UnitPrice) --itt hibát követünk el
values(@order_id, @prod_id, @quantity, @unitprice) -itt hibát követünk el
-insert [order details] (orderid, productid, quantity,
UnitPrice, Discount) --a helyes sor
-values(@order_id, @prod_id, @quantity, @unitprice, 0)
--a helyes sor
-- 3. update product stock
update products set unitsInStock = unitsInStock - @quantity
where productid = @prod_id
set @status = 0
set @status_message = cast(@order_id as varchar(20)) + ' order
processed successfully.'
end
end
end
print @status
print @status_message
end try
begin catch
print 'OTHER ERROR: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20))
+ ')'
end catch
go
--paraméterek beállítása teszthez
```

```sql
set nocount off
update products set unitsInStock = 900 where productid=40
update customers set balance=1000 where CustomerID='AROUT'
delete [Order Details] where OrderID in (select orderid from Orders where
CustomerID='AROUT' and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
--futtatjuk a scriptet, majd ellenőrizzük:
select * from Customers where CustomerID='AROUT'
select * from Products where productid=40
select top 3 * from Orders where CustomerID='arout' order by OrderDate desc
--Seems fine. However we neglected a NOT NULL constraint of the discount field:
--"OTHER ERROR: Cannot insert the value NULL into column 'Discount'"
--Even worse, we still decreased the balance of the customer!
--in a concurrent environment, other errors may manifest as well
--after correction, test the other two branches as well
```

- További olvasnivalók a programozásról:
  - •

```
https://docs.microsoft.com/en-us/sql/t-sql/language-elements/control-of-flow
```

GYAKORLAT: az előző gyakorlatban megvalósított táblák és szkriptek felhasználásával,

- Írj egy forgatókönyvet, amely ellenőrzi, hogy egy alkalmazottnak szüksége van-e az a. által kínált készségekre
  tréningen, és ha igen, jelentkezz be minden ilyen foglalkozásra.
- Futtasd a szkriptet egy tárolt eljárásban.
- MEGOLDÁS: train_solution.sql

```sql
### Cursors
Cursors can be used for problems for which the procedural row-by-row approach is more suitable than
the set-based querying approach.
EXAMPLE for cursor syntax
declare @emp_id int, @emp_name nvarchar(50), @i int, @address nvarchar(60)
declare cursor_emp cursor for
select employeeid, lastname, address from employees order by lastname
set @i=1
open cursor_emp
fetch next from cursor_emp into @emp_id, @emp_name, @address
while @@fetch_status = 0
begin
print cast(@i as varchar(5)) + ' EMPLOYEE:'
print 'ID: ' + cast(@emp_id as varchar(5)) + ', LASTNAME: ' + @emp_name + ', ADDRESS: '
+ @address
set @i=@i+1
fetch next from cursor_emp into @emp_id, @emp_name, @address
end
close cursor_emp
deallocate cursor_emp
go
--ez ezzel egyenértékű egy SELECT-tel
select 'ID: ' + cast(employeeid as varchar(5)) + isnull(', LASTNAME: ' + lastname, '') +
isnull( ', ADDRESS: ' + address, '')
from employees order by lastname
--vagy sorszámmal
select cast(row_number() over(order by lastname) as varchar(50))+
'. ügynök: ID: ' + cast(employeeid as varchar(5)) + isnull(', LASTNAME: ' + lastname, '') +
isnull( ', ADDRESS: ' + address, '')
from employees
```

GYAKORLAT: Valósíts meg egy kurzort, amely megismétli az egyesült államokbeli ügyfeleket, és kiírd a számukat
a megfelelő rendeléseket soronként.

### Tranzakciókezelés

- A tranzakciós alapfogalmak
  - A „tranzakciót” úgy definiáljuk, mint egy üzleti tevékenység logikailag koherens sorozatát
    folyamatot. A „logikailag koherens” azt jelenti, hogy a műveletek szemantikai egységet alkotnak.
    A tranzakciók beágyazhatók pl. a helikopter vásárlási tranzakció tartalmazza a
    ügylet az ügyfél azonosítása és a számlafizetés tranzakciója
    banki átutalással stb.
  - Az atomitás, a konzisztencia, az elszigeteltség és a tartósság a környezet követelményei
    a tranzakciókat megvalósító környezetekkel szemben támasztott követelmények. Az utolsó
    rendelésfeldolgozási példában megszegtük az atomitási és izolációs követelményt.
  - Vannak implicit és explicit (programozott) tranzakciók. Az implicit tranzakciók azok
    az összes SQL DML utasítás.
  - A T-SQL-ben a tranzakciókat a `BEGIN TRANSACTION`, `COMMIT TRANSACTION` és
    `ROLLBACK TRANSACTION` utasításokkal programozzuk. A tranzakció a
    `BEGIN TRANSACTION` és a `COMMIT TRANSACTION` vagy `ROLLBACK TRANSACTION`
    közötti összes utasításból áll. A `COMMIT` lezárd a tranzakciót, és felszabadítja az összes
    erőforrást, például a táblazárakat, amelyeket a szerver a tranzakciókezeléshez használt. A
    `ROLLBACK` ugyanezt teszi, de előtte visszavonja a tranzakció összes módosítását. Ehhez a
    szerver egy kifinomult naplózási mechanizmust használ, az úgynevezett Write-Ahead Logot
    (WAL). Ha nem csonkolják vagy nem mentik le, a tranzakciós napló akár nagyobb is lehet, mint
    maga az adatbázis.
  - Az MS SQL Serverben, ha az XACT_ABORT be van kapcsolva, és a tranzakció egyik utasítása
    hibát okoz, a szerver leállítja a tranzakció végrehajtását, és automatikus műveletet hajt végre
    `ROLLBACK`-ot.

```sql
PÉLDA
--egyszerű atomitási demo, XACT_ABORT-tal
set xact_abort off
delete t2
go
begin tran
insert t2 (id, t1_id) values (10, 1)
insert t2 (id, t1_id) values (11, 2) --idegen kulcs megszorítás megsértése
insert t2 (id, t1_id) values (12, 3)
commit tran
go
--"Az INSERT utasítás ütközött a FOREIGN KEY megszorítással ..." etc
select * from t2
id
t1_id
--az atomitás nem maradt meg
set xact_abort on
delete t2
go
begin tran
insert t2 (id, t1_id) values (10, 1)
insert t2 (id, t1_id) values (11, 2) --idegen kulcs megszorítás megsértése
insert t2 (id, t1_id) values (12, 3)
commit tran
go
```

```sql
--"Az INSERT utasítás ütközött a FOREIGN KEY megszorítással ..." stb.
select * from t2
id
t1_id
--az atomitás megmaradt
```

- A beágyazott tranzakciók technikailag több BEGIN TRANSACTION nyilatkozatot jelentenek. A
  Az egyszeri ROLLBACK visszaállítja az összes megkezdett tranzakciót, lásd a példát
  alább

```sql
begin tran
print @@trancount --1
begin tran
print @@trancount
commit tran
print @@trancount --1
commit tran
print @@trancount --0
begin tran
print @@trancount --1
begin tran
print @@trancount
rollback tran
print @@trancount --0
```

- ```
  --2
  ```

```
--2
```

Súlyos programozási hiba, ha nem zárunk le egy tranzakciót sem COMMIT, sem a
ROLLBACK segítségével. A befejezetlen tranzakció továbbra is kiszolgáló erőforrásokat fogyaszt
és végül megbénítja a rendszert. A @@TRANCOUNT globális változó lehet
annak ellenőrzésére szolgál, hogy az aktuális kapcsolatnak van-e befejezetlen tranzakciója.

```sql
PÉLDA: az előző rendelésfeldolgozó script hiányosságainak kijavításához
csomagoljuk azt tárolt eljárásba, és adjunk hozzá TRY/CATCH hibakezelést és tranzakciós támogatást.
go
create procedure sp_new_order
@prod_name nvarchar(40), @quantity smallint, @cust_id nchar(5)
as
set nocount on
set xact_abort on
--változók
declare @status_message nvarchar(100), @status int --az üzleti folyamat eredménye
declare @res_no int --találatok száma
declare @prod_id int, @order_id int --azonosítók
declare @stock int --meglévő készlet
declare @cust_balance money --vevőegyenleg
declare @unitprice money --termék egységára
begin tran
begin try
select @res_no = count(*) from products where productname like '%' + @prod_name +
'%'
if @res_no <> 1 begin
set @status = 1
set @status_message = 'ERROR: Ambiguous Product name.';
end else begin
--ha pontosan egy terméket találunk, lekérdezzük az azonosítót és a készletet
select @prod_id = productID, @stock = unitsInStock from products where
productName like '%' + @prod_name + '%'
--elég-e a készlet?
if @stock < @quantity begin
set @status = 2
set @status_message = 'ERROR: Stock is insufficient.'
end else begin
--van-e elég fedezete a vevőnek?
select @cust_balance = balance from customers where customerid =
@cust_id
```

```sql
--ha nincs találat, az @cust_balance értéke NULL lesz
--legfeljebb egy találat lehet
select @unitprice = unitPrice from products where productID =
@prod_id --nincs kedvezmény
if @cust_balance < @quantity*@unitprice or @cust_balance is null
begin
set @status = 3
set @status_message = 'ERROR: Customer not found or balance
insufficient.'
end else begin
--nincs több ellenőrzés, elindítjuk a tranzakciót (2 lépés)
--1. csökkentjük az egyenleget
print 'Processing order...'
update customers set balance = balance-(@quantity*@unitprice)
where customerid=@cust_id
--2. új rekord az Orders és Order Details táblákba
insert into orders (customerID, orderdate) values (@cust_id,
getdate()) --orderid: identity
set @order_id = @@identity --az utolsó identity eredménye
-- hibás sor:
--insert [order details] (orderid, productid, quantity, UnitPrice)
--values(@order_id, @prod_id, @quantity, @unitprice)
-- helyes sor:
insert [order details] (orderid, productid, quantity,
UnitPrice, Discount) values(@order_id, @prod_id, @quantity, @unitprice, 0)
set @status = 0
set @status_message = 'Order No. ' + cast(@order_id as
varchar(20)) + ' processed successfully.'
end
end
end
print 'Status: ' + cast(@status as varchar(50))
print @status_message
if @status = 0 commit tran else begin
print 'Rolling back transaction'
rollback tran
end
end try
begin catch
print 'OTHER ERROR: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20))
+ ')'
print 'Rolling back transaction'
rollback tran
end catch
go
--teszt
--paraméterek beállítása teszthez
set nocount off
update customers set balance=1000 where CustomerID='AROUT'
delete [Order Details] where OrderID in (select orderid from Orders where
CustomerID='AROUT' and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
--futtatjuk a tárolt eljárást
exec sp_new_order 'boston', 10, 'Arout'
--ellenőrizzük az eredményt:
select * from Customers where CustomerID='AROUT' --816-nak kell lennie
select top 3 * from Orders o inner join [Order Details] od on o.OrderID=od.OrderID
where CustomerID='arout' order by OrderDate desc --látszania kell az új tételnek
select @@trancount --0-nak kell lennie
```

- Teszteld a fent tárolt eljárást különféle hibákra: programozási és logikai hibákra
  hibák, mint például az elégtelen készlet. Ellenőrizd az adatbázis integritását. Ellenőrizd, hogy a
  A tranzakciós támogatás megakadályozza a súlyos hibákat.

- Az elszigeteltség biztosítása érdekében a szerver zárakat használ a sorokon (rekordokon), tartományokon vagy táblákon. An
  Az Isolation Level egy zárolási stratégia, amelyet a szerver kényszerít ki. Az MS SQL fő zártípusai
  A szerver olvasási (megosztott), írási (kizárólagos) és frissítése. Az alábbiakban a 4 ANSI szabvány található
  elszigeteltségi szinteket, bár a jelenlegi adatbázis-technológiák nem csak ezeket a 4-et támogatják.
  
  - OLVASÁS NEM KÖTELEZETT: nincs reteszelés
  - READ COMMITTED: a zárolások eltávolítása az SQL utasítás befejezése után
  - ISMÉTELHETŐ OLVASÁS: a tranzakcióhoz adott zárolások a végéig megmaradnak
    a tranzakcióról
  - SOROZHATÓ: más tranzakciók nem tudnak olyan rekordokat beilleszteni egy táblába, amelyhez a
    a tranzakció sor- vagy tartományzárral rendelkezik, a fantomolvasás nem lehetséges

```sql
--egyszerű izolációs demo: a webáruház esete
create table test_product(id int primary key, prod_name varchar(50) not null, sold
varchar(50), buyer varchar(50))
insert test_product(id, prod_name, sold) values (1, 'car', 'for sale')
insert test_product(id, prod_name, sold) values (2, 'horse', 'for sale')
go
select * from test_product
update test_product set sold='for sale', buyer=null where id=2
go
set tran isolation level read committed --alapértelmezett
go
begin tran
declare @sold varchar(50)
select @sold=sold from test_product where id=2
if @sold='for sale' begin
waitfor delay '00:00:10' --now we are performing the bank transfer
update test_product set sold='sold', buyer='My name' where id=2
print 'sold successfully'
end else print 'product not available'
commit tran
go
--a fenti tranzakciót két lekérdezőablakban párhuzamosan futtatjuk
--a második script:
set tran isolation level read committed
go
begin tran
declare @sold varchar(50)
select @sold=sold from test_product where id=2
if @sold='for sale' begin
waitfor delay '00:00:10' --now we are performing the bank transfer
update test_product set sold='sold', buyer='Your name' where id=2 --note the diff
print 'sold successfully'
end else print 'product not available'
commit tran
go
--check what happens:
select * from test_product
id
prod_name
sold
buyer
car
for sale
NULL
horse
sold
Your name
--A lovat két vásárló is sikeresen megvette, de csak a második név kerül a rekordba.
Very awkward.
update test_product set sold='for sale', buyer=null where id=2
--Now try the same with set tran isolation level repeatable read
--"Transaction (Process ID 53) was deadlocked on lock resources with another process and
has been chosen as the deadlock victim. Rerun the transaction."
--No logical error. Only one horse is sold.
--Conclusion: be careful to select the right isolation level.
```

```sql
EXAMPLE of a dummy stored procedure syntax using a transaction:
go
create procedure sp_example (@emp_id int)
as
set xact_abort on --auto rollback in case of any error
begin tran
begin try
declare @i int
select @i=count(*) from employees where EmployeeID=@emp_id
if @i>0 print 'Employee found: ' + cast(@emp_id as varchar(50))
else print 'Not found: ' + cast(@emp_id as varchar(50))
if @i>0 begin
update employees set salary=salary*1.1 where EmployeeID=@emp_id
commit tran
print 'Salary successfully increased'
end else begin
print 'Rolling back transaction'
rollback tran
end
end try
begin catch
print 'OTHER ERROR: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as
varchar(20)) + ')'
print 'Rolling back transaction'
rollback tran
end catch
go
--teszt
exec sp_example 12 --Not found: 12 Rolling back transaction
exec sp_example 11 --Employee found: 11 Salary successfully increased
```

- •
  További információ a tranzakciókezelésről:
  
  - ```
    https://docs.microsoft.com/en-us/sql/t-sql/language-elements/control-of-flow
    ```
  
  - ```
    https://learn.microsoft.com/en-us/sql/t-sql/language-elements/transactionstransact-sql?view=sql-server-ver16
    ```
  
  - ```
    https://www.sqlshack.com/transactions-in-sql-server-for-beginners/
    ```

GYAKORLAT: Adj tranzakciós támogatást a saját képzésmenedzsment tárolt eljárásához és
teszteld a különféle hibákat.

2. Laza csatolás triggerek és jobok alapján
   Probléma forgatókönyv
   Az új rendeléseket a Megrendelések és a Rendelési tételek táblákban tároló harmadik fél kereskedési alkalmazás nem rendelkezik nyitott API-val, vagy valamilyen más okból nem teszi lehetővé események létrehozását. Ezért a Northwind Traders Ltd. Zrt. jelenlegi rendelésfeldolgozási munkafolyamatában a
   kereskedelmi osztály e-mailben (vagy bármely más módon) kommunikál a Szállítási és Logisztikai (SL) részleggel
   kézi üzenetküldő rendszer) az új vagy megváltozott rendelésekről. Cégünk az informatikáért felel
   támogatás az SL menedzsmentben. Az SL divízió vezetője minden alkalommal elkészíti a részletes napi munkatervet
   reggel a különböző egységek számára a kereskedelmi osztálytól kapott e-mailek szerint. Ehhez
   ő használd a szoftvereszközünket. Mind a kereskedés, mind az SL ugyanazt a Northwind SQL Server adatbázist használd.
   Arra kérünk, hogy mentesítsük a kereskedési és az SL személyzetet az e-mailek kézi írásától és a manuális beviteltől
   e-mailekből származó adatokat egy másik alkalmazásba a rendelésfeldolgozási munkafolyamat automatizálásával annyi, mint
   lehetséges.
   Megoldás
   Mivel a kereskedési rendszer egy „fekete doboz”, adatbázis szintű eseményekre kell hagyatkoznunk. Minden alkalommal, amikor egy rendelés
   létre vagy módosítva, akkor a szükséges (meglehetősen összetett) logikát kell futtatnunk a létrehozó adatbázison
   vagy módosítja a szükséges rekordokat az SL táblákban, például a Termékek. Így az írás és a feldolgozás is
   e-mailekből lesz szükség.
   Létfontosságú azonban, hogy megoldásunk legalább ne zavarja a kereskedési rendszert. Nem lehet
   jelentősen lelassítja a rendelés mentési folyamatát, és a feldolgozás során esetlegesen fellépő hibákat sem
   az SL oldalon egy megbízási eseményt vissza kell juttatni a kereskedési rendszerbe.
   Emiatt a laza csatolás koncepciót használjuk. Csak az INSERT és UPDATE eseményeket naplózzuk
   rendeléseket egy speciális táblában lévő triggeren keresztül, és ezeket az eseményeket ütemezett által végrehajtott kötegekben dolgozza fel
   munkát. A munka nyomon követi az egyes események feldolgozásának állapotát és eredményeit is. Mivel a
   az esemény feldolgozása folyamaton kívül történik, a feldolgozási hiba nem jelenik meg hibaként
   a kereskedési rendszerben.
   Megjegyzés: a trigger egy speciális tárolt eljárás, amelyet az adatbázis automatikusan meghív
   felügyeleti rendszer olyan adatbázisesemények esetén, mint a tábla INSERT, UPDATE vagy DELETE.
   A rendszer áttekintése:
   Megrendelések
   tábla
   Eseménynapló
   tábla
   Beszúrás
   trigger
   Gyártás
   táblák
   Rendeldn
   feldolgozás
   munkát
   Rövid áttekintés a triggerekről
   A triggerek a szerveren tárolt speciális eljárások, amelyek automatikusan futnak, ha egy előre meghatározott
   feltétele teljesül. Az SQL Server a következő típusú triggereket támogatja a triggerrel kapcsolatban
   esemény:
- DML triggerek (tábla szintű triggerek), amelyek akkor futnak le, amikor egy DELETE, INSERT vagy UPDATE művelet
  táblán hajtják végre

- DDL triggerek (adatbázis szintű triggerek), amelyek az adatbázis sémájának megváltozásakor indulnak el
  pl. tábla jön létre

- Bejelentkezési triggerek (szerverszintű triggerek), amelyek a bejelentkezés hitelesítési szakasza után indulnak el
  befejezi
  Most a DML triggerekre összpontosítunk. A trigger definíciója tartalmazza a céltáblát, a trigger
  eseményét (`DELETE`, `INSERT` vagy `UPDATE`) és a működési módot. Az SQL Server a következő
  működési módokat támogatja:

- `AFTER`: a megadott SQL utasítás sikeres végrehajtása után aktiválódik. Ez azt jelenti, hogy az
  ellenőrzések, a megszorítások és a DML-hez kapcsolódó kaszkádos frissítések vagy törlések is
  már sikeresen lefutottak. Egy objektumon több trigger is lehet, akár azonos típusúak is, például
  két `INSERT` trigger. Ilyenkor a végrehajtás sorrendjét a trigger tulajdonságai befolyásolják.

- `INSTEAD OF`: a DML utasítás helyett a trigger fut le. A trigger kódja a módosított rekordokat a
  speciális `inserted` és `deleted` virtuális táblákon keresztül éri el. Az SQL Server a következő
  két logikai táblát biztosítja:

- `deleted`: a `DELETE` trigger esetén a törölt rekordokat, `UPDATE` trigger esetén pedig az eredeti,
  régi rekordokat tartalmazza. Az `UPDATE` logikailag egy törlés és egy beszúrás kombinációja. Az
  `INSERT` trigger esetén a `deleted` tábla üres.

- `inserted`: az `INSERT` utasítással beszúrt rekordokat, illetve `UPDATE` trigger esetén az új
  rekordokat tartalmazza. A `deleted` tábla `DELETE` trigger esetén üres.
  
  Az SQL Server az `INSERTED` vagy `UPDATE` triggerekben használható `UPDATE([mezőnév])`
  függvényt is támogatja. Ez igazat ad vissza, ha a DML utasítás megváltoztatta a megadott mezőt.
  A mező nem lehet számított oszlop.
  
  Ha a trigger hibát jelez, akkor a kiváltó DML utasítás is visszagördül.
  
  Egy trigger olyan kódot is futtathat, amely más triggert vagy akár ugyanazt a triggert
  rekurzívan hívd meg, az SQL Serveren legfeljebb 32 szintig. Ezt a funkciót a beágyazott
  triggerek szerveropció vezérli (lásd lentebb).

Azok az esetek, amikor DML trigger használata javasolt

- Adminisztrációs feladatok, például naplózás vagy a megváltozott rekordok korábbi értékeinek
  megőrzése biztonsági táblákban.
- Az üzleti logikából következő, illetve azon túlmutató adatintegritási szabályok érvényesítése,
  amelyek túlmutatnak az egyszerű elsődleges kulcs, idegen kulcs vagy ellenőrzési megszorítások
  hatókörén. Példa a Northwind adatbázisban:
  - Nem engedjük a nehéz csomagok külföldre küldését. Ezért a 200 kg feletti, nem amerikai
    `ShipCountry`-val rendelkező rendeléseket elutasítjuk. Ez megvalósítható egy `INSERT AFTER`
    vagy `INSERT INSTEAD OF` triggerrel a `Orders` táblában. Az ilyen ellenőrzéseket természetesen
    a kliensszoftverbe is be kell építeni, azonban az adatbázis-szintű integritás a végrehajtás
    során megakadályozhatja az alkalmazáshibákat vagy a feltörési kísérleteket.
  - Üzleti munkafolyamatok automatizálása. Példák a Northwind adatbázisban:
    - Automatikus e-mailt küldünk az ügyfélnek, amikor a szállítási dátumot beállítottuk, például
      amikor a rendelés `ShipDate` mezője módosul (`UPDATE` trigger).
    - Automatikusan elküldjük a megrendelést a nagykereskedelmi beszállítónknak, amikor a
      `UnitsInStock` a `ReorderLevel` alá esik (`UPDATE` vagy `INSERT` trigger).
    - A `Products` tábla `UnitsInStock` mezőjét automatikusan frissítjük, amikor a megfelelő
      rendelési tétel mennyisége megváltozik (`UPDATE` trigger).
    - GYAKORLAT: írj egy `UPDATE` triggert a `Order Details` táblához. Ha a mennyiség változik,
      frissítsd a termék `UnitsInStock` értékét. Feltételezheted, hogy egyszerre csak egy rendelési
      tétel frissül.
    - GYAKORLAT: tételezd fel, hogy a fenti feladatban egyszerre több rendelési tétel frissül.
    - FIGYELMEZTETÉS: a triggerek működése „néma”, és súlyos problémákat okozhat, ha megfeledkezel
      róluk. Például ha a rendszergazda egy biztonsági másolatból visszaállítja a rendelési tételek
      tábláját egy trigger előzetes letiltása nélkül...
  - Az SQL Server triggerekre vonatkozó további példákért lásd:
- ```
  http://sqlhints.com/2016/02/28/inserted-and-deleted-logical-tables-in-sql-server/
  ```

```sql
Szoros csatolás
Az alábbi példában egy új INSERT triggert hozunk létre az Orders táblán, amely sokáig fut és kivált egy
kivételt dob, így letiltja a rendelésmentési folyamatot.
drop trigger tr_demo_bad
go
create trigger tr_demo_bad on orders for insert as
declare @orderid int
select @orderid=OrderID from inserted
print 'New order ID: ' + cast(@orderid as varchar(50))
waitfor delay '00:00:10' --10 s
select 1/0 --hibát generálunk
go
--1. teszt: mindkét utolsó sor kommentben
insert Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
--tábla visszaállítása
delete Orders where CustomerID='AROUT' and EmployeeID is null
--2. teszt: hozd létre újra a triggert, az utolsó sorok kommentben
insert Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
--sokat kell várnunk, de nincs hiba
```

```sql
--tábla visszaállítása
delete Orders where CustomerID='AROUT' and EmployeeID is null
--3. teszt: hozd létre újra a triggert, az összes sorral
insert Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
--sokáig kell várnunk, majd megjelenik az üzenet:
'New order ID: 11094
Msg 8134, Level 16, State 1, Procedure tr_demo_bad, Line 6 [Batch Start Line 276]
Divide by zero error encountered.
The statement has been terminated.'
select * from Orders where CustomerID='AROUT' and EmployeeID is null
--nincs ilyen rekord, mert
--az INSERT utasítás visszagördült -> a kereskedelmi rendszer leállt
```

Pontosan ezt NEM akarjuk. A szoros csatolás helyett laza csatolást valósítunk meg.
A lazán csatolt rendszer
Az ötlet az, hogy a trigger csak az eseményeket menti egy naplótáblába. Ezután feldolgozzuk a táblát a
tárolt eljárás.

```sql
A naplótábla és a trigger
A trigger az `inserted` és `deleted` virtuális táblákat használd. Ez a trigger több rekordos INSERT-eket is tud kezelni
és UPDATE-eket is.
--a naplótábla
go
--drop table order_log
go
create table order_log (
event_id int IDENTITY (1, 1) primary key ,
event_type varchar(50) NOT NULL ,
order_id int NOT NULL ,
orderitem_id int NULL ,
status int NOT NULL default(0),
time_created datetime NOT NULL default(getdate()) ,
time_process_begin datetime NULL ,
time_process_end datetime NULL ,
process_duration as datediff(second, time_process_begin, time_process_end)
)
go
drop trigger tr_log_order
go
create trigger tr_log_order ON Orders for insert, update as
declare @orderid int
select @orderid=orderid from inserted --az inserted-ben több mint egy rekord is lehet
print 'OrderID of the LAST record: ' + cast(@orderid as varchar(50))
if update(orderid) begin --if the orderid has changed, then this is an INSERT
print 'Figyelem: új rendelés'
insert order_log (event_type, order_id) --status, time_created use default
select 'new order', orderid from inserted
end else if update(shipaddress) or update(shipcity) begin --shipaddress or shipcity has
changed
print 'Figyelem: cím megváltozott'
insert order_log (event_type, order_id)
select 'address changed', orderid from inserted
end else begin --other change
print 'Figyelem: egyéb módosítás'
insert order_log (event_type, order_id)
select 'other change', orderid from inserted
end
go
--test #1
insert Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
```

```sql
select * from order_log
--egy új rekord került a naplótáblába
--teszt #2
insert Orders (CustomerID, OrderDate) values ('AROUT', GETDATE()), ('HANAR', GETDATE())
select * from order_log
--két új rekord került a naplótáblába
--teszt #3
update Orders set ShipVia = 3 where OrderID in (11097, 11096) --these are the IDs of test
#2
select * from order_log
--két új rekord került a következő típusból 'other change'
--a táblák visszaállítása
delete Orders where CustomerID in ('AROUT', 'HANAR') and EmployeeID is null
delete order_log
```

```sql
Az új rendelések feldolgozására szolgáló tárolt eljárás
We expect that the items of a new order are inserted subsequently after the order record is created.
--a simple stored procedure that processes a new order
--and returns 0 if all of its items could be committed to the inventory without error
--demonstrating also the use of output parameters
drop proc sp_commit_new_order_to_inventory
go
create procedure sp_commit_new_order_to_inventory
@orderid int,
@result int output
as
begin try
update products set unitsInStock = unitsInStock - od.quantity
from products p inner join [Order Details] od on od.ProductID=p.ProductID
where od.OrderID=@orderid
set @result=0
end try
begin catch
print ' Inventory error: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as
varchar(20)) + ')'
set @result=1
end catch
go
--test
select * from order_log --11097
select * from Products where ProductID=10 --unitsinstock =31
select * from Products where ProductID=9 --unitsinstock =29
insert [Order Details] (orderid, productid, quantity, UnitPrice, Discount)
values (11097, 9, 10, 30, 0),(11097, 10, 40, 30, 0) --a második tétel hibát fog okozni
in sp_commit_new_order_to_inventory
go
declare @res int
exec sp_commit_new_order_to_inventory 11097, @res output
print @res
exec sp_commit_new_order_to_inventory 11096, @res output
print @res
go
--check: no change in unitsinstock (OK)
select * from Products where ProductID=10 --unitsinstock =31
select * from Products where ProductID=9 --unitsinstock =29
```

```sql
Az eseménynapló feldolgozására szolgáló tárolt eljárás
Mivel az esemény típusától függően teljesen eltérő műveleteket kell végrehajtani, kurzort használunk az
`order_log` bejárására.

```sql
-- tárolt eljárás az order_log feldolgozására
--drop proc sp_order_process
go
create proc sp_order_process as
declare @event_id int, @event_type varchar(50), @order_id int, @result int
declare cursor_events cursor forward_only static
for
select event_id, event_type, order_id
from order_log where status=0 --csak a még nem feldolgozott események érdekelnek minket
set xact_abort on
set nocount on
open cursor_events
fetch next from cursor_events into @event_id, @event_type, @order_id
while @@fetch_status = 0
begin
print 'Esemény feldolgozása ID=' + cast(@event_id as varchar(10)) + ', Rendelési azonosító=' +
cast(@order_id as varchar(10))
update order_log set time_process_begin=getdate() where event_id=@event_id
begin tran
set @result = null
if @event_type = 'new order' begin
print ' Új rendelés feldolgozása...'
exec sp_commit_new_order_to_inventory @order_id, @result output
end else if @event_type = 'address changed' begin
print ' Címmódosítás feldolgozása...'
waitfor delay '00:00:01' -- csak a másik eseménytípus feldolgozását szimuláljuk
set @result=0
end else if @event_type = 'other change' begin
print ' Egyéb módosítás feldolgozása...'
waitfor delay '00:00:01'
set @result=0
end else begin
print ' Ismeretlen eseménytípus...'
waitfor delay '00:00:01'
set @result=1
end
if @result=0 begin
print 'Az eseményfeldolgozás sikeres'
commit tran
end else begin
print 'Az eseményfeldolgozás sikertelen'
rollback tran
end
print ''
update order_log set time_process_end=getdate(),
status=case when @result=0 then 2 else 1 end
where event_id=@event_id
fetch next from cursor_events into @event_id, @event_type, @order_id
end
close cursor_events deallocate cursor_events
go
--teszt
update order_log set status=0
select *from orders where EmployeeID is null
select * from order_log
exec dbo.sp_order_process
select * from order_log
```

```
-- kapjuk:
Esemény feldolgozása ID=5, Rendelési azonosító=11097
Új rendelés feldolgozása...
Készlethiba: Az UPDATE utasítás ütközött a CHECK megszorítással stb.
Az eseményfeldolgozás sikertelen
Esemény feldolgozása ID=6, Rendelési azonosító=11096
Új rendelés feldolgozása...
Az eseményfeldolgozás rendben
Az ütemezett feladat, amely meghívd az eseménynapló-feldolgozót
A munkát az SSMS GUI segítségével valósítjuk meg és a Job Activity Monitorban ellenőrizzük a működését.
GYAKORLAT: hozz létre egy laza csatolású megoldást, amely figyeli a Termékek táblát és új készletet rendel
a kapcsolódó Szállítótól, ha az UnitsinStock értéke a pontban meghatározott érték alá esik
ReorderLevel mező.

3. Replikáció, naplószállítás és feladatátvétel
   A laza csatolás esettanulmányában valójában a replikáció egy speciális formáját valósítottuk meg.
   Replikációs koncepciók és architektúra
   A replika az eredeti másolatát jelenti. Az adatbázis-technológiában a replikáció automatizálására szolgál
   adatok másolása és egyesítése több forrásból vagy forrásba. A replikációs metafora összetevői
   a következők.
- A közzétevő az az entitás (egy adatbázis-kiszolgáló), amely megosztani kívánt adatokkal rendelkezik. Az ilyen adatok
   kiadványokba rendezve. Minden kiadvány egy vagy több cikket tartalmaz. A cikkek képesek
   lehetnek táblák vagy táblák részei, tárolt eljárások vagy egyéb adatbázis-objektumok.
- Az előfizető az a jogalany, amely a kiadványokra előfizet. Ez lehet ugyanaz az adatbázis-kiszolgáló
   mint a kiadó vagy egy másik szerver. Több előfizető, esetleg különböző szervereken, előfordulhat
   előfizetni ugyanarra a kiadványra.
- Az előfizetés különféle módozatokat tartalmazhat az előfizetés módját és ütemezését illetően
   másolás. Tartalmazhat adatszűrőket vagy on-the-fly adatátalakítási lépéseket is. Ez lehet lökés ill
   egy pull előfizetés. A lekérhető előfizetéseket az előfizető hozd létre, és az előfizető ütemezi.
   A replikáció fő típusai és alkalmazási forgatókönyvei a következők.
- Pillanatkép replikáció. A cikkek első pillanatképe után a másolt objektumok a következők lesznek
   minden adatfrissítéskor eldobják és újra létrehozzák az előfizetőn, függetlenül attól
   történt-e változás a kiadványban. OLTP részeinek másolására használható
   adatbázist egy adattárházba vagy egy jelentéskészítő kiszolgálóra, munkaidőn kívül ütemezve. An
   például a nappal generált adatok egyik napról a másikra elküldése („időpontjelentések”). Mivel
   több előfizetés mutathat ugyanarra a céladatbázisra, a replikáció is használható
   ETL (extract-transform-load) mechanizmus, ha az SQL Server technológiát minden kiadó használd.
   FIGYELEM: a drop/re-create mechanizmus miatt az előfizetőnél tárgyak lehetnek
   átmenetileg elérhetetlen. Az adatok késleltetését is el kell viselni. Minden más replikáció
   az alábbi típusok pillanatfelvétellel vannak inicializálva.
- Tranzakciós replikáció. Csak a módosított adatokat másold, és lehet
   közel valós idejű adatszinkronizálásra konfigurálva. A replikált táblák elsődleges kulcsa a
   szükséges. Akkor alkalmazható, ha a jelentős késleltetés problémát jelent, és amikor nem akarunk mozogni
   változatlan adatok. Példa erre egy cég külső fióktelepe, amelyek saját helyi fiókkal rendelkeznek
   a központi adatbázisnak csak a működésük szempontjából releváns részeit tároló szerverek. Ilyen egy
   az architektúra javítja a webhely autonómiáját és az információs rendszer robusztusságát.
- Replikáció egyesítése. Ebben a sémában az előfizetők maguk generálhatnak módosításokat a
   adatokat, és létezik egy olyan mechanizmus, amely ezeket a változtatásokat az összes félhez eljuttatja és egyesíti
   konzisztens adatbázisba. Az összevonás folyamata konfliktusfeloldással is járhat. In
   A rekordok több szerveren történő azonosítása érdekében a tábláknak rendelkezniük kell egy mezővel
   UNIQUEIDENTIFIER adattípus ROWGUIDCOL3 tulajdonsággal. Tipikus forgatókönyv az eset
   utazó üzletemberek, akik nem mindig csatlakoznak a központi adatbázishoz. A változásokat
   A helyi adatbázisukban végrehajtott módosítások automatikusan összevonódnak mások módosításaival.
   A replikáció típusát mindig a kiadvány határozza meg.
   A replikációs technológia ütemezett jobokon alapul, és egyesítési replikáció esetén a bekapcsolásokon alapul
   megjelent cikkek.
   Úgy működik, mint egy identitásoszlop mag nélkül és globálisan egyedi értékekkel.

A replikáció nem ajánlott, ha a teljes adatbázis pontos másolatát kell karbantartani a
távoli szerver és a cél a rendelkezésre állás és a megbízhatóság javítása, mert a naplószállítás és a
Az SQL Server 2012 és újabb verzióinak Always-On technológiája egyszerűbb és robusztusabb megoldást kínál.
FIGYELMEZTETÉS: bár a replikáció több másolatot készít az adatokról, ez nem helyettesíti a biztonsági másolatokat
és a katasztrófa utáni helyreállítás tervezése.
A replikációban három kiszolgálói szerepkör van: a kiadó, a terjesztő és az előfizető. Mind a három
A szerepköröket ugyanaz a kiszolgálópéldány veheti fel, amikor egy helyi adatbázist egy másik helyi adatbázisba replikálnak
adatbázisból vagy különböző példányokból. Reálisabb beállításoknál az Elosztó szerepét egy másik veszi át
szervert a kiadó tehermentesítéséhez. A megváltozott adatok megosztott formában történő tárolásáért az Elosztó felelős
mappát vagy terjesztési adatbázist és az adatok továbbítását az előfizetőknek. Egy kiadó rendelkezhet
csak egy Elosztó, de egy Elosztó több előfizetőt is kiszolgálhat.
Kétirányú vagy frissíthető replikáció esetén az előfizető módosíthatod a fájlt
kiadó is.
Az SQL-kiszolgáló különféle ügynökökkel valósítja meg a replikációs funkciókat. Ezek az ügynökök futó feladatok
az SQL Server Agent felügyelete alatt.

- A Snapshot ügynök létrehozd a pillanatképet, és eltárolja a pillanatkép mappájában a
  Elosztó. Az ügynök a `bcp` (bulk copy) segédprogramot használd a kiadvány cikkeinek másolásához.
- Az elosztó ügynök. Pillanatkép-replikáció esetén ez az ügynök a pillanatképet a
  előfizető, és a tranzakciós replikációban futtatja a disztribúcióban tárolt tranzakciókat
  adatbázis az előfizetőről. A disztribúciós adatbázis egy rendszeradatbázis az Elosztón,
  ezért a Rendszeradatbázisok csoportban találja meg. Ez az ügynök a következő előfizetőjénél fut
  pull előfizetések, és a kiadónál fut a push előfizetések esetén.
- A Naplóolvasó ügynök beolvasd a tranzakciós naplót a kiadónál, és lemásold a megfelelőt
  tranzakciókat a naplóból az elosztási adatbázisba. Kizárólag tranzakciók során használatos
  replikáció. Minden közzétett adatbázishoz külön ügynök tartozik.
- A sorolvasó ügynök az előfizetők által végrehajtott módosításokat a kiadóba másold egy
  frissíthető vagy kétirányú tranzakciós replikáció.
- A Merge agent egyesíti az előfizetőnél és az előfizetőnél egyaránt előforduló növekményes változtatásokat
  kiadó az egyesített replikációban. A változások észlelése triggereken alapul. Az egyesítő ügynök nem
  tranzakciós replikációban használják.
  A pull-előfizetés kivételével minden ügynök az Elosztón fut.
  Pillanatkép replikáció
  Először is állítsd be a tesztkörnyezetet. Ahhoz, hogy a replikációs példák a várt módon működjenek, Te
  három „nevű” MS SQL Server példányt kell telepíteni ugyanarra a szervergépre. Azoknak kell lenniük
  PRIM, SECOND és THHIRD néven.
  Forgatókönyv: az amerikai vásárlók megrendeléseit egy másik adatbázisba szeretnénk replikálni ugyanazon
  szerver (fő) a jelentési adattárház egyik napról a másikra frissítéséhez. Pillanatkép replikációt választunk.
  A kiadvány létrehozása
1. Csatlakozz a főkiszolgálóhoz, és hozz létre egy új Northwind adatbázist, ha nem
   léteznek. Futtasd a Northwind adatbázis létrehozási kiírásását.
2. A „Nem hajtható végre adatbázis-főként” hiba elkerülése érdekében, mert a megbízó
   "dbo" nem létezik, stb., ami a Northwind adatbázis hiányos visszaállításának köszönhető,
   futtasd a következő szkriptet a Northwind adatbázisban:

```sql
EXEC sp_changedbowner 'sa';
ALTER AUTHORIZATION ON DATABASE::northwind TO sa;
```

3. Hozz létre egy másik üres adatbázist nw_repl néven, szintén a PRIM szerveren.

4. Indítsd el az SQL Server Agentet, ha nem fut

5. A Replikáció -> Elosztás konfigurálása menüpontot választva állítsd be a PRIM-et saját terjesztőjeként. Megjegyzés
   hogy a pillanatkép mappa ez lesz:
   C:\Program Files\Microsoft SQL Server\MSSQL14.PRIM\MSSQL\ReplData

6. Indítsd el az Új kiadvány varázslót, és válaszd ki a northwind-et publikációs adatbázisként:

7. A következő panelen válaszd ki a Pillanatkép kiadványt, majd válaszd ki a Megrendelések táblát egyetlenként
   a kiadvány cikke:

8. A Szűrőtábla párbeszédpanelen kattints a Hozzáadás gombra

9. Töltsd ki a szűrési utasítást az amerikai ügyfelek kiszűréséhez

10. Add meg, hogy a pillanatkép-ügynök kétpercenként fusson a következőnél a Módosítás lehetőség kiválasztásával
    panel. Megjegyzés: Ezt a rövid időintervallumot csak bemutató célokra használjuk. Az ügynök futtatja a bcp-t
    segédprogram, amely az egész táblat zárolja a másolás befejezéséig a garancia érdekében
    adatok konzisztenciája. Ez minden egyéb módosítani kívánt tranzakció blokkolását jelenti
    az táblat. Az éles rendszerekben a pillanatképek generálását ennek figyelembevételével kell ütemezni
    teljesítmény következményei.

11. Most meg kell adnunk az ügynök biztonságát. A Biztonsági beállítások lapon állítsd be saját felhasználóját
    hitelesítő adatok és megszemélyesíteni folyamatfiókot. Ez a legegyszerűbb módja annak, hogy a

snapshot agent írási jogosultsággal rendelkezik a pillanatkép mappába. Megjegyzés: csodálkozhat
miért használ az SQL Server Agent szolgáltatás vagy az SQLSERVER szolgáltatás alacsony jogosultságokkal rendelkező, nem rendszergazdai Windows-fiókot. Ennek az az oka, hogy ily módon egy támadó, aki
a DBMS sikeres feltörésével kisebb az esélye az egész szerver megrongálására.
12. A következő panelen válaszd a kiadvány létrehozása lehetőséget, és nevezd el „megrendelések”-nek.
A kiadvány ellenőrzése
Az új kiadvány a Helyi kiadványok alatt jelenik meg. A pillanatkép mappák a C:\Program mappában jönnek létre
Fájlok\Microsoft
SQL
Szerver\MSSQL14.PRIM\MSSQL\repldata\unc\WINMTFQ8CJAV81$PRIM_NORTHWIND_TEST, de nem készült tényleges pillanatkép, mert nem
az előfizetések még inicializálásra szorulnak.
Ellenőrizd az SQL Server Agent jobs alatt megjelenő új feladatot. A munkatörténet azt mutatja, hogy az ügynök igen
rendszeresen fut a konfiguráció szerint.
Push előfizetés létrehozása

1. Indítsd el az új előfizetési varázslót a rendelési kiadvány előugró menüjéből. Válaszd ki a
   közzétételt rendel el forrásként

2. A következő panelen válaszd az Összes ügynök futtatása a terjesztőnél lehetőséget a push előfizetéshez

3. Add meg ugyanazt a kiszolgálót, mint az előfizető, és az nw_repl értéket az előfizetési adatbázisnak

4. Állítsd be a terjesztési ügynök biztonságát a pillanatkép ügynökével megegyező módon

5. Az ütemezéshez válaszd a Futtatás folyamatosan lehetőséget, hogy minimális késleltetést biztosítson

6. A következő panelen válaszd az inicializálást. Ezzel létrejön az első pillanatkép a terjesztésben
   mappát.

7. Fejezze be az új előfizetés létrehozását
   Megjegyzés: az előfizetések és kiadványok tulajdonságait később módosíthatod, ha a Tulajdonságok lehetőséget választod
   előugró menüjükből.

Az előfizetés ellenőrzése

1. Keresd meg az új Rendelések táblát az nw_repl adatbázisban, és ellenőrizd, hogy tartalmazza-e az USA rendeléseit.
2. Ellenőrizd a pillanatkép mappa tartalmát. A tömeges másolás az SQL-kiszolgáló által használt gyors beszúrási módszer
   az adatokat közvetlenül az adatbázis-fájlokba.
3. Indítsd el a Replikációs figyelőt az új előfizetés előugró menüjéből, és ellenőrizd a
   a kiadvány és az előfizetés állapota. Itt megtekintheti az aktív replikációs ügynököket is:
4. Nyisd meg a Munkaaktivitás-figyelőt. A terjesztési ügynök új feladatként jelenik meg a listában, a következővel
   Állapot Végrehajtás mindig
5. Módosítsd a rendelési tábla első USA rekordját a kiadónál egy UPDATE utasítással.
   A változás röviddel (kb. 30 másodperccel) a pillanatkép-ügynök után megjelenik a replikált táblában
   legközelebb fut.
6. Végül töröld az előfizetést és a kiadványt. Ezt kiválasztással lehet elérni
   Parancsfájlok generálása a Replikációs csoport előugró menüjéből, add meg a „Eldobni…” és a
   futtatni a szkriptet egy szerkesztőben. Alternatív megoldásként az objektumokat egyenként kézzel is törölheti.
7. Az előfizetőnél lévő replikált táblák az előfizetés törlésével nem törlődnek, így
   töröld kézzel a Rendelések táblát az nw_repl adatbázisból.
   GYAKORLAT: hozz létre egy push snapshot kiadványt az nw_repl táblába, amely másold az alkalmazottakat
   az Alkalmazottak táblaból, amelynek címe Értékesítési képviselő. Ellenőrizd a helyes működést, majd töröld
   minden kapcsolódó objektum.
   Tranzakciós replikáció
   Forgatókönyv: közel valós idejű (ütemezett) laza csatolást kívánunk létrehozni a központi között
   Northwind adatbázis és egy off-site részleg, amely csak a kategória termékeivel foglalkozik
   „Italok” (CategoryID=1). Csak a rendeléseket és az italokat tartalmazó tételeket reprodukáljuk ezen keresztül
   tranzakciós replikáció.
   Először ezt a bemutatót egyetlen szerveren valósítjuk meg (Principal). A fenti szűrőfeltétel meghatározható
   az alábbiak szerint:

```sql
select * from [Order Details] where ProductID in (select productid from Products where
CategoryID=1)
select * from orders where orderid in (
select orderid from [Order Details] where ProductID in (select productid from
Products where CategoryID=1)
)
```

1. A replikációs konfigurációt visszaállíthatja a Közzététel és terjesztés letiltása lehetőség kiválasztásával
   a Replikáció menüből

2. Határozza meg a kiadvány típusát tranzakciósként a Kiadványtípus párbeszédpanelen

3. A Cikkek panelen válaszd ki a Rendelések és Megrendelés részletei táblákat

4. A Szűrőtábla panelen egyenként add hozzá a szűrőt a két táblahoz a WHERE másolásával.
   részben a fenti lekérdezésekből. A rendelések táblahoz:

5. Mindkét táblahoz meg kell adni a szűrőket:

6. A következő panelen válaszd a Pillanatkép azonnali létrehozása lehetőséget

7. A következő paneleken állítsd be az ügynökök biztonságát ugyanúgy, mint az előző demóban

8. Nevezze el a kiadványt nw_trans, és fejezze be a kiadvány létrehozását

9. Válaszd az Új előfizetés lehetőséget a kiadvány előugró menüjében

10. Válaszd az Összes ügynök futtatása az Elosztón lehetőséget a következő panelen (push előfizetés)

11. Válaszd ki az nw_repl adatbázist előfizetési adatbázisként:

12. Állítsd be a terjesztési ügynök biztonságát az előző bemutatóhoz hasonlóan

13. Add meg a Folyamatos futtatást a naplóolvasó és a terjesztési ügynökök ütemezéséhez:

14. A következő, Előfizetések inicializálása panelen válaszd az Azonnal lehetőséget

15. Teszteld a tranzakciós replikáció megfelelő működését. Frissítsd az alkalmazotti azonosítót az elsőben
    a Rendelések tábla rekordját az északi szél adatbázisban, majd válaszd ki ugyanazt a rekordot a
    nw_repl adatbázis. 10 másodpercen belül látnod kell a megváltozott értéket.

16. Ellenőrizd a replikációs ügynökök működését

17. Tisztítsa meg a replikációt az összes replikációs objektum törlésével
    Replikáció különálló szerverek között4
    A következő demóban ugyanazt a tranzakciós replikációt valósítjuk meg egy valósághűbb forgatókönyv használatával
    a PRIM mint kiadó, a MÁSODIK szerver mint terjesztő és a HARMADIK mint előfizető,
    ill. Egy még reálisabb forgatókönyv szerint ezek nem csak különálló szerverpéldányok, hanem
    külön szervergépeken is laknának. Egy ilyen forgatókönyvet azonban nem tudunk megvalósítani
    a laborban.
    Az elosztó konfigurálása

18. Indítsd el a MÁSODIK és a HARMADIK példányt, valamint az SQL Server Agentet a SECOND helyen

19. Állítsd vissza a PRIM replikációs konfigurációját a Közzététel és terjesztés letiltása lehetőség kiválasztásával
    a Replikáció menüből

20. A MÁSODIK példány replikációjának előugró menüjében válaszd az Elosztás konfigurálása lehetőséget, majd
    fogadd el az első választást. Ez létrehozd a terjesztési adatbázist a SECOND napon.
    A Windows 10 rendszereken futó SQL Server 2019 egyik hibája miatt a varázsló az `sp_adddistributor`
    használatakor a megadott jelszó helyett üres jelszót küldhet a távoli Elosztónak, és a 21768-as kivételt
    adhatja vissza. A bemutató futtatásához futtasd manuálisan az `sp_adddistributor` parancsot a helyes
    jelszóval, például:
    
    ```sql
    use master
    exec sp_adddistributor @distributor = 'DESKTOP-....\SECOND', @password = 'type password here'
    ```

21. A következő panelen válaszd ki, hogy manuálisan indítsuk el a Server Agentet

22. A következő panelen fogadd el a pillanatkép mappa helyét.

23. A következő panelen fogadd el a terjesztési adatbázis helyének és nevének alapértelmezett beállításait.

24. Ezután meg kell adnunk, hogy mely kiadói szerverek használhatják ezt a terjesztési adatbázist.
    A következő ablaktáblán töröld a SECOND kijelölését (mivel a SECOND nem kerül közzétételre), és a Hozzáadás megnyomásával,
    add hozzá a PRIM példányt:

25. A következő panelen meg kell adnia a disztribúciót használó kiadók jelszavát
    adatbázist kell használni. Ugyanazt a jelszót add meg, amelyet a bejelentkezéshez használ. Erre szükségünk lesz
    jelszót később.

26. A folyamat végén sikeresen konfigurálta az elosztót:
    A kiadó konfigurálása

27. Ahhoz, hogy a PRIM-et kiadóként konfigurálhassuk, először letiltjuk terjesztőként. Emlékezz arra
    eddig a PRIM saját Elosztójaként működött. A Replikáció előugró menüjében válaszd a Letiltás lehetőséget
    Terjesztés és kiadás. Ha a PRIM disztribútorként le van tiltva, megjelenik a felugró ablak
    menü változások. Válaszd most az Elosztás konfigurálása lehetőséget, és add meg a MÁSODIK példányt mint a
    PRIM Elosztóját:

28. A következő ablaktáblában add meg ugyanazt a jelszót, mint korábban (a 8. lépésben).

29. Az elosztás most be van állítva.
    A kiadvány és az előfizetés hozzáadása

30. Folytasd a tranzakciós kiadvány létrehozását a PRIM-en a szokásos módon (Rendelések tábla nélkül
    bármilyen szűrő).

31. Nem konfiguráljuk a terjesztési tulajdonságokat a THIRDON, mert a THIRD nem a
    kiadó.

32. Hozz létre egy új előfizetést a HARMADIK példányon a Hozzáadás a helyi előfizetésekből lehetőség kiválasztásával.
    Válaszd ki a PRIM-et kiadóként, és válaszd ki az előző lépésben létrehozott kiadványt.

33. Válaszd az Összes ügynök futtatása az Elosztón lehetőséget.

34. A varázsló új adatbázisként létrehozhatja az előfizetési adatbázist a HARMADIK oldalon
    nw_repl.

35. Teszteld az előfizetést. Nyiss meg egy lekérdezésszerkesztőt a PRIM-en, és frissítsd a Rendelések tábla rekordját.
    Nyiss meg egy lekérdezésszerkesztőt a HARMADIK oldalon, és ellenőrizd, hogy a változás átkerült-e a replikáltra
    táblát 10 másodpercen belül.

36. Töröld a kiadványt a PRM-nél és az előfizetést a HARMADIK oldalon. Töröld a replikált táblát
    HARMADIK.
    GYAKORLAT: implementáld a laza csatolási forgatókönyvet a rendelési esemény feldolgozásához tranzakciós használatával
    replikáció a Termékek, Rendelések és Rendelés részletei táblákban. Használd a három szervert a fenti beállításban,
    a SECOND elosztóként. Feltételezzük, hogy a logisztikai részleg saját adatbázissal rendelkezik,
    a HARMADIK szerveren fut.

37. Adj hozzá egy új „státusz” nevű mezőt a Rendelések táblához a PRIM northwind adatbázisában.
    példány, amelynek alapértelmezett értéke 0.

38. Módosítsd a meglévő rendelések állapotát 0-ról 2-re. Nem kívánunk minden meglévő rendelést feldolgozni.

39. Replikálja a három táblát az nw_repl adatbázisba tranzakciós replikáció segítségével

40. Mivel az előfizető megváltoztathatja a replikált rekordokat, és mivel a kereskedési alkalmazást használd
    a Megrendelések tábla soha nem frissíti az állapot mezőt, ezt a mezőt használjuk az előfizetőnél
    naplózza a rendelési rekordok feldolgozási állapotát az esettanulmányos megoldáshoz hasonló módon. Ebben
    így kerüljük el az extra naplótábla használatát. Részletek:
    a. Tudjuk, hogy az új rendelések állapota alapértelmezés szerint 0 lesz. A megváltozott jelölés érdekében
    megrendelések esetén használhatunk egy frissítési triggert a kiadónál, amely megváltoztatja az állapotát
    már meglévő rekord 1-re
    b. Az előfizetőnél végzett munka feldolgozza a 0 vagy 1 állapotú rendelésrekordokat, és beállítja a
    státusz 2-re siker esetén5

41. Valósítsd meg és teszteld a megoldást

42. Töröld a kiadványt és az előfizetést
    Peer-to-Peer tranzakciós replikáció
    Lehetővé teszi az írást bármelyik csomópontra, a változtatások automatikusan és csak az összes csomópontra terjesztésre kerülnek
    egyszer. Méretezéses olvasási terheléselosztáshoz tervezték. Ugyanazon rekord egyidejű írása többszörösen
    a csomópontok, azaz az írási ütközések nem engedélyezettek, és kritikus hibaként kezelhetők, amely manuális kezelést igényel
    felbontás6.
    Merge replikáció
    Forgatókönyv: értékesítési munkatársaink utaznak és új rendeléseket adnak le ügyfeleiknek. Alkalmanként ők
    a korábbi rendeléseket is módosítani kell, ha például megváltozik a szállítási cím. Az is lehet
    előfordulhat, hogy két alkalmazott ugyanazt a rendelést módosítja. Az alkalmazottak nincsenek folyamatosan kapcsolatban
    az internetre. Olyan replikációs megoldást kell terveznünk, amely az összes ilyen változtatást egyesíti egymással
    és a központi Northwind adatbázissal.
    Az egyesített replikáció során a naplóolvasó ügynök feladatait a triggerek, táblák és nézetek veszik át, amelyek
    automatikusan létrejön minden előfizetői adatbázisban és a kiadói adatbázisban is. A triggerek naplózzák
    változások az „MSmerge_*” nevű speciális rendszertáblákban, amelyek ugyanabban az adatbázisban jönnek létre, mint a
    replikált tábla. Minden táblához három „MSmerge_[ins, upd, del]_*” triggert hoztak létre.
    Vannak adatbázisszintű sémaindítók is, amelyek naplózzák a replikált sémájában bekövetkezett változásokat
    táblák.
    Az egyesítési replikáció egy pillanatkép-ügynök által létrehozott kezdeti pillanatfelvétellel kezdődik. Alapértelmezés szerint a pillanatfelvétel
    ügynök úgy van beállítva, hogy 14 naponként fusson. Ekkor az egyesítő ügynök feladata hasonló az elosztáshoz
    ügynök a tranzakciós replikációban azzal a különbséggel, hogy az egyesítési replikáció alapértelmezés szerint be van állítva
    kétirányú. Ez azt jelenti, hogy az ügynök az előfizetői és a kiadói oldalon is alkalmazza a változtatásokat.
    Minden előfizetéshez külön egyesítő ügynök tartozik. Az egyesítő ügynök push előfizetés esetén az Elosztón
    push előfizetés esetén és az előfizetőn pull-előfizetés esetén.
    A terjesztési adatbázis csak az előzményeket és a hibainformációkat tárolja.
    A kétirányú adatszinkronizálás támogatása érdekében az egyesített replikációban lévő cikkeknek rendelkezniük kell a
    egyedi azonosító (GUID) típusú oszlop, amely hasonló az azonosító adattípushoz, de globálisan állítja elő
    egyedi azonosítók7. Ha ilyen oszlop nem létezik, akkor automatikusan hozzáadódik a táblákhoz – ami igen
    Ez jól működik, ha a rendelést csak egyszer frissítik a kiadói oldalon.
    https://learn.microsoft.com/en-us/sql/relational-databases/replication/transactional/peer-to-peertransactional-replication
    Használd ezt az adattípust a következőképpen: CREATE TABLE teszt (my_guid egyedi azonosító DEFAULT NEWSEQUENTIALID()
    ROWGUIDCOL, stb

esetleg összeomlik a táblát már használó régi alkalmazások. Az új mező eltávolításra kerül, amikor a
kiadvány törlésre kerül.
A szinkronizálási folyamat részleteit ez a szöveg nem tartalmazza8.
A kiadvány
GYAKORLAT: A megoldás fejlesztéséhez kövesd az alábbi lépéseket.

1. Állítsd be a MÁSODIK példányt kiadóként akkor is, ha egyébként nem tesz közzé publikációt
   a megoldók listája nem lesz elérhető:

2. Állítsd be a MÁSODIK példányt a PRIM terjesztőjeként (lásd az előző részt). Utána
   ez az, amit látnod kell a PRIM-en:

3. Engedélyezd a northwind adatbázist az egyesített replikációhoz. Válaszd a Kiadványadatbázisok lapot
   a kiadó (PRIM):
   
   ```
   https://documentation.help/replsql/repltypes_30z7.htm
   ```

4. Válaszd ki a Northwind adatbázist a publikációs adatbázishoz, és válaszd ki a kiadvány típusát:

5. Fogadd el az alapértelmezett előfizetői típusokat, és válaszd ki a Megrendelések táblát az egyetlen cikkként
   kiadvány.

6. Az egyes cikkekhez különböző tulajdonságokat állíthat be a Cikk tulajdonságai menüpont kiválasztásával, beleértve a
   különböző típusú konfliktusokhoz használható megoldó. Konfliktus akkor következik be, amikor egy ügynök megpróbál változtatni
   egy rekord, amelynek függőben lévő módosítása van. A beépített megoldó modulok jelenleg regisztrálva vannak a
   szervert az sp_enumcustomresolvers eljárással lehet listázni. A szükséges paraméterekhez
   a beépített feloldók közül lásd 9. Saját feloldóját is hozzáadhatja tárolt eljárásként vagy
   DLL10. Az alapértelmezett feloldó az „első a megjelenítő nyer” stratégiát valósítja meg:
   a. ha a konfliktus egy Kiadó és egy Előfizető között lép fel, a Kiadó változása az
   elfogadásra kerül, és az Előfizetői érték elutasításra kerül.
   b. ha az ütközés két pull-előfizetést használó Előfizető között történik, akkor a
   az első Előfizetőről történő módosítás a Kiadóval való szinkronizáláshoz elfogadásra kerül, és
   másokat elutasítanak.

7. A következő panel arra figyelmeztet, hogy egy új GUID kerül hozzáadásra a táblahoz. Ez nem változtat a
   a tábla elsődleges és idegenkulcsos megszorításai.
   
   ```sql
   https://learn.microsoft.com/en-us/sql/relational-databases/replication/merge/advanced-merge-replicationconflict-com-based-resolvers?view=sql-server-ver16
   https://learn.microsoft.com/en-us/sql/relational-databases/replication/implement-a-custom-conflictresolver-for-a-merge-article
   Az egyéni feloldó eljárás a kiadón fut, és az Egyesítő ügynök hívd meg. Lekérdezi a
   changed record from the Subscriber using the row GUID received from the Merge agent, and returns a result
   set with a single record that has the same fields as the base table and that contains the values for the winning
   version of the record.
   ```

8. A pillanatkép ügynök ütemezésénél fogadd el az alapértelmezett értékeket, majd határozza meg az ügynök biztonságát a
   szokásos módon.

9. Nevezze el a kiadványt nw_merge, és hozd létre. Ellenőrizd az új GUID oszlopot és a 3 új oszlopot
   triggereket a Rendelések táblában.
   Az előfizetés
   Két előfizetőt adunk hozzá, hogy működés közben lássuk az egyesítési folyamatot.

10. Indítsd el manuálisan az SQL Server Agentet a THIRD webhelyen

11. A HARMADIK példányon válaszd az Új előfizetés lehetőséget, és add meg a PRIM-et kiadóként:

12. A következő ablaktáblán válaszd ki az előfizetés lekérését. Ez összhangban van azzal a szokásos elvárással, hogy a
    az előfizetők szeretnénk ütemezni a szinkronizálást.

13. Add hozzá a két előfizetőt, egyet a HARMADIK példányon és egyet a PRIM-en az újonnan létrehozott
    nw_merge_1-2 nevű adatbázisok.

14. Állítsd be az ügynökök biztonságát a szokásos módon.

15. Mindkét egyesítő ügynök szinkronizálási ütemezését a „Futtatás folyamatosan” értékre állítottuk. Megjegyzés: ez a beállítás
    csak teszt és demó célokra. Valós forgatókönyv esetén az egyesítési folyamat is elindulna
    meghatározott időközönként vagy igény szerint, amikor egy adott esemény, pl. VPN-kapcsolat jön létre a
    előfizető.

16. Azonnal inicializálja az előfizetéseket.

17. Összevont kiadványban az előfizetők újra kiadhatják azt a kiadványt, amelyhez
    előfizetnek (Server típusú előfizetés), így hierarchikus előfizetés jön létre
    építészet. A szerver típusú előfizetés explicit numerikus hozzárendelését is lehetővé teszi
    prioritást minden egyes kiszolgálónak, amelyet ütközés esetén használunk (lásd később). Válaszd ki az Ügyfél típusát
    előfizetés.

18. Zárd le és indítsd el a replikációt.

19. Győződjön meg arról, hogy a megváltozott értékek bármelyik előfizetőtől vagy a kiadótól eljutnak az összeshez
    a Megrendelések tábla három külön szerkesztőben történő szerkesztésével. Legyen türelmes: akár 2-ig is eltarthat
    perc a szinkronizálás befejezéséhez11.

20. Teszteld az érkezési sorrendben történő alapértelmezett konfliktusfeloldást, amikor a két előfizető
    egy rekord frissítése „egyidejűleg” (figyelembe véve, hogy az ügynökök percenként egyszer lekérdezik a naplókat).
    A kiadói adatbázist először elérő módosítási kérelem minden félre vonatkozik. Használd
    az Ablak -> Vízszintes tabulátorcsoport hozzáadása parancs az SSMS-ben mindhárom tábla megtekintéséhez
    egyidejűleg. Az adatrácsokat a Ctl-R billentyűkombinációval frissítheti.
    Az elosztott adatbázis-rendszerek a megfigyelés bármely időpontjában inkonzisztensek lehetnek, de a szinkronizálási mechanizmus
    garantálja, hogy ha nem történik további frissítés, akkor bizonyos idő elteltével globális konszenzus (konszenzus) születik
    idő. Ezt a viselkedést végső konzisztenciának nevezik. A CAP tétel szerint a C, A, P tulajdonságok nem
    minden elosztott adatbázisrendszerben teljes mértékben teljesüljön: Konzisztencia (minden olvasás megkapja a legutóbbi írási ill
    hiba), Elérhetőség (minden olvasás tartalmaz adatokat, de lehet, hogy nem a legfrissebbek), Partíciótűrés (a rendszer
    tolerálja a hálózati hibákat) -> mivel hálózati hibák előfordulnak, a konzisztenciát és a rendelkezésre állást ki kell cserélni
    az alkalmazás követelményeitől függően. A bemutatott egyesítési folyamat támogatja a rendelkezésre állást
    következetesség. Lásd: https://www.bmc.com/blogs/cap-theorem/

21. Az összevonási ütközések megtekinthetők és manuálisan feloldhatók a Replikációs konfliktus-megjelenítő eszközben,
    amely a kiadvány előugró menüjéből érhető el. Ha egy rekordot frissített
    mindhárom szerver, azaz a konfliktus 3 felet érint, két külön konfliktusként jelenik meg, a
    ugyanaz a győztes. Itt vagy elfogadhatja az alapértelmezett felbontást (a Küldés gombra kattintva
    Nyertes) vagy visszaállíthatja (a vesztes elküldése gombra kattintva):

22. Megtekintheti az egyesítési folyamat jelenlegi állapotát a Szinkronizálási állapot megtekintése lehetőség kiválasztásával
    az előfizetés előugró menüjében. A folyamatot manuálisan is elindíthatja.

23. Generálj és tekintsdn át replikációs szkripteket mindkét példányon a Parancsfájlok generálása innen lehetőség kiválasztásával
    a Replikáció csoport előugró menüjét.

24. Töröld az összes replikációs objektumot.
    GYAKORLAT: Az új forgatókönyvben az alkalmazottak frissítik a Termékek tábla egységárát a
    Northwind adatbázis és az egyidejű változások összevonása. Az egyik alkalmazott, aki a HARMADIK szervert használd,
    alacsonyabb prioritású, mint a másik. Hozz létre egy összevont kiadványt a PRIM-ből a pull-előfizetéssel
    MÁSODIK és HARMADIK. A prioritás beállításához használd a Szerver típusú előfizetést. Használd a Query konzolokat és a

Az ütközésmegjelenítő segítségével ellenőrizd, hogy az alacsonyabb prioritású alkalmazott mindig veszít-e, függetlenül attól, hogy a
időzítés.
A naplószállítás
Míg a replikáció elsődleges alkalmazási területe az üzleti folyamatok automatizálása, a naplószállítás
az adatbázis katasztrófa-helyreállításának előkészítésére szolgál, egy pontos, általában csak olvasható
másolat létrehozásával és szinkronizálásával, más néven „meleg” készenléti adatbázissal. A tranzakciós napló
az elsődleges szerverről több másodlagos szerverre is továbbítható.
A naplók szállítása az adatbázis teljes biztonsági másolatával kezdődik, amely visszaállításra kerül az ügyfélen. Aztán a három
a naplószállítás lépései a következők.

1. Az elsődleges kiszolgálón futó biztonsági mentési feladat biztonsági másolatot készít az adatbázis új részéről
   tranzakciós naplót a helyi szerverre

2. A másodlagos kiszolgálón futó másolási feladat a naplót egy konfigurálható célhelyre másold (pl.
   hálózati fájlszerver)

3. A másodlagos kiszolgálón futó visszaállítási feladat visszaállítja a biztonsági másolatot a másodlagos kiszolgálóra
   adatbázis(ok)
   Egy riasztási feladat is futhat, és figyeli, hogy az egyes lépések a várt módon és időben végrehajtódnak-e.
   A jobok ütemezésétől függően van késés a két adatbázis között. Ez a késleltetés
   kihasználható, ha az elsődleges adatbázis tévedésből módosul.
   GYAKORLAT: A mi forgatókönyvünkben létrehozunk egy „meleg biztonsági másolatot” a Northwind adatbázisról. Ez azt jelenti, hogy be
   szerverhiba esetén a készenléti kiszolgáló (azaz a melegmentés) helyettesítheti az éles szervert
   néhány perc alatt, anélkül, hogy hoszdsan visszaállítaná a teljes biztonsági másolatot. Az elsődleges és a másodlagos
   a szerverek normál módon futnak különböző szervergépeken, de a bemutatónkban ugyanazt a gépet és
   két szerverpéldány, az elsődleges és a másodlagos. Ezenkívül a Harmadik szerver a
   Monitor.

4. Hozz létre egy mappát a naplók tárolására, és egy másikat, ahová a másolatot el kell helyezni.

5. Állítsd mindkét mappa megosztását mindenkivel megosztásra (Tulajdonságok/Megosztás/Megosztás). Írd be a Mindenkit
   és állítsd be a Read/Write beállítást.

6. Az elsődleges szerveren lévő Northwind adatbázis előugró menüjében válaszd a Tulajdonságok és a lehetőséget
   ellenőrizd, hogy a Northwind adatbázis helyreállítási modellje Full értékre van-e állítva. Ez azt jelenti, hogy a
   A napló inaktív részei nem törlődnek egy ellenőrzőponton.

7. A PRIM-en a Nortwind adatbázis Feladatok -> Szállítási tranzakciónaplók panelen engedélyezd a
   adatbázis a szállításhoz, és válaszd a Biztonsági mentés beállításai lehetőséget. Írd be a \\WIN-MTFQ8CJAV81\logs parancsot
   a biztonsági mentési mappa hálózati elérési útja, a helyi mappa elérési útja pedig a C:\ship\logs.

8. Válaszd a Feladat szerkesztése lehetőséget, és állíts be egy ütemezést, amely percenként futtatja a feladatot. Megjegyzés: ez a beállítás csak a
   demó célokra.

9. Térj vissza az Adatbázis tulajdonságai panelre, és válaszd a Hozzáadás lehetőséget a Másodlagos adatbázisok részben:

10. A Másodlagos adatbázis-beállítások panelen írd be az új adatbázisnevet: nw_ship. Fogadd el a
    alapértelmezés az inicializáláshoz. A Fájlok másolása lapon írd be a C:\ship\dest címet a cél elérési útjaként. Állítsd be
    az ütemezés 1 percenként. Megjegyzés: ez a beállítás csak bemutató célokat szolgál.

11. A Visszaállítás lapon válaszd a Készenléti mód és a Felhasználók leválasztása lehetőséget, és add meg a visszaállítást is
    1 percenkénti ütemezés. Megjegyzés: ez a beállítás csak bemutató célokat szolgál.

12. Opcionálisan beállíthatja a HARMADIK kiszolgálót Monitor szerverként. A Monitor szerver a
    példány, amely mind az elsődleges, mind a másodlagos kiszolgálót figyeli, és a naplót is futtatja
    szállítási riasztási munka. Ez a feladat hibát generál, ha a három folyamat (biztonsági mentés, másolás,
    visszaállítás) nem hajtják végre sikeresen az előre beállított küszöbértéknél hoszdbb ideig
    (ami alapértelmezés szerint 45 perc). Használjon rövidebb időszakot, pl. 2 perc tesztelési célból. Használd
    az sa SQL Server egyszerű, hogy hitelesítse a riasztási feladatot az elsődleges és másodlagos hozzáféréshez
    esetek. Ezenkívül két riasztás is automatikusan beállításra kerül a monitorpéldányon a hiba miatt
    az elsődleges és a másodlagos példányok, de üres válaszokkal (azaz lenni
    a rendszergazda konfigurálta). Tipikus válasz az lenne, ha egy e-mailt küldenénk egy
    operátor.

13. Végezd el és futtasd a konfigurációt.

14. Ellenőrizd a helyes működést mindkét adatbázishoz való csatlakozással. Lehet, hogy 3 percet kell várnia
    a másodlagos adatbázis változásainak megtekintéséhez. Jelentést készíthet az aktuális állapotról
    a naplószállításról a Monitor szerver felugró menüjéből -> Reports -> Standard Reports ->
    Tranzakciónapló Szállítási állapot.

15. Ellenőrizd a napló és a célmappa tartalmát. Látnod kell a tranzakciós napló biztonsági másolatait
    percenként jelennek meg.

16. Tiltsd le a naplószállítást a PRIM szerveren. Mivel a másodlagos szállított adatbázis benne van
    készenléti állapotban, akkor a következő parancsokat kell végrehajtania, mielőtt eldobná (lásd alább).
    Alternatív megoldásként beállíthatja az adatbázist egyfelhasználós módba az SSMS GUI-n, és visszaállíthatja a
    adatbázis helyreállításával, és állítsd vissza többfelhasználósra.
    
    ```sql
    use master
    alter database nw_ship set single_user with rollback immediate
    restore database nw_ship with recovery
    alter database nw_ship set multi_user
    ```

Feladatátvevő klaszterek
Egy definíció szerint „Failover clustering (FC) a Windows Server olyan szolgáltatása, amely lehetővé teszi
csoportosítson több kiszolgálót egy hibatűrő fürtbe a rendelkezésre állás és a méretezhetőség növelése érdekében
alkalmazások és szolgáltatások, mint például… Microsoft SQL Server”12. Az FC működéséhez szervertípus szükséges
egynél több szervergépen futó rendszer. Ez az egyik oka annak, hogy nem tehetjük
bemutatni ezt a technológiát ezen a tanfolyamon.
Az FC beállítása után a fürttagokon futó SQL Server-példányok konfigurálhatók
egy Always On Availability Clusterbe. Egy ilyen klaszterben definiálhatunk adatbázisok egy csoportját, a.k.a.
„rendelkezésre állási adatbázisok”, amelyeket más példányokba másolnak, és amelyek együtt áthidalják. A feladatátvételen kívül
támogatás, egy ilyen architektúra konfigurálható automatikus olvasási terheléselosztáshoz nagy terhelés esetén
adatbázisok is.

```
https://docs.microsoft.com/hu-hu/windows-server/manage/windows-admin-center/use/manage-failoverclusters
https://docs.microsoft.com/hu-hu/windows-server/failover-clustering/failover-clustering-overview
```

4. Adatminőség és törzsadatkezelés
   Adattípusok egy cégnél:
- Tranzakciós (OLTP adatbázisokban)

- Hierarchikus (taxonómiák, adattárházak)

- Félig strukturált (XML, json)

- Strukturálatlan (e-mail, pdf, blogok)

- Törzsadatok

- Metaadatok (adatok az adatokon)
   A magas adatminőség (DQ) követelménye szigorúbb, mint az adatintegritás követelménye (például amikor szeretnénk
   elgépelt értékek kijavítására).
   Az adatminőség dimenziói:

- •
   Kemény méretek
  
  - Teljesség – rendelkezünk minden adattal?
  
  - Pontosság – pontosak az értékek?
  
  - Konzisztencia – ellentmondanak-e az adatok a különböző rendszerek között?
    Lágy dimenziók: a felhasználók által érzékelt jellemzők, például a bizalom.

Ha mind a lágy, mind a kemény dimenziók értékelése alacsony, akkor Master Data Management (MDM)
megoldást érdemes alkalmazni. Az MDM központi adattárolást igényel, valamint Data Governance-et,
vagyis az adatminőség bevezetésének és fenntartásának folyamatát, továbbá Data Stewardokat, akik
egyes adattípusok minőségéért felelnek, például egy steward felelhet az ügyféladatokért. Az MDM
technológiáit ez a jegyzet nem tárgyalja részletesen.

Az adatminőség (DQ) javítható tervezetten vagy reaktív módon; ez utóbbi kisebb cégnél is alkalmazható.
Egy DQ-megoldás sikerét például úgy mérhetjük, hogy figyeljük, hogyan csökken az idő előrehaladtával
a hibás vagy ismeretlen rekordok száma egy táblában.

DEMO: elemezzük a táblák oszlopait teljesség, konzisztencia, funkcionális függőség stb. szempontjából:

```sql
    use AdventureWorksDW2019
    --check if there is a functional dependency between two columns
    select SalesReasonKey, SalesReasonName, SalesReasonReasonType from DimSalesReason
    -- az adatok arra utalnak, hogy a SalesReasonReasonType oszlop a SalesReasonName oszloptól függ,
    -- vagyis az előbbi mindig meghatározható az utóbbiból
    --check if the data supports this assumption
    select SalesReasonReasonType, count(*) from DimSalesReason group by
    SalesReasonReasonType --3 groups with 4,5,1 members
    select SalesReasonName, count(*) from DimSalesReason group by SalesReasonName --each
    group has 1 member -> candidate key
    -- következtetés: a SalesReasonName valószínűleg a SalesReasonReasonType egyik alkategóriája
    -- funkcionális függőség ellenőrzése
    -- hogyan ellenőrizhető, hogy a CountryRegionCode funkcionálisan függ-e a StateProvinceCode-tól
    select * from DimGeography
    ```

Ezt az adatbázist a https://github.com/Microsoft/sql-serversamples/releases/download/adventureworks/AdventureWorksDW2019.bak címről lehet letölteni.

```sql
select StateProvinceCode, count(*) from DimGeography group by StateProvinceCode --71
select StateProvinceCode, count(*) from DimGeography group by
StateProvinceCode,CountryRegionCode --71
--71=71 so a StateProvinceCode will always have the same CountryRegionCode
--it is highly likely that we have a functional dependency between the two fields
select color, count(*) from dimproduct group by color --10
select ProductLine, count(*) from dimproduct group by productline --5
select ProductLine, count(*) from dimproduct group by productline, color --27 > 5, 27
> 10
```

```sql
-- nincs funkcionális függőség a két mező között
```

GYAKORLAT: elemezze a DimCustomer és DimEmployee táblák oszlopait a teljesség és
funkcionális függőség. DimCustomer: Iskolai végzettség<->Foglalkozás, DimAlkalmazott: Értékesítési Terület<>Nem
A de facto funkcionális függőség oka lehet egy nem modellezett, de létező üzleti szabály
üzleti tartomány. Egy ilyen rejtett kapcsolat tranzitív függőségen keresztül megsértheti a 3NF struktúrát
táblán belül, és ez redundanciához és következetlenséghez vezethet. Ezért érdeke a
hogy az ilyen kapcsolatokat adatelemzéssel észlelje.
PÉLDA: alkalmazottaink beosztási kóddal rendelkeznek (például kutató, menedzser, műszaki vagy titkár)
és egy oktatási szint kódja (például általános iskola, középiskola, Phd). Lehet, hogy létezik egy szabályzat
az a cég, amely egy bizonyos munkakörhöz csak egyetlen iskolai végzettséget tesz lehetővé, ezzel létrehozva egy de
tényleges funkcionális függőség a két mező között. Az iskolai végzettség függhet a munkakörtől.
Adatprofilalkotás
Az adatprofilozás vagy feltárás azt jelenti, hogy automatikusan megtalálja a statisztikákat és az adatminőséggel kapcsolatos jellemzőket
egy oszlopból:

- A funkcionális függőségek, a jelölt kulcsok és a potenciális idegen kulcsok azonosítása (lásd fent)
- Oszlopérték-eloszlások és egyéb statisztikák kiszámítása
- Mérje meg a nullarányt és a hossz-eloszlást karakterlánctípusoknál
- Vezess le de facto oszlopmintákat reguláris kifejezésekként azokból az értékekből, amelyeket használhat
  domain szabályok (lásd később)
  Az MS SQL Serverben az adatprofilozás az Integration Services adatprofilozási feladatként is elvégezhető
  amely XML-fájlba menti az eredményeket (ebben a szövegben nem részletezzük)14.
  SQL Server adatminőségi szolgáltatások
  A DQS szolgáltatás felelős a referenciaadatok tisztításáért, profilalkotásáért és egyeztetéséért. A DQS szerver
  tartalmazza a DQS motort és a DQS adatbázisokat:
- DQS_MAIN: tárolt eljárások, amelyek megvalósítják a DQS motort, plusz tudásbázisok, pl.
  US – Vezetéknév tudásbázis, referencia adatok: pl. városok Magyarországon. Szerepek a DQS_MAIN-ben

```
https://docs.microsoft.com/en-us/sql/integration-services/control-flow/data-profiling-task-and-viewer
```

adatbázis: dqs_admininstrator, dqs_kb_editor, dqs_kb_operator (különbözőhöz rendelhető
felhasználók)

- DQS_PROJECTS: a tisztításhoz és a projektek egyeztetéséhez szükséges adatok

- DQS_STAGING_DATA: ideiglenes tárhely a tisztítandó adatok számára, a tisztítás eredménye
  Adatminőségi kliens által elvégzendő feladatok: tudásbázisok kezelése, tisztítás/illesztés végrehajtása
  projekteket, adminisztrálja a DQS-t. Kliens implementációk:

- Az SQL Server Integration Services „DQS Cleansing transformation” csomópontja tisztítást végezhet
  egy SSIS-csomag adatfolyamában

- SQL Server 2017 Data Quality Client (DQC), egy táblai alkalmazás
  Adattisztító projektek
  Kétféle DQS projekt létezik:

- Alapvető adattisztítás: a cél az egyes mezőértékek korrigálása. demonstrálni fogunk
  ilyen típusú projekt ezen a tanfolyamon.

- Identitás leképezés és duplikáció megszüntetése egyezési szabályok szerint: a cél az azonosítás és
  távolítsa el az esetleg duplikált rekordokat, azaz az entitásokat. Az illesztési szabály KB szinten van meghatározva
  az adattudomány közös távolságmérőivel. Ezt a típust nem fogjuk demonstrálni
  projekt ezen a tanfolyamon.
  Mindkét típus a DQS_MAIN adatbázisban már telepített tudásbázison (KB) és használaton alapul
  ezeket a paramétereket:

- Tisztítás: a Minimális pontszám a javaslatokhoz paraméter állítja be a minimális hasonlóságot a generáláshoz
  egy javaslatot. Alacsonyabbnak kell lennie, mint az automatikus korrekció minimális pontszáma.

- Egyezés (de-duplikáció): az egyezési szabályzat küszöbértéke. Ez a rekord mértéke
  hasonlóság.
  A DQS tudásbázis (KB) több tartományt, azaz a tisztításhoz használt referenciaérték-készleteket tartalmazhat.
  A tartományt a következő összetevők határozzák meg:

- Név és adattípus pl. húr

- Normalizálási beállítások, mint például a nagybetűssé alakítás vagy az üres karakterek eltávolítása,
  formázás és helyesírás-ellenőrzés

- Referencia adatok, amelyek a DQS_MAIN adatbázisban tárolhatók, vagy alternatívaként lehetnek
  külső szolgáltatás nyújtja
  
  - A referenciaértékek, úgynevezett tartományértékek. A tartományérték egy sor, amely tartalmazza a
    vezető érték és szinonimáinak listája

- Tartományszabályok, hasonlóan a CHECK megszorításokhoz

- Olyan kifejezés alapú relációk, amelyek az értéknek csak egy részére vonatkoznak, pl. ‘%Ltd.%’ -> ‘%Limited
  Vállalat%'
  Szemantikailag összefüggő mezőkből összetett tartományok hozhatók létre, pl. város, utca stb. részei an
  egynél több oszlopban tárolt cím.
  Néhány alapértelmezett KB már telepítve van a DQS_MAIN-ben a PRIM szerveren, például Ország/régió,
  Amerikai megyék, amerikai vezetéknevek stb. Saját KB-kat is fejleszthetünk.
  DEMO: Megtisztítjuk a táblák vezetékneveit az alapértelmezett KB használatával
  Indítsd el a DQC-t, és írd be a kiszolgáló nevét: WIN-MTFQ8CJAV81\PRIM.

- Az Adminisztráció->Konfiguráció->Általános beállítások panelen tekintsd át a minimális pontszámot
  Javaslatok és minimális pontszám az automatikus javítási beállításokhoz. Ezeket a beállításokat a
  próba-hiba alapon

- A Tudásbázis kezelőpanelen tekintsd át az előre telepített KB-kat

- Hozz létre egy új, `Lastnames` nevű adattisztítási projektet.

- Válaszd a `KB: DQS Data` tudásbázist és a `US_Last Name` domént. A művelet legyen `Cleansing`.

- A Térkép oldalon válaszd ki az AdventureworksDW2019 adatbázist, a DimCustomer táblát és
  a Vezetéknév mezőt, és rendeld hozzá a US_Last Name tartományhoz

- Indítsd el a tisztítási folyamatot. Mivel több mint 18000 vezetéknevünk van a DimCustomerben
  táblát a tisztításhoz, az előfeldolgozás kb. 5 perc, tisztítás kb. 30 s. FIGYELMEZTETÉS: 15

- Ellenőrizd a teljesség (100%) és a pontosság (98%) kemény méreteit. Tisztítás után a
  az érték a következő állapotok egyikében lehet:
  
  - Helyes: a domain értékekben található
  - Javítva: automatikusan megváltozott egy domain értékre, mert a hasonlóság fent volt
    az automatikus javítás minimális pontszáma
  - Javasolt: új érték csak azért javasolt, mert a hasonlóság a Min
    Pontszám a javaslatokért
  - Új: hasonló érték nem található a tartományértékek között, de az érték megfelel
    a domain szabályokat
  - Érvénytelen: egy új érték, amely ellentmond a tartományszabályoknak
    Ha az előfeldolgozás során „Párhuzamos feldolgozási feladat nem sikerült” hibaüzenetet kap, ellenőrizd a
    DQServerLog.DQS_MAIN.log fájl a példány Log könyvtárában. A hiba a „DELETE utasítás
    ütközött a REFERENCE "B_INDEX_LEXICON_EXTENSION_B_INDEX_LEXICON_FK" megszorítással. A konfliktus
    előfordult a "DQS_PROJECTS" adatbázisban, a "DQProject1000001.B_INDEX_LEXICON_EXTENSION" tábla oszlopában
    'TERM_ID'. Az SSMS Kulcsok módosítása panelen állítsd be a Törléskor műveletet a
    B_INDEX_LEXICON_EXTENSION_B_INDEX_LEXICON_FK idegen kulcs kényszere a CASCADE-hez.

- A fenti Min Score beállításokkal a folyamat talál néhány olyan esetet, amikor korrekcióra van szükség
  javasolt és 3 olyan eset, amikor a korrekciót automatikusan végrehajtották. 328 név volt
  helyesen megtalálható a KB-ban.

- Próbáljon meg jóváhagyni egy javasolt változtatást -> a sor átkerül a Javítva ablaktáblára

- Végül mentsd el a LastNameSource és LastNameOutput oszlopokat tartalmazó megtisztított táblát
  az eredeti adatbázisban, és dolgozza fel T-SQL parancsokkal.
  GYAKORLAT: tisztítsa meg az AdventureworksDW2019.DimGeography.EnglishCountryRegionName mezőt
  az Ország/régió tartomány használatával. Próbáld újra, miután felvett egy hibásan elírt országot a táblahoz (Austrila).
  Saját tudásbázis létrehozása
  Egy táblamezőben meglévő értékkészletet használhatunk egyéni KB létrehozásához. A lépések:
1. Automatikus tudásfeltárás az adatminta segítségével

2. Kézi tartománykezelés és konfigurálás
   DEMO: létrehozunk egy KB-t
- Hozz létre egy új nézetet a `DQS_STAGING_DATA` adatbázisban:
  
  ```sql
  use DQS_STAGING_DATA
  go
  create view vi_places as
  select distinct City, StateProvinceName StateProvince, EnglishCountryRegionName
  CountryRegion
  from AdventureworksDW2019.dbo.DimGeography
  ```
  
  ```
  go
  ```

- Indítsd el a DQS-ügyfelet, és hozz létre egy új KB-t helyek néven

- Válaszd a Tudásfelderítés lehetőséget, állítsd be a forrást a vi_places értékre, és hozz létre két nevű tartományt
   city_domain és countryregion_domain a vi_places azonos nevű mezőivel
   nézet

- Indítsd el a felfedezést

- A Muehlheim nyílásban állítsd a típust Error értékre, és kézzel írd be a Mühlheimet a „Helyes” mezőbe.
  mezőbe, majd nyomd meg az Enter billentyűt

- Válaszd ki az új tudásbázist a főmenüből, majd az előugró menüben válaszd a `Domain management` lehetőséget.

- Manuálisan adj hozzá egy születési_domain nevű új domaint egy egyszerű tartományszabállyal:

- Tegye közzé a KB-t

- Válaszd ki kezelésre az új tudásbázist, és exportáld `places.dqs` nevű fájlba.

- Hozz létre egy új `test_customer` táblát a `DQS_STAGING_DATA` adatbázisban a `DimCustomer`
  és a `DimGeography` tábla `GeographyKey` oszlopon történő összekapcsolásával.

- Módosítsd az első ügyfél születési dátumát 1925-01-02-re, a várost pedig Muehlheimre. Változás
  a második vásárló városa Piripócsra.

- Használd az új `places` tudásbázist a `test_customer` tábla tisztításához, majd tekintsd át az eredményeket.

GYAKORLAT: Hozz létre egy KB-t a DimProduct tábla, ProductName mező segítségével, és mutasd be alkalmazását
mint fent.
Az adattisztításhoz, törzsadatkezeléshez ingyenes, független eszközök is rendelkezésre állnak pl.
https://openrefine.org/

5. Oszloptár és particionálás
   Oszloptár
   Az oszloptár a relációs adatok tárolásának alternatív módja. Nagy, sok mezőt tartalmazó és ritkán változó
   adattárház-táblákhoz ajánlott. A táblablokkokban (oldalak) a mezők a
   egy rekordot nem tárolunk együtt, hanem minden mezőt külön-külön tárolunk, és a rekord értékeit
   össze vannak kapcsolva16. Gyorsaságát a tömörítés miatti kevés I/O műveletnek (blokkolvasásnak) köszönheti
   oldalak közül 17 (csökkentett méret -> kevesebb oldal), és az a tény, hogy a lekérdezések általában nem igényelnek olvasást
   az egész rekordot, csak néhány mezőt. Ez különösen akkor nyilvánvaló, ha az táblán nagyon
   nagy számú mező, ami jellemző az adattárházakra. A tömörítés típusai:
- A sortömörítés a rögzített hosszúságú adattípusokat változó hosszúságú adatokkal helyettesíti, például egy 4 bájtos
   egész szám típusú mező a tényleges értéktől függően akár 1 bájton is tárolható. OLTP alkalmazásoknál használható.

- Az oldaltömörítés egész oldalakat tömörít, és jobban alkalmazható az adattárházra
   alkalmazásokhoz vagy a ritkán frissített OLTP-alkalmazásokhoz. A tömörítés különösen
   akkor hatásos, ha egy mező értékei meglehetősen hasonlóak, más néven alacsony számosságú mezők.
  
  Az oszloptárat és az oldaltömörítést SQL Serveren mutatjuk be, mivel a Postgres ingyenes verziója
  jelenleg nem támogatja a tömörítést.
  
  ```sql
  use AdventureWorksDW2016_ext
  /*
  --create a BTREE table
  select * into FactResellerSalesXL_BTREE from FactResellerSalesXL_CCI --2 min 30 s
  alter table FactResellerSalesXL_BTREE alter column SalesOrderLineNumber tinyint not
  null
  alter table FactResellerSalesXL_BTREE alter column SalesOrderNumber nvarchar(20) not
  null
  alter table FactResellerSalesXL_BTREE add constraint c1 primary key
  (SalesOrderLineNumber, SalesOrderNumber) --2 min
  */
  --RESTART SERVER
  set statistics time on
  set statistics io on
  go
  select count(*) from FactResellerSalesXL_BTREE --11669638
  exec sp_spaceused 'dbo.FactResellerSalesXL_BTREE', @updateusage = 'TRUE'
  --data: 2523168 KB KB, index: 9776 KB KB
  select count(*) from FactResellerSalesXL_PageCompressed --11669638
  exec sp_spaceused 'dbo.FactResellerSalesXL_PageCompressed', @updateusage = 'TRUE'
  --data: 695624 KB KB KB, index: 2344 KB KB KB
  select count(*) from FactResellerSalesXL_CCI --11669638
  exec sp_spaceused 'dbo.FactResellerSalesXL_CCI', @updateusage = 'TRUE'
  --data: 525344 KB, index: 157624 KB
  go
  dbcc freeproccache --
  ```
  
  ```
  https://learn.microsoft.com/en-us/sql/relational-databases/indexes/columnstore-indexesoverview?view=sql-server-ver16
  https://learn.microsoft.com/en-us/sql/relational-databases/data-compression/data-compression?view=sqlserver-ver16
  ```

```sql
dbcc dropcleanbuffers -- empty data buffer
--B-TREE
--======
select b.SalesTerritoryRegion
,FirstName + ' ' + LastName as FullName
,count(SalesOrderNumber) as NumSales
,sum(SalesAmount) as TotalSalesAmt
,Avg(SalesAmount) as AvgSalesAmt
,count(distinct SalesOrderNumber) as NumOrders
,count(distinct ResellerKey) as NumResellers
from FactResellerSalesXL_BTREE a
inner join DimSalesTerritory b on b.SalesTerritoryKey = a.SalesTerritoryKey
inner join DimEmployee d on d.Employeekey = a.EmployeeKey
inner join DimDate c on c.DateKey = a.OrderDateKey
where b.SalesTerritoryKey = 3 and c.FullDateAlternateKey between '1/1/2006' and
'1/1/2010'
group by b.SalesTerritoryRegion,d.EmployeeKey,d.FirstName,d.LastName,c.CalendarYear
--CPU time = 3949 ms, elapsed time = 9568 ms
--DATA_COMPRESSION = PAGE
--================================
go
select b.SalesTerritoryRegion
,FirstName + ' ' + LastName as FullName
,count(SalesOrderNumber) as NumSales
,sum(SalesAmount) as TotalSalesAmt
,Avg(SalesAmount) as AvgSalesAmt
,count(distinct SalesOrderNumber) as NumOrders
,count(distinct ResellerKey) as NumResellers
from FactResellerSalesXL_PageCompressed a
inner join DimSalesTerritory b on b.SalesTerritoryKey = a.SalesTerritoryKey
inner join DimEmployee d on d.Employeekey = a.EmployeeKey
inner join DimDate c on c.DateKey = a.OrderDateKey
where b.SalesTerritoryKey = 3
and c.FullDateAlternateKey between '1/1/2006' and '1/1/2010'
group by b.SalesTerritoryRegion,d.EmployeeKey,d.FirstName,d.LastName,c.CalendarYear
GO -- CPU time = 3264 ms, elapsed time = 3776 ms.
--column store with page compression
--create clustered columnstore index [IndFactResellerSalesXL_CCI] on
[dbo].[FactResellerSalesXL_CCI]
--with (drop_existing = off, compression_delay = 0, data_compression = columnstore) on
[primary]
--===============================
select b.SalesTerritoryRegion
,FirstName + ' ' + LastName as FullName
,count(SalesOrderNumber) as NumSales
,sum(SalesAmount) as TotalSalesAmt
,Avg(SalesAmount) as AvgSalesAmt
,count(distinct SalesOrderNumber) as NumOrders
,count(distinct ResellerKey) as NumResellers
from FactResellerSalesXL_CCI a
inner join DimSalesTerritory b on b.SalesTerritoryKey = a.SalesTerritoryKey
inner join DimEmployee d on d.Employeekey = a.EmployeeKey
inner join DimDate c on c.DateKey = a.OrderDateKey
where b.SalesTerritoryKey = 3
and c.FullDateAlternateKey between '1/1/2006' and '1/1/2010'
group by b.SalesTerritoryRegion,d.EmployeeKey,d.FirstName,d.LastName,c.CalendarYear
GO -- CPU time = 360 ms, elapsed time = 492 ms
```

Megjegyzés az olvasási statisztikákhoz:

- A logikai olvasások 8 KB-os oldalolvasások az adatpufferből
- A fizikai beolvasások olyan olvasások, amelyeket a tárolóból (az operációs rendszerből) kellett lekérni, ezek azok
  blokkolja a lekérdezés végrehajtását
- Az előreolvasás aszinkron olvasási kérelmek az operációs rendszer felé olyan oldalak esetében, amelyek valószínűleg ilyenek
  szükséges a lekérdezéshez. Ezek nem blokkolják a lekérdezést.
  A kimenet a `Workfile` és a `Worktable` elemeket is említi a többi tábla mellett. A munkatábla (`Worktable`)
  egy belső tábla, amely mindig szükséges a sormódú `hash join` művelethez, a bemenet hash partíciókra
  bontásához. A munkafájlok (`Workfile`) a hash-illesztések és a hash-aggregátumok ideiglenes eredményeinek
  tárolására szolgálnak.
  Partícionálás
  A particionálás célja: oszd meg és uralkodj. Ha egy tábla egy mező mentén particionálva van:
- Mivel a fizikai olvasások jelentik az adatbázislekérdezések végrehajtásának szűk keresztmetszetét, a lekérdezések gyorsabban futnak, ha
  minden partíció más fizikai tárolón van, mert az olvasások párhuzamosíthatók. Mert
  a legtöbb lekérdezés esetén elegendő lehet néhány partíció elolvasása (nem mindegyik).
- A nagy tábláknál gyakran korlátozott a betöltési idő, pl. éjszakánként egy bankrendszerben stb., amikor
  az adatok nem változnak. Az INSERT és a DELETE naplózott utasítások (implicit, naplózott
  tranzakciók), így túl sok rekord beszúrása vagy törlése egyszerre lassú (pl. indexeknek kell
  utána újjá kell építeni). A particionálás gyorsabbá teszi a betöltést, mert a nagy tábla helyett
  beszúrása esetén egy üres táblapartícióra írunk, ami egy gyors „minimálisan bejelentkezett” művelet (in
  egyszerű helyreállítási mód).
  Nehéz meghatározni a pontos táblaméretet, ahol már érdemes particionálni, de szabály
  hüvelykujj az, hogy a tábla mérete meghaladd az adatbázis-kiszolgáló fizikai memóriáját.
  Tipikus particionáló kulcs a dátum, pl. hónap vagy év szerint. A tábla oszloptári indexe, ha van
  egyet, szintén particionálni kell (igazított index). Ekkor a partícióváltás nem igényel átépítést
  az index, csak a metaadatok módosulnak. Az SQL Server alapvető particionálási koncepciói:
- Partícionálási séma: partíciókat rendel fájlcsoportokhoz
- Partícionálási funkció: minden rekordot hozzárendel egy partícióhoz a mögöttes mező(i) alapján
  particionálás, például a dátum
  Megjegyzés: A partíciók mérete (rekordok száma) eltérő lehet.
  Ajánlott bevált gyakorlat egy nagy tábla particionálásához és betöltéséhez minimális naplózással (pl.
  amikor új adatok érkeznek az adattárházba) a következő.
1. Hozd létre a particionálási sémát és függvényt
2. Meglévő adatok betöltése (kezdeti betöltés)
3. Az új adatok betöltéséhez hozz létre egy üres segéd (staging) táblát azzal
   séma (és tömörítés) mint a tábla
4. Ebben a táblában egy ellenőrzési kényszer védi a particionáló kulcsot, hogy ne legyenek hibás adatok
   behelyezve
5. Az új adatok betöltődnek a segédtáblába, és létrejön egy oszloptári index
6. Cserélje le a segédtáblát a ténytábla következő üres partíciójára
7. A következő partíció betöltése előtt törölnünk kell az oszloptár indexét és frissítenünk kell a
   ennek megfelelően ellenőrizd a kényszert

```sql
set statistics time off
set statistics io off
--by year:
select min(OrderDate), max(OrderDate) from FactInternetSales s
--2010..2014
--we'll have 5 partitions for the 5 years
--drop table InternetSales
go
--part. function:
--drop partition function PfInternetSalesYear
create partition function PfInternetSalesYear (tinyint) as range left for values (10,
11, 12, 13)
--e.g. '10' will mean that the year <= 2010 (due to the LEFT)
--TINYINT: 1 byte, 0..255
--part. scheme: all in the same filegroup
--drop partition scheme PsInternetSalesYear
create partition scheme PsInternetSalesYear as partition PfInternetSalesYear all to
([PRIMARY])
go
--Note: we must combine the identity key with the part. number because the identity
may be unique only within the part.
--drop table InternetSales
create table InternetSales(
InternetSalesKey int not null identity(1,1),
PcInternetSalesYear tinyint not null, --part. number
ProductKey int not null,
DateKey int not null,
OrderQuantity smallint not null default 0,
SalesAmount money not null default 0,
UnitPrice money not null default 0,
DiscountAmount float not null default 0,
constraint PK_InternetSales primary key (InternetSalesKey, PcInternetSalesYear)
)
ON PsInternetSalesYear(PcInternetSalesYear) --this'll make the partitions
GO
--adding external keys and page compression
--ALTER TABLE dbo.InternetSales ADD CONSTRAINT FK_InternetSales_Customers FOREIGN
KEY(CustomerDwKey)
--REFERENCES dbo.Customers (CustomerDwKey);
ALTER TABLE dbo.InternetSales ADD CONSTRAINT FK_InternetSales_Products FOREIGN
KEY(ProductKey)
REFERENCES dbo.DimProduct (ProductKey);
ALTER TABLE dbo.InternetSales ADD CONSTRAINT FK_InternetSales_Dates FOREIGN
KEY(DateKey)
REFERENCES dbo.DimDate (DateKey);
ALTER TABLE dbo.InternetSales REBUILD WITH (DATA_COMPRESSION = PAGE);
GO
--load data up to 2013
INSERT INTO dbo.InternetSales (PcInternetSalesYear, ProductKey, DateKey,
OrderQuantity, SalesAmount, UnitPrice, DiscountAmount)
SELECT CAST(SUBSTRING(CAST(OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) AS
PcInternetSalesYear,
--note the trick: dates are stored as int e.g. 20110223 to save space
ProductKey, OrderDateKey, OrderQuantity, SalesAmount, UnitPrice, DiscountAmount
FROM FactInternetSales AS FIS
WHERE CAST(SUBSTRING(CAST(FIS.OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) < 13
GO
--how many records in partitions?
SELECT $PARTITION.PfInternetSalesYear(PcInternetSalesYear) AS PartitionNumber,
COUNT(*) AS NumberOfRows
FROM InternetSales GROUP BY $PARTITION.PfInternetSalesYear(PcInternetSalesYear)
PartitionNumber
NumberOfRows
--2010
```

```sql
--2011
--2012
--az utolsó partíció még mindig üres
--columnstore:
CREATE COLUMNSTORE INDEX CSI_InternetSales ON dbo.InternetSales
(InternetSalesKey, PcInternetSalesYear, ProductKey, DateKey,
OrderQuantity, SalesAmount, UnitPrice, DiscountAmount)
ON PsInternetSalesYear(PcInternetSalesYear) --Note: the index is aligned to the
partition
GO
--a new staging table to receive the year 2013 data
--in order to avoid errors we use a check constraint
create TABLE dbo.InternetSalesNew (
InternetSalesKey INT NOT NULL IDENTITY(1,1),
PcInternetSalesYear TINYINT NOT NULL CHECK (PcInternetSalesYear = 13), --check
ProductKey INT NOT NULL,
DateKey INT NOT NULL,
OrderQuantity SMALLINT NOT NULL DEFAULT 0,
SalesAmount MONEY NOT NULL DEFAULT 0,
UnitPrice MONEY NOT NULL DEFAULT 0,
DiscountAmount FLOAT NOT NULL DEFAULT 0,
CONSTRAINT PK_InternetSalesNew PRIMARY KEY (InternetSalesKey,
PcInternetSalesYear)
)
GO
ALTER TABLE dbo.InternetSalesNew ADD CONSTRAINT FK_InternetSalesNew_Products FOREIGN
KEY(ProductKey) REFERENCES dbo.dimProduct (ProductKey);
ALTER TABLE dbo.InternetSalesNew ADD CONSTRAINT FK_InternetSalesNew_Dates FOREIGN
KEY(DateKey) REFERENCES dbo.dimDate (DateKey);
go
ALTER TABLE dbo.InternetSalesNew REBUILD WITH (DATA_COMPRESSION = PAGE)
GO
--load 2013
--since the table was empty, the insert will not be logged
INSERT INTO dbo.InternetSalesNew (PcInternetSalesYear,ProductKey, DateKey,
OrderQuantity, SalesAmount,UnitPrice, DiscountAmount)
SELECT CAST(SUBSTRING(CAST(OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) AS
PcInternetSalesYear,
ProductKey, OrderDateKey,OrderQuantity, SalesAmount, UnitPrice, DiscountAmount
FROM FactInternetSales
WHERE CAST(SUBSTRING(CAST(OrderDateKey AS CHAR(8)), 3, 2) AS TINYINT) = 13
GO
--columnstore for the staging table
CREATE COLUMNSTORE INDEX CSI_InternetSalesNew
ON dbo.InternetSalesNew (InternetSalesKey, PcInternetSalesYear, ProductKey, DateKey,
OrderQuantity, SalesAmount, UnitPrice, DiscountAmount);
GO
--a kulcsfontosságú lépés a 4. partíció betöltése
ALTER TABLE dbo.InternetSalesNew SWITCH TO dbo.InternetSales PARTITION 4
--this required no data transfer
--partitions:
SELECT $PARTITION.PfInternetSalesYear(PcInternetSalesYear) AS PartitionNumber,
COUNT(*) AS NumberOfRows
FROM dbo.InternetSales GROUP BY $PARTITION.PfInternetSalesYear(PcInternetSalesYear)
order by PartitionNumber
PartitionNumber
NumberOfRows
52801
```

```sql
select count(*) from InternetSalesNew --0!
```

```sql
You can do all this also in the Storage menu of the SSMS GUI.
PRACTICE: create a partitioning scheme for the FactResellerSales table according to the DueDateKey
field and load it partition by partition.
A Postgres alternatíva a partíciók közvetlen kezelését igényli táblákként18.
select * from products where productname <'N'
select * from products where productname >='N'
--drop table products_p
create table products_p --a szülőtábla virtuális, nem tárol adatot
(productid int, productname varchar(40), part_key char(1), unitprice money)
partition by range(part_key)
create table products_p_a_m partition of products_p for values from ('a') to ('m'); -mind the overlap, ‘m’ will go to the second partition
create table products_p_m_z partition of products_p for values from ('m') to ('z');
--create table products_p_n_z partition of products_p for values from ('n') to ('z')
tablespace very_fast_drive;
insert into products_p (productid, productname, part_key, unitprice)
select productid, productname, substring(productname, 1,1), unitprice from
products
--queries are redirected to the right partition
select * from products_p where productname <'d' --5
--a partíciók közvetlenül is lekérdezhetők
select * from products_p_a_m where productname <'d' --5
select * from products_p_m_z where productname <'d' --0
--partitons can be managed independently
drop table products_p_a_m;
--remove from the parent table but keep the data
alter table products_p detach partition products_p_a_m;
--for loading, the new partiton can be created independently, then attached to the
parent table
alter table products_p attach partition products_p_a_m for values from ('a') to ('m');
--it is recommended to create check constraints on partitions -> helps the query
optimizer
```

A Postgresben a tábla öröklődési mechanizmusát is használhatod a particionálás támogatására, azonban a
a folyamat bonyolultabb19:

1. Hozd létre a „szülő” táblát, amelyből az összes partíció örökölni fog.

2. Hozz létre több „gyermek” táblát (mindegyik az adatok egy-egy partícióját képviseli), amelyek mindegyikétől öröklik
   a szülő.

3. Adj meg kényszereket a partíciós táblákhoz az egyes partíciók sorértékeinek meghatározásához.

4. Hozz létre indexeket bármely szülő- és gyermektáblán külön-külön. (Az indexek nem terjednek innen
   a szülőtáblákból a gyermektáblákba).

5. Írj egy megfelelő trigger függvényt a fő táblába úgy, hogy az beszúródjon a szülőtáblába
   irányítsa át a megfelelő partíciós táblába.
   
   ```
   https://www.postgresql.org/docs/current/ddl-partitioning.html#DDL-PARTITIONING-DECLARATIVE-BESTPRACTICES
   https://medium.com/timescale/scaling-partitioning-data-postgresql-10-explained-cd48a712a9a1
   ```

```sql
6. Create a trigger that calls the trigger function.
7. Remember to redefine the trigger function when the set of child tables changes.
Alternatively, the steps 5-6 can be avoided by a rule as in the example below.
create table products_i --a szülőtábla virtuális, nem tárol adatot
(productid int, productname varchar(40), unitprice money);
--drop table products_i_a_m cascade;
--drop table products_i_n_z cascade;
create table products_i_a_m () inherits (products_i);
alter table products_i_a_m add constraint df_a_m check (lower(left(productname, 1)) >=
'a' and lower(left(productname, 1)) <= 'm');
create table products_i_n_z () inherits (products_i); --no overlap!
alter table products_i_n_z add constraint df_n_z check (lower(left(productname, 1)) >
'm' and lower(left(productname, 1)) <= 'z');
create rule products_insert_a_m as
on insert to products_i where lower(left(productname, 1)) >= 'a' and
lower(left(productname, 1)) <= 'm'
do instead insert into products_i_a_m values (new.*);
create rule products_insert_n_z as
on insert to products_i where lower(left(productname, 1)) > 'm' and
lower(left(productname, 1))<= 'z'
do instead insert into products_i_n_z values (new.*);
delete from products_i;
--loaded data will end up in the right partition
insert into products_i (productid, productname, unitprice)
select productid, productname, unitprice from products ;
--a select will look up all the partitions
select * from products_i --77
select * from only products_i --0
select * from products_i_a_m --41
select * from products_i_n_z --36
```

6. Adatbázis migráció
   Az adatbázis-migráció az adatbázis-technológia megváltoztatását jelenti egy információs rendszerben. A
   a probléma összetettsége a változás mértékétől függ:
- Ugyanaz a fő technológia, ugyanaz a gyártó, más verzió. Példa: Postgres 8 -> 17
- Ugyanaz a fő technológia, más gyártó. Példa: Postgres 17 -> MS SQL Server 2019
- Különböző fő technológia, például relációs, grafikon, dokumentumtár, kulcsérték tároló. Példa:
   Postgres -> Firestore
   Migráció a relációs technológiák között
   A relációs->relációs migráció végrehajtható import/export függvényekkel vagy kézi szerkesztéssel
   forrásadatbázisból létrehozott dump, de több esetben csak speciális eszköz vagy egyedi
   dedikált szoftver képes megoldani a problémát. Tipikus problémák:
- Adattípusok
- Különbségek az SQL DDL/DML szintaxisában
- A hitelesítési modellek különbségei
- Bármely szerveroldali logikát, például a tárolt eljárásokat, újra meg kell valósítani
   Ebben a bemutatóban áttelepítjük az SQL Server Northwind adatbázisát a Postgres rendszerbe. Telepítsd a Postgres-t és
   pgAdmin, majd futtasd a pg_script.sql parancsfájlt a postgres adatbázisban. A forgatókönyv tartalma a következő
   következik.
7. Létrehozd a Termékek, Rendelések, Rendelés részletei, Vevők táblákat, és adatokat szúr be
8. Létrehoz egy új tárolt függvényt, amely támogatja egy új rendelés létrehozását
9. Létrehoz egy új nézetet, amely felsorolja az utolsó 5 rendelés tulajdonságait
   Megjegyzések:
   A szkriptet manuálisan szerkesztették az SSMS20 által generált dump szkript alapján.
   Példa egy alapértelmezett megszorítás két dialektusára:
- Postgres: ALTER TABLE termékek ALTER COLUMN Egységár SET DEFAULT 0
- SQL Server: ALTER TABLE termékek ADD CONSTRAINT DF_Products_UnitPrice
   ALAPÉRTELMEZETT ((0)) Az egységárhoz
   Egy másik példa a logikai típusra: az SQL Server elfogadd a 0/1 értéket, míg a Postgres nem.
   A szkript tartalmaz egy tárolt függvényt, amely egy tranzakciót valósít meg. Ennek a tranzakciónak az atomitása
   fontos üzleti szabály, amelyet be kell tartani.
   Áttérés relációs tárolóból dokumentumtárba
   Adatmodellek: relációs vs dokumentumtár
   A relációs adatmodellt a tartománymodell határozza meg, és a 3NF-ben normalizálják. A
   A relációs modell univerzális, bármilyen lekérdezés hatékonyan futtatható. A modell egy bizonyosra hangolható
   alkalmazás indexeken keresztül.
   További információ erről a problémáról: https://severalnines.com/database-blog/migrating-mssql-postgresql-what-youshould-know

A noSQL modellekkel, mint például a dokumentumtárolók és kulcsérték-tárolók, a megfelelő és hatékony adatmodell
csak a tervezett pályázat és a várható lekérdezések tekintetében határozható meg. Erre
ok, míg egy relációs modell meglehetősen simán áttelepíthető egy másik relációs technológiába,
nincs egyszerű vagy automatizált megoldás egy relációs modell noSQL-modellbe való migrálására.
A migráció különösen nehézkes a bonyolult relációs struktúrákkal rendelkező relációs modellek esetében
az táblákat. Míg a hierarchikus egy-a-többhez relációk könnyen leképezhetők a noSQL-struktúrákra, egyéni
megfontolások szükségesek a sok-sok kapcsolatok megvalósításához. A szerkezetet meg kell tervezni
manuálisan, és egy egyedi alkalmazást kell megvalósítani az adatbetöltési folyamat kezeléséhez.
A demo alkalmazás
Egy egyszerű python Flask alkalmazást fogunk használni a migrációs folyamat bemutatására. Az alkalmazás használd
a Northwind adatbázis Rendelések, Megrendelés részletei, Termékek és Vevők táblái. A funkcionalitás
a következő.

- A felhasználó a legördülő listából kiválaszthat egy terméket, megadhatja a mennyiséget, és leadhatja a rendelést
  a Northwind adatbázisba. A visszakapott oldal visszaigazolja a rendelést, és felsorolja az utolsó 5 rendelést.

- Az alkalmazás hibaüzenetet ad vissza, ha a termék készlete vagy a vásárló egyenlege van
  túl alacsony.

- A megrendelés feladása tranzakcióban történik.
  A demóalkalmazás futtatása localhoston egy Postgres háttérrendszerrel
  Hajtsd végre a következő lépéseket:
1. (a virtuális gépen már megtörtént) Az Anaconda python telepítése:
   https://www.anaconda.com/products/individual

2. (már megtörtént a virtuális gépen) Hozz létre egy virtuális környezetet a projekthez:
   a. Anaconda adminisztrátori promptban állítsd be: `https_proxy=http://proxy.uni-pannon.hu:3128`
   b. http://proxy.mik.uni-pannon.hu
   c. (különben az „SSL: WRONG_VERSION_NUMBER” üzenetet kapja)
   d. `conda create -n flask_demo pip` `// python=3.8.5`
   (a pip függőségként hozzáadva)
   python verzió: `python --version` `// 3.9.11`
   elérhető virtuális környezetek: `conda env list`)
   e. `conda activate flask_demo` (később telepítjük a szükséges csomagokat a
   flask_demo környezet)
   f. `pip install flask`
   g. `pip install psycopg2`

3. Töltsd le a `northwind.py` alkalmazást, és `cd`-zz a Flask-projekt mappájába.
   
   További információ:
   
   - https://blog.usejournal.com/why-and-how-to-make-a-requirements-txt-f329c685181e

4. Indítsd el az Anaconda Spyder python szerkesztőt, és állítsd be a jelszót …-ra, a portot pedig 5432-re

5. sor. Nézd át az alkalmazást. Vedd figyelembe, hogy a „kapcsolattal:” blokk futtatja a hívását
   new_order() függvény egy tranzakcióban.

6. A conda promptnál állítsd be a `FLASK_APP=northwind.py` változót (a `DEBUG=1` beállításával nem lesz szükség
   a webszerver manuális újraindításához minden alkalommal). Megjegyzés: a main.py-t használjuk alkalmazásnévként a
   GCP, így nincs szükség konkrét beállításra.

7. `flask run`

8. Teszteld az oldalt a http://localhost:5000/order_form címen
   Alkalmazott technológiák:
   a. A sablonok mappa a html oldalakat tartalmazza, amelyeket a jinja sablon dolgoz fel
   motor. A python változók a {% for ... in / if …else HTML-sablonokban érhetők el
   / / blokkal, kiterjeszti a %}-ot, és a sablonokat a „block”-tal lehet legjobban kiegészíteni22.
   b. Bootstrap (formázás)

9. Jobbá vagy biztonságosabbá lehetne tenni, de most nem ez áll a fókuszunkban23.
   Dokumentumtárak: A Cloud Firestore áttekintése
   Ezt az alkalmazást át fogjuk helyezni a Google Cloud Firestore szolgáltatásba. A Google Cloud Firestore egy dokumentumtár.
   Támogatja több dokumentumgyűjtemény tárolását. Ez az előző Realtime új kiadása
   Adatbázis, amely egyetlen monolitikus json24-et használt. A Cloud Firestore szolgáltatásai:
- „Firestore adatbázis=Dokumentumgyűjtemények”.

- Minden dokumentum lényegében egy json rekord pl.
   név:
   először: "Joe"
   utolsó: "hosszú"
   született: 1995

- A gyűjteménynek nincs sémája, vagyis tetszőleges szerkezetű dokumentumokat tárolhat ugyanabban a
   gyűjteményben. Ennek ellenére, bár beszúráskor nincs sémaellenőrzés, a gyűjteményt olvasó bármely
   reális alkalmazás elvár egy bizonyos sémát. Ez a `schema-on-read` (olvasáskori séma) megközelítés.
   Ez ellentétben áll a relációs adatbázisok `schema-on-write` (íráskori séma) megközelítésével, ahol a
   sémának nem megfelelő írási műveletek nem engedélyezettek.

- Minden dokumentumnak rendelkeznie kell egyedi kulccsal, amely automatikusan generálható, de nem lehet a
   számot.

- A gyűjtemények nem ágyazhatók egymásba. Egy dokumentum azonban tartalmazhat algyűjteményt is
   coll-doc-coll-doc-coll-… stb. hierarchiában, amelynek maximális mélysége 100.

- Speciális dokumentum adattípusok: 1-D tömb, térkép (asszociatív tömb), referencia típus. Egy hivatkozás
   egy dokumentumhoz vezető elérési út, pl. egy hierarchiában lévő dokumentumra mutató hivatkozás.
   A következő formátumú lehet: coll_id/doc_id/coll_id/… stb. Egy lehetséges probléma az algyűjteményekkel
   hogy a szülőgyűjtemény törlése esetén is fennmaradhatnak „árva” állapotban.

- Az egy-a-többhez kapcsolatok beágyazással valósíthatók meg, a sok-sok gyűjtemények pedig igen
   hivatkozásokkal kombinált beágyazással valósult meg.
   Flask alkalmazás: https://www.youtube.com/watch?v=MwZwr5Tvyxo
   HTML-sablonok https://www.youtube.com/watch?v=QnDWIZuWYW0
   WTF-űrlapok https://www.youtube.com/watch?v=UIJKdCIEXUQ
   Adatbázis ORM https://www.youtube.com/watch?v=cYWiDiIUxQc
   Az összehasonlításhoz lásd: https://firebase.google.com/docs/firestore/rtdb-vs-firestore#key_considerations

- A Firestore támogatja a valós idejű egyidejű frissítéseket és az atomi tranzakciókat. A lekérdezések vannak
  szűrőkkel valósítják meg.

- A Valós idejű/pillanatkép figyelő eseményt generál, amikor egy dokumentum megváltozik, és egy
  Az alkalmazás visszahívási funkcióval25 feliratkozhat az eseményre.
  További információ a bevált módszerekről: https://firebase.google.com/docs/firestore/best-practices
  Firestore dokumentumtárunk tervezése, létrehozása és betöltése
  Át kell alakítanunk az adatokat, ami egy alkalmazásspecifikus folyamat. Tervezett megkereséseink:

- Termékek és vásárlók listázása

- Új rendelés leadása egyetlen tétellel

- Az utolsó 5 rendelési tétel felsorolása a rendelés részleteivel és a vásárlói adatokkal együtt
  Ezeket a kérdéseket figyelembe véve 3 kollekciót tervezünk: egy lapos Termékek, egy lapos Ügyfél és egy hierarchikus
  Rendelések->Rendelési cikkek gyűjtése. Ne feledje, hogy ez nem felel meg a megrendelt termékek és a
  mikor, de egy ilyen lekérdezés (még) nem része az alkalmazásunknak.
  Alternatív megoldásként beágyazhatjuk a Rendelések->Rendelések gyűjteményt az Ügyfelek gyűjteményébe.
  Ez azonban megnehezítené a lekérdezést pl. a megbízások időrendi listája, lekérdezéseként
  algyűjtemények általában nem engedélyezettek a szülő dokumentumgyűjtemény iterációja nélkül.
  Egyéb megfontolások:

- Automatikus dokumentumazonosítókat fogunk használni

- A rendeléseket dátum szerint rendezzük, hogy támogassuk az utolsó 5 tétel felsorolását

- Az Ügyfélazonosító automatikusan indexelésre kerül
  
  A migrációs folyamat 2 fő lépésből áll:
1. Az új adatbázis megvalósítása és adatok átalakítása/betöltése

2. Az ügyfélalkalmazás újratelepítése az új adatbázissal való együttműködéshez
   Az új adatbázis bevezetése és adatok átalakítása/betöltése
   Programozottan létrehozzuk és betöltjük a dokumentumtárat a Postgres adatbázisból való olvasással
   localhoston fut, és a felhőben lévő dokumentumtárba ír.
   Létre kell hoznunk egy GCP-szolgáltatásfiókot, hogy elérhessük a Firebase adattárat a helyi gépünkről.

3. Nyisd meg a Firebase-konzolt: https://console.firebase.google.com/
   a. A Google-hitelesítés után hozz létre egy új projektet
   b. Ebben a projektben nincs szükségünk sem a Geminire, sem a Google-analitikára
   c. Nyisd meg a https://console.firebase.google.com/u/0/project/[Your projektazonosítót]/firestore
   és hozz létre egy adatbázist. Megpróbálhatja manuálisan hozzáadni/törölni/szerkeszteni gyűjteményeket és
   dokumentumokat itt vagy a GCP GUI-n oldalon.
   d. Hozz létre egy könyvek nevű gyűjteményt két könyvdokumentumból
   
   A GCP-projekten belül futó alkalmazásból nem feltétlenül lenne szükség szolgáltatásfiókra az adattár
   eléréséhez, de helyi fejlesztéshez és hibakereséshez sokkal egyszerűbb és gyorsabb szolgáltatásfiókot
   használni, majd az alkalmazást később szükség esetén telepíteni a GCP-re.
   
   További információ:
   
   - https://firebase.google.com/docs/firestore/query-data/listen
   - https://cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances

e. Nyisd meg a Firebase konzolt -> fogaskerék ikon -> Szolgáltatásfiókok -> Szolgáltatásfiók létrehozása
-> Új privát kulcs létrehozása. Itt létrehozhatsz egy JSON fájlt, amely tartalmazza az automatikusan létrehozott
szolgáltatásfiók kulcsát. Mentsd el ezt a fájlt biztonságos helyre, mert hozzáférést biztosít az adatbázishoz.

f. Itt egy Python-kódrészletet is találsz a kapcsolódáshoz.

4. (a virtuális gépen már megtörtént) A conda promptnál válts át a virtuális környezetre, és írd be:
   `pip install firebase_admin`

5. Ezután már csatlakozhatsz az adatbázishoz: `db = firestore.client()`
   a. Ellenőrizd, hogy a Postgres szolgáltatás működik, és a Northwind táblák elérhetők-e
   b. Ellenőrizd, hogy a proxy ki van kapcsolva a virtuális gépen
   c. Nézd át és futtasd a `main.py` szkriptet a `flask_gcp_firestore` mappában, amely betölti a 3 gyűjteményt.
      Ezúttal nincs szükség Flask webalkalmazásra, így a szkriptet a conda promptból is elindíthatod a
      `python main.py` paranccsal
   d. Ellenőrizd a gyűjtemények tartalmát a Firebase konzolon

GYAKORLAT: Nézd át és futtasd az új `northwind.py` webalkalmazást, amely a rendelésfeldolgozási
tranzakciót Firestore adatbázissal valósítja meg.

- Manuálisan töröld a `main.py` által beillesztett bemutató rendelést

- Valósítsd meg a hiányzó `list_orders()` függvényt, amely minden rendelési tételhez összegző sort ad vissza
  az utolsó 5 rendelésből. Az eredményt az `order_list.html` sablon jeleníti meg.
  A reprodukálandó funkcionalitás a következő:
  válaszd ki az o.orderdate::timestamp(0)-t időzóna nélkül rendelési dátumként,
  c.cégnév, c.ország, c.egyenleg, p.terméknév, od.mennyiség,
  od.quantity * od.unitprice mint érték, p.unitsinstock
  termékekből p csatlakozz a rendelés részletei od p.productid=od.productid
  Join orders o on o.orderid=od.orderid
  csatlakozz az ügyfelekhez c a c.customerid=o.customerid oldalon
  rendelés rendelési dátum szerint desc limit 5;

- Ugyanazokat a HTML-sablonokat használhatod.

- Teszteld a webalkalmazást itt: http://localhost:5000/
  További információ a Firestore fejlesztésről:

- Firestore programozási hivatkozás: https://firebase.google.com/docs/firestore/managedata/add-data

- https://medium.com/google-cloud/firebase-developing-an-app-engine-service-withpython-and-cloud-firestore-1640f92e14f4

- https://towardsdatascience.com/nosql-on-the-cloud-with-python-55a1383752fc

Firestore szolgáltatás létrehozása:

- https://firebase.google.com/docs/firestore/quickstart#python_1

Ha hitelesítési hibát kap, annak valószínűleg a virtuális helytelen rendszeridő-beállítása az oka
gép. A dátum és idő beállítási rendszerpaneljén állítsd át a rendszeridőt kézire, majd vissza
automatikus az idő frissítéséhez.

Az alábbi tábla az adatok integritásának érvényesítésére szolgáló eszközök összehasonlítását mutatja be:
Postgres
Firestore
A séma minden DML-műveletben érvényesül:
"írási séma"
A gyűjtemény minden dokumentuma rendelkezhet
különböző attribútumok (mezők): „séma olvasáskor”
Adattípusok és felhasználó által meghatározott adatok gazdag készlete
típusok (például felsorolástípusok)
Nagyon korlátozott adattípusok, pl. nincs pénz, ill
decimális típus
Elsődleges kulcsok és idegen kulcsok
A gyűjtemény azonosítójának egyedinek kell lennie, és lehet
automatikusan létrejön (mint egy soros típus)
de nem lehet szám. Idegen kulcsok lehetnek
attribútumként tárolják és a biztonság kényszeríti ki
szabályokat.
Egyedi kényszerek és ellenőrzési kényszerek
Biztonsági szabályok28
Az ACID tranzakciós biztonság támogatott
A tranzakciók az ügyféltől indulhatnak
megakadályozza a tesztelés és beállítás típushibáit és az atomitást
kötegelt írások őrzik29, de
a tranzakciók nem kombinálhatók kötegelt
írd (lásd később).
Tranzakciók a Firestore vs Postgres oldalon
DEMO: Teszteld a rendelési tranzakció atomitását a Postgres-en. A PgAdmin konzolon szúrjon be egy
hiba a new_order() függvényben a következő utasítás lecserélésével:
beszúrni a rendelésekbe (orderid, customerid) értékeket (var_orderid, var_custid);
ezzel a kijelentéssel
beilleszteni a rendelésekbe (orderid, customerid) értékeket (var_orderid, ‘HIBA’);
Ez megsérti az idegen kulcs megkötését, és futásidejű hibát eredményez a következő híváskor. Használata
a webalkalmazásban, adj le új rendelést, és ellenőrizd, hogy a hiba után az ügyfél egyenlege helyreállt
az eredeti értékre, még akkor is, ha azt már az insert utasítás előtt csökkentették. A
a tranzakció automatikusan vissza lett vonva.
DEMO: Logikai hibák a Firestore-on párhuzamos környezetben

- Adj hozzá 10 másodperces késleltetést a készlet és az egyenleg ellenőrzése után (importidő és
  idő.alvás(10))
- Állítsd be manuálisan mindhárom ügyfél egyenlegét `10000`-re, a `Chai` termék készletét pedig `3`-ra
  a Cloud Firestore webes konzolján.

A Firebase Admin SDK-kat használó kliensoldali alkalmazás adminisztrátori jogosultságokkal fut, és
megkerüli a Firestore adatbázishoz definiált biztonsági szabályokat. A biztonsági szabályokat csak mobil
klienssel tudnánk bemutatni, ezért ezeket nem részletezzük ebben a jegyzetben.

További információ:

- https://firebase.google.com/docs/firestore/security/get-started

- https://firebase.google.com/docs/firestore/manage-data/transactions#python_1

- Indítsd el az alkalmazást 3 böngészőablakban, és rendeldn 2 egység Chai-t minden vásárlónak (érték:
  2*18=36). Arra számítunk, hogy a korlátozottság miatt a háromból csak egy rendelés lehet sikeres
  állomány.

- Győződjön meg arról, hogy mind a 3 megrendelés feldolgozása SIKERÜLT, mind a 3 ügyfélnek 36-ot kell fizetnie, és
  Az új részvényérték 1. Láthatjuk, hogy tranzakciós ellenőrzés nélkül komoly logikai hibák is előfordulhatnak
  előfordulnak.
  Firestore-tranzakció használata

A Firestore tranzakció tartalmazhat olvasási műveleteket, amelyeket írási műveletek követnek. Ha egy tranzakció
beolvas egy dokumentumot, majd a dokumentumot egy másik kliens módosítja a véglegesítés előtt,
a tranzakció visszagördül és automatikusan újraindul (legfeljebb 5 újrapróbálkozással). A tranzakció
atomitása azonban így sem teljes körű. Példa:

```python
# hozz létre manuálisan egy test nevű új ügyfelet, és állítsd az egyenlegét 9-re
# majd futtasd ezt a szkriptet két párhuzamos munkamenetben

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

cred = credentials.Certificate("token.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
transaction = db.transaction()
cust_ref = db.collection('customers').document('test')

@firestore.transactional
def update_in_transaction(transaction, cust_ref):
    cust_ref_snapshot = cust_ref.get(transaction=transaction)
    new_balance = cust_ref_snapshot.get('balance') + 1
    print("Új egyenleg:", new_balance)
    time.sleep(10)
    if new_balance <= 10:
        transaction.update(cust_ref, {'balance': new_balance})
        print("Egyenleg növelve")
    else:
        print("Az egyenleg már maximális")

update_in_transaction(transaction, cust_ref)
```

Állítsd manuálisan a `test` ügyfél egyenlegét `9`-re, és futtasd a fenti szkriptet két párhuzamos
munkamenetben. Bár mindkét munkamenetből megkapjuk az „Egyenleg növelve” üzenetet, a végső
egyenleg `10` lesz (és nem `11`), mert az egyik tranzakció visszagördül és újra lefut. Így érvényesíthető
az az üzleti szabály, hogy az egyenleg nem haladhatja meg a `10`-et, még párhuzamos végrehajtás esetén sem.
GYAKORLAT: A fenti kódrészletet sablonként használva add hozzá a tranzakciós vezérlést az order_proc paraméterhez
funkciót a Firestore-alapú python Flask alkalmazásban, és teszteld a helyes működését a forgatókönyvben
a Konkurencia demó részben leírtak szerint. Arra számítunk, hogy több egyidejű tranzakció közül
csak az egyik fut sikeresen, és az adatbázis konzisztenciája megmarad. Ez azt jelenti
az összes tranzakció lejárta után a készlet megfelelő lesz, csak egy rendelést fogadunk el és csak
egy ügyfél egyenlege kerül felszámításra.

Kötegelt írások

A több `doc.set`, `update` vagy `delete` műveletet tartalmazó köteg atomitása a `db.batch()` objektummal
érvényesíthető. Fontos, hogy ez a megoldás nem véd a kliens által már beolvasott dokumentumokon végrehajtott
külső módosítások ellen, ezért nem tudja megakadályozni a „test-and-set” típusú logikai hibákat.
Nem lehetséges a kötegelt írások egymásba ágyazása egy tranzakción belül. Ezért el kell döntenünk, hogy megtesszük-e
biztosítják az atomitást vagy az ACID-követelmények elkülönítését.
A tranzakciók csak online működnek, azaz kapcsolatot igényelnek a szerverrel, de a kötegelt írások igen
offline is dolgozhat.
DEMO: tekintsd át és teszteld a demóalkalmazás kötegelt verzióját (`northwind_batch_write.py`) úgy,
hogy két írás közé szúrsz egy futásidejű hibát, például `print(1/0)` utasítást.
Néhány további Firestore-korlát:

- Egy tranzakció vagy írási köteg legfeljebb 500 dokumentumot írhat
- Az olvasási műveleteknek (get()) meg kell előznie az írási műveleteket (set(), update())
- „A tranzakciókra vagy kötegelt írásokra vonatkozó biztonsági szabályokban 20 dokumentum hozzáférési korlát van érvényben
  lehívd a teljes atomműveletet a normál 10 hívási limiten felül minden egyes egyedi esetében
  dokumentum művelet a kötegben.”
- stb…
  Általános következtetésként leszögezhetjük, hogy a NoSQL technológiákkal a kliens (vagy az üzleti logika
  réteg) támogatnia és megvalósítania kell az összes alacsony szintű adatfeldolgozási műveletet, mint például a gyűjtemények összekapcsolása stb.
  A tranzakciók ellenőrzése és az adatok integritásának érvényesítése szintén kevésbé robusztus a relációshoz képest
  adatbázis technológiák. Ezért a NoSQL technológiák viszonylag egyszerűre ajánlhatók
  üzleti tartományok és folyamatok. Példa erre egy blogger webhely.
  Egyéb érdekes Firestore-funkciók, amelyeket itt nem részletezünk
- valós idejű frissítések
- offline adatmegmaradás
- felhőszolgáltatásokkal való integráció

Megjegyzés: a Firestore dokumentációja szerint:
"Firestore allows you to run sophisticated ACID transactions against your document data."
https://cloud.google.com/firestore

7. Felhőalapú adatbázis-technológiák
   Áttekintés
   A felhőszolgáltatók, mint például az Amazon, a Google, az IBM, a Microsoft adatbázis-kezelést kínálnak SaaS-en vagy
   PaaS alapon. Egy ilyen megoldás életképessége a privát adatbázis-kiszolgálók helyett attól függ
   gazdasági és bizonyos mértékig műszaki megfontolások. Néhány ezek közül:
   ✓ A felhőszolgáltatások földrajzilag magas rendelkezésre állást kínálnak (jobbat, mint a vállalati szerverek).
   elosztott infrastruktúra.
   ✓ A felhőszolgáltatások automatizált igény szerinti méretezhetőséget kínálnak rugalmas, legalább részben terhelésfüggő számlázási sémákkal.
   ✓ A felhő számos más felhőn belüli szolgáltatást kínál, például adatelemzést, képfeldolgozást, NLP-t stb.
   amelyek hozzáférhetnek a felhő adatbázishoz és amelyek integrálhatók egy megoldásba.
    A felhőalapú adatbázis-szolgáltatások által kínált funkcionalitás jellemzően gyengébb, mint a privát
   kiszolgálókra, bár egyes funkciók más eszközökkel helyettesíthetők.
    Bár bizonyos költségek arányosak a használattal, vannak fix költségek is, amelyeket fizetni kell
   pl. adattárolás. Minden ilyen költséget figyelembe kell venni a tervezett üzleti tervében
   szolgáltatás vagy megoldás.
    Az adatbiztonság veszélybe kerülhet, ha nagyon érzékeny adatok (például személyes egészségügyi nyilvántartások)
   fizikailag elhagyja a vállalati hálózatot. Incidensek vagy súlyos adatvesztés is előfordulhat31.
    A kritikus szolgáltatások, például a termelési rendszer vezérlése nem függhet az internet-hozzáféréstől. Ezeket
   ez utóbbi két probléma enyhíthető egy privát felhőben32.
   Új GCP-projekt indítása
   Ebben a projektben az App motort használjuk a Flask alkalmazás, a felhőalapú SQL-adatbázis és a Firestore futtatására
   dokumentumtár.
8. Indíts el egy privát böngészőt, és engedélyezd az előugró ablakokat
9. Aktiváld az 50 dolláros kupont az egyetemi e-mail címével, és kövesd az utasításokat
   kapott a Neptun üzenetben
10. Jelentkezz be a https://console.cloud.google.com címre
11. Indíts el egy új projektet, vagy töröld a meglévőt: IAM & Admin -> Erőforrások kezelése
12. Meg kell adnia egy egyedi projektnevet, amelyre ebben a PROJEKT-ID-ként hivatkozunk
    kézikönyvet. Ellenőrizd a projekthez kapcsolt számlázási fiókot. Indításkor 50 dollár jóváírással kell rendelkeznie.
13. A Firestore oldalon: KIVÁLASZTÁS NATIVE MODE, majd ADATBÁZIS LÉTREHOZÁSA. Csak egyetlen
    A Firestore-adatbázis engedélyezett a GCP-projektekben.
    A Postgres adatbázis áttelepítése a GCP-re
14. GCP-adatbázisok->SQL->példány létrehozása -> PostgreSQL (engedélyeznie kell a számítási motort
    API)
15. Válassz példányazonosítót és jelszót. Ez az adatbázis-kiszolgáló példány neve, nem a
    az adatbázis vagy az adatbázis felhasználó neve. Készlet:
    https://www.theguardian.com/australia-news/article/2024/may/09/unisuper-google-cloud-issue-accountaccess
    pl. https://www.openstack.org/

régió: Európa, PostgreSQL 13-as verzió, egyetlen zóna (nincs feladatátvétel),
testreszabhatja példányát: nyilvános IP engedélyezve
3. kapcsolatok: „A projektben minden alkalmazás alapértelmezés szerint engedélyezett”, azonban tervezzük a hozzáférést
az adatbázist az internetről a PgAdmin segítségével, így bármilyen IP-címet engedélyezünk (=pg_hba.conf bejegyzés).
Hálózat hozzáadása: 0.0.0.0/0. Megtakarítás.
4. A Speciális beállításoknál engedélyezd a Lekérdezési statisztikákat.
5. Várja meg a példány létrehozását, majd változtassa meg a Postgres felhasználó jelszavát.
Keresd meg az SQL áttekintését a kiszolgáló nyilvános IP-címének megkereséséhez.
6. A PgAdmin alkalmazásban csatlakozz a felhőpéldányhoz a nyilvános IP-cím használatával, majd tekintsd át és futtasd a
dump fájl pg_script.sql.
7. Módosítsd az IP-címet a python alkalmazásban nyilvános GCP IP-re, és teszteld az alkalmazást. Ugyanúgy kell működnie
a helyi szerverrel. Ellenőrizd, hogy az új rendelések megjelennek-e a Postgres táblákban.
8. Visszatérve a GCP-hez, nyisd meg a Query insights alkalmazást, és ellenőrizd a lekérdezés végrehajtási tervét SELECT *
FROM last_orders. Vedd figyelembe, hogy akár 10 percig is eltarthat, amíg a lekérdezés megjelenik a Lekérdezésben
insights statisztikák, amely egy offline elemző eszköz.
A bemutató alkalmazás megvalósítása GCP33 -> Cloud programozás MSc tanfolyamon
Telepítjük az alkalmazást a GCP-alkalmazásmotorban34.

1. (a virtuális gépen már megtörtént) Telepítsd a Cloud SDK-t és a gcloud CLI-t táblai számítógépére
   https://cloud.google.com/sdk/docs/install

2. Nyiss meg egy cmd terminált Windows rendszergazdaként, cd a flask_gcp könyvtárba, és állítsd be
   HTTPS_PROXY=http://proxy.uni-pannon.hu:3128

3. a promptnál írd be: gcloud init (a személyes google profilunkhoz hitelesítés szükséges) és
   válaszd ki a SAJÁT PROJEKTazonosítót

4. Az SDK nem tartalmazza az alkalmazásmotor-bővítményt, ezért azt külön kell telepíteni. at
   a Google Cloud SDK shell prompt típusa: gcloud összetevők telepítése app-engine-python
   Ez eltart néhány percig.

5. gcloud config set project YOUR-PROJECT-ID

6. //számlázás ellenőrzése: gcloud béta számlázási fiókok listája

7. A northwind.py szkriptben módosítsd az adatbázis-kapcsolat paramétereit a nyilvános GCP IP-címre
   címet, és mentsd el main.py néven. (Frissítsd a követelmények.txt fájlt.)

8. A Cloud Build API-t használjuk az alkalmazást futtató tároló létrehozásához, ezért ennek az API-nak
   engedélyezve van a projektben: a gcloud szolgáltatások engedélyezik a cloudbuild.googleapis.com webhelyet

9. Inicializálja az alkalmazásmotort a projektben: gcloud app create --project=YOUR-PROJECT-ID

10. gcloud alkalmazás telepítése
    Megkapja a cél URL-t, amelyen elérheti az alkalmazást. Azt is elindíthatja a
    böngésző az alkalmazáshoz: gcloud alkalmazás tallózás

11. A futásidejű hibaüzeneteket a webalapú GCP-konzol App engine -> Services menüpontjában tekintheti meg
    -> Diagnózis: Naplók
    
    ```sql
    If you are already familiar with cloud programming concepts, you can skip this section and go on with the app
    running on localhost
    https://medium.com/@dmahugh_70618/deploying-a-flask-app-to-google-app-engine-faa883b5ffab
    ```

GYAKORLAT: javítsa a GCP alkalmazást az esetleges hiba okának megjelenítésével, azaz vagy alacsony
egyenleg vagy alacsony készlet, lásd alább. Ehhez a tárolt new_order() enyhe módosítására van szükség
eljárást, valamint az ügyfél HTML-sablonokat. Telepítsd a módosított alkalmazást a gcloud app deploy beírásával
MÉG TÖBB GYAKORLAT: Oszd fel a fenti táblát két táblára, amelyek az utolsó 5 rendelést és az egyenleget mutatják
az érintett ügyfelek külön-külön.
Mielőtt elmész…

1. Állítsd le az alkalmazást: Alkalmazásmotor -> Beállítások -> Alkalmazás letiltása

2. Állítsd le a Postgres szervert: SQL -> Overview -> STOP

3. Állítsd le a GCP projektet
   A BigQuery áttekintése és bemutatója
   „A BigQuery-t strukturált és félig strukturált adatok szabványos SQL használatával lekérdezésére tervezték”35
   A BigQueryt úgy tervezték, hogy csak olvasható, OLAP-szerű lekérdezéseket futtasson denormalizált (egyesített)
   adattárház-táblákon döntéstámogatáshoz és üzleti elemzéshez. A natív tárolási modell a
   tömörített (és opcionálisan particionált) oszloptároló (Dremel néven)36. Minden adatot titkosítva tárolunk
   formában. A BigQuery közvetlenül is futtathat lekérdezéseket más adatforrásokon, például Bigtable, Cloud Storage vagy
   Google drive is. A legjobb teljesítmény érdekében az ilyen külső forrásokból származó adatok legyenek az elsők
   importált a Dremel oszlopboltba.
   A logikai adatmodell egy adatkészlet, amely kapcsolódó táblákat tartalmaz rögzített sémával és beírt mezőkkel,
   hivatkozva, mint a project.dataset.table
   A Northwind adatbázis bányászata
   Ebben a demóban mi
- ```sql
   use the SQL Server version of Northwind
  ```

- ```sql
   create a denormalized view and export it to csv
  ```

- töltsd be a csv-t egy BigQuery-táblába
  
  ```
  https://panoply.io/data-warehouse-guide/bigquery-architecture/
  ```
  
  ```
  https://medium.com/google-cloud/bigquery-explained-storage-overview-70cac32251fa
  ```

- ```sql
  use the table to create a linear regression BigQueryML model
  ```

- felmérni a modell pontosságát
  Lépések:
1. Hozz létre egy nézetet, amely tartalmazza a rendelési tételek értékét a következő mezőkkel:
   value_numeric, country, categoryid, p_unitprice, discount, pyear
2. Exportáld a nézetet csv fájlba
3. Chrome böngészővel hozz létre egy új projektet: GCP főmenü -> IAM&admin -> Kezelés
   erőforrásokat
4. GCP főmenü -> Analytics -> BigQuery, API engedélyezése
5. A projekt „…” menüjéből -> Adatkészlet létrehozása, válaszd az „USA” elnevezésű Multi-régiót
   (az Egyesült Államok több régiója)”. Meg kell adnia egy azonosítót. Nevezze el az adatkészletet „északszél”. A
   Az adatkészlet titkosított formában kerül tárolásra. Ugrás az adatkészlethez.
6. Válaszd ki a + tábla létrehozása elemet, és add meg a Tábla létrehozása feltöltésből -> séma automatikus észlelése lehetőséget. Betöltés
   a denormalizált táblát, és ellenőrizd az adattípusokat. Nevezze el a táblát „nw”-nek. A pénz típusa lehet a
   probléma. Menj az táblahoz.
7. Nézd át a sémát és az előnézeti adatokat
8. Az elemzés előtt érdemes ellenőrizni a forrásadatok érvényességét és tartalmát.
   Az Analytics -> Dataplex egy GCP-szolgáltatás, amely támogatja ezt.
   a. A Dataplexből vagy közvetlenül a BigQuery Studióból (utolsó lap a Séma lap mellett),
   hozz létre és indíts el egy igény szerinti profilfeladatot a Gyors adatprofil -> Részletek lehetőségre kattintva.
   Ez a feladat a háttérben fut kb. 5 percig, majd jelenítse meg az oszlopot
   statisztikák és hisztogramok.
   b. Indíts el egy adatminőségi vizsgálatot egy manuálisan hozzáadott minőségi szabállyal (pl. Fuvar >=0).
   A „de facto” szabályokat is áttekintheti és elfogadhatja az eredmény alapján
   profilfeladat, pl. a benyújtott fuvarra kikövetkeztetett szabály: „min: 0,02, max: 1007,64”. A
   A vizsgálattal kapcsolatos adminisztratív információk a Northwind adatkészletben tárolhatók. A
   Az eredmények a Dataplex -> Adatminőség menüpontban a szkennelés nevére kattintva érhetők el
   oldalt, és válaszd ki a Munkaelőzmények lapot.
9. A BigQuery alkalmazásban az SQL-lekérdezések a konzolon futtathatók. Új lekérdezés létrehozása -> SQL konzol
   ablakot
10. Hozz létre egy modellt, amely előrejelzi a value_numeric mezőt az ország, kategóriaazonosító,
    p_unitprice, discount, pyear mezőket a következő SQL utasítás használatával (ha a
    „Northwind” adatkészlet és az „nw” tábla):

MODELL LÉTREHOZÁSA `northwind.nw_model` OPCIÓK (model_type='linear_reg', input_label_cols=['valu
e_numeric']) AS
SELECT érték_szám, ország, kategóriaazonosító, p_egységár, kedvezmény, pév -- ha
a
válaszd ki
listát
nem
nem
tartalmaznak
a
osztályban
címke,
te
kap
a
hiba
üzenetet
„Nem sikerült azonosítani a címkeoszlopot”
`Northwind.nw`-től
A WHERE érték_száma nem null
11. Építsd meg a northwind.nw_model-t (kb. 30 másodpercet vesz igénybe)37, majd menj a modellhez. Ellenőrizd a Részletek és
az Értékelés. Láthatja, hogy az adatkészlet automatikusan fel lett osztva egy képzési táblahoz
(1702 rekord) és egy értékelő tábla (453 rekord). Az átlagos abszolút hiba 301.
12. A modellt ki tudjuk értékelni a teljes adatkészlet felhasználásával (bár nem ajánlott legjobb
gyakorlat az adattudományban, és ezt csak az EVALUATE módszer bemutatására tesszük). Te
használhatod a következő parancsot.
KIVÁLASZTÁS

* FROM ML.EVALUATE(MODEL `northwind.nw_model`, (
  SELECT value_numeric, country, categoryid, p_unitprice, discount, pyear
  `Northwind.nw`-től
  ))
13. Az eredmények azt mutatják, hogy az előrejelzés átlagos hibája 342, a magyarázott szórás 53%.
    tehát gyenge a modell teljesítménye: a függő változó közötti kapcsolat
    a független változók pedig gyenge. Ha újra létrehozzuk a modellt a
    CALCULATE_P_VALUES = igaz, CATEGORY_ENCODING_METHOD='DUMMY_ENCODING'
    opciók esetén azt is meg kell néznünk, hogy az egyes változók hozzájárulása a modellhez
    jelentős38. Azokat a rekordokat is lekérdezhetjük, ahol a hiba 40%-nál kisebb volt a
    következő parancsot. Hasonlóképpen azt taptáblajuk, hogy a legroszdbb előrejelzés 517,9 volt 17,0 helyett.
    SELECT * FROM ML.PREDICT(MODEL `northwind.nw_model`, (
    SELECT value_numeric, country, categoryid, p_unitprice, discount, pyear
    `Northwind.nw`-től
    )) ahol abs((prediktált_érték_numerikus-érték_numerikus))/érték_numerikus <0,4
    GYAKORLAT: Módosítsd a nézetet úgy, hogy tartalmazzon egy value_nominal mezőt, amely három kategóriával rendelkezik az alacsony, közepes és magas árú cikkekhez. Próbáld megjósolni a value_nominal mezőt a
    "BOOSTED_TREE_CLASSIFIER" vagy a "LOGISTIC_REG" metódus. Hány esetben/hány százalékban
    helyesen tudod megjósolni az osztálycímkét?
    Egy kis segítség:
    válaszd ki az od.unitprice*od.quantity*(1-od.discount) értéket,
    eset, amikor (od.egységár*od.mennyiség*(1-od.kedvezmény)) < 200, akkor 'L'
    amikor (od.egységár*od.mennyiség*(1-od.kedvezmény)) < 1200, akkor 'M'
    amikor (od.egységár*od.mennyiség*(1-od.kedvezmény)) >= 1200, akkor 'H'
    else 'N/A' end value_nominal,
    c.Ügyfélazonosító, c.Cégnév, c.Ország, c.Egyenleg, o.Rendelésazonosító, o.Rendelés dátuma, o.Kötelező dátum,
    év (o.orderdate) pév,
    o.ShippedDate, o.ShipVia, o.Freight, o.ShipName, o.ShipAddress, o.ShipCity, o.ShipRegion,
    o.ShipPostalCode, o.ShipCountry, od.UnitPrice, od.Quantity, od.Discount,
    p.ProductName, p.SupplierID, p.CategoryID,
    p.QuantityPerUnit, p.UnitPrice p_unitprice, p.UnitsInStock, p.UnitsOnOrder, p.ReorderLevel,
    p.Megszűnt
    from Customers AS c join Orders AS o ON c.CustomerID = o.CustomerID csatlakozás
    [Rendelés részletei] AS od ON o.OrderID = od.OrderID csatlakozás
    
    ```
    https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create
    However, this feature does not seem to work
    ```

Termékek AS p ON od.ProductID = p.ProductID
GYAKORLAT: A nyilvános bigquery-public-data.samples.natality39 teszttábla segítségével megjósolhatja egy
baba lineáris regresszió segítségével. Ez a tábla sok rekordot tartalmaz, így mintát vehet a rekordkészletből
a WHERE RAND() < 0,0001 záradék.
Egy kis segítség:

- Ha az adatkészletet nem az Egyesült Államokban hozták létre, hozz létre egy új adatkészletet a többrégióban „USA
  (több régió az Egyesült Államokban)” us_dataset néven, majd futtasd az alábbi lekérdezést. Ezt
  így nem kell manuálisan beállítania a lekérdezés régióját (a TOVÁBBI -> Lekérdezés beállításai ->
  Speciális beállítások)
  MODELL LÉTREHOZÁSA `us_dataset.natality_model`
  OPCIÓK
  (model_type='linear_reg',
  input_label_cols=['weight_pounds']) AS
  KIVÁLASZTÁS
  weight_pounds,
  is_male,
  terhességi hét,
  anya_kor,
  CAST(anya_faj AS string) AS anyafaj
  FROM
  `bigquery-public-data.samples.natality`
  HOL
  weight_pounds NEM NULL ÉS RAND() < 0,0001
  KIVÁLASZTÁS
* FROM
  ML.TRAINING_INFO(MODEL `dataset_nev.natality_model`)
  
  ```sql
  SELECT * FROM ML.PREDICT(MODEL `dataset_nev.natality_model`,
  (select true as is_male, 40 as gestation_weeks, 30 as mother_age,'38' as mother_race))
  ```
  
  További olvasnivalók
- Kari képzés https://edu.google.com/programs/faculty/training

- Tanulási utak https://cloud.google.com/training

- •
  Rövid útmutatók , rövid útmutatók a Cloud Platform termékekkel, szolgáltatásokkal,
  és API-k https://cloud.google.com/gcp/getting-started
  Mintaprojektek https://go.google-mkto.com/CPI00b01C3FT0A2j1tciC0V

- GCP-dokumentumok https://cloud.google.com/docs
  
  ```
  https://cloud.google.com/bigquery-ml/docs/bigqueryml-natality
  ```
8. Speciális adattípusok
   Grafikonmodellezés
   A hagyományos adatbázis-modellezésben UML osztálymodell vagy entitáskapcsolati modell lehet
   használatával relációs modellré alakítjuk át
- egy az egyhez kapcsolatok az egy az egyhez asszociációkhoz és az örökléshez (szülő/gyermek
   specializáció)

- egy-a-többhöz kapcsolatok egy-a-többhöz asszociációkhoz, összesítéshez és összetételhez

- sok-sok kapcsolatok a sok-sok egyesületek számára
   Ezután az egy az egyhez és az egy a sokhoz kapcsolatokat a relációs modellben úgy lehet megvalósítani
   idegen kulcsokat, míg a sok a sokhoz kapcsolatokat táblák összekapcsolásával valósítják meg.
   Van azonban egy természetesebb és kevésbé korlátozott módja az összes UML/ERM modellezésének és megvalósításának
   jellemzők: a gráfkoncepció, amely csak a csomóponttípusokat és éltípusokat használd a hozzájuk tartozó attribútumokkal
   séma, valamint csomópont- és élpéldányok az adatbázisban. Valójában a gráf technológia egy újjáéledése
   régi adatbázis-struktúra, az úgynevezett hálózati adatbázis-modell.
   Grafikon táblák SQL Serveren
   Az MS SQL Server 2022-ben a gráf- és éltípusú táblák sok-sok kapcsolatokat képesek kifejezni.
   természetes módon, mint a relációs modell hagyományos összekapcsoló táblái. A grafikontáblák használhatók
   komplex hálózatokat modellezni különféle típusú csomópontokkal40.

- A „gráf” gráf- és éltáblák gyűjteménye. Adatbázisonként csak egy gráfunk lehet.

- A csomóponttáblák tartalmazzák azokat az entitásokat, amelyeket csatlakoztatni szeretnénk. A rejtett $node_id automatikusan megjelenik
   minden rekordhoz generált.

- Az éltáblák a csomópontokat összekötő éleket tartalmazzák. Jó gyakorlat az élek szétválasztása
   bizonyos típusú csomópontok összekapcsolása más típusú csomópontok összekapcsolásával, behelyezésükkel
   külön szélű táblák. Az élek az engedélyezett célcsomóponthoz képest is korlátozhatók
   típusúak, így rendelkezhetünk a hálózat bizonyos „gráfsémájával”41. Egy élnek lehetnek attribútumai.
   Minden rekordhoz automatikusan létrejön egy rejtett $él_id. Egy él mindig innen irányul
   $from_id - $to_id.

- Az SQL-lekérdezések megadhatnak kapcsolati mintákat a csomópontok vagy részgráfok lekéréséhez
   kapcsolati funkciók a MATCH kulcsszó használatával. A minta egy részgráfot ad vissza. A
   két részgráf metszéspontja az ÉS gombbal választható ki a minta specifikációban.

- Bár a grafikontábláknak nincs elsődleges kulcsa, egy egyedi, nem fürtözött index van
   automatikusan létrejön a nullálható $node_id, $edge_id a keresések felgyorsítása érdekében42.

- A MATCH minták tartalmazhatnak egy SHORTEST_PATH konstrukciót, amely a legrövidebb utat add vissza
   csomópontok között43.
   Az alábbi példa egy egyszerű gráfot használ három csomóponttípussal44:
  
  ```
  https://learn.microsoft.com/en-us/sql/relational-databases/graphs/sql-graph-architecture?view=sql-serverver16
  http://www.nikoport.com/2018/10/28/sql-graph-part-ii-the-edge-constraints/
  https://sqlserverfast.com/blog/hugo/2023/07/sql-graph-indexing-i-stand-corrected/
  https://www.red-gate.com/simple-talk/sql/t-sql-programming/sql-graph-objects-sql-server-2017-good-bad/
  https://docs.microsoft.com/en-us/sql/relational-databases/graphs/sql-graph-sample?view=sql-server-ver15
  ```

```sql
--source: https://docs.microsoft.com/en-us/sql/relational-databases/graphs/sql-graphsample?view=sql-server-ver15
go
--use graphdemo
go
--drop table likes
--drop table friendof
--drop table livesin
--drop table locatedin
--drop table person
--drop table restaurant
--drop table city
-- create node tables
create table person (
id integer primary key,
name varchar(100)
) as node
create table restaurant (
id integer not null,
name varchar(100),
-- city varchar(100)
) as node
create table city (
id integer primary key,
name varchar(100),
statename varchar(100)
) as node
-- create edge tables.
create table likes (rating integer) as edge
create table friendof as edge
--a `friendof` él típust csak személyek közötti kapcsolatra korlátozzuk:
alter table friendof add constraint ec_1 connection (person to person)
create table livesin as edge
create table locatedin as edge
```

```sql
-- insert data into node tables. inserting into a node table is same as inserting into
a regular table
insert into person values (1,'john')
insert into person values (2,'mary')
insert into person values (3,'alice')
insert into person values (4,'jacob')
insert into person values (5,'julie')
insert into person values (6,'tom')
insert into restaurant values (1,'taco dell')
insert into restaurant values (2,'ginger and spice')
insert into restaurant values (3,'noodle land')
insert into city values (1,'bellevue','wa')
insert into city values (2,'seattle','wa')
insert into city values (3,'redmond','wa')
--select $node_id, * from city
-- insert into edge table. while inserting into an edge table,
-- you need to provide the $node_id from $from_id and $to_id columns.
insert into likes values ((select $node_id from person where id = 1),
(select $node_id from restaurant where id = 1),9)
insert into likes values ((select $node_id from person where id = 2),
(select $node_id from restaurant where id = 2),9)
insert into likes values ((select $node_id from person where id = 3),
(select $node_id from restaurant where id = 3),9)
insert into likes values ((select $node_id from person where id = 4),
(select $node_id from restaurant where id = 3),9)
insert into likes values ((select $node_id from person where id = 5),
(select $node_id from restaurant where id = 3),9)
--select * from likes
insert into livesin values ((select $node_id from person where id = 1),
(select $node_id from city where id = 1))
insert into livesin values ((select $node_id from person where id = 2),
(select $node_id from city where id = 2))
insert into livesin values ((select $node_id from person where id = 3),
(select $node_id from city where id = 3))
insert into livesin values ((select $node_id from person where id = 4),
(select $node_id from city where id = 3))
insert into livesin values ((select $node_id from person where id = 5),
(select $node_id from city where id = 1))
insert into locatedin values ((select $node_id from restaurant where id = 1),
(select $node_id from city where id =1))
insert into locatedin values ((select $node_id from restaurant where id = 2),
(select $node_id from city where id =2))
insert into locatedin values ((select $node_id from restaurant where id = 3),
(select $node_id from city where id =3))
--delete friendof
-- insert data into the friendof edge.
insert into friendof values ((select $node_id from person where id = 1), (select
$node_id from person where id = 2))
insert into friendof values ((select $node_id from person where id = 1), (select
$node_id from person where id = 5))
insert into friendof values ((select $node_id from person where id = 2), (select
$node_id from person where id = 3))
--friendof is a DIRECTED edge though friendship is undirected (mutual) --> no way to
express undirected relationships except using two edges
```

```sql
insert into friendof values ((select $node_id from person where id = 3), (select
$node_id from person where id = 2))
insert into friendof values ((select $node_id from person where id = 3), (select
$node_id from person where id = 5))
--repeated edge:
insert into friendof values ((select $node_id from person where id = 3), (select
$node_id from person where id = 6))
insert into friendof values ((select $node_id from person where id = 3), (select
$node_id from person where id = 6))
insert into friendof values ((select $node_id from person where id = 4), (select
$node_id from person where id = 2))
insert into friendof values ((select $node_id from person where id = 5), (select
$node_id from person where id = 4))
--repeated edges:
select * from friendof where json_value($from_id, '$.id') = 2 and json_value($to_id,
'$.id') = 5
--a belső csomópontazonosító-indexelés 0-tól indul, ezért a 3->6 él helyett ezt adjuk meg
2->5
--töröljük a duplikált élt:
delete friendof where json_value($edge_id, '$.id') = 8
```

```sql
We can visualize friendships with Gephi, a free tool.
--------------------------------QUERIES--------------------------- friends of john
select p2.name
from person p1, person p2, friendof
where match(p1-(friendof)->p2)
and p1.name='john'
-- find restaurants that john likes
select restaurant.name
from person, likes, restaurant
where match (person-(likes)->restaurant)
and person.name = 'john'
-- find restaurants that john's friends like
select restaurant.name
from person person1, person person2, likes, friendof, restaurant
where match(person1-(friendof)->person2-(likes)->restaurant)
and person1.name='john'
--find people who like a restaurant in the same city they live in
select person.id, person.name
from person, likes, restaurant, livesin, city, locatedin
where match (person-(likes)->restaurant-(locatedin)->city and person-(livesin)->city)
--find people who have at least one friend who likes a restaurant in the same city
they live in
select distinct p1.id, p1.name
from person p1, person p2, friendof, likes, restaurant, livesin, city, locatedin
where match (p1-(friendof)->p2 and p2-(likes)->restaurant-(locatedin)->city and p2(livesin)->city)
-- find 2 people who are both friends with same person
--friendof is a DIRECTED edge though the relationship is undirected (mutual) --no way
to express undirected relationships except using two edges
select p0.name person, p1.name Friend1, p2.name Friend2
```

```sql
from person p1, friendof f1, person p2, friendof f2, person p0
--where match(p1-(f1)->p0<-(f2)-p2) and p1.id <> p2.id
where match(p1-(f1)->p0 and p2-(f2)->p0) and p1.id <> p2.id --equivalent
--SHORTEST_PATH----------------------------------------------barátok: John összes legrövidebb útja
select p1.name, p1.name+'->'+string_agg(p2.name, '->') within group (graph path)
paths,
last_value(p2.Name) within group (graph path) last_name
,count(p2.name) within group (graph path) depth
from person p1, person for path as p2,
friendof for path as friend
--where match(shortest_path(p1(-(friend)->p2) {1,2})) and p1.name='john' --nem tartalmazza
contain the length 3 john->mary->alice->tom path
where match(shortest_path(p1(-(friend)->p2) +)) and p1.name='john' --contains all
--friends: the shortest path between John and Jacob
select name, paths, depth
from (
select p1.name, p1.name+ '->'+string_agg(p2.name, '->') within group (graph
path) paths,
last_value(p2.Name) within group (graph path) last_name
, count(p2.name) within group (graph path) depth
from person p1, person for path as p2,
friendof for path as friend
where match(shortest_path(p1(-(friend)->p2)+)) and p1.name='john' --and
p2.name='jacob' --ERROR: cannot select columns from FOR PATH tables
) a where last_name = 'jacob'
```

Vedd figyelembe, hogy ugyanaz a tartomány modellezhető „hagyományos relációs” módon, mindössze 5 táblával, mint
logikusan feltételezve, hogy egy személy egyetlen városban él:

```sql
--drop table r_friendof
--drop table r_person
--drop table r_restaurant
--drop table r_city
go
create table r_city (id int primary key, name varchar(100), statename varchar(100))
create table r_person (id int primary key, name varchar(100), city_id int references
r_city)
create table r_restaurant (id int primary key, name varchar(100), city_id int
references r_city)
go
create table r_likes (
person_id int not null references r_person,
restaurant_id int not null references r_restaurant,
rating int,
constraint p_1 primary key (person_id, restaurant_id))
create table r_friendof (
person1_id int not null references r_person,
person2_id int not null references r_person,
constraint p_21 primary key (person1_id, person2_id))
go
insert r_city values (1,'bellevue','wa'),(2,'seattle','wa'),(3,'redmond','wa')
insert r_person values (1,'john', 1), (5,'julie', 1), (4,'jacob', 3), (3,'alice', 3),
(2,'mary', 2)
insert r_restaurant values (1,'taco dell', 1), (2,'ginger and spice', 2), (3,'noodle
land', 3)
insert r_likes values (1,1,9),(2,2,9),(3,3,9),(4,3,9),(5,3,9)
```

```sql
insert r_friendof values (1,2),(1,5),(2,3),(3,5),(4,2),(5,4)
go
use db_vi
-- friends of john
select p2.Name
from r_person p1 join r_friendof f on p1.id=f.person1_id join r_person p2 on
p2.id=f.person2_id
where p1.Name ='john'
-- find restaurants that john likes
select r.name
from r_restaurant r join r_likes l on r.id=l.restaurant_id join person p on
p.id=l.person_id
where p.Name ='john'
-- find restaurants that john's friends like
select r.name
from r_person p1 join r_friendof f on p1.id=f.person1_id join r_person p2 on
p2.id=f.person2_id
join r_likes l on l.person_id=p2.id join r_restaurant r on r.id=l.restaurant_id
where p1.Name ='john'
--keresd meg azokat, akik olyan éttermet szeretnek, amely ugyanabban a városban van, ahol élnek
select p.name
from r_restaurant r join r_likes l on r.id=l.restaurant_id join r_person p on
p.id=l.person_id
where r.id=p.city_id
--keresd meg azokat, akiknek legalább egy olyan barátjuk van, aki olyan éttermet szeret, amely ugyanabban a városban van
(s)he lives in
select p1.name
from r_person p1 join r_friendof f on p1.id=f.person1_id join r_person p2 on
p2.id=f.person2_id
join r_likes l on l.person_id=p2.id join r_restaurant r on r.id=l.restaurant_id
where r.id=p2.city_id
```

GYAKORLAT: Végezd el a Northwind adatbázis Rendelések, Rendelési adatok és Termékek tábláit a
grafikonon, és írj egy T-SQL szkriptet, amely átmásold a tartalmat az új gráftáblákba. Kérdezd meg a bevételt
év és terméknév szerint.
Hasonlítsa össze a relációs verziót ugyanazon lekérdezés gráf alapú verziójával.
Teljesítmény
A Jánostól Jacobig tartó legrövidebb út tényleges végrehajtási terve a lekérdezés széleskörű használatát mutatja
ideiglenes táblák és egymásba ágyazott hurokműveletek, valamint azt is, hogy az összes személy elérési útjának meg kellett lennie
kiszámolták, mielőtt a Jacobnál végződőt kiválasztanák – messze nem ideális megoldás.

GYAKORLAT: Írj egy rövid T-SQL szkriptet, amely egy véletlenszerű gráf adatbázist generál egyetlen csomóponttípussal
(pl. személy) és egy éltípus (pl. friend_of). A csomópontok száma (N) és az átlagos szám
Az élek számát csomópontonként (E) paraméterezni kell. Mérje meg az átmérő megtalálásának végrehajtási idejét
a gráf (azaz az összes legrövidebb út maximuma) függvényében a két paraméter függvényében. Kezdje azzal
N=100, E=3, és növeljük az N-t, amíg a végrehajtási idő meg nem haladd a 30 másodpercet. Mit vársz és mit csinálsz
méred?
Tippek

- ```sql
  A WHILE <logikai kifejezés> BEGIN … END szerkezetet ciklus megvalósítására használd. Találsz
  lecture notes about T-SQL on the Moodle pages.
  ```

- A sorszámláló üzeneteket kikapcsolhatja és a tényleges végrehajtási időt mérheti a
  beállítások alatt. A CPU-idő többprocesszoros rendszereken meghaladhatja az Eltelt időt. Meg kéne
  tiltsd le a statisztikai idő/io beállítást az adatbázis generálása közben.

```sql
set nocount on
set statistics time on
set statistics io on
```

További olvasnivaló:

- ```
  https://www.red-gate.com/simple-talk/databases/sql-server/t-sql-programming-sqlserver/sql-server-2019-graph-database-and-shortest_path/
  ```

- ```
  https://learn.microsoft.com/en-us/sql/relational-databases/graphs/sql-graphoverview?view=sql-server-ver16
  ```

- ```
  https://learn.microsoft.com/en-us/sql/relational-databases/tables/graph-edgeconstraints?view=sql-server-ver16
  ```

- ```
  https://learn.microsoft.com/en-us/sql/relational-databases/graphs/sql-graph-shortestpath?source=recommendations&view=sql-server-ver16
  ```

- ```
  https://learn.microsoft.com/en-us/sql/t-sql/queries/match-sql-graph?view=sql-server-ver16
  ```

GraphQL interfészek
Az ötlet az, hogy a hagyományos SQL-lekérdezésekben az összekapcsolásokat az intuitívabb gráf alapú szintaxisra cseréljük.
Funkcionalitás:

- Csatlakozás adatbázis-háttérrendszerhez

- A graphQL lekérdezések elemzése és a séma megfelelőségének ellenőrzése

- A lekérdezés végrehajtása a háttérben, és az eredmények visszaadása graphQL formátumban
  További információ:

- A graphQL szerver specifikációja: https://spec.graphql.org/October2021/

- ```
  https://www.howtographql.com/graphql-python/0-introduction/
  ```

- ```
  https://blog.bitsrc.io/so-what-the-heck-is-graphql-49c27cb83754
  ```

- ```
  https://hasura.io/learn/
  ```

- ```
  https://cloud.hasura.io/projects
  ```

Illesztőprogram={ODBC-illesztőprogram SQL-kiszolgálóhoz};Szerver=…szerver IP-címe, portszám;Adatbázis=…;Uid=…
Egy natív gráf adatbázis: neo4j
Technikai problémák
Konfiguráció, több memória hozzáadása:

- Biztonságosan állítsd le a virtuális gépet

- Növelje a memóriát 8 GB-ra

- Indítsd el a gépet
  Konfiguráció, engedélyek hozzáadása:

- 1. lépés: Lépjen a c:\Program Files\Neo4j Desktop elemre.

- 2. lépés: Kattints jobb gombbal a Neo4j Desktop elemre, válaszd ki a tulajdonságokat

- 3. lépés: Válaszd a „Biztonság” lapot. Ezen válaszd ki a FELHASZNÁLÓT

- 4. lépés: Kattints a Szerkesztés gombra, és válaszd a FELHASZNÁLÓK lehetőséget

- 5. lépés: Az Engedélyben jelöld be a Teljes vezérlés engedélyezése négyzetet

- 6. lépés: Kattints az Alkalmaz gombra az alján.
     Bevezetés
     A Neo4j a legnépszerűbb, nyílt forráskódú, Java alapú gráf adatbázis technológia, amely mindkét táblai számítógépet kínálja
     és felhő alapú adatbázis-kiszolgálók45. Az adatbázisfájlok minden példányhoz külön mappákban tárolódnak
     a C:\Users\db\.Neo4jDesktop\relate-data\dbmss mappában. Az adatbázis mappán belül a
     a megmaradt adatfájlok a data\databases\neo4j mappában találhatók. Az adatokat linkelt listákban tároljuk
     a következő adatfájlok46:

- Neostore.nodestore.* fájlok: a csomópontok. A csomópontok azonosításához egyedinek kell lennie
   ingatlan, pl. 'név'.
  
  ```
  https://neo4j.com/docs/getting-started/
  https://neo4j.com/developer/kb/understanding-data-on-disk/
  ```

- Neostore.label.* fájlok: A csomópontokhoz címkéket lehet csatolni, hogy csoportosíthassuk őket, pl. minden csomópont
  a megbízást reprezentáló Megrendelések címkével lehetne ellátni. Ez hasonlít egy csomóponttípusra, de egy csomópont igen
  több címkével rendelkezik.

- Neostore. kapcsolat.* fájlok: Ezek a fájlok tárolják az éleket (más néven kapcsolatokat).

- Minden kapcsolatnak irányítottnak kell lennie, amikor létrehozzuk őket, de egy él irányába
  lekérdezéskor figyelmen kívül hagyható.

- A kapcsolatok indexelhetők.

- A kapcsolatoknak egyetlen típusa van (=a kapcsolat egyetlen címkéje)
  Neostore. property.* fájlok: a csomópontokhoz és élekhez kapcsolódó tulajdonságok (attribútumok).
  A tulajdonságok kulcs-érték párok. Egy élnek vagy csomópontnak több tulajdonsága is lehet.
  Az attribútum típusazonosítója minden attribútumhoz az attribútum tényleges adatai előtt kerül tárolásra
  adatblokk. Az adatblokk 8 bájtot foglal el, az attribútumrekord pedig 4 blokkot. A bennszülött
  adattípusok: bool, float, integer, point, string, date/time és ezek listája (tömbje). A PATH adatok
  A típus csomópontok és kapcsolatok váltakozó sorozata. Bármely típus felveheti a NULL értéket.
  A gráfnak van egy „opcionális” sémája, azaz minden csomópont vagy él eltérő tulajdonságokkal rendelkezhet
  Megszorítások hozzáadhatók egy tartománymodell kényszerítéséhez.
  A Cypher lekérdezési nyelv
  Az adatbázis kezelése a Cypher47 lekérdezési nyelven történik. Az alábbi minták demo adatbázist használnak
  című filmek.
  A Cypher mintákra épül.
  Egy példa csomópontmintára: (:Movie {title: 'Forrest Gump', kiadás: 1994})
  Példa kapcsolati mintára: -[:ACTED_IN {roles: ['Forrest']}]]->
  Néhány szabály:
  
  - Egy álnév (referenciaváltozó) megadható a kettőspont előtt a csomópontban vagy a csomópontban
    kapcsolati specifikációk, pl. „p:Személy”.
  - Az irányítatlan kapcsolatokat használó lekérdezésekben a nyílnak nincs feje.
  - A kapcsolattípusok és tulajdonságértékek megkülönböztetik a kis- és nagybetűket, bár maga a Cypher nyelv
    nem.
  - A minták lekérdezésekben kombinálhatók.
    Néhány példa:

```
https://neo4j.com/docs/cypher-manual/current/introduction/
```

- MATCH (filmek:Movie) RETURN films.title
  címke
- MATCH (színész:személy)-[:ACTED_IN]-(film:film)
  WHERE actor.name='Tom Hanks'
  VISSZA színész.név, film.cím;
  //azon filmek listája, amelyekben T.H. cselekedett
- MATCH (színész:személy)-[:ACTED_IN]-(film:film),
  (rendező:Személy)-[:IRÁNYÍTOTT]-(film:Film)
  WHERE actor.name='Tom Hanks'
  VISSZA színész.név, film.cím, rendező.név; //mint fent, a rendezővel
  //minden csomópont, amelyik rendelkezik a filmmel
  A RETURN egy fő állítás. Tipikus főbb állítások:
- RETURN: keresd meg és add vissza a megfelelő részgráfot
- TÖRLÉS: csomópontok, kapcsolatok vagy elérési utak törlése
- REMOVE: tulajdonságok eltávolítása csomópontokról és kapcsolatokról, címkék eltávolítása a csomópontokról
- SET: frissítsd a csomópontok címkéit, valamint a csomópontok és kapcsolatok tulajdonságait
- LÉTREHOZÁS: csomópontok és kapcsolatok hozzáadása
- MERGE: próbáljon megfeleltetni egy mintát (amely tartalmazhat tulajdonságértékeket is), ha nincs pontos egyezés
  megtalálta, hozd létre a mintát. Kombinálható RETURN-el
  MERGE és CREATE példák:
- •
- •

```sql
create (m:Movie {name: 'old movie'}) return *;
//returns the new node
merge (m:Movie {name: 'old movie'}) return *; //no new node created because
an exact match was found
create (m:Movie {name: 'old movie'}) return *;
//we have now 2 ‘old
movie’ nodes
match (m:Movie {name: 'old movie'}) delete m; //we deleted both of them
```

```
In the following example, we create a new Person and relate it to an existing movie via a new
relationship, ‘WROTE’:
merge (p:Person {name: 'Henry Hukk'}) return p;
match (p:Person {name: 'Henry Hukk'}), (m:Movie {title: 'Top Gun'})
merge (p)-[:WROTE]->(m) return p,m;
```

A CREATE példa:
LÉTREHOZÁS
(:Személy:Színész {név: 'Tom Hanks', született: 1956})
//ez egy csomópont 2-vel
címkéket
-[:ACTED_IN {roles: ['Forrest']}]->
//a szerepek egy tömbben vannak
(:Film {cím: 'Forrest Gump', megjelenés: 1994})
<-[:IRÁNYÍTOTT]//figyeld meg a nyíl irányát
(:Személy {név: 'Robert Zemeckis', született: 1951})
Így állíthatunk be vagy hozhatunk létre új tulajdonságot egy csomóponton:
egyezés (p:Person {name: 'Paul Blythe'})
set p.birthdate = dátum({év: 2018}) //felülírd, ha létezik
visszatérés p

Példa ingatlanértéken alapuló szűrőre (keresdn hasonló véleményeket):
egyezés (p1:Személy)-[r1:VIZSGÁLT]->(m1:Film), (p2:Személy)-[r2:ÁTTEKINTÉS]->(m2:Film)
ahol r1.rating=r2.rating
return p1.name, r1.rating, m1.title, p2.name, r2.rating, m2.title;
GYAKORLAT:

1. Nyisd meg a Neo4j Desktop alkalmazást, és indítsd el a példaprojekthez kapcsolódó adatbázispéldányt. Kattints rá
   Film DBMS -> Start. Egy idő után egy piros Stop gomb jelzi, hogy a példány elindult:
2. Importáld a minta Filmek adatbázist az adatbázis kiírásából. Ehhez használd a Megnyitás gombot
   amely akkor jelenik meg, ha az egérmutatót a load-movies.cypher címke fölé viszi. Ez megnyitja a dump szkriptet
   a Neo4j böngészőben. Futtasd a szkriptet a kék háromszögre kattintva. -> „179 címke hozzáadva, létrehozva
   179 csomópont, 580 tulajdonság beállítása, 258 kapcsolat létrehozása”
3. A neo4j$ promptba írd be a CALL db.schema.visualization() parancsot a csomópont megtekintéséhez és
   kapcsolattípusok
4. Próbáld meg futtatni a fenti lekérdezéseket, és ellenőrizd az eredményeket. Ha VISSZA a teljes csomópontokat ahelyett
   csak a csomópontok tulajdonságait, az eredményeket Graph nézetben is megjelenítheti. Például
   A „VISSZASZÍNÉSZ, film, rendező” használata a harmadik lekérdezésben a következőt eredményezi:

GYAKORLAT: Írd meg és teszteld ezeket a lekérdezéseket

- Kérdezd meg azokat a személyeket, akik olyan filmet rendeztek, amelyben szerepeltek
- Keresd meg a fenti személyek összes követőjét
- Keresd meg azt a személyt, aki a legtöbb 50 feletti értékelésű filmben szerepelt
- Adjunk hozzá egy új hipotetikus filmet a grafikonhoz, amelyet Ron Howard rendezett
  A csoportosítás implicit módon történik összesített eredmények visszaadásával. A csoportkulcsok azok lesznek
  tulajdonságok, amelyeket nem összesítünk:
  egyezés (p1:Személy)-[r1:REVIEWED]->(m1:Movie)
  return m1.title, count(*), max(r1.rating), avg(r1.rating) mint patkány, min(r1.rating)
  rendelés rat des
  Hány film van az adatbázisban:
  mérkőzés (:film) visszatérési száma (*)
  A legrövidebb út keresése48:

```
https://neo4j.com/docs/cypher-manual/current/patterns/shortest-paths/
```

match p=shortestPath((p1:Person)-[:FOLLOWS*]-(p2:Person)) //p egy elérési út. Jegyezd meg a
*
ahol p1.name='James Thompson' és p2.name='Paul Blythe'
return [n in node(p) | n.name] megállóként
//visszatér: ["James Thompson", "Jessica Thompson", "Angela Scope", "Paul Blythe"]
A grafikon átmérője az irányítatlan FOLLOWS dimenzió mentén:
egyezés (p1:Személy), (p2:Személy) ahol id(p1)<>(id(p2)) //kezdet és vége nem lehet
ugyanaz
egyezés p=legrövidebbútvonal((p1:személy)-[:KÖVETÉSEK*]-(p2:személy))
vissza p, hossz(p) hossz sorrendként hossz desc limit 1 szerint
Vedd figyelembe, hogy nincs sémánk. Így lehet lekérdezni a gráfban ténylegesen használt tulajdonságokat:
egyezés (p:Film) különböző kulcsokat (p), méretet (billentyűk (p)) ad vissza
egyezés ()-[r:REVIEWED]->() különböző kulcsokat (r), méretet (kulcsok (r)) ad vissza
Ez törli az összes kapcsolatot, majd az összes csomópontot az adatbázisból:
egyezés ()-[r]-() törlés r
egyezés (n) n törlése

```sql
Importing data to Neo4j
A gráf SQL Serverből Neo4j-be történő migrálásának legegyszerűbb módja a CSV-fájlok használata. Ez a
graph version of the core Northwind tables.
1. Create suitable views that contain only the data we need in the graph
use northwind
create view vi_products as select productid, productname from products
go
create view vi_orders as select orderid, cast(orderdate as date) odate from orders
go
create view vi_orders_products as
select o.orderid, p.productid, od.Quantity quantity, od.Quantity*od.UnitPrice*(1od.Discount) price
from orders o join [Order Details] od on o.orderid=od.OrderID
join products p on od.ProductID=p.productid
go
```

2. Exportáld ezeket a nézeteket CSV-fájlokba az SSMS Adatexportálás eszközzel
3. Másolás
   a
   fájlokat
   be
   a
   import
   mappát
   -ból
   C:\Users\db\.Neo4jDesktop\relate-data\dbmss\[DB id]\import
   a
   Neo4j
   adatbázis:
4. Töltsd be és hozd létre a rendeléseket, a termékeket és végül a rendelési tételeket, azaz a köztük lévő éleket
   megrendeléseket és termékeket
   töltsd be a csv-t a fejlécekkel a „file:///products.csv” sorból
   létrehozás (p:product {id: line.productid, name: line.productname})
   return p.id, p.name
   töltsd be a csv-t a fejlécekkel a „file:///orders.csv” sorból
   létrehozás (o:orders {id: line.orderid, odate: date(line.odate)})
   return o.id, o.odate;
   töltsd be a csv-t a fejlécekkel a „file:///order_products.csv” sorból
   egyezés (p:product {id: line.productid}), (o:orders {id: line.orderid})
   egyesítése (o) -[c:TARTALMAZ

{mennyiség: toInteger(sor.mennyiség), ár: toFloat(sor.ár)}]-> (p)
vissza c;
GYAKORLAT: A Northwind adatok betöltése után kérdezd le a Cypherben a bevételt év és terméknév szerint.
Hasonlítsa össze a relációs verziót ugyanazon lekérdezés gráf alapú verziójával.
GYAKORLAT:

1. Állítsd le a Neo4j adatbázist

2. Írj egy T-SQL parancsfájlt egy véletlenszerű gráf létrehozásához 1000 csomóponttal és 500 éllel az SQL Serverben
   és mérje meg az átmérő kiszámításához szükséges időt

3. Exportáld a grafikont CSV-fájlokba

4. Állítsd le az SQL Server szolgáltatást, és indítsd el a Neo4j adatbázist

5. Állítsd át a grafikont Neo4j-re

6. Mérje meg az átmérő kiszámításához szükséges időt, és hasonlítsa össze az SQL Serverrel
   teljesítményt

7. Magyarázd el az eredményeket
   Képek és BLOB-ok tárolása
- Közepes méretű egyedi képek (például egy webáruházban található árucikkek képei) esetén a
   VARBINARY(MAX) adattípus javasolt:
  
  ```sql
  insert my_table(image_column)
  ```
  
  ```sql
  select * from openrowset(bulk 'c:\my_path\my_photo.png', single_blob)
  ```

- Nagyméretű videó- ​​és egyéb BLOB-fájlok esetén a FileTables technológia ajánlott az SQL Serveren.
   A fájltáblákhoz hasonlóan az adatbázisból és más alkalmazásokból is elérhetők
   a fájlrendszerben tárolt normál fájlok49.
   GYAKORLAT: Valósíts meg egy FileTable megoldást a kurzus képernyőrögzítő videóinak tárolására.
  
  ```
  https://docs.microsoft.com/en-us/sql/relational-databases/blob/load-files-into-filetables?view=sql-server2017
  ```
8. Memórián belüli táblák az SQL Serverben
   Memórián belüli táblák, más néven memóriaoptimalizált táblák (MOT), natívan lefordított tárolt táblákkal kombinálva
   A logika az OLTP relációs adatbázis-technológia Formula-1-je50, amelyet a memória engedélyezett
   egyre olcsóbb.
   Jellemzők:
- Párhuzamos adatfeldolgozási módszerek, finomított memórián belüli adatstruktúrák, hash indexek és a
   különálló, dedikált memórián belüli adatbázismotor -> nagy teljesítmény.
  
  - Minden MOT táblaszerkezethez vagy natívan lefordított eljáráshoz egy új dll jön létre
  - A zárolások elkerülése érdekében sorverziót használnak, azaz amikor egy sor frissül, a sor egy másik verziója
    a sor létrejön (=automatikus pillanatkép elkülönítés). A törlések is logikusak, törölve
    sorok mindaddig megőrződnek, amíg az adott verziót használni tudó összes tranzakció véglegesítésre nem kerül

- Teljes ACID támogatás. A tartósság biztosított, minden változtatás a nem felejtő (lemez alapú) fájlba kerül.
   tranzakciós napló

- A MOT-okat a tempdb alternatívájaként tranziens adatok tárolására is tartóssá lehet tenni
   táblák. Az ilyen táblákban lévő adatok módosítása nem igényel lemez I/O-t. További előnye, hogy
   a tábla szerkezete megmarad, ellentétben az ideiglenes táblákéval. Nem tartós
   A MOT-ok memória-gyorsítótárként használhatók.

- A MOT-ok ugyanabban az adatbázisban lehetnek, mint a hagyományos táblák

- ```sql
   If a stored procedure is not natively compiled and it uses a MOT, it must run in interpreted
   mode (note that the MOT is managed by another engine)51
  ```
  
   Követelmények és korlátozások52:

- Csak a hash vagy nem fürtözött BTree indexek támogatottak

- Elegendő memóriának kell lennie
  
  - A MOT és indexei
  - Soros verziózás
  - Táblázatváltozók és növekményes növekedés
    Ökölszabály: „kezdjük a memóriaoptimalizált táblák várt méretének kétszeresével és
    indexek” 53

- A MOT nem érhető el másik adatbázisból (nincs adatbázis-lekérdezések vagy tranzakciók
   megengedett), és nem particionálható

- Az oldal- és sortömörítés, valamint a DDL-triggerek nem támogatottak

- Csak a tranzakciós replikáció támogatott MOT előfizetőként

- A DDL (CREATE/ALTER/DROP) nem támogatott a tranzakciókon belül
  
  ```
  https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/overview-and-usagescenarios?view=sql-server-ver16
  https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/a-guide-to-query-processingfor-memory-optimized-tables
  https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/unsupported-sql-serverfeatures-for-in-memory-oltp?view=sql-server-ver16
  https://learn.microsoft.com/en-us/sql/relational-databases/in-memory-oltp/estimate-memoryrequirements-for-memory-optimized-tables?view=sql-server-ver16
  ```

- A natívan összeállított tárolt eljárások csak a memóriára optimalizált táblákra hivatkozhatnak

- Azonosító elsődleges kulcsok
  Ajánlott alkalmazási területek:

- Nagy teljesítményű tranzakciófeldolgozás, pl. nagyszámú párhuzamos, alacsony késleltetésű tőzsdei tranzakció támogatása. A megvalósítás memóriaoptimalizált módon használd
  tranzakciós táblák és az üzleti logika natívan lefordított tároltként valósul meg
  eljárások. Különösen azok az eljárások, amelyekben a CPU-idő dominál, profitálnak a natív előnyeiből
  összeállítása.

- Valós idejű adatgyűjtés és adattranszformáció sok forrásból, pl. IoT érzékelők. Ha a méret
  Ha korlátozni kell a tábla adatait, akkor egy jobot kell használni az adatok cseréjére a memóriában lévő táblából
  lemez alapú oszloptároló. Ha sok frissítés van, az alaptábla lehet időbeli
  memóriaoptimalizált tábla. A történelmi feljegyzéseket lemezen tárolják.

- Hasonló forgatókönyv az adatok kibontása-átalakítása-betöltése (ETL) folyamatának megvalósítása
  raktár, amely nem tartós, memóriára optimalizált táblákat használ állomásozó táblaként. Nem tartós táblák
  nincs szükség lemez I/O-ra, ami felgyorsítja az ETL folyamatot.

- Gyorsítótárazás. Ebben az esetben egy nem tartós memóriatáblát használnak kulcsérték-tárolóként (blob vagy json).

- A táblatípusok memóriaoptimalizálttá is tehetők. Az ilyen típusok használhatók táblaértékesítéshez
  tárolt eljárások paraméterei.
  GYAKORLAT54
  Egy új tesztadatbázisban mérjük a MOT teljesítménynövekedését egy normál táblahoz képest. Összehasonlítjuk
  három forgatókönyv a tábla beszúrásához:
1. lemez alapú tábla és értelmezett Transact-SQL

2. memóriára optimalizált tábla hash indexszel és értelmezett Transact-SQL-lel

3. memóriára optimalizált tábla hash indexszel és natívan lefordított tárolt eljárással
   Tervezési migráció az In-Memory-ba
   A migráció jelentős erőfeszítés lehet. Vannak beépített eszközök az OLTP -> In-Memory migrációhoz.
   GYAKORLAT
- ```sql
   Töröld a Northwind adatbázist, majd állítsd vissza a dumpból
  ```

- Adatbázis -> Jelentések -> Normál jelentések -> Tranzakcióteljesítmény-elemzés áttekintése. Ezt
   eszköz ajánlásokat ad a jelölt táblákhoz és eljárásokhoz. Kattints a
   tábla/proc név a részletes statisztikákhoz. A már a memóriában lévő táblákat/procokat nem tartalmazza.

- Az összes tábla összesítő táblaának létrehozásával ellenőrizheti az áttelepítések számát
   blokkolók. Látható, hogy a legroszdbb eset a Vevők tábla 36 blokkolóval. Ez esedékes
   a kiírásás hibájára, amely ugyanazon idegen kulcs több példányát eredményezte. Helyes
   a szemétlerakó.

- Adatbázis -> Feladatok -> Memórián belüli OLTP-migrációs ellenőrzőlisták létrehozása (nem működik)
   Az SQL Server 2022 nevű példányán a fájl memóriaoptimalizált fájlcsoporthoz való hozzáadása meghiúsul a hibával.
   üzenet: „Nem sikerült feldolgozni a műveletet. Az Always On Availability Groups replikakezelő le van tiltva ezen
   példa… stb.” Ez ismert probléma. Az SQL Server 2019 alapértelmezett példányát használjuk (azaz NEM elnevezett példányt)
   helyette.

- Táblázat neve -> Táblamemória optimalizálási tanácsadó: első lépésként létrehozd az ellenőrzőlistát. Mind
  az idegenkulcs-megszorításokat a táblából/táblába kézzel kell eldobni az áttelepítés előtt és
  majd újra létrehozva.

- A tanácsadó megtervezheti és végrehajthatja az áttelepítést. A régi tábla megmarad és átnevezzük.
  GYAKORLAT
  Reálisabb forgatókönyv esetén a rendelésfeldolgozási tárolt eljárás teljesítményét teszteljük
  Northwind adatbázis párhuzamos munkamenetekben.
1. Dobja el az adatbázist, és hozd létre újra egy kiírásásból, majd hozd létre az sp_new_order() eljárást.
2. Állítsd be a teszteléshez szükséges paramétereket, és futtasd le a procit 10000-szer 3 párhuzamos munkamenetben, olvasás közben
   elszigeteltséget követett el, és 100-szor ismételhető olvasásban. Mérje meg a futási időt.
3. Nézd át meg a Tranzakcióteljesítmény-elemzés áttekintését. A MOT-hoz ajánlott táblák a következők
   Termékek, rendelések, rendelési adatok, területek és ügyfelek.
4. A Termékek, Rendelések, Rendelés részletei, Ügyfelek táblák áttelepítése:
   a. Hozz létre egy új adatbázist Northwind_mot néven, és futtasd benne a javított dump szkriptet
   b. Töröld az idegenkulcs-megszorításokat a fenti táblákból
   c. A táblák áttelepítése az Advisor segítségével. Ne felejtsen el adatokat felvenni az új táblaba
5. módosítsd az adatbázis aktuális beállítását: memory_optimized_elevate_to_snapshot = on
6. Futtasd a régi sorrendű procit, teszteld és hasonlítsa össze a futási időket
7. Készítsd el a tárolt eljárás natívan lefordított változatát, és ismételje meg a teszteket
8. Magyarázd el az eredményeket!

Köszönetnyilvánítás
A kurzus jegyzeteinek néhány példája Dejan Sarka, Matija Lah, Grega Jerkič könyvén alapul:
70-463 vizsga: Adattárház megvalósítása Microsoft SQL Server 2012-vel, Microsoft Press, ISBN
978-0-7356-6609-2, 2015. További példákra a lábjegyzetekben hivatkozunk.

FÜGGELÉK A: SQL DML példák önálló tanuláshoz

```sql
use NORTHWIND
select * from employees
select lastname, birthdate from employees
--a Londonban található ügyfelek neve
select companyname, city
from customers
--where city LIKE 'L%' and (city LIKE '%b%' or city LIKE '%n%') --partial matching
where city IN ('London', 'Lander')
where city ='London' or city ='Lander'
where city IN ('London')
where city = 'London'
--who is the youngest employee? What is her name?
--1/2) the maximal birthdate
--aggregate functions: max, min, avg, std, sum, count
select max(birthdate) as max_year, min(birthdate) as min_year
--, lastname --would be an error
from employees
--2/2) embed this query
select lastname, birthdate from employees
where birthdate = ('1966-01-27 00:00:00.000')
select lastname, birthdate as "birth date" from employees
where birthdate = (
select max(birthdate) as max_year
from employees
)
--PROBLEM: find the ShipAddress of the first order
select orderdate, shipaddress from orders
where orderdate = (
select min(orderdate) as min_date
from orders
)
--ship addresses of the youngest employee
--joining tables
select distinct lastname, shipaddress
from orders o inner join employees e on o.employeeid=e.employeeid
where e.employeeid = (
select employeeid from employees
where birthdate = (
select max(birthdate) as max_year
from employees
)
)
order by shipaddress --desc
```

```sql
--which products were ordered form the youngest employee
--note: always start with the FROM part of the query
select distinct p.productname, e.lastname
from orders o inner join employees e on o.employeeid=e.employeeid
inner join [order details] od on od.orderid=o.orderid
inner join products p on p.productid=od.productid
where e.employeeid=9 --she is the youngest
order by productname
--PROBLEM: which are the ship cities of products with CategoryID=1?
select distinct o.shipcity
```

```
from orders o inner join [order details] od on od.orderid=o.orderid
inner join products p on p.productid=od.productid
where p.categoryid = 1 --our search conditon
order by shipcity
```

```sql
--No. of orders per employee?
--1/5) GROUPING
select employeeid, count(*)
from orders
group by employeeid
--a note aside: how to test for null?
select * from orders where employeeid is null
delete from orders where employeeid is null
--2/5) DO NOT DO THIS:
select e.lastname, count(*)
from orders o inner join employees e on o.employeeid=e.employeeid
group by e.lastname
--results in logical error if there are
--2 persons with the same lastname!!!
--3/5)
select e.lastname, e.firstname, count(*)
from orders o inner join employees e on o.employeeid=e.employeeid
group by e.employeeid, e.lastname, e.firstname
--this query misses the agent with no orders
--PROBLEM: list the number of products in each Category (we need the CategoryName also)
3. select c.categoryid, c.categoryname, count(*) as no_prod
1. from products p inner join categories c on p.categoryid=c.categoryid
2. group by c.categoryid, c.categoryname
4. order by no_prod desc
--4/5)
select e.employeeid, e.lastname, e.firstname, count(*)
from employees e left outer join orders o on o.employeeid=e.employeeid
group by e.employeeid, e.lastname, e.firstname
--problem: we have a fake count of 1 for the idle agent
--5/5)
select e.employeeid, e.lastname, e.firstname, count(o.orderid) as no_ord
from employees e left outer join orders o on o.employeeid=e.employeeid
group by e.employeeid, e.lastname, e.firstname
order by no_ord desc
--all problems solved
--who is whose boss
select e.lastname, boss.lastname as boss, bboss.lastname as boss_of_boss
from employees e left outer join employees boss on e.reportsto=boss.employeeid
left outer join employees bboss on boss.reportsto=bboss.employeeid
```

```sql
--No. of orders per employee?
select e.lastname, count(orderid)
--count(*) would produce an order for Lamer who has no order at all
from employees e left outer join orders o on
--from employees e inner join orders o on
e.employeeid = o.employeeid
group by e.employeeid, e.lastname
order by count(*) desc
--who has no orders?
select e.*
```

```
from employees e left outer join orders o on
e.employeeid = o.employeeid
where o.orderid is null
--which is the biggest order?
--arithmetics
4. select o.orderid,
cast(o.orderdate as varchar(50)) as order_date,
str(sum((1-discount)*unitprice*quantity), 15, 2) as order_total,
sum(quantity) as no_of_units,
count(d.orderid) as no_of_items
1. from orders o inner join [order details] d on o.orderid=d.orderid
2. where...
3. group by o.orderid, o.orderdate
--order by o.orderdate
5. order by sum((1-discount)*unitprice*quantity) desc
--in order to order by date:
```

```
group by o.orderid, o.orderdate
```

```sql
--who's the most successful agent? with how many orders?
-- observe: having
-- count distinct
-- formatting numbers
select u.titleofcourtesy+' '+u.lastname+' '+ u.firstname +' ('+u.title +')'
--select u.lastname as name,
str(sum((1-discount)*unitprice*quantity), 15, 2) as cash_income,
count(distinct o.orderid) as no_of_orders, count(productid) as no_of_items
from orders o inner join [order details] d on o.orderid=d.orderid
inner join employees u on u.employeeid=o.employeeid
group by u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname
```

névként,

```sql
--having count(o.orderid)>200 –if we are only interested in agents with more than 200
orders
order by cash_income
--sum((1-discount)*unitprice*quantity) desc
--why do we have only 9?
select count(*) from employees
--it should be 10!
--szükségünk lenne azokra is, akiknek 0 rendelésük van
-- isnull function
select isnull(u.titleofcourtesy, '')+' '+isnull(u.lastname, '')+' '+ isnull(u.firstname,
'') +' ('+isnull(u.title, '') +')' as name,
isnull(str(sum((1-discount)*unitprice*quantity), 15, 2), 'N/A') as cash_income,
count(distinct o.orderid) as no_of_orders, COUNT(d.productid) as no_of_items
from employees u left outer join
(orders o inner join [order details] d on o.orderid=d.orderid)
on u.employeeid=o.employeeid
--where u.titleofcourtesy='Mr.' –if we are only interested in men
group by u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname
order by sum((1-discount)*unitprice*quantity) desc
--which is the most popular product?
-- top 1
select top 1 p.productid, p.productname, count(*) as no_app,
sum(quantity) as total_pieces
from products p left outer join [order details] d on p.productid=d.productid
group by p.productid, p.productname
order by no_app desc
```

```sql
--which agent sold the most of the most popular product?
--first version
select top 1 u.titleofcourtesy+' '+u.lastname+' '+ u.firstname +' ('+u.title +')'
name,
sum(quantity) as no_pieces_sold
from orders o inner join [order details] d on o.orderid=d.orderid
inner join employees u on u.employeeid=o.employeeid
where d.productid = 59 --ezt már tudjuk
group by u.employeeid, u.titleofcourtesy, u.title, u.lastname, u.firstname
-- having....
order by sum(quantity) desc
```

mint

```sql
/************************************************************************
PROBLEM
--which agent sold the most of the most popular product, and what is the name of that
product?
--in the pubs_access database: which is the most frequnted publisher of the author with the
most publications?
**************************************************************************/
--MULTI LEVEL GROUPING
--datetime fUNCTIONS
select 2
select getdate() --datetime data type
select DATEDIFF(s,'2013-10-10 12:13:50.370', '2013-10-10 14:16:50.370')
select DATEADD(s, 1000, '2013-10-10 14:16:50.370')
select YEAR(getdate()), MONTH(getdate())
--ORDERS BY MONTH AND AGENT
select e.employeeid, lastname, year(orderdate) as year, month(orderdate) as month,
count(orderid) as no_of_orders
from employees e left outer join orders o on e.employeeid=o.employeeid
group by e.employeeid, lastname, year(orderdate), month(orderdate)
order by lastname, year, month
--ugyanez másképp:
select e.employeeid, lastname,
cast(year(orderdate) as varchar(4)) +'_'+ cast(month(orderdate) as char(2)) as month,
count(orderid) as no_of_orders
from employees e left outer join orders o on e.employeeid=o.employeeid
group by e.employeeid, lastname, cast(year(orderdate) as varchar(4)) +'_'+
cast(month(orderdate) as char(2))
order by lastname, month
--select case
select e.employeeid, lastname,
case
when month(orderdate) < 10 then cast(year(orderdate) as varchar(4)) +'_0'+
cast(month(orderdate) as char(2))
when month(orderdate) >= 10 then cast(year(orderdate) as varchar(4)) +'_'+
cast(month(orderdate) as char(2))
else 'N.A'
end as month,
count(orderid) as no_of_orders
from employees e left outer join orders o on e.employeeid=o.employeeid
group by e.employeeid, lastname,
case
when month(orderdate) < 10 then cast(year(orderdate) as varchar(4)) +'_0'+
cast(month(orderdate) as char(2))
when month(orderdate) >= 10 then cast(year(orderdate) as varchar(4)) +'_'+
cast(month(orderdate) as char(2))
else 'N.A'
end --a function serves better for this purpose
```

```sql
order by lastname, month
--using temp tables
select GETDATE() as ido into #uj_tabla
select * from #uj_tabla
drop table #uj_tabla
select * into #uj_tabla from employees
```

```sql
--drop table #tt
select e.employeeid, lastname, year(orderdate) as ev, month(orderdate) as month,
count(orderid) as no_of_orders
into #tt
from employees e left outer join orders o on e.employeeid=o.employeeid
group by e.employeeid, lastname, year(orderdate), month(orderdate)
order by lastname, month
select * from #tt
--Warning: Null value is eliminated by an aggregate or other SET operation.
--reason: an aggregate function(max,sum,avg..) exists on null values
select * from #tt
select lastname, str(avg(cast(rend_szam as float)), 15, 2) as avg_no_of_orders
--select lastname, avg(rend_szam) as avg_no_of_orders
from #tt group by employeeid, lastname
order by atlagos_rend_szam desc
--another solution for the same problem with an embedded query
select forras.lastname, str(avg(cast(forras.rend_szam as float)), 15, 2) as
avg_no_of_orders
from (
select e.employeeid, lastname, year(orderdate) as ev, month(orderdate) as month,
count(orderid) as no_of_orders
from employees e left outer join orders o on e.employeeid=o.employeeid
group by e.employeeid, lastname, year(orderdate), month(orderdate)
) as f –using an alias is compulsory
group by employeeid, lastname
order by avg_no_of_orders desc
--HOMEWORK PROBLEMS:
--AVG monthly number of orders for all products?
--Who had more than double order total compared to his boss?
```

B FÜGGELÉK: Adatbázis adminisztráció és karbantartás
A relációs adatbázis-adminisztráció leggyakoribb feladatai a következők.

- Adatbázis fájlkezelés

- Az adatbázis teljesítményének fenntartása – olyan problémák megoldása, mint a fájlok töredezettsége és az újraszámítás
  tábla statisztika

- Felhasználó- és biztonságkezelés, azaz bejelentkezési szerepkörök, jogosultságok, házirendek és adatbázis-titkosítás

- Biztonsági mentési stratégia megvalósítása

- Riasztások konfigurálása kritikus állapotokhoz
  Ezeket az elemeket külön-külön is meg lehet valósítani, vagy egyetlen adatbázisban egyesíthetjük
  karbantartási terv.
  Adatbázis fájlok
  Minden SQL Server adatbázishoz legalább két fájlnak kell társítania, amelyek közül az egyik tartalmazza az adatbázist
  objektumok (mdf fájl), a másik pedig a tranzakciós naplót (ldf fájl) tartalmazza. Ez a naplófájl, amely a legtöbb
  kritikus a feladatátvételi helyreállítás szempontjából, ezért ezt a fájlt redundáns adathordozón kell tárolni, pl. a
  RAID tömb.
  A töredezettség elkerülése érdekében a fájlokat legjobb olyan köteteken elhelyezni, amelyeket más programok nem használnak. A
  Az adatbázis kezdeti mérete a tervezett alkalmazás alapján megbecsülhető. Túl kis mennyiségben
  az automatikus növekedés töredezettséghez is vezethet.
  Az adatbázis integritásának ellenőrzéséhez jó gyakorlat a DBCC CHECKDB ('DB_name') futtatása a következővel:
  NO_INFOMSGS, ALL_ERRORMSGS, ahányszor teljes biztonsági másolat készül. Bármilyen kimenet korrupciót jelent
  az adatbázisból.
  Adatbázis teljesítmény
  Válaszd ki a megfelelő helyreállítási módot. Csak akkor használd a Teljes módot, ha az alkalmazásnak valóban szüksége van rá. Készíts
  győződjön meg arról, hogy a következő adatbázis-beállítások be vannak állítva:

- Automatikus frissítési statisztika = TRUE

- Statisztikák automatikus létrehozása = TRUE

- Automatikus zsugorítás = HAMIS (ha lehetséges, egyáltalán ne használjon tábla vagy adatbázis zsugorítást)

- Oldal ellenőrzése = ELLENŐRZŐ SZUM
  Az adatbázis alkalmazáshoz való hangolása túlmutat ennek a kurzusnak a keretein.
  Biztonsági mentések
  Egy kliens-szerver adatbázis-alkalmazásban az előre írható tranzakciós naplót használjuk az adatvesztés kezelésére
  helyzetekben. Háromféle hiba létezik, amelyekre fel kell készülnünk:
1. Megszakadt a kapcsolat az ügyféllel. -> A napló segítségével visszaállítjuk az összes nem véglegesített tranzakciót

2. A szerver folyamat leáll, azaz elveszítjük a memóriában lévő adatokat és naplózó puffereket -> amikor a szerver
   újraindul, először azokat a tranzakciós lépéseket görgeti előre a tranzakciónaplóból, amelyekhez a
   a releváns adatlapok nem lettek kiírva az adatfájlokba, akkor az összes nem véglegesített adatot visszagörgeti
   tranzakciók

3. Az adatfájl elveszett -> készíts biztonsági másolatot a tranzakciós naplóról, használd a korábbi teljes és differenciális biztonsági mentéseket
   majd a napló biztonsági mentését az adatbázis visszaállításához, majd visszaállítja az összes nem véglegesített tranzakciót
   A rendszeres biztonsági mentések készítése a katasztrófa utáni helyreállításra való felkészülés gyakori módja. A biztonsági másolat fájljait tárolni kell
   médián az adatbázis adatoktól és naplófájloktól eltérő formában. A három leggyakoribb stratégia:
   #1. A minimum: használjon teljes biztonsági másolatot SIMPLE helyreállítási módban55, pl. napi rendszerességgel tehermentes állapotban
   időszakokban. A biztonsági másolatokat körbe-körbe kell tárolni és újraírni, pl. felett a
   heti időszak. Ily módon az adatvesztés egy napra korlátozható. Ez egy jó gyakorlat
   tartalmazza a biztonsági mentésbe a master, a modell és az msdb adatbázisokat is.
   #2. Használjon teljes biztonsági mentéseket és differenciális biztonsági mentéseket SIMPLE helyreállítási módban, pl. napi teljes biztonsági mentés
   és differenciális biztonsági mentések 2 óránként. Ily módon az adatvesztés 2 órára korlátozható.
   #3. Ha az alkalmazás megköveteli az adatvesztés lehetőségének minimalizálását, akkor az adatbázisnak ezt kell tennie
   állítsd TELJES helyreállítási módra, és a második stratégiát kombinálni kell a tranzakciónaplóval
   biztonsági mentések. A teljes helyreállítási mód azt jelenti, hogy biztonsági mentés nélkül a napló jelentősen növekedhet. An
   példa stratégia egy napi teljes biztonsági mentés, a 2 óránkénti differenciális biztonsági mentések és egy tranzakció
   20 percenként naplózza a biztonsági mentést. Ha az adatfájl elveszik, az összes lekötött tranzakció megtörténik
   megőrizve.
   A biztonsági mentések BACKUP DATABASE/RESTORE DATABASE SQL utasítások formájában is végrehajthatók
   így 56:
   HASZNÁLAT [mester]
   ADATBÁZIS VISSZAÁLLÍTÁSA [northwind] LEMEZRŐL = N'C:\Program Files\Microsoft SQL
   Szerver\MSSQL14.PRIM\MSSQL\Backup\nw' WITH FILE = 1, NOUNLOAD, REPLACE, STATS = 5
   GYAKORLAT: Lemezhibát szimulálunk. Teljes biztonsági másolatot készítünk a Northwind adatbázisról egy fájleszközön,
   állítsd le az SQL Server PRIM szolgáltatást, töröld az adatbázisfájlt, indítsd újra a szolgáltatást, és állítsd vissza innen
   biztonsági mentést a WITH REPLACE opció használatával. Ellenőrizd a tartalmat.
   Normál biztonsági mentés esetén lehetséges a BACKUP SQL utasítás végrehajtása egy ütemezett feladatban, amelyet mi
   készítsd elő manuálisan. Alternatív megoldásként a biztonsági mentési feladatok integrálhatók egy adatbázis-karbantartási tervbe.
   
   ```sql
   Maintenance plans
   Before the plan can be created, we must enable the use of extended stored procedures for SQL Server
   agent:
   use master
   sp_configure 'show advanced options', 1
   go
   reconfigure
   go
   sp_configure 'Agent XPs', 1
   go
   reconfigure
   go
   ```
   
   PRACTICE: Implement the backup strategy #1 in a new maintenance plan for a new test database by
   setting the schedule to every 2 minutes (for demo purposes). Tartalmazza még az index újraszámítását és
   Az egyszerű helyreállítási mód azt jelenti, hogy a napló inaktív részeit rendszeresen csonkolják.
   SQL-szkriptek generálhatók az SSMS minden párbeszédpaneléről.

integritás-ellenőrzés, mint napi szinten végrehajtandó feladat. Használd a Kezelés -> Karbantartási terveket.
Ne használd a varázslót. A 2 perces ismétlődő intervallumot csak demó céljára állítjuk be.
Ellenőrizd, hogy a biztonsági mentések 2 percenként jönnek-e létre.

Nem tudjuk tesztelni a tisztítási feladatot, mert nem állíthatunk be egy napnál rövidebb törlési kort.
GYAKORLAT: A 3. biztonsági mentési stratégiát megvalósítjuk a Northwind új karbantartási tervében
adatbázis:
Figyelmeztetések
Jó gyakorlat minden 24-es súlyosságú hiba esetén riasztást beállítani. Egy másik klasszikus kritikus állapot az
amikor az adatbázisfájlokat tároló kötetben fogy a szabad hely.
GYAKORLAT: Ebben a bemutatóban beállítunk egy riasztást, amely akkor aktiválódik, amikor a Northwind adatbázis mérete eléri
A jelenlegi méret 150%-a. Először ellenőrizzük az adatbázis aktuális méretét a C:\Program Files\Microsoft mappában
SQL Server\MSSQL14.PRIM\MSSQL\DATA mappa: 8,2 MB.
Ha a méret lényegesen nagyobb, először a helyreállítási módot állítjuk egyszerűre, majd csökkentjük az adatbázist,
vagyis csak 10% szabad kihasználatlan terület marad:

```sql
use master
dbcc shrinkdatabase (northwind, 10)
```

A riasztás beállításának folyamata 4 lépésből áll:

1. Állítsd be az adatbázis levelezési profilját

2. Engedélyezd a levélprofilt az SQL szerver ügynökben, amely a riasztást futtatja

3. Hozz létre egy operátort (egy személyt, aki megkapja a figyelmeztetést és megoldja a problémát)

4. Hozd létre és teszteld a riasztást
   Adatbázis-levelezés beállítása
   Válaszd a Server -> Management node -> Database mail -> Configure Database mail lehetőséget, majd az Új
   profil panelen írd be a prim_mail parancsot a profilnévhez, majd kattints az SMTP-fiók hozzáadása lehetőségre. Add meg a mi nevét
   SMTP szerver.

Ezután meg kell adnia annak az új levelezési profilnak a nevét, amely az SMTP-fiókot fogod használni:
A profil nyilvánossá tételével minden felhasználó használhatod e-mailek küldésére:
Ellenőrizd, hogy a profil működik-e az Adatbázis mail -> Teszt e-mail küldése lehetőség kiválasztásával. Ellenőrizd, hogy az e-mail
a vártnak megfelelően megkapta:

```sql
A levélprofil engedélyezése az SQL Server Agentben
Válaszd a Properties menüpontot az SQL Server Agent csomópont helyi menüjéből:
```

Operátor létrehozása
Válaszd az Operátorok lehetőséget az SQL-kiszolgáló ügynök csomópontjából, és adj hozzá egy új operátort. Az „E-mail név” szövegben
mezőbe írd be a saját e-mail címét.

```sql
Riasztás hozzáadása
Válaszd az Alerts menüpontot az SQL Server Agent csomópontjánál, és adj hozzá egy új riasztást:
```

```sql
Állítsd a választ arra, hogy e-mailben értesítse az operátort (NW rendszeradminisztrátor):
```

A Beállítások lapon adj hozzá egyéni üzenetet. Állítsd a késleltetést 1 percre. Ezt a beállítást csak demóhoz használjuk
célokra. Megjegyzés: Ha a válaszok közötti késleltetést 0-ra állítja, a válasz megismétlődik
folyamatosan, amíg a riasztási feltétel teljesül.
Teszteld a riasztást a következő szkripttel.
válaszd ki

```sql
object_name(object_id) as 'tablename',
count(*) as 'totalpages',
sum(Case when is_allocated=0 then 1 else 0 end) as 'unusedPages',
sum(Case when is_allocated=1 then 1 else 0 end) as 'usedPages'
from sys.dm_db_database_page_allocations(db_id(),null,null,null,'DETAILED')
group by
object_name(object_id)
--létrehozunk egy nagy táblát
go
create table big_table (a char(4000))
declare @i int=0
while @i<1000 begin
insert big_table values ('a')
set @i=@i+1
end
--big_table has 500 pages -> alert is fired
```

Ellenőrizd a riasztási előzményeket és a postafiókját. A figyelmeztető levelek folyamatosan érkeznek. Ne felejtse el leejteni
a big_table, és tiltsd le vagy töröld a figyelmeztetést.

```sql
Overview of principals, privileges, schemas, roles
A kiszolgálóbejelentkezések és az adatbázis-felhasználók viszonya mint főszereplők. A bejelentkezés hozzá van kötve az adatbázis-felhasználókhoz, és ez
normally has a default database.
use master
create login nw_user with password='...', default_database=northwind
use northwind –context switch
create user nw_user for login nw_user
alter role db_datareader add member nw_user
```

```sql
PRACTICE: create a new database, a new login and a new database user
Overview of privileges, GRANT [which privilege] ON [which object] TO [whom], REVOKE, DENY.
use northwind
alter role db_datareader drop member nw_user
go
create procedure sp_list_employees
@city varchar(50) = 'London' –default value for the parameter
as
select * from Employees where City=@city
go
exec sp_list_employees
go
exec sp_list_employees 'Seattle'
go
grant execute on sp_list_employees to nw_user
go
```

```sql
Roles are groups of privileges, like read access to all tables.
Important server level roles: public, dbcreator, serveradmin, sysadmin
Important database level roles: db_owner, db_datareader, db_datawriter, negative roles:
db_denydatawriter, db_denydatareader
use adworks
alter role exec_all_sp drop member nw_user
alter role db_owner add member nw_user
alter role db_denydatawriter add member nw_user
--check in a nw_user client connection:
use adworks
select * from Sales.Store
--(701 rows affected)
exec Person.sp_DeletePerson_Temporal 2
--(1 row affected)
--(1 row affected)
create table test (id int)
--Commands completed successfully.
insert test (id) values (25)
--Msg 229, Level 14, State 5, Line 10
--Az INSERT jogosultság megtagadva az objektumon 'test', database 'adworks', schema
'dbo'.
drop table test
--Commands completed successfully.
```

```sql
You can also create your own roles.
use northwind
revoke execute on sp_list_employees from nw_user
go
--így adhatunk végrehajtási jogot az adatbázis ÖSSZES objektumára
```

```sql
grant execute to nw_user
--check in a client connection
--a new role
use adworks
create role exec_all_sp
grant execute on schema::Person to exec_all_sp--a szerepkör úgy viselkedik, mint egy principal
--could also be: grant select, update on schema::Person to read_update_only_role etc.
create user nw_user for login nw_user
alter role exec_all_sp add member nw_user
--check in a client connection
use adworks
select * from Sales.Store
--Msg 229, Level 14, State 5, Line 8
--A SELECT jogosultság megtagadva az objektumon 'Store', database 'adworks', schema
'Sales'.
exec Person.sp_DeletePerson_Temporal 2
--(1 row affected)
--(1 row affected)
```

GYAKORLAT: hozz létre egy új szerepet a db_datareader és a db_datawriter szerepkör fúziójaként, és rendeld hozzá a
új felhasználó ebbe a szerepkörbe. Teszt.
Az adatbázis-objektumok egy sémához tartoznak, és a sémának egyetlen tulajdonosa van (nem a
a db_owner adatbázis szerepkör tagja). A tulajdonos eldobhatja a sémát, és objektumokat hozhat létre vagy dobhat el
a sémában.
A jogosultságokat általában a séma/szerepkör, és nem az egyéni felhasználó/tábla szinten szabályozzák.
Hogyan ellenőrizhető, hogy mely megbízók milyen szerepet töltenek be?
válaszd ki a DP1.name-t DatabaseRoleName-ként, az isnull-t (DP2.name, 'Nincs tag') mint
DatabaseUserName
sys.database_role_members DRM jobb külső csatlakozásként
sys.database_principals mint DP1 a DRM-en.role_principal_id = DP1.principal_id bal külső
csatlakozz a sys.database_principals-hoz DP2-ként a DRM-en.member_principal_id = DP2.principal_id
ahol DP1.type = 'R' --R: adatbázis szerepkör

```
order by DP1.name
```

A sémák, valamint az alkalmazásokhoz tartozó szerepek és jogosultságok tervezése fontos részét képezi
relációs modellezés. Példa: AdventureWorks adatbázis.
GYAKORLAT: tervezze meg a sémákat, szerepköröket és jogosultságokat egy olyan nagy nemzeti könyvtár számára, mint az OSzK
Adatbiztonság az SQL Serverben
Érzékeny adatok
Az SQL Server 2017-ben a mezők automatikusan vagy manuálisan is besorolhatók w.r.t. információ típusa (pl. „Személyes”)
és érzékenységi szintje (pl. „Bizalmas-GDPR”).
Használd az adatbázis Feladatok -> Adatok osztályozása eszközt. Elmentheti az elfogadott ajánlásokat. Megtehetjük
ennek lekérdezéséhez használd a sys.extended_properties nevű Extended Properties katalógusnézetet is
információkat. Így néz ki egy érzékenységi jelentés:

Automatikus sebezhetőségelemzést is futtathat:

Az adatbiztonság területei

- Biztonságos ügyfélkapcsolatok -> SSL. Telepíteni kell egy tanúsítványt, amelyet a szerver használ.

- Adatbázisfájlok és biztonsági mentési fájlok (az adatok nyugalmi állapotban)

- Fájlszint: biztonsági mentési titkosítás és transzparens adattitkosítás (TDE).
  az adatfájlok titkosítása is

- Mezőszint: az érzékeny oszlopokat akár a rendszergazdák elől is elrejthetjük ("mindig titkosítva"),
  titkosítás és visszafejtés használatával a kliensekben
  A szerver által használt adatok (az adatok mozgásban vannak)

- Dinamikus adatmaszkolás: az érzékeny oszlopok részeinek elrejtése a következőben meghatározott maszk segítségével
  séma pl. ALTER COLUMN [Társadalombiztosítási szám] <adattípus> MASKED WITH
  (FUNCTION = 'partial(0,"XXX-XX-",4)') – csak az utolsó 4 számjegy megjelenítése, és az XX.
  minta a többihez. Az UNMASK jogosultsággal rendelkező felhasználók elolvashatják az eredeti értéket57.

```sql
Az ajánlott jó gyakorlat az, hogy mezőszintű védelmet alkalmazzunk a bizalmasnak minősített mezőkre.
DEMO: masking
use northwind
--alter table employees drop column SSN
--alter table employees drop column email
alter table employees add ssn char(10) null, email varchar(200) --sensitive columns
alter table employees alter column ssn char(10) masked with (function =
'partial(1,".....",4)')
alter table employees alter column email char(200) masked with (function = 'email()')
go
update Employees set ssn ='1234567890'
update Employees set email ='sohase_mondd@citromail.hu'
select lastname, ssn, email from Employees --minden érték látható
--however, if we create a read-write user
use master
create login test with password='h6twqPNO', default_database=northwind
go
use northwind --context switch
create user test for login test
alter role db_datareader add member test
alter role db_datawriter add member test
go
--válts át a tesztfelhasználó kapcsolatára
execute as user = 'test'
select lastname, ssn, email from Employees
revert
go
--this is what we see:
lastname
ssn
email
Davolio
1.....7890
sXXX@XXXX.com
Fuller
1.....7890
sXXX@XXXX.com
--most UNMASK jogosultságot adunk a tesztfelhasználónak
grant UNMASK to test
go
execute as user = 'test'
select lastname, ssn, email from Employees
revert
```

```
https://www.sqlshack.com/using-dynamic-data-masking-in-sql-server-2016-to-protect-sensitive-data/
```

menj
--ezt látjuk:
vezetéknév
ssn
Davolio
1234567890
Fuller
1234567890
e-mailben
sohase_mondd@citromail.hu
sohase_mondd@citromail.hu

```sql
--WARNING: the user can still modify the columns!!!
go
execute as user = 'test'
update Employees set email ='mondj_igent@citromail.hu'
select lastname, ssn, email from Employees
revert
go
revoke UNMASK from test
```

GYAKORLAT:
próbáld meg
a
alapértelmezett()
és
véletlen ()
AdventureworksDW2019.dbo.DimCustomer tábla.
maszkolás
funkciókat
-on
a
SSL konfigurálása

- ```sql
  create a new self-signed certificate with the certreq -new -f certparam.inf local.cer command,
  using the inf file to set the parameters
  ```

- ```sql
  use the mms console All tasks -> Manage private keys to add the MSSQL$PRIM user as a user
  with full control of the private key of the certificate
  ```

- az SS Config Managerben a Protocols -> Properties használatával állítsd be a Enforce encryption opciót, és
  indítsd újra a szolgáltatást

- az SSMS típusban válaszd ki a * elemet a sys.dm_exec_connections listából, és ellenőrizd a mezőket:
  encrypt_option=TRUE -> SSL, auth_scheme=SQL (utóbbi jelentése SQL Server
  hitelesítés)

```sql
Backup encryption
A Service Master Key (SMK) is created automatically when the instance is installed. In order to encrypt
database backups, we need a Master Key that will be stored in the master database encrypted with
the password specified and another copy encrypted with the SMK to enable automated use. This MK
will be used to encrypt the private keys for the certificates created for database backups.58
DEMO: We create a master key:
use master
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'h6twqPNO'
go
--készíts biztonsági mentést az új MK-ról
OPEN MASTER KEY DECRYPTION BY PASSWORD = 'h6twqPNO'
go
--a biztonsági mentéshez másik jelszót használunk
BACKUP MASTER KEY TO FILE = 'C:\install\exportedmasterkey'
ENCRYPTION BY PASSWORD = 'h6twqPNOh6twqPNO'
go
--létrehozunk egy privát-nyilvános kulcspárt és egy önaláírt tanúsítványt
CREATE CERTIFICATE backup_cert_master
--ez az MK-val lesz titkosítva
WITH SUBJECT = 'NW DB backup',
EXPIRY_DATE = '20301031'
--érdemes biztonsági másolatot készíteni róla katasztrófa esetére
```

```
https://docs.microsoft.com/en-us/sql/relational-databases/backup-restore/backup-encryption?view=sqlserver-2017
```

```
BACKUP CERTIFICATE backup_cert_master TO FILE = 'C:\install\exportedcert'
--you can restore it by CREATE CERTIFICATE …
--mentést készítünk az adatbázisról
BACKUP DATABASE northwind TO DISK = 'C:\install\nw_enc.bak'
WITH COMPRESSION, ENCRYPTION (
ALGORITHM = AES_256,
SERVER CERTIFICATE = backup_cert_master
), STATS = 10
GO
```

Próbáld meg visszaállítani a titkosított biztonsági mentési készletet egy új adatbázisba a PRIM-en. A biztonsági másolat visszafejtésre kerül
automatikusan a backup_cert_master használatával. Ezután próbáld meg megtenni ugyanezt a SECOND-on. A tartalma
a biztonsági másolat olvashatatlan lesz.
GYAKORLAT: használd a főkulcsot a tesztadatbázis biztonsági mentéséhez. Próbáld meg visszaállítani a HARMADIK kiszolgálón.
Mindig titkosítva
A titkosítás/visszafejtés az ügyfélben történik, és a kulcsok a szerverpéldányon kívül kerülnek tárolásra
(akár helyileg a Windows tanúsítványtárolójában, akár az Azure Key Vaultban).
DEMO: az Alkalmazottak tábla Cím oszlopához hozzáadjuk az Always Encrypted elemet.

1. Válaszd az Északi szél -> Táblázatok -> Alkalmazottak -> Oszlopok titkosítása lehetőséget, és válaszd ki a Cím mezőt.

2. Válaszd a Véletlenszerű típust. Ez azt jelenti, hogy a csoportosítás, az egyenlőség szerinti szűrés és a táblák összekapcsolása be van kapcsolva
   titkosított oszlopok nem lesznek lehetségesek a szerveren, de egy ECB59 típusú támadás a
   oszlop meg van akadályozva

3. Válaszd ki az új oszlopkulcs létrehozását

4. Fogadd el, hogy a leválogatás binárisra változik

5. A következő ablaktáblában válaszd ki a Windows tanúsítványtárolót. Ez kívül esik az SQL szerver példányán
   így a sysadmin kiszolgálói szerepkörben lévő SQL-kiszolgáló rendszergazdája nem fog hozzáférni.

6. Ellenőrizd az új tanúsítványt a certmgr.msc mmc alkalmazásban:

7. SELECT * a táblaból az eredmény ellenőrzéséhez – ezt fogod látni a rendszergazda

8. Ha szeretnéd látni a visszafejtett eredményeket, nyiss meg egy új kapcsolatot, és a Beállításokban válaszd a lehetőséget
   További kapcsolati paraméterek, és írd be: „Oszloptitkosítási beállítás = Engedélyezve”.

9. Lekérdezés futtatásakor engedélyeznie kell a paraméterezést, hogy támogassa a beszúrásokat,
   a titkosított oszlopok frissítése vagy szűrése.
   GYAKORLAT: válaszd ki a Determinisztikus titkosítás típusát a Cím oszlopban, és ellenőrizd, hogy ugyanaz
   titkosított szöveg ugyanahhoz az egyszerű szöveghez jön létre, ami lehetővé teszi az EKB támadást.
   
   ```
   https://searchsecurity.techtarget.com/definition/Electronic-Code-Book
   ```
