use northwind
go

create or alter procedure dbo.usp_stock_upsert_product
    @termeknev nvarchar(40),
    @mennyiseg int,
    @szallito nvarchar(40)
as
begin
    set nocount on;

    declare @prod_cnt int,
            @prod_id int,
            @supplier_cnt int,
            @supplier_id int,
            @msg nvarchar(200);

    begin try
        begin tran;

        select @prod_cnt = count(*)
        from Products
        where ProductName like '%' + @termeknev + '%';

        if @prod_cnt > 1
        begin
            set @msg = 'HIBA: a terméknév nem egyértelmű.';
            rollback tran;
            print @msg;
            return;
        end

        if @prod_cnt = 1
        begin
            select @prod_id = ProductID
            from Products
            where ProductName like '%' + @termeknev + '%';

            update Products
            set UnitsInStock = UnitsInStock + @mennyiseg
            where ProductID = @prod_id;

            set @msg = 'Raktárkészlet növelve.';
            commit tran;
            print @msg;
            return;
        end

        -- nincs termék: beszállító keresése
        select @supplier_cnt = count(*)
        from Suppliers
        where CompanyName like '%' + @szallito + '%';

        if @supplier_cnt > 1
        begin
            set @msg = 'HIBA: a beszállító neve nem egyértelmű.';
            rollback tran;
            print @msg;
            return;
        end

        if @supplier_cnt = 1
        begin
            select @supplier_id = SupplierID
            from Suppliers
            where CompanyName like '%' + @szallito + '%';
        end
        else
        begin
            insert into Suppliers (CompanyName)
            values (@szallito);

            set @supplier_id = scope_identity();
        end

        insert into Products
            (ProductName, SupplierID, CategoryID, QuantityPerUnit,
             UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
        values
            (@termeknev, @supplier_id, null, null,
             0, @mennyiseg, 0, 0, 0);

        set @msg = 'Új termék felvéve a raktárba.';
        commit tran;
        print @msg;
    end try
    begin catch
        if @@trancount > 0
            rollback tran;

        print 'EGYÉB HIBA: ' + error_message() + ' (' + cast(error_number() as varchar(20)) + ')';
    end catch
end
go

exec dbo.usp_stock_upsert_product
    @termeknev = 'Raclette',
    @mennyiseg = 12,
    @szallito = 'Formago Company'
go
