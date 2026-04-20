use northwind
go

-- Segédeljárás: ProductID alapján visszaadja a kategória nevét OUTPUT paraméterben
create or alter procedure dbo.sp_product_category_out
    @product_id int,
    @category_name nvarchar(100) output
as
begin
    set nocount on;

    select @category_name = c.CategoryName
    from Products p
    left join Categories c on c.CategoryID = p.CategoryID
    where p.ProductID = @product_id;
end
go

-- Fő eljárás: terméknév alapján keres, és ha pontosan 1 találat van, kiírja a kategóriát
create or alter procedure dbo.sp_product_category_by_name
    @product_name nvarchar(40)
as
begin
    set nocount on;

    begin try
        declare @res_no int,
                @product_id int,
                @category_name nvarchar(100)

        select @res_no = count(*)
        from Products
        where ProductName = @product_name

        if @res_no = 0
        begin
            print 'Nincs ilyen nevű termék.'
            return
        end

        if @res_no > 1
        begin
            print 'Több mint 1 termék illeszkedik a névre.'
            return
        end

        select @product_id = ProductID
        from Products
        where ProductName = @product_name

        exec dbo.sp_product_category_out
            @product_id = @product_id,
            @category_name = @category_name output

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

exec dbo.sp_product_category_by_name @product_name = 'Chai'
go
