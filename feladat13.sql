use northwind
go

set nocount on

declare
    @agent_name nvarchar(50) = 'Fuller%',
    @emp_id int,
    @order_id int,
    @order_date datetime,
    @order_total decimal(19,4),
    @curr_is_low bit,
    @prev_is_low bit = null,
    @high_count int = 0,
    @consecutive_low_pairs int = 0,
    @first_high_date datetime = null,
    @last_high_date datetime = null,
    @avg_days decimal(10,2)

select @emp_id = EmployeeID
from Employees
where LastName like @agent_name

if @emp_id is null
begin
    print 'Nincs ilyen ügynök.'
end
else
begin
    declare order_cursor cursor fast_forward for
    select
        o.OrderID,
        o.OrderDate,
        sum(convert(decimal(19,4), od.UnitPrice * od.Quantity * (1 - od.Discount))) as OrderTotal
    from Orders o
    inner join [Order Details] od on od.OrderID = o.OrderID
    where o.EmployeeID = @emp_id
    group by o.OrderID, o.OrderDate
    order by o.OrderDate, o.OrderID

    open order_cursor

    fetch next from order_cursor into @order_id, @order_date, @order_total

    while @@fetch_status = 0
    begin
        set @curr_is_low = case when @order_total > 200 then 0 else 1 end

        if @curr_is_low = 0
        begin
            set @high_count = @high_count + 1

            if @first_high_date is null
                set @first_high_date = @order_date

            set @last_high_date = @order_date
        end
        else if @prev_is_low = 1
        begin
            set @consecutive_low_pairs = @consecutive_low_pairs + 1
        end

        set @prev_is_low = @curr_is_low

        fetch next from order_cursor into @order_id, @order_date, @order_total
    end

    close order_cursor
    deallocate order_cursor

    if @high_count = 0
    begin
        print 'Nincs 200 dollár feletti rendelés.'
        print 'Két kis értékű rendelés egymás után: ' + cast(@consecutive_low_pairs as varchar(20))
    end
    else
    begin
        set @avg_days =
            cast(datediff(day, @first_high_date, @last_high_date) as decimal(10,2))
            / @high_count

        print 'Nagy értékű rendelések száma: ' + cast(@high_count as varchar(20))
        print 'Átlagos gyakoriság napokban: ' + cast(@avg_days as varchar(20))
        print 'Két kis értékű rendelés egymás után: ' + cast(@consecutive_low_pairs as varchar(20))
    end
end
go
