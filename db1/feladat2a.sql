-- ÖNÁLLÓ FELADAT #2a: sorokban a napok, oszlopokban a csapatok, a szerdát kihagyva
use northwind;
go

select
    nap_nev,
    pt.[Lusta],
    pt.[Szorgos]
from (
    select
        nap_nev,
        csapat_nev,
        sum(leadott_lada) as leadott_lada
    from eredm_pivot
    where nap_nev <> 'szerda'
    group by nap_nev, csapat_nev
) as forras
pivot (
    sum(leadott_lada) for csapat_nev in ([Lusta], [Szorgos])
) as pt
order by nap_nev;
go
