USE northwind;
GO

select
    object_name(object_id) as 'tablename',
    count(*) as 'totalpages',
    sum(Case when is_allocated=0 then 1 else 0 end) as 'unusedPages',
    sum(Case when is_allocated=1 then 1 else 0 end) as 'usedPages'
from sys.dm_db_database_page_allocations(db_id(),null,null,null,'DETAILED')
group by
    object_name(object_id)

--létrehozunk egy nagy táblát
go
create table big_table (a char(4000))
declare @i int=0
while @i<1000 begin
    insert big_table values ('a')
    set @i=@i+1
end
--a big_table 500 lapos -> a riasztás elsül
