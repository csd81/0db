USE northwind;
GO

use northwind
revoke execute on sp_list_employees from nw_user
go
--így adható végrehajtási jog az adatbázis ÖSSZES objektumára
grant execute to nw_user

--új szerepkör
use adworks
create role exec_all_sp
grant execute on schema::Person to exec_all_sp --a szerepkör rendszerbiztonsági tagként viselkedik
--alternatíva lehet: grant select, update on schema::Person to read_update_only_role stb.
create user nw_user for login nw_user
alter role exec_all_sp add member nw_user

--ellenőrzés egy kliens-kapcsolatban
use adworks
select * from Sales.Store
--Msg 229, Level 14, State 5, Line 8
--A SELECT jogosultságot megtagadta a 'Store' objektum, 'adworks' adatbázis, 'Sales' séma esetén.
exec Person.sp_DeletePerson_Temporal 2
--(1 sort érint)
--(1 sort érint)
