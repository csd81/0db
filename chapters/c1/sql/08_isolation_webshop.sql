USE northwind;
GO

-- egyszerű izolációs szint bemutató: webáruház eset
create table test_product(id int primary key, prod_name varchar(50) not null, sold varchar(50), buyer varchar(50))
insert test_product(id, prod_name, sold) values (1, 'car', 'for sale')
insert test_product(id, prod_name, sold) values (2, 'horse', 'for sale')
go
select * from test_product
update test_product set sold='for sale', buyer=null where id=2
go
set tran isolation level read committed -- az alapértelmezett
go
begin tran
    declare @sold varchar(50)
    select @sold=sold from test_product where id=2
    if @sold='for sale' begin
        waitfor delay '00:00:10' -- épp a banki átutalást végezzük
        update test_product set sold='sold', buyer='My name' where id=2
        print 'sold successfully'
    end else print 'product not available'
commit tran
go
-- futtassuk a fenti tranzakciót egyidejűleg két lekérdezés-szerkesztőben;
-- a második szkript csak a buyer='Your name' részben tér el.

-- nézzük meg, mi történt:
select * from test_product
-- id  prod_name  sold       buyer
-- 1   car        for sale   NULL
-- 2   horse      sold       Your name
-- A lovat két vevőnek is sikeresen eladtuk, de csak "Your name" fogja megkapni. Nagyon kínos.

update test_product set sold='for sale', buyer=null where id=2
-- Próbáljuk meg most ugyanezt: set tran isolation level repeatable read
--   "Transaction (Process ID 53) was deadlocked on lock resources with another process and
--    has been chosen as the deadlock victim. Rerun the transaction."
-- Nincs logikai hiba. Csak egy lovat adtunk el.
-- Következtetés: körültekintően válaszd meg a megfelelő izolációs szintet.
