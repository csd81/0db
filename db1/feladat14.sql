use northwind
go

set nocount on

declare
    @emp_id int,
    @emp_name nvarchar(100),
    @order_id int,
    @order_date datetime,
    @outer_fetch_status int,
    @inner_fetch_status int

declare agent_cursor cursor fast_forward for
select EmployeeID, LastName
from Employees
where Title like '%Sales%'
order by LastName

open agent_cursor

fetch next from agent_cursor into @emp_id, @emp_name
set @outer_fetch_status = @@fetch_status

while @outer_fetch_status = 0
begin
    print 'Ügynök: ' + @emp_name

    declare order_cursor cursor fast_forward for
    select OrderID, OrderDate
    from Orders
    where EmployeeID = @emp_id
    order by OrderDate

    open order_cursor

    fetch next from order_cursor into @order_id, @order_date
    set @inner_fetch_status = @@fetch_status

    while @inner_fetch_status = 0
    begin
        print '  Rendelés: ' + cast(@order_id as varchar(10))
            + ', dátum: ' + convert(varchar(10), @order_date, 120)

        fetch next from order_cursor into @order_id, @order_date
        set @inner_fetch_status = @@fetch_status
    end

    close order_cursor
    deallocate order_cursor

    fetch next from agent_cursor into @emp_id, @emp_name
    set @outer_fetch_status = @@fetch_status
end

close agent_cursor
deallocate agent_cursor
go
