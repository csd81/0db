USE northwind;
GO

use northwind
alter role db_datareader drop member nw_user
go
create procedure sp_list_employees
    @city varchar(50) = 'London' --a paraméter alapértelmezett értéke
as
    select * from Employees where City=@city
go
exec sp_list_employees
go
exec sp_list_employees 'Seattle'
go
grant execute on sp_list_employees to nw_user
go
