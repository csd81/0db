USE northwind;
GO

drop trigger tr_demo_bad
go
create trigger tr_demo_bad on orders for insert as
declare @orderid int
select @orderid=OrderID from inserted
print 'New order ID: ' + cast(@orderid as varchar(50))
waitfor delay '00:00:10'  --10 s
select 1/0  --hibát generálunk
go
--1. teszt: az utolsó két sorral kikommentezve
insert Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
--tábla visszaállítása
delete Orders where CustomerID='AROUT' and EmployeeID is null
--2. teszt: a trigger újbóli létrehozása, az utolsó sorokkal kikommentezve
insert Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
--sokáig kell várnunk, de nincs hiba
--3. teszt: a trigger újbóli létrehozása, minden sorral
insert Orders (CustomerID, OrderDate) values ('AROUT', GETDATE())
--sokáig kell várnunk, majd megkapjuk az üzenetet:
-- 'New order ID: 11094
-- Msg 8134, Level 16, State 1, Procedure tr_demo_bad, Line 6 [Batch Start Line 276]
-- Divide by zero error encountered.
-- The statement has been terminated.'
select * from Orders where CustomerID='AROUT' and EmployeeID is null
--nincs ilyen rekord, mert
--az insert utasítás visszagörgetésre került -> a kereskedelmi rendszer működése megszakadt
