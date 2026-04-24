USE northwind;
GO

use adworks
alter role exec_all_sp drop member nw_user
alter role db_owner add member nw_user
alter role db_denydatawriter add member nw_user

--ellenőrzés egy nw_user kliens-kapcsolatban:
use adworks
select * from Sales.Store
--(701 sort érint)
exec Person.sp_DeletePerson_Temporal 2
--(1 sort érint)
--(1 sort érint)
create table test (id int)
--A parancsok sikeresen lefutottak.
insert test (id) values (25)
--Msg 229, Level 14, State 5, Line 10
--Az INSERT jogosultságot megtagadta a 'test' objektum, 'adworks' adatbázis, 'dbo' séma esetén.
drop table test
--A parancsok sikeresen lefutottak.
