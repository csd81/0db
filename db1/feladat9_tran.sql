use northwind
go

set nocount on
set xact_abort off
go

declare @order_id int = 10248
declare @res_no int
declare @msg nvarchar(200)

begin try
    begin tran

    select @res_no = count(*)
    from [Order Details]
    where OrderID = @order_id

    if @res_no = 0
    begin
        set @msg = 'HIBA: nincs ilyen rendelés vagy nincs hozzá tétel.'
        rollback tran
        print @msg
        return
    end

    if exists (
        select 1
        from Products p
        inner join [Order Details] od on od.ProductID = p.ProductID
        where od.OrderID = @order_id
          and p.UnitsInStock - od.Quantity < 0
    )
    begin
        set @msg = 'HIBA: a rendelés nem teljesíthető, mert valamelyik tételnél elfogyna a készlet.'
        rollback tran
        print @msg
        return
    end

    update p
    set p.UnitsInStock = p.UnitsInStock - od.Quantity
    from Products p
    inner join [Order Details] od on od.ProductID = p.ProductID
    where od.OrderID = @order_id

    commit tran
    print cast(@order_id as varchar(20)) + ' számú rendelés a raktárba átvezetve.'
end try
begin catch
    if @@trancount > 0
        rollback tran

    print 'EGYÉB HIBA: ' + error_message() + ' (' + cast(error_number() as varchar(20)) + ')'
end catch
go

-- Tesztelés:
select ProductID, UnitsInStock from Products where ProductID in (11, 42, 72)
select * from [Order Details] where OrderID = 10248
go
