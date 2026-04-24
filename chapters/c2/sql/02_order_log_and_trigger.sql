USE northwind;
GO

--a naplótábla
go
--drop table order_log
go
create table order_log (
        event_id int IDENTITY (1, 1) primary key ,
        event_type varchar(50) NOT NULL ,
        order_id int NOT NULL ,
        orderitem_id int NULL ,
        status int NOT NULL default(0),
        time_created datetime NOT NULL default(getdate()) ,
        time_process_begin datetime NULL ,
        time_process_end datetime NULL ,
        process_duration as datediff(second, time_process_begin, time_process_end)
)
go
drop trigger tr_log_order
go
create trigger tr_log_order ON Orders for insert, update as
declare @orderid int
select @orderid=orderid from inserted  --az inserted táblában több rekord is lehet
print 'OrderID of the LAST record: ' + cast(@orderid as varchar(50))
if update(orderid) begin  --ha az orderid megváltozott, akkor ez egy INSERT
        print 'Warning: new order'
        insert order_log (event_type, order_id)  --a status és time_created az alapértelmezett értéket kapja
                select 'new order', orderid from inserted
end else if update(shipaddress) or update(shipcity) begin  --a szállítási cím megváltozott
        print 'Warning: address changed'
        insert order_log (event_type, order_id)
                select 'address changed', orderid from inserted
end else begin  --egyéb változás
        print 'Warning: other change'
        insert order_log (event_type, order_id)
                select 'other change', orderid from inserted
end
go

--1. teszt
insert Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
select * from order_log
--egy új rekordot kaptunk a naplótáblában

--2. teszt
insert Orders (CustomerID, OrderDate) values ('AROUT', GETDATE()), ('HANAR', GETDATE())
select * from order_log
--két új rekordot kaptunk a naplótáblában

--3. teszt
update Orders set ShipVia = 3 where OrderID in (11097, 11096)  --a 2. teszt rendelésazonosítói
select * from order_log
--két új 'other change' típusú rekordot kaptunk

--táblák visszaállítása
delete Orders where CustomerID in ('AROUT', 'HANAR') and EmployeeID is null
delete order_log
