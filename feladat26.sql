drop trigger if exists tr_demo
go

create trigger tr_demo
on [order details]
after insert
as
begin
    set nocount on;

    begin try
        declare @ord_no int

        select @ord_no = count(*)
        from inserted

        print 'inserted records: ' + cast(@ord_no as varchar(50))

        update p
        set p.UnitsInStock = p.UnitsInStock - i.Quantity
        from Products p
        inner join inserted i on i.ProductID = p.ProductID
    end try
    begin catch
        print 'Hiba: túl nagy mennyiség a rendelési tételen.'
    end catch
end
go

-- Teszt
insert [Order Details] (OrderID, ProductID, Quantity, UnitPrice, Discount)
values (10248, 11, 2, 14, 0)
go

select * from Products where ProductID = 11
go
