-- ÖNÁLLÓ FELADAT #6: az előző termék-kategóriás script kiegészítése találati szám ellenőrzéssel
use northwind;
go

set nocount on;

declare
    @name nvarchar(100) = 'King',
    @res_no int,
    @category nvarchar(100);

select @res_no = count(*)
from Products
where ProductName = @name;

if @res_no = 0
begin
    print 'Nincs ilyen nevű termék.';
end
else if @res_no > 1
begin
    print 'Több mint 1 termék illeszkedik a névre.';
end
else
begin
    select @category = c.CategoryName
    from Products p
    inner join Categories c on c.CategoryID = p.CategoryID
    where p.ProductName = @name;

    if @category is null
        print 'A terméknek nincs kategóriája.';
    else
        print 'A termék kategóriája: ' + @category;
end
go
