use northwind;
go

-- Kereszttablas peldahoz szukseges mintaadatok

if object_id('dbo.eredm_pivot', 'U') is not null
    drop table dbo.eredm_pivot;
go

if object_id('dbo.eredm', 'U') is not null
    drop table dbo.eredm;
go

if object_id('dbo.nap', 'U') is not null
    drop table dbo.nap;
go

if object_id('dbo.gyumolcs', 'U') is not null
    drop table dbo.gyumolcs;
go

if object_id('dbo.csapat', 'U') is not null
    drop table dbo.csapat;
go

create table dbo.csapat (
    csapat_id int not null primary key,
    csapat_nev nvarchar(50) not null
);
go

create table dbo.gyumolcs (
    gyumolcs_id int not null primary key,
    gyumolcs_nev nvarchar(50) not null
);
go

create table dbo.nap (
    nap_id int not null primary key,
    nap_nev nvarchar(50) not null
);
go

create table dbo.eredm (
    eredm_id int identity(1,1) primary key,
    csapat_id int not null references dbo.csapat(csapat_id),
    nap_id int not null references dbo.nap(nap_id),
    gyumolcs_id int not null references dbo.gyumolcs(gyumolcs_id),
    leadott_lada int not null
);
go

insert dbo.csapat (csapat_id, csapat_nev)
values (1, 'Szorgos'), (2, 'Lusta');

insert dbo.gyumolcs (gyumolcs_id, gyumolcs_nev)
values (1, 'alma'), (2, 'szilva');

insert dbo.nap (nap_id, nap_nev)
values (1, 'hetfo'), (2, 'kedd'), (3, 'szerda');

insert dbo.eredm (csapat_id, nap_id, gyumolcs_id, leadott_lada)
values
    (1, 1, 1, 50), (1, 2, 1, 60), (1, 3, 1, 70),
    (1, 1, 2, 100), (1, 2, 2, 120), (1, 3, 2, 140),
    (2, 1, 1, 5), (2, 2, 1, 6), (2, 3, 1, 7),
    (2, 1, 2, 10), (2, 2, 2, 12), (2, 3, 2, 14);
go

select *
from dbo.eredm;
go

-- Néhány csoportosító lekérdezés
select cs.csapat_nev, n.nap_nev, sum(e.leadott_lada) as teljesitmeny
from dbo.eredm e
inner join dbo.csapat cs on cs.csapat_id = e.csapat_id
inner join dbo.nap n on n.nap_id = e.nap_id
inner join dbo.gyumolcs gy on gy.gyumolcs_id = e.gyumolcs_id
group by cs.csapat_id, cs.csapat_nev, n.nap_id, n.nap_nev
order by cs.csapat_nev, n.nap_nev;
go

select cs.csapat_nev, gy.gyumolcs_nev, sum(e.leadott_lada) as teljesitmeny
from dbo.eredm e
inner join dbo.csapat cs on cs.csapat_id = e.csapat_id
inner join dbo.nap n on n.nap_id = e.nap_id
inner join dbo.gyumolcs gy on gy.gyumolcs_id = e.gyumolcs_id
group by cs.csapat_id, cs.csapat_nev, gy.gyumolcs_id, gy.gyumolcs_nev
order by cs.csapat_nev, gy.gyumolcs_nev;
go

select gy.gyumolcs_nev, sum(e.leadott_lada) as teljesitmeny
from dbo.eredm e
inner join dbo.csapat cs on cs.csapat_id = e.csapat_id
inner join dbo.nap n on n.nap_id = e.nap_id
inner join dbo.gyumolcs gy on gy.gyumolcs_id = e.gyumolcs_id
group by gy.gyumolcs_id, gy.gyumolcs_nev
order by gy.gyumolcs_nev;
go

-- Egyetlen szoveges forrastabla
select cs.csapat_nev, n.nap_nev, gy.gyumolcs_nev, e.leadott_lada
into dbo.eredm_pivot
from dbo.eredm e
inner join dbo.csapat cs on cs.csapat_id = e.csapat_id
inner join dbo.nap n on n.nap_id = e.nap_id
inner join dbo.gyumolcs gy on gy.gyumolcs_id = e.gyumolcs_id;
go

select *
from dbo.eredm_pivot;
go

-- PIVOT: gyümölcsök oszlopokban
select csapat_nev, nap_nev, pt.alma, pt.szilva
from (
    select csapat_nev, nap_nev, gyumolcs_nev, leadott_lada
    from dbo.eredm_pivot
) as forras
pivot (
    sum(leadott_lada) for gyumolcs_nev in ([alma], [szilva])
) as pt
order by csapat_nev, nap_nev;
go

-- PIVOT: csapatok oszlopokban
select gyumolcs_nev, pt.Lusta, pt.Szorgos
from (
    select csapat_nev, gyumolcs_nev, sum(leadott_lada) as leadott_lada
    from dbo.eredm_pivot
    group by csapat_nev, gyumolcs_nev
) as forras
pivot (
    sum(leadott_lada) for csapat_nev in ([Lusta], [Szorgos])
) as pt
order by gyumolcs_nev;
go

-- UNPIVOT: visszaalakitas
if object_id('tempdb..#temp') is not null
    drop table #temp;
go

select csapat_nev, pt.alma, pt.szilva
into #temp
from (
    select csapat_nev, gyumolcs_nev, sum(leadott_lada) as leadott_lada
    from dbo.eredm_pivot
    group by csapat_nev, gyumolcs_nev
) as forras
pivot (
    sum(leadott_lada) for gyumolcs_nev in ([alma], [szilva])
) as pt;
go

select csapat_nev, gyumolcs_nev, leadott_lada
from #temp
unpivot (
    leadott_lada for gyumolcs_nev in (alma, szilva)
) as upt
order by csapat_nev, gyumolcs_nev;
go

select csapat_nev, nap_nev, pt.alma, pt.szilva
into #temp
from dbo.eredm_pivot
pivot (
    sum(leadott_lada) for gyumolcs_nev in ([alma], [szilva])
) as pt;
go

select csapat_nev, nap_nev, gyumolcs_nev, leadott_lada
from #temp
unpivot (
    leadott_lada for gyumolcs_nev in (alma, szilva)
) as upt
order by csapat_nev, nap_nev, gyumolcs_nev;
go
