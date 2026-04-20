-- ÖNÁLLÓ FELADAT #2: a korábbi PIVOT-os eredmény visszaalakítása soros formára UNPIVOT-tal
use northwind;
go

-- Először előállítjuk a csapatok x gyümölcsök kereszttáblát.
select
    csapat_nev,
    alma,
    szilva
into #temp_pivot
from (
    select
        csapat_nev,
        gyumolcs_nev,
        sum(leadott_lada) as leadott_lada
    from eredm_pivot
    group by csapat_nev, gyumolcs_nev
) as forras
pivot (
    sum(leadott_lada) for gyumolcs_nev in ([alma], [szilva])
) as pt;
go

-- Az oszlopok visszaalakítása sorokká.
select
    csapat_nev,
    gyumolcs_nev,
    leadott_lada
from #temp_pivot
unpivot (
    leadott_lada for gyumolcs_nev in ([alma], [szilva])
) as upt
order by csapat_nev, gyumolcs_nev;
go

drop table #temp_pivot;
go
