USE northwind;
GO

go
create procedure sp_example (@emp_id int)
as
set xact_abort on -- automatikus visszagörgetés bármilyen hiba esetén
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
    print 'OTHER ERROR: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20)) + ')'
    print 'Rolling back transaction'
    rollback tran
end catch
go

-- teszt
exec sp_example 12  -- Not found: 12, Rolling back transaction
exec sp_example 11  -- Employee found: 11, Salary successfully increased
