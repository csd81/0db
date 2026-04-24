USE northwind;
GO

--egyszerű tárolt eljárás, amely feldolgoz egy új rendelést
--és 0-t ad vissza, ha az összes tétel hibamentesen rögzíthető a készletbe
--egyben bemutatja az OUTPUT paraméterek használatát
drop proc sp_commit_new_order_to_inventory
go
create procedure sp_commit_new_order_to_inventory
@orderid int,
@result int output
as
begin try
        update products set unitsInStock = unitsInStock - od.quantity
        from products p inner join [Order Details] od on od.ProductID=p.ProductID
        where od.OrderID=@orderid
        set @result=0
end try
begin catch
        print ' Inventory error: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20)) + ')'
        set @result=1
end catch
go

--teszt
select * from order_log  --11097
select * from Products where ProductID=10  --unitsinstock =31
select * from Products where ProductID=9   --unitsinstock =29
insert [Order Details] (orderid, productid, quantity, UnitPrice, Discount)
values (11097, 9, 10, 30, 0),(11097, 10, 40, 30, 0)  --a második tétel hibát fog okozni
go
declare @res int
exec sp_commit_new_order_to_inventory 11097, @res output
print @res
exec sp_commit_new_order_to_inventory 11096, @res output
print @res
go
--ellenőrzés: az unitsinstock értéke nem változott (OK)
select * from Products where ProductID=10  --unitsinstock =31
select * from Products where ProductID=9   --unitsinstock =29
