use northwind
go

-- napló tábla
if object_id('dbo.products_log', 'U') is not null
    drop table dbo.products_log
go

create table dbo.products_log
(
    log_id int identity(1,1) primary key,
    product_id int not null,
    product_name nvarchar(40) not null,
    units_in_stock int null,
    log_time datetime not null default getdate()
)
go

-- trigger: termék módosításakor naplóz
if object_id('dbo.tr_products_update', 'TR') is not null
    drop trigger dbo.tr_products_update
go

create trigger dbo.tr_products_update
on dbo.Products
after update
as
begin
    set nocount on;

    insert into dbo.products_log (product_id, product_name, units_in_stock)
    select
        i.ProductID,
        i.ProductName,
        i.UnitsInStock
    from inserted i
end
go

-- Teszt
update Products
set UnitsInStock = UnitsInStock + 1
where ProductID = 1
go

select *
from products_log
go
