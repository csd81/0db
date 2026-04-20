use northwind
go

set nocount on

declare
    @termeknev nvarchar(40) = 'Uj teszt termek',
    @kat_id int = 1,
    @prod_id int,
    @kat_cnt int

begin try
    begin tran

    insert into Products
        (ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice,
         UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
    values
        (@termeknev, null, @kat_id, null, 0, 0, 0, 0, 0)

    set @prod_id = scope_identity()

    select @kat_cnt = count(*)
    from Products
    where CategoryID = @kat_id

    if @kat_cnt > 10
    begin
        print 'A kategóriában már több mint 10 termék van, visszagörgetés.'
        rollback tran
        return
    end

    update Products
    set UnitsInStock = 100
    where ProductID = @prod_id

    commit tran
    print 'Tranzakció sikeres, a termék felvéve és a készlet 100-ra állítva.'
end try
begin catch
    if @@trancount > 0
        rollback tran

    print 'EGYÉB HIBA: ' + error_message() + ' (' + cast(error_number() as varchar(20)) + ')'
end catch
go

-- Ellenőrzés: rollback esetén itt 0 sort kell kapnunk.
select *
from Products
where ProductName = 'Uj teszt termek'
  and CategoryID = 1
go
