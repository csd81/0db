use northwind
go

set nocount on

declare @cust_id nchar(5),
        @cust_name nvarchar(40),
        @order_date datetime,
        @order_no int,
        @outer_fetch_status int,
        @inner_fetch_status int

declare customer_cursor cursor fast_forward for
select CustomerID, CompanyName
from Customers
where Country = 'USA'
order by CompanyName

open customer_cursor

fetch next from customer_cursor into @cust_id, @cust_name
set @outer_fetch_status = @@fetch_status

while @outer_fetch_status = 0
begin
    select @order_no = count(*)
    from Orders
    where CustomerID = @cust_id

    print @cust_name + ' - eddigi rendelések száma: ' + cast(@order_no as varchar(10))

    declare order_cursor cursor fast_forward for
    select OrderDate
    from Orders
    where CustomerID = @cust_id
    order by OrderDate

    open order_cursor

    fetch next from order_cursor into @order_date
    set @inner_fetch_status = @@fetch_status

    while @inner_fetch_status = 0
    begin
        print '  rendelés dátuma: ' + convert(varchar(10), @order_date, 120)

        fetch next from order_cursor into @order_date
        set @inner_fetch_status = @@fetch_status
    end

    close order_cursor
    deallocate order_cursor

    fetch next from customer_cursor into @cust_id, @cust_name
    set @outer_fetch_status = @@fetch_status
end

close customer_cursor
deallocate customer_cursor
go
