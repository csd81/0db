USE northwind;
GO

use northwind
--alter table employees drop column SSN
--alter table employees drop column email
alter table employees add ssn char(10) null, email varchar(200) --érzékeny oszlopok
alter table employees alter column ssn char(10) masked with (function = 'partial(1,".....",4)')
alter table employees alter column email char(200) masked with (function = 'email()')
go
update Employees set ssn ='1234567890'
update Employees set email ='sohase_mondd@citromail.hu'
select lastname, ssn, email from Employees --minden értéket látunk

--ha viszont létrehozunk egy írási/olvasási jogú felhasználót
use master
create login test with password='h6twqPNO', default_database=northwind
go
use northwind --context switch
create user test for login test
alter role db_datareader add member test
alter role db_datawriter add member test
go

--váltsunk át a test felhasználó kapcsolatára
execute as user = 'test'
select lastname, ssn, email from Employees
revert
go
--ezt látjuk:
--lastname     ssn           email
--Davolio      1.....7890    sXXX@XXXX.com
--Fuller       1.....7890    sXXX@XXXX.com

--most adjuk meg az UNMASK jogosultságot a test felhasználónak
grant UNMASK to test
go
execute as user = 'test'
select lastname, ssn, email from Employees
revert
go
--most ezt látjuk:
--lastname     ssn           email
--Davolio      1234567890    sohase_mondd@citromail.hu
--Fuller       1234567890    sohase_mondd@citromail.hu

--FIGYELEM: a felhasználó továbbra is módosíthatja az oszlopokat!!!
go
execute as user = 'test'
update Employees set email ='mondj_igent@citromail.hu'
select lastname, ssn, email from Employees
revert
go
revoke UNMASK from test
