use northwind
go

create or alter procedure dbo.sp_product_category
    @product_id int
as
begin
    set nocount on;

    begin try
        declare @res_no int,
                @product_name nvarchar(40),
                @category_name nvarchar(100)

        select @res_no = count(*)
        from Products
        where ProductID = @product_id

        if @res_no = 0
        begin
            print 'Nincs ilyen azonosítójú termék.'
            return
        end

        select
            @product_name = p.ProductName,
            @category_name = c.CategoryName
        from Products p
        left join Categories c on c.CategoryID = p.CategoryID
        where p.ProductID = @product_id

        if @category_name is null
            print 'A terméknek nincs kategóriája.'
        else
            print 'Termék: ' + @product_name + ', kategória: ' + @category_name
    end try
    begin catch
        print 'EGYÉB HIBA: ' + error_message() + ' (' + cast(error_number() as varchar(20)) + ')'
    end catch
end
go

exec dbo.sp_product_category @product_id = 1
go
