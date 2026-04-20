use northwind;
go

-- Cursor practice: iterate USA customers and print their order counts row by row.
set nocount on;

declare
    @cust_id nchar(5),
    @cust_name nvarchar(100),
    @order_count int;

declare cursor_usa_customers cursor fast_forward for
select
    CustomerID,
    CompanyName
from Customers
where Country = 'USA'
order by CompanyName;

open cursor_usa_customers;

fetch next from cursor_usa_customers into @cust_id, @cust_name;

while @@fetch_status = 0
begin
    select @order_count = count(*)
    from Orders
    where CustomerID = @cust_id;

    print @cust_name + ' - orders: ' + cast(@order_count as varchar(10));

    fetch next from cursor_usa_customers into @cust_id, @cust_name;
end

close cursor_usa_customers;
deallocate cursor_usa_customers;
go
