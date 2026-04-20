use northwind
go

set nocount on

declare @order_id int = 10248
declare @bad_product_id int
declare @bad_product_name nvarchar(100)

begin try
    update p
    set p.UnitsInStock = p.UnitsInStock - od.Quantity
    from Products p
    inner join [Order Details] od on od.ProductID = p.ProductID
    where od.OrderID = @order_id

    print cast(@order_id as varchar(20)) + ' számú rendelés a raktárba átvezetve.'
end try
begin catch
    if error_number() = 547
    begin
        select top 1
            @bad_product_id = p.ProductID,
            @bad_product_name = p.ProductName
        from [Order Details] od
        inner join Products p on p.ProductID = od.ProductID
        where od.OrderID = @order_id
          and p.UnitsInStock - od.Quantity < 0
        order by p.ProductID

        if @bad_product_id is not null
            print 'RAKTÁRKÉSZLET-HIBA: '
                + cast(@order_id as varchar(20))
                + ' számú rendelésen a '
                + @bad_product_name
                + ' ('
                + cast(@bad_product_id as varchar(20))
                + ') tétel nem teljesíthető.'
        else
            print 'RAKTÁRKÉSZLET-HIBA: '
                + cast(@order_id as varchar(20))
                + ' számú rendelés nem teljesíthető.'
    end
    else
        print 'EGYÉB HIBA: ' + error_message() + ' (' + cast(error_number() as varchar(20)) + ')'
end catch
go
