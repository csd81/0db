-- Demonstrates an SQL example from the notes.
-- SNIPPET 0001
Order Details: a rendelés tételei
(UnitPrice*Quantity) 5%-kal csökkentendő.


-- Demonstrates converting field-oriented data to record-oriented form.
-- SNIPPET 0002
use [saját ab]
select * from northwind.dbo.Employees
--drop table employee_field
select employeeid, lastname, title, city into employee_field from northwind.dbo.Employees
select * from employee_field
create table attributes (
attrib_id int primary key,
attrib_name nvarchar(100),
attrib_type nvarchar(100))
go
insert attributes (attrib_id, attrib_name, attrib_type) values
(1, 'Last name', 'text'), (2, 'Title', 'text'), (3, 'City', 'text')
--drop table employee_record
create table employee_record (
emp_id int not null,
attrib_id int not null references attributes (attrib_id),
attrib_value nvarchar(500)
--a feladat az employee_field tartalmának reprodukálása az employee_record táblában
--egy rekordból több rekord lesz:
insert employee_record (emp_id, attrib_id, attrib_value)
select employeeid, 1, lastname from employee_field where lastname is not null
select employeeid, 2, title from employee_field where title is not null
select employeeid, 3, city from employee_field where city is not null
--ellenőrzés: Lamer NULL rekordjai ugye nincsenek benne
select * from employee_record
--a kliens GUI számára fontosak a mezőnevek, típusok is:
select e.emp_id, a.attrib_name, a.attrib_type, e.attrib_value
from employee_record e inner join attributes a on e.attrib_id=a.attrib_id
--most alakítsuk vissza: több rekordból lesz egy rekord
select emp_id as employeeid,
min(case --MIN helyén lehetne MAX is, mert csak egy rekordot dolgoz fel
when attrib_id=1 then attrib_value
else null
end) as lastname,
min(case
when attrib_id=2 then attrib_value
else null


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0003
end)
min(case


-- Demonstrates converting field-oriented data to record-oriented form.
-- SNIPPET 0004
when attrib_id=3 then attrib_value
else null
end) as city
from employee_record group by emp_id
--megkaptuk az employee_field tartalmát


-- Demonstrates crosstab aggregation on fruit-harvest data.
-- SNIPPET 0005
drop table csapat
CREATE TABLE [dbo].[csapat] (
[csapat_id] [int] NOT NULL primary key,
[csapat_nev] [nvarchar] (50) NOT NULL
drop table gyumolcs
CREATE TABLE [dbo].[gyumolcs] (
[gyumolcs_id] [int] NOT NULL primary key,
[gyumolcs_nev] [nvarchar] (50) NOT NULL
drop table nap
CREATE TABLE [dbo].[nap] (
[nap_id] [int] NOT NULL primary key,
[nap_nev] [nvarchar] (50) NOT NULL
go
drop table eredm
CREATE TABLE [dbo].[eredm] (
eredm_id int identity (1,1) primary key,
[csapat_id] [int] NOT NULL references csapat (csapat_id),
[nap_id] [int] NOT NULL references nap (nap_id),
gyumolcs_id int not null references gyumolcs (gyumolcs_id),
[leadott_lada] [int] NOT NULL
insert csapat (csapat_id, csapat_nev) values (1, 'Szorgos'),(2, 'Lusta')
insert gyumolcs (gyumolcs_id, gyumolcs_nev) values (1, 'alma'),(2, 'szilva')
insert nap (nap_id, nap_nev) values (1, 'hétfő'),(2, 'kedd'),(3, 'szerda')
insert eredm (csapat_id, nap_id, gyumolcs_id, leadott_lada) values
(1,1,1,50), (1,2,1,60), (1,3,1,70), (1,1,2,100), (1,2,2,120), (1,3,2,140),
(2,1,1,5), (2,2,1,6), (2,3,1,7), (2,1,2,10), (2,2,2,12), (2,3,2,14)
select * from eredm
--NÉHÁNY PÉLDA CSOPORTOSÍTÓ LEKÉRDEZÉSEKRE
--kérdés pl. a csapatok teljesítménye naponta
select cs.csapat_nev, n.nap_nev, sum(leadott_lada) as teljesítmény
from eredm e inner join csapat cs on cs.csapat_id=e.csapat_id
inner join nap n on n.nap_id=e.nap_id
inner join gyumolcs gy on gy.gyumolcs_id=e.gyumolcs_id --elhagyható
group by cs.csapat_id, cs.csapat_nev, n.nap_id, n.nap_nev
order by cs.csapat_nev, n.nap_nev
--csapatok teljesítménye gyümölcsönként
select cs.csapat_nev, gy.gyumolcs_nev, sum(leadott_lada) as teljesítmény
from eredm e inner join csapat cs on cs.csapat_id=e.csapat_id
inner join nap n on n.nap_id=e.nap_id --elhagyható


-- Demonstrates PIVOT-based crosstab queries.
-- SNIPPET 0006
inner join gyumolcs gy on gy.gyumolcs_id=e.gyumolcs_id
group by cs.csapat_id, cs.csapat_nev, gy.gyumolcs_id, gy.gyumolcs_nev
order by cs.csapat_nev, gy.gyumolcs_nev
--ládaszám gyümölcsönként
select gy.gyumolcs_nev, sum(leadott_lada) as teljesítmény
from eredm e
inner join csapat cs on cs.csapat_id=e.csapat_id --elhagyható
inner join nap n on n.nap_id=e.nap_id --elhagyható
inner join gyumolcs gy on gy.gyumolcs_id=e.gyumolcs_id
group by gy.gyumolcs_id, gy.gyumolcs_nev
order by gy.gyumolcs_nev
--Az egyszerűség kedvéért legyen egyetlen szöveges kiinduló táblánk:
drop table eredm_pivot
select cs.csapat_nev, n.nap_nev, gy.gyumolcs_nev, e.leadott_lada
into eredm_pivot
from eredm e
inner join csapat cs on cs.csapat_id=e.csapat_id
inner join nap n on n.nap_id=e.nap_id
inner join gyumolcs gy on gy.gyumolcs_id=e.gyumolcs_id
go


-- Demonstrates PIVOT-based crosstab queries.
-- SNIPPET 0007
select csapat_nev, nap_nev, pt.alma, pt.szilva
from eredm_pivot
pivot (sum(leadott_lada) for gyumolcs_nev in (alma, szilva)) as pt
--a SUM azért kell, mert lehetnének egyező sorok
order by csapat_nev, nap_nev
/*
select * from eredm_pivot where csapat_nev='lusta'
--most összesítünk: a napok nem érdekesek
--csapatok teljesítménye gyümölcsönként: sorokban a csapatok, oszlopokban a gyümölcsök
select pt.csapat_nev, pt.alma, pt.szilva
from (select csapat_nev, gyumolcs_nev, sum(leadott_lada) as leadott_lada


-- Demonstrates PIVOT-based crosstab queries.
-- SNIPPET 0008
from eredm_pivot group by csapat_nev, gyumolcs_nev) as forras --az alias
pivot (sum(leadott_lada) for gyumolcs_nev in ([alma], [szilva])) as pt
--sorokban a gyümölcsök, oszlopokban a csapatok
select gyumolcs_nev, pt.Lusta, pt.Szorgos
from (select csapat_nev, gyumolcs_nev, sum(leadott_lada) as leadott_lada
from eredm_pivot group by csapat_nev, gyumolcs_nev) as forras
pivot (sum(leadott_lada) for csapat_nev in ([Lusta], [Szorgos])) as pt
--mi lenne, ha kihagynánk a keddet? -> a belső lekérdezés változik
select gyumolcs_nev, pt.Lusta, pt.Szorgos
from (select csapat_nev, gyumolcs_nev, sum(leadott_lada) as leadott_lada
from eredm_pivot
group by csapat_nev, gyumolcs_nev) as forras
pivot (sum(leadott_lada) for csapat_nev in ([Lusta], [Szorgos])) as pt
/*
*/
--a sorokban lehet több szintű bontás is: sorokban a csapatok és napok, oszlopokban a
select csapat_nev, nap_nev, pt.alma, pt.szilva
from (select csapat_nev, nap_nev, gyumolcs_nev, sum(leadott_lada) as leadott_lada
from eredm_pivot group by csapat_nev, nap_nev, gyumolcs_nev) as forras -ehhez már nem is kellett volna belső lekérdezés
pivot (sum(leadott_lada) for gyumolcs_nev in ([alma], [szilva])) as pt
order by csapat_nev, nap_nev


-- Demonstrates cross-tab conversion with PIVOT and UNPIVOT.
-- SNIPPET 0009
--induljunk ki egy pivotált táblából:
select csapat_nev, pt.alma, pt.szilva
into #temp
from (select csapat_nev, gyumolcs_nev, sum(leadott_lada) as leadott_lada
from eredm_pivot group by csapat_nev, gyumolcs_nev) as forras
pivot (sum(leadott_lada) for gyumolcs_nev in ([alma], [szilva])) as pt
select * from #temp
--és tegyük vissza gyümölcsöket a sorokba:
select * from #temp
select csapat_nev, gyumolcs_nev, leadott_lada
from #temp
unpivot (leadott_lada for gyumolcs_nev in (alma, szilva)) as upt
--persze a csoportosítást már nem tudjuk visszacsinálni, ott információ veszett el


-- Demonstrates cross-tab conversion with PIVOT and UNPIVOT.
-- SNIPPET 0010
--ha nem volt csoportosítás, akkor a tábla teljesen visszaalakítható:
drop table #temp
go
select csapat_nev, nap_nev, pt.alma, pt.szilva
into #temp
from eredm_pivot
pivot (sum(leadott_lada) for gyumolcs_nev in ([alma], [szilva])) as pt
order by csapat_nev, nap_nev
select csapat_nev, nap_nev, gyumolcs_nev, leadott_lada
from #temp
unpivot (leadott_lada for gyumolcs_nev in (alma, szilva)) as upt
order by csapat_nev, nap_nev, gyumolcs_nev


-- Demonstrates converting record-oriented data back to field-oriented form with PIVOT.
-- SNIPPET 0011
--a dolgozós rekordorientált modell visszaírása mezőorientáltra PIVOT segítségével
--Mi a mezőnév-készlet?
select distinct a.attrib_name
from employee_record e inner join attributes a on e.attrib_id=a.attrib_id
--eredmény:
--ezzel a megoldás:
select emp_id, pt.[City], pt.[Last name], pt.[Title]
from (
select e.emp_id, a.attrib_name, e.attrib_value
from employee_record e inner join attributes a on e.attrib_id=a.attrib_id) as forras
pivot (max(attrib_value) for attrib_name in ([City],[Last name],[Title])) as pt
--max helyett lehetne min is


-- Demonstrates batch handling and error behavior with GO.
-- SNIPPET 0012
--drop table pelda
create table pelda (szam int)
insert pelda values (44)
go
--1. kísérlet
update pelda set szam=21
go
go
select * from pelda --eredmeny 21, mert az első batch sikerult
go
--2. kísérlet: ugyanez egy kötegben
update pelda set szam=22
update pelda set szam=23
go
select * from pelda --eredmény: 21
--mert szintaktikai hiba esetén az egész batchból semmi sem hajtódik végre
--3. kísérlet
--ha az objektumnév hibás (nem szintaktikai hiba), akkor a hiba előtti rész végrehajtódik
go
update pelda set szam=22
select * from plda --Invalid object name
update pelda set szam=23 --ez már nem hajtódik végre
go
select * from pelda --eredmény: 22
go
--4. kísérlet: speciális hibák (nullával osztás, külső kulcs kényszer)
update pelda set szam=23
select 1/0 --division by zero


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0013
update pelda set szam=24 --végrehajtódik
go
select * from pelda --eredmény: 24
go
update pelda set szam=25
delete employees --The DELETE statement conflicted with the REFERENCE constraint
update pelda set szam=26 --végrehajtódik
go
select * from pelda --eredmény: 26


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0014
GOTO <címke>


-- Demonstrates variables and a simple WHILE loop.
-- SNIPPET 0015
declare @i int, @eredm int
set @i = 1
--ehelyett működne ez is: declare @i int = 1, @eredm int = 0
set @eredm=0
--azonos eredményt ad: select @eredm=0
while @i < 50 begin
set @eredm = @eredm + @i
set @i = @i + 1
end
print 'az 50-nél kisebb számok összege: '+cast(@eredm as varchar(15))
go
--print @eredm --Must declare the scalar variable "@eredm".
--a változó csak a kötegen belül látható


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0016
use northwind
--select * from Employees
declare @name nvarchar(20), @address nvarchar(max)
set @name='Fuller%'
select @address=Country+', '+City+' '+Address
from Employees where LastName like @name


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0017
if @address is not null print 'A talált cím: ' + @address
/*megjegyzés: az utolsó sor működik. de jobban olvasható így:
if (@address is not null) begin
print 'A talált cím:' + @address
end
*/
go


-- Demonstrates counting matches before using a variable assignment.
-- SNIPPET 0018
declare @name nvarchar(20), @address nvarchar(max), @res_no int
set @name='Kinkg%'
select @res_no=count(*) from Employees where LastName like @name
--Figyelem, ebben az esetben üres recordsetre a @res_no értéke nem NULL, hanem 0 lesz!
if @res_no=0 print 'Nincs találat.'
else if @res_no>1 print 'Több, mint 1 találat.'
else begin
select @address=Country+', '+City+' '+Address from Employees where LastName like @name
print 'A talált cím: ' + @address
end
go
--megjegyzés: mivel csak 1 rekordot várunk, a 2. select megúszható lett volna így:
declare @name nvarchar(20), @address nvarchar(max), @res_no int
set @name='Buchanan%'
select @res_no=count(*), @address=max(Country+', '+City+' '+Address)
from Employees where LastName like @name
if @res_no=0 print 'Nincs találat.'
else if @res_no>1 print 'Több, mint 1 találat.'


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0019
select @i=count(*) from Products where 1=0 group by ProductID --@i értéke NULL marad


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0020
else print 'A talált cím: ' + @address
go


-- Demonstrates concatenating values into a single list.
-- SNIPPET 0021
declare @nev_lista nvarchar(max) = ''
select @nev_lista = @nev_lista + ', '+ LastName from Employees order by Lastname
select 'A nevek listája: ' + right(@nev_lista, len(@nev_lista)-1) lista
--SQL Server 2017-ben vagy afelett így is megoldható:
select string_agg(lastname, ', ') within group (order by Lastname) lista from Employees


-- Demonstrates that variable assignment cannot be mixed with row output.
-- SNIPPET 0022
declare @lastname nvarchar(20), @emp_id int = 1
select @lastname = LastName, Address from Employees where EmployeeID = @emp_id
print @lastname
"Msg 141, Level 15, State 1, Line 108


-- Demonstrates counting matches before using a variable assignment.
-- SNIPPET 0023
set nocount on
declare @name nvarchar(20), @address nvarchar(max), @res_no int, @emp_id int
set @name='Fuller%'
select @res_no=count(*) from Employees where LastName like @name
if @res_no=0 print 'Nincs találat.'
else if @res_no>1 print 'Több, mint 1 találat.'
else begin --épp egy találat
select @address=Country+', '+City+' '+Address, @emp_id=EmployeeID
from Employees where LastName like @name
print 'Dolgozó ID: ' + cast(@emp_id as varchar(10)) + ', cím: ' + @address
update Employees set salary=1.1*salary where EmployeeID=@emp_id
print 'Fizetés növelve.'
end
go


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0024
update Products set UnitsInStock=-1 where ProductID=3 --check constraint sértés


-- Demonstrates error checking with @@ERROR.
-- SNIPPET 0025
go
select 1/0
if @@ERROR=8134 print '0-val osztottunk'
go


-- Demonstrates TRY/CATCH error handling and logging.
-- SNIPPET 0026
create table #log(time_stamp datetime, err_num int)
go
begin try
update Products set UnitsInStock=-13 where ProductID=3 --check constraint sértés
select 1/0
end try
begin catch
insert #log (time_stamp, err_num) values (getdate(), ERROR_NUMBER())
end catch
select * from #log
go


-- Demonstrates updating stock based on order lines.
-- SNIPPET 0027
select * from [Order Details] where OrderID=10248 --11: 42, 42: 40, 72:40
select ProductID, UnitsInStock from Products where ProductID in (11, 42, 72) --82, 20, 20
--az utolsó 2 tétel miatt az alábbi update hibára fut (nem lehet negatív raktárkészlet)
go
declare @order_id int = 10248
update Products set UnitsInStock=UnitsInStock-od.Quantity
from [Order Details] od inner join Products p on p.ProductID=od.ProductID
print cast(@order_id as varchar(20))+' számú rendelés a raktárba átvezetve.'--hibás


-- Demonstrates updating stock based on order lines.
-- SNIPPET 0028
--a szükséges táblák: products, customers, orders, order details
--ezekről készítsünk másolatot a saját adatbázisunkba!
--változók
declare @prod_name varchar(20), @quantity int, @cust_id nchar(5)
--a telefonból (a vevő-ID szöveges)
declare @status_message nvarchar(100), @status int --a folyamat visszatérési értékei
declare @res_no int --találatok száma
declare @prod_id int, @order_id int --azonosítók
declare @stock int --raktárkészlet
declare @cust_balance money --a vevő egyenlege
declare @unitprice money --a termék egységára
-- paraméterek
set @prod_name = 'boston'
set @quantity = 10
set @cust_id = 'AROUT'
begin try
select @res_no = count(*) from products where productname like '%' + @prod_name + '%'
if @res_no <> 1 begin
set @status = 1
set @status_message = 'HIBA: a terméknév nem egyértelmű.';
end else begin
-- ha egy terméket találunk, megkeressük a kulcsot és a raktárkészletet
select @prod_id = productID, @stock = unitsInStock from products where
productName like '%' + @prod_name + '%'
-- van-e raktáron? a rendelt mennyiség elérheto-e?
if @stock < @quantity begin
set @status = 2
set @status_message = 'HIBA: a raktárkészlet nem fedezi a megrendelést.'
end else begin
-- mennyibe kerül? Van elég pénze a vevönek?
select @cust_balance = balance from customers where customerid =
@cust_id
--ha nem találjuk a vásárlót, akkor az egyenleg null
--mivel kulcsra keresünk, max. 1 találat lehet
select @unitprice = unitPrice from products where productID = @prod_id
--nincs discount
if @cust_balance < @quantity*@unitprice or @cust_balance is null begin
set @status = 3
set @status_message = 'HIBA: a vásárló nem található vagy az
end else begin
-- Ellenőrzések vége, elkezdjük a tranzakciót (2 lépés)
-- 1. vásárló egyenlegének frissítése
update customers set balance = balance-(@quantity*@unitprice) where
-- 2. új bejegyzés az Orders, Order Details táblákba
insert into orders (customerID, orderdate) values (@cust_id,
getdate()) --orderid: identity
set @order_id = @@identity --az utolsó identity insert eredménye


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0029
insert [order details] (orderid, productid, quantity, UnitPrice)
--itt a hiba
--itt a hiba
insert [order details] (orderid, productid, quantity, UnitPrice,


-- Demonstrates updating stock based on order lines.
-- SNIPPET 0030
set @status = 0
set @status_message = cast(@order_id as varchar(20)) + ' sz.
end
end
end
print @status
print @status_message
end try
begin catch
print 'EGYÉB HIBA: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20)) +
end catch
go
--teszteléshez beállítjuk a paramétereket
set nocount off
update products set unitsInStock = 900 where productid=40
update customers set balance=1000 where CustomerID='AROUT'
delete [Order Details] where OrderID in (select orderid from Orders where CustomerID='AROUT'
and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
--most futtatjuk a scriptet, utána ellenőrzés:
select * from Customers where CustomerID='AROUT'
select * from Products where productid=40
select top 3 * from Orders where CustomerID='arout' order by OrderDate desc
--Tehát elvileg minden rendben. Azonban a discount mező NOT NULL kényszere miatt a futtatás
--"EGYÉB HIBA: Cannot insert the value NULL into column 'Discount'"
--DE! a vásárló egyenlegét azért sikerült csökkenteni!
--további hibalehetőség: ha egyszerre több konkurens kérés érkezik, akkor
--érdekes hibák léphetnek fel.
--javítás után teszteljük a másik két ágat is!


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0031
set @termeknev = 'Raclette'
set @mennyiseg = 12
set @szallito = 'Formago Company'


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0032
if ($stmt = mysqli_prepare($mysqllink, "SELECT title, isbn FROM books WHERE title LIKE ?")) {


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0033
if (mysqli_stmt_num_rows($stmt) == 0) { echo "Nincs találat! <br>";
while (mysqli_stmt_fetch($stmt)) {


-- Demonstrates a forward-only cursor over employees.
-- SNIPPET 0034
go
declare @emp_id int, @emp_name nvarchar(50), @i int, @address nvarchar(60)
declare cursor_emp cursor fast_forward for
select employeeid, lastname, address from employees order by lastname
set @i=1
open cursor_emp
fetch next from cursor_emp into @emp_id, @emp_name, @address
while @@fetch_status = 0
print cast(@i as varchar(5)) + '. ügynök:'
print concat('ID: ', @emp_id, ', Név: ', @emp_name, ', cím: ', @address)
set @i=@i+1
fetch next from cursor_emp into @emp_id, @emp_name, @address
end
close cursor_emp
deallocate cursor_emp
go
--ez egyenértékű egy ilyen SELECT utasítással:
select 'ID: ' + cast(employeeid as varchar(5)) + isnull(', Név: ' + lastname, '') + isnull( ',
from employees order by lastname
--illetve ha az ügynök sorszámát is szeretnénk:
select cast(row_number() over(order by lastname) as varchar(50))+
from employees


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0035
--példa dinamikus, mozgatható kurzorra
go
declare c cursor global dynamic scroll for select LastName from Employees
print @@cursor_rows --eredm: 0, nincs nyitott kurzor
open c
print @@cursor_rows --eredm: -1, mivel dinamikus, nem megállapítható a sorok száma
--de ha volna egy order by LastName a forráson, a rendezéshez létrehozná a táblát,
--és a cursor_rows is 10 értéket adna vissza
declare @name varchar(50)
fetch last from c into @name --fetch absolute nem lehet dinamikus kurzoron
print @name --Lamer
close c
deallocate c
--példa statikus kurzorra
go
declare c cursor global static scroll for select LastName from Employees
open c
print @@cursor_rows --10
declare @name varchar(50)
fetch absolute 2 from c into @name
print @name --Fuller (rendezés nélkül)
close c
deallocate c


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0036
jön létre, de a default kurzortípus magától a lekérdezéstől is függ, ezért célszerű mindig meghatározni a
declare @emp_id int, @emp_name nvarchar(50), @i int, @address nvarchar(60),
@city nvarchar(50)
create table #eredm (adatid int, dolg_id int,


-- Demonstrates a forward-only cursor over employees.
-- SNIPPET 0037
adatnev varchar(50), adatertek nvarchar(100))
declare cursor1 cursor fast_forward
select employeeid as emp_id, firstname+' '+lastname as emp_name,address, city
from employees
set @i=0
open cursor1
fetch next from cursor1 into @emp_id, @emp_name, @address, @city
while @@fetch_status = 0
--print @emp_id print @emp_name print @i
if @emp_name is not null begin
insert #eredm values(@i, @emp_id, 'dolgozo_neve', @emp_name)
set @i=@i+1
end
if @address is not null begin
insert #eredm values(@i, @emp_id, 'dolgozo_cime', @address)
set @i=@i+1
end
if @city is not null begin
insert #eredm values(@i, @emp_id, 'dolgozo_varosa', @city)
set @i=@i+1
end
fetch next from cursor1 into @emp_id, @emp_name, @address, @city
--print @emp_id
end
close cursor1
deallocate cursor1
print @i
print 'feldolgozás vége'
select * from #eredm
drop table #eredm
GO


-- Demonstrates analytic/window functions.
-- SNIPPET 0038
FIRST_VALUE, LAST_VALUE(kifejezés) OVER…: a rendezett lista/partíció első/utolsó rekordjából


-- Demonstrates analytic/window functions.
-- SNIPPET 0039
ROW_NUMBER() OVER…: a rendezett lista/partíció minden rekordjához egy futó sorszámot ad


-- Demonstrates analytic/window functions.
-- SNIPPET 0040
LAG(kifejezés, [offset], [default]) OVER…: a rendezett lista/partíció aktuális rekordja előtti offset


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0041
go
drop table #tmp --az átláthatóság érdekében használjunk egy ideiglenes táblát
go
select orderdate, cast(sum((1-discount)*unitprice*quantity) as money) as value
into #tmp from orders o inner join [order details] d on o.orderid=d.orderid


-- Demonstrates analytic/window functions.
-- SNIPPET 0042
group by o.orderid, o.orderdate --96
order by OrderDate
go
select * from #tmp order by OrderDate
select orderdate, max(value) over
(order by orderdate rows between 1 preceding and current row) as maxi-- maxi: a
from #tmp
--ahol ebben a listában 200 alatti érték van, ott 2 kicsi jött egymás után:
select a.OrderDate, a.maxi
from (
select orderdate, max(value) over
(order by orderdate rows between 1 preceding and current row) as maxi
from #tmp
) as a where a.maxi < 200 --3 db
--MEGJEGYZÉS:
--vigyáznunk kell, mert a lista elején tévesen emelnénk ki a rekordot, ha már az első is
--helyesebben:
select a.OrderDate, a.maxi
from (
select orderdate,
max(value) over
(order by orderdate rows between 1 preceding and current row) as maxi,
row_number() over
(order by orderdate) as sorsz
from #tmp
) as a where a.maxi < 200 and sorsz > 1


-- Demonstrates analytic/window functions.
-- SNIPPET 0043
select year(orderdate) ev,
row_number() over (
order by orderdate) sorszam, --éven belüli futó sorszám
cast(orderdate as date) datum,
sum(value) over (
order by orderdate
avg(value) over (
order by orderdate
sum(value) over (
from #tmp


-- Demonstrates analytic/window functions.
-- SNIPPET 0044
--melyik évben melyik volt a legkisebb/legnagyobb értékű rendelés (al-lekérdezés nélkül,
drop table #tmp2
go
select o.*, v.value
into #tmp2 --rendelések értékei a value mezőben
from orders o inner join
(select orderid, cast(sum((1-discount)*unitprice*quantity) as money) as value
from [order details] group by orderid ) as v
select distinct year(orderdate), --a distinct miatt évente 1 rekord lesz
first_value(orderdate) over (partition by year(orderdate) order by value asc) as
first_value(orderid) over (partition by year(orderdate) order by value asc) as
first_value(value) over (partition by year(orderdate) order by value asc) as
first_value(orderdate) over (partition by year(orderdate) order by value desc) as
first_value(orderid) over (partition by year(orderdate) order by value desc) as
first_value(value) over (partition by year(orderdate) order by value desc) as
from #tmp2


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0045
create table t1 (id int primary key)
create table t2 (id int primary key, t1_id int references t1(id))
go
insert t1 (id) values (1), (3), (4), (5)
insert t2 (id, t1_id) values (10, 3) --a (3) rkord nem törölhető
go
delete t1 --implicit tr.
--"The DELETE statement conflicted with the REFERENCE constraint ..." etc
select * from t1 –minden rekord megvan


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0046
ROLLBACK utasítással ér véget. A COMMIT felszabadítja a tranzakció által lefoglalt erőforrásokat, mint
utasítása hibára fut. A default beállítás, OFF esetén folytatódik a végrehajtás. ON esetén a rendszer
set xact_abort off
delete t2
go
begin tran
insert t2 (id, t1_id) values (10, 1)
insert t2 (id, t1_id) values (11, 2) –külső kulcs hiba
insert t2 (id, t1_id) values (12, 3)
commit tran
go
--"The INSERT statement conflicted with the FOREIGN KEY constraint ..." etc
select * from t2
--az atomicitás sérült
set xact_abort on
delete t2
go
begin tran
insert t2 (id, t1_id) values (10, 1)
insert t2 (id, t1_id) values (11, 2) –külső kulcs hiba
insert t2 (id, t1_id) values (12, 3)
commit tran
go
--"The INSERT statement conflicted with the FOREIGN KEY constraint ..." etc
select * from t2
-- az atomicitás nem sérült


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0047
--rendelés-felvétel tranzakció-kezeléssel
declare @prod_name varchar(20), @quantity int, @cust_id nchar(5) --a telefonból (a vevő-ID
declare @status_message nvarchar(100), @status int --a folyamat visszatérési értéke
declare @res_no int --találatok száma
declare @prod_id int, @order_id int --azonosítók
declare @stock int --raktárkészlet
declare @cust_balance money --a vevő egyenlege
declare @unitprice money --a termék egységára
-- paraméterek


-- Demonstrates updating stock based on order lines.
-- SNIPPET 0048
set @prod_name = 'boston'
set @quantity = 10
set @cust_id = 'AROUT'
begin tran
begin try
select @res_no = count(*) from products where productname like '%' + @prod_name + '%'
if @res_no <> 1 begin
set @status = 1
set @status_message = 'HIBA: a terméknév nem egyértelmű.';
end else begin
-- ha egy terméket találunk, megkeressük a kulcsot és a raktárkészletet
select @prod_id = productID, @stock = unitsInStock from products where
productName like '%' + @prod_name + '%'
-- van-e raktáron? a rendelt mennyiség elérheto-e?
if @stock < @quantity begin
set @status = 2
set @status_message = 'HIBA: a raktárkészlet nem fedezi a megrendelést.'
end else begin
-- mennyibe kerül? Van elég pénze a vevönek?
select @cust_balance = balance from customers where customerid =
@cust_id
--ha nem találjuk a vásárlót, akkor az egyenleg
--mivel kulcsra keresünk, max. 1 találat lehet
select @unitprice = unitPrice from products where productID = @prod_id -nincs discount
if @cust_balance < @quantity*@unitprice or @cust_balance is null begin
set @status = 3
set @status_message = 'HIBA: a vásárló nem található, vagy az
end else begin
-- Ellenőrzések vége, elkezdjük a tranzakciót (2 lépés)
-- 1. vásárló egyenlegének frissítése
update customers set balance = balance-(@quantity*@unitprice)
-- 2. új bejegyzés az Orders, Order Details táblákba
insert into orders (customerID, orderdate) values (@cust_id,
getdate()) --orderid: identity
set @order_id = @@identity --az utolsó identity insert eredménye
insert [order details] (orderid, productid, quantity, UnitPrice)
--itt a hiba
--itt a hiba
--ez a jó
-values(@order_id, @prod_id, @quantity, @unitprice, 0)
--ez a jó
set @status = 0
set @status_message = cast(@order_id as varchar(20)) + ' sz.
end
end
end
print 'Állapot: ' + cast(@status as varchar(50))
print @status_message
if @status = 0 commit tran else begin
print 'Visszagörgetve'
rollback tran
end
end try
begin catch


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0049
print 'EGYÉB HIBA: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20)) +
rollback tran
end catch
go


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0050
--teszteléshez beállítjuk a paramétereket
set nocount off
update customers set balance=1000 where CustomerID='AROUT'
delete [Order Details] where OrderID in (select orderid from Orders where CustomerID='AROUT'
and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
--most futtatjuk a scriptet, utána ellenőrzés:
select * from Customers where CustomerID='AROUT'
select top 3 * from Orders where CustomerID='arout' order by OrderDate desc
--a programozási hiba előtti update és insert utasítás visszagördült


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0051
@@TRANCOUNT globális változóval támogatja.
begin tran
print @@trancount --1
begin tran
print @@trancount
commit tran
print @@trancount --1
commit tran
print @@trancount --0
go
begin tran
print @@trancount --1
begin tran
print @@trancount
rollback tran
print @@trancount --0


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0052
Update (U): ideiglenes zár, melyet az adatmódosításra készülő tranzakció a szűrőfeltétel


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0053
set transaction isolation level read committed --vagy bármelyik másik
begin tran
update Employees set Salary = 1000 where EmployeeID = 1
select @@SPID --63 (session ID)
select resource_type, request_mode, request_type,
from sys.dm_tran_locks where request_session_id=63 --63 helyett a saját session ID-nk


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0054
select * from Employees where EmployeeID = 2 --lefut, mert az ID-re van index
select * from Employees where FirstName = 'Andrew' --várakozik, mert minden rekordot meg kell


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0055
--ebben az editor ablakban:
set transaction isolation level serializable --tehát az S zár marad
begin tran
select * from Employees where FirstName = 'Andrew' --range S zár marad
select distinct resource_type, request_mode, request_type,
from sys.dm_tran_locks where request_session_id=@@SPID --S lock a táblára: GRANT
--másik editorban kérdezzük le a @@SPID-t, legyen most ez 51
--utána a másik editorban futtassuk ezt:
set transaction isolation level serializable --S zár marad
begin tran
update Employees set Salary = 1000 where EmployeeID = 1
--várakozik
--ebben az editorban ellenőrizzük a másik, várakozó tr. zárjait:
select distinct resource_type, request_mode, request_type,
from sys.dm_tran_locks where request_session_id=51
--megjelenik a KEY X típusú WAIT állapotú zár
--ezek után egy harmadik editor ablakban:


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0056
set transaction isolation level serializable --S zár marad
begin tran
select * from Employees where EmployeeID = 1
--szintén várakozik, mert az X zár mellett az S zárat nem tudja megkapni
--így kerülhető el az adatmódosító tr. kiéheztetése: Ha az 1. tr. lefut, utána
--a 2. megkapja majd az X zárat, aztán jöhet a 3. tr. olvasása:
--ebben az ablakban:
commit tran
--erre a 2. ablakban lefut az update, de a 3. tr. még mindig várakozik
--ekkor a 2. ablakban:
commit tran
--erre az 1. ablakban is lefut a select
--tehát a később jött select-nek meg kellett várnia az update végét
--ne feledjük a 3. ablakban is:
commit tran


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0057
create table test_product(id int primary key, prod_name varchar(50) not null, sold
varchar(50), buyer varchar(50))
insert test_product(id, prod_name, sold) values (1, 'car', 'for sale')
insert test_product(id, prod_name, sold) values (2, 'horse', 'for sale')
go
select * from test_product
update test_product set sold='for sale', buyer=null where id=2
go
set tran isolation level read committed -- default
go
begin tran
declare @sold varchar(50)
select @sold=sold from test_product where id=2
if @sold='for sale' begin
waitfor delay '00:00:10' –terheljük a bankszámlát
update test_product set sold='sold', buyer='My name' where id=2
print 'sold successfully'
end else print 'product not available'
commit tran
go
--a fenti tranzakciót párhuzamosan két editorban futtatjuk
--a másik script:
set tran isolation level read committed
go
begin tran
declare @sold varchar(50)
select @sold=sold from test_product where id=2
if @sold='for sale' begin
waitfor delay '00:00:10'
update test_product set sold='sold', buyer='Your name' where id=2 –ez a 2. vásárló
print 'sold successfully'
end else print 'product not available'
commit tran
go
--ez történik:


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0058
select * from test_product


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0059
use test
set tran isolation level repeatable read
go
begin tran
declare @sold varchar(50)
select @sold=sold from test_product where id=2
if @sold='for sale' begin
waitfor delay '00:00:10' --terheljük a bankszámlát
update test_product set sold='sold', buyer='...' where id=2
print 'sold successfully'
end else print 'product not available'
commit tran
go


-- Demonstrates counting matches before using a variable assignment.
-- SNIPPET 0060
go
create procedure sp_inc_salary @name nvarchar(20) as
begin try
set nocount on
declare @address nvarchar(max), @res_no int, @emp_id int
select @res_no=count(*) from Employees where LastName like @name
if @res_no=0 print 'Nincs találat.'
else if @res_no>1 print 'Több, mint 1 találat.'
else begin --épp egy találat
select @address=Country+', '+City+' '+Address, @emp_id=EmployeeID
from Employees where LastName like @name
print 'Dolgozó ID: ' + cast(@emp_id as varchar(10)) + ', cím: ' + @address
update Employees set salary=1.1*salary where EmployeeID=@emp_id
print 'Egyenleg növelve.'
end
end try
begin catch
print 'EGYÉB HIBA: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20)) +
end catch
go
--teszt
execute sp_inc_salary 'Fuller'


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0061
SELECT eredmény-rekordhalmazát. Egy eljárásnak több visszaadott rekordhalmaza is lehet. Ez a
kényelem SQL Server specifikus, más rendszereken kurzor típusú OUTPUT paramétert kell


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0062
drop proc p
go
create proc p as print 'sikeres futás'
go
declare @eredm int
exec @eredm=p
print @eredm --0
drop proc p
go
create proc p as
print 'sikeres futás'
return 1
go
declare @eredm int
exec @eredm=p
print @eredm --1
drop proc p
go
create proc p as select 1/0
go
declare @eredm int
exec @eredm=p
print @eredm --


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0063
drop procedure sp_raktárkészlet_aktualizalo
go
create procedure sp_raktárkészlet_aktualizalo
@orderid int, --a rendelés azonosítója
@result varchar(50) output --visszajelzés
begin try
update products set unitsInStock = unitsInStock - od.quantity
from products p inner join [Order Details] od on od.ProductID=p.ProductID
set @result='OK'
end try
begin catch --hiba akkor lehet, ha valamelyik tétel negatívba vinné a készletet
print ' Készletezési hiba: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as
set @result='HIBA'
end catch
go


-- Demonstrates updating stock based on order lines.
-- SNIPPET 0064
--teszt
insert orders (OrderDate) values (getdate())
select @@identity --12105
select * from Products where ProductID=9 --unitsinstock =29
select * from Products where ProductID=10 --unitsinstock =31
insert [Order Details] (orderid, productid, quantity, UnitPrice, Discount)
values (12105, 9, 10, 30, 0),(12105, 10, 40, 30, 0)
--tehát a második tétel hibát ad az sp_raktárkészlet_aktualizalo hívásakor:
go
declare @eredm varchar(50)
exec sp_raktárkészlet_aktualizalo 12105, @eredm output
print @eredm
go
--helyreállítás
delete [Order Details] where OrderID=12105
delete Orders where OrderID=12105
update Products set UnitsInStock=29 where ProductID=9
update Products set UnitsInStock=31 where ProductID=10
select * from Products
--a rendelés-felvételi tranzakció tárolt eljárásban
--a raktárkészlet ellenőrzését most a fenti eljárásra bízzuk
create procedure uj_rendeles
@prod_name varchar(20),
@quantity int,
@cust_id nchar(5) --a három bemeneti paraméter
declare @status_message nvarchar(100), @status int --a folyamat visszatérési értéke
declare @res_no int --találatok száma
declare @prod_id int, @order_id int --azonosítók
declare @stock int --raktárkészlet
declare @cust_balance money --a vevő egyenlege
declare @unitprice money --a termék egységára
-- paraméterek
begin tran
begin try
select @res_no = count(*) from products where productname like '%' + @prod_name + '%'
if @res_no <> 1 begin
set @status = 1
set @status_message = 'HIBA: a terméknév nem egyértelmű.'
end else begin
-- ha egy terméket találunk, megkeressük a kulcsot
select @prod_id = productID from products where productName like '%' +
@prod_name + '%'
--INNEN KIVETTÜK A RAKTÁR ELLENŐRZÉSÉT
-- mennyibe kerül? Van elég pénze a vevönek?
select @cust_balance = balance from customers where customerid = @cust_id
--ha nem találjuk a vásárlót, akkor az egyenleg null
--mivel kulcsra keresünk, max. 1 találat lehet
select @unitprice = unitPrice from products where productID = @prod_id --nincs
if @cust_balance < @quantity*@unitprice or @cust_balance is null begin
set @status = 2
set @status_message = 'HIBA: a vásárló nem található vagy az egyenlege
end else begin
-- Ellenőrzések vége, elkezdjük a tranzakciót (3 lépés)
-- 1. vásárló egyenlegének frissítése
update customers set balance = balance-(@quantity*@unitprice) where


-- Demonstrates updating stock based on order lines.
-- SNIPPET 0065
-- 2. új bejegyzés az Orders, Order Details táblákba
insert into orders (customerID, orderdate) values (@cust_id, getdate())
--orderid: identity
set @order_id = @@identity --az utolsó identity insert eredménye
insert [order details] (orderid, productid, quantity, UnitPrice,
--ITT AZ ÚJ RÉSZ:
-- 3. raktárkészlet aktualizálása
declare @raktar_eredm varchar(50)
exec sp_raktárkészlet_aktualizalo @order_id, @raktar_eredm output
if @raktar_eredm = 'OK' begin
set @status = 0
set @status_message = cast(@order_id as varchar(20)) + ' sz.
end else begin
set @status = 3
set @status_message = 'HIBA: a raktárkészlet nem elegendő.'
end
end
end
print 'Státusz: ' + cast(@status as varchar(50))
print @status_message
if @status = 0 commit tran else begin
rollback tran
print 'A tranzakció visszagörgetve.'
end
end try
begin catch
print 'EGYÉB HIBA: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20)) +
rollback tran
print 'A tranzakció visszagörgetve.'
end catch
go
--teszt
--beállítjuk a paramétereket
set nocount off
select * from Products where ProductName like 'Boston%' --id: 40, unitsinstock: 900
update customers set balance=1000 where CustomerID='AROUT'
delete [Order Details] where OrderID in (select orderid from Orders where CustomerID='AROUT'
and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
--most futtatjuk, kis mennyiségnél nem várunk hibát
exec uj_rendeles 'boston', 10, 'AROUT' --nincs hiba
--ell.
select * from Customers where CustomerID='AROUT'
select top 3 * from Orders where CustomerID='arout' order by OrderDate desc
select * from Products where ProductName like 'Boston%' --unitsinstock: 890 (OK)
--helyreállítás:
delete [Order Details] where OrderID in (select orderid from Orders where CustomerID='AROUT'
and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
update Products set UnitsInStock=9 where ProductID=40 --kis készletet állítuk be
update customers set balance=1000 where CustomerID='AROUT'
--újra futtatjuk, a mennyiség miatt most hibát várunk
exec uj_rendeles 'boston', 10, 'AROUT' --megjött a hiba
select top 3 * from Orders where CustomerID='arout' order by OrderDate desc --nincs új
--az eredeti helyzet helyreállítása


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0066
delete [Order Details] where OrderID in (select orderid from Orders where CustomerID='AROUT'
and EmployeeID is null)
delete Orders where CustomerID='AROUT' and EmployeeID is null
update Products set UnitsInStock=900 where ProductID=40 --kis készletet állítunk be
update customers set balance=1000 where CustomerID='AROUT'


-- Demonstrates analytic/window functions.
-- SNIPPET 0067
FIRST_VALUE, LEAD, ROW_NUMBER, RANK


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0068
RETURN kell, hogy legyen.


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0069
go
drop function fn_ev_honap
go
create function fn_ev_honap (@datum datetime)
returns varchar(50) as
declare @eredm varchar(50)
set @eredm = case
when month(@datum) < 10 then cast(year(@datum) as varchar(4)) +'_0'+
cast(month(@datum) as varchar(2))
when month(@datum) >= 10 then cast(year(@datum) as varchar(4)) +'_'+
cast(month(@datum) as varchar(2))
else 'N.A'
end
return @eredm
end
go
--SELECT lekérdezésben felhasználható:
select e.employeeid, lastname, dbo.fn_ev_honap(orderdate) as honap,
count(orderid) as rend_szam
from employees e left outer join orders o on e.employeeid=o.employeeid
group by e.employeeid, lastname, dbo.fn_ev_honap(orderdate)
order by lastname, honap


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0070
ha valamelyik NULL, akkor pedig a 'N.A.' stringet!
create function kateg_termekei (@kat_id int) returns table as
return (


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0071
select p.ProductName as termeknev, COUNT(*) as rendelesek_szama
from Products p inner join [Order Details] od on p.ProductID=od.ProductID
group by p.ProductID, p.ProductName)
go
select * from dbo.kateg_termekei(1) where rendelesek_szama>30


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0072
drop trigger tr_uj_rend
go
create trigger tr_uj_rend on orders after insert as
declare @i int
select @i=COUNT(*) from inserted
print 'Beszúrt rekordok száma: '+cast(@i as varchar(50))
update Employees set Salary=Salary*1.02
where EmployeeID in (select EmployeeID from inserted)
end
--több rekordra is működik
go


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0073
--teszt
select salary from Employees where EmployeeID=3 --100
insert Orders (EmployeeID) values (3)
select salary from Employees where EmployeeID=3 --102


-- Demonstrates an SQL example from the notes.
-- SNIPPET 0074
drop trigger tr_demo
go
create trigger tr_demo on [order details] after update as
declare @ord_no int
begin try
select @ord_no = count(*) from inserted
print 'updating records: ' + cast(@ord_no as varchar(50))
update Products set UnitsInStock = UnitsInStock-(i.quantity-d.quantity)
from products p inner join inserted i on p.ProductID=i.ProductID
inner join deleted d on i.ProductID=d.ProductID
end try
begin catch
print 'Hiba: túl nagy mennyiség a rendelési tételen.'
end catch
go
--teszt
select top 1 * from [Order Details] --quantity 12
update [Order Details] set Quantity=13000 where OrderID=10248 and ProductID=11 --hibát
select top 1 * from [Order Details] --quantity 12 (az update visszagördül magától)

