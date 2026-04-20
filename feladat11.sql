use northwind
go

set nocount on

declare @cust_id nchar(5),
        @cust_name nvarchar(40),
        @order_no int

declare customer_cursor cursor fast_forward for
select CustomerID, CompanyName
from Customers
where Country = 'USA'
order by CompanyName

open customer_cursor

fetch next from customer_cursor into @cust_id, @cust_name

while @@fetch_status = 0
begin
    select @order_no = count(*)
    from Orders
    where CustomerID = @cust_id

    print @cust_name + ' - eddigi rendelések száma: ' + cast(@order_no as varchar(10))

    fetch next from customer_cursor into @cust_id, @cust_name
end

close customer_cursor
deallocate customer_cursor
go
