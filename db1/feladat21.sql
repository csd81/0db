go
create or alter function dbo.fn_employee_order_count (@emp_id int)
returns int
as
begin
    declare @order_count int

    select @order_count = count(*)
    from Orders
    where EmployeeID = @emp_id

    return @order_count
end
go

select
    EmployeeID,
    LastName,
    dbo.fn_employee_order_count(EmployeeID) as OrderCount
from Employees
order by LastName
go
