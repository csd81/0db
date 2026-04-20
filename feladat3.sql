-- ÖNÁLLÓ FELADAT #3: visszaalakítás a "sorokban a napok és a gyümölcsök, oszlopokban a csapatok" alakból
use northwind;
go

select
    nap_nev,
    gyumolcs_nev,
    csapat_nev,
    leadott_lada
from (
    select
        nap_nev,
        gyumolcs_nev,
        [Lusta],
        [Szorgos]
    from (
        select
            csapat_nev,
            nap_nev,
            gyumolcs_nev,
            sum(leadott_lada) as leadott_lada
        from eredm_pivot
        group by csapat_nev, nap_nev, gyumolcs_nev
    ) as forras
    pivot (
        sum(leadott_lada) for csapat_nev in ([Lusta], [Szorgos])
    ) as pt
) as x
unpivot (
    leadott_lada for csapat_nev in ([Lusta], [Szorgos])
) as u
order by nap_nev, gyumolcs_nev, csapat_nev;
go
