use northwind;
go

-- Rekord-orientalt valtozat a Products tabla harom tarolt attribumahoz.
-- A Products torzstabla megmarad, mert mas tablák is hivatkozhatnak ra.

if object_id('dbo.product_attributes', 'U') is not null
    drop table dbo.product_attributes;
go

create table dbo.product_attributes (
    attrib_id int not null primary key,
    attrib_name nvarchar(100) not null,
    attrib_type nvarchar(100) not null
);
go

insert dbo.product_attributes (attrib_id, attrib_name, attrib_type)
values
    (1, 'ProductName', 'text'),
    (2, 'UnitPrice', 'decimal'),
    (3, 'Discontinued', 'bit');
go

if object_id('dbo.product_record', 'U') is not null
    drop table dbo.product_record;
go

create table dbo.product_record (
    product_id int not null,
    attrib_id int not null references dbo.product_attributes(attrib_id),
    attrib_value nvarchar(500) null,
    primary key (product_id, attrib_id)
);
go

-- Egy rekordbol tobb rekord lesz.
insert dbo.product_record (product_id, attrib_id, attrib_value)
select ProductID, 1, ProductName
from dbo.Products
where ProductName is not null

union all

select ProductID, 2, cast(UnitPrice as nvarchar(500))
from dbo.Products
where UnitPrice is not null

union all

select ProductID, 3, cast(Discontinued as nvarchar(500))
from dbo.Products
where Discontinued is not null;
go

-- Ellenorzes: a rekord-orientalt tabla tartalma.
select *
from dbo.product_record
order by product_id, attrib_id;
go

-- Visszaalakitas mezorientalt formatumba.
select
    pr.product_id as ProductID,
    max(case when pr.attrib_id = 1 then pr.attrib_value end) as ProductName,
    max(case when pr.attrib_id = 2 then pr.attrib_value end) as UnitPrice,
    max(case when pr.attrib_id = 3 then pr.attrib_value end) as Discontinued
from dbo.product_record pr
group by pr.product_id
order by pr.product_id;
go
