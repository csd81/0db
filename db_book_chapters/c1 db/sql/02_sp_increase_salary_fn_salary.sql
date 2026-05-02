USE northwind;
GO

--egyszerű szkript: alkalmazott keresése, és ha egyetlen egyező rekordot találunk,
--a fizetés emelése 10%-kal
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

--tárolt eljárásba csomagolva
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
--teszt
select Salary from Employees where LastName like 'Fuller%'
exec sp_increase_salary 'Fuller'
select Salary from Employees where LastName like 'Fuller%'

--skaláris értékű függvény: visszaadja egy személy fizetését, vagy 0-t, ha nem található
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
