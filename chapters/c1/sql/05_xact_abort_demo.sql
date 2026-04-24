USE northwind;
GO

--atomicitás bemutatója xact_abort nélkül
set xact_abort off
delete t2
go
begin tran
        insert t2 (id, t1_id) values (10, 1)
        insert t2 (id, t1_id) values (11, 2) --idegen kulcs megszorítás megsértése
        insert t2 (id, t1_id) values (12, 3)
commit tran
go
select * from t2
-- 10   1
-- 12   3
-- atomicitás NEM teljesült

set xact_abort on
delete t2
go
begin tran
        insert t2 (id, t1_id) values (10, 1)
        insert t2 (id, t1_id) values (11, 2) --idegen kulcs megszorítás megsértése
        insert t2 (id, t1_id) values (12, 3)
commit tran
go
select * from t2
-- (üres)
-- atomicitás teljesült
