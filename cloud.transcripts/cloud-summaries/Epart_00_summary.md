# Epart_00 összefoglaló

## A mai terv: Bigtable, BigQuery, Data Studio

Ez a rész egy új adatkezelési blokkot vezet be.

- Először a `Bigtable` kerül sorra.
- Utána a `BigQuery`.
- Végül a `Data Studio` jellegű vizualizációs eszközök.

Az oktató azt jelzi, hogy ezekkel a szolgáltatásokkal már nem elsősorban az infrastruktúra, hanem a nagy adatmennyiségű tárolás, elemzés és megjelenítés kerül előtérbe.

## Mi a Bigtable?

A `Bigtable` egy nagy méretű adattáblák kezelésére alkalmas szolgáltatás.

- `fully managed`, vagyis a Google menedzseli a működését,
- `scalable`, tehát automatikusan skálázható,
- nagyon nagy méretű táblákat tud kezelni.

Az oktató kiemeli, hogy itt már terabájtos vagy petabájtos nagyságrendű adatok is szóba kerülnek.

## Kulcs-érték alapú, ritka tábla

A Bigtable nem klasszikus relációs táblaként működik.

- Kulcs-érték alapú tárolási logikát használ.
- `Sparse`, vagyis ritka táblaformátumot alkalmaz.
- Csak azokat a cellákat tárolja, amelyekben ténylegesen van érték.

Ez fontos különbség az olyan mátrixszerű modellekhez képest, ahol az üres cellák is implicit részét képezik a szerkezetnek.

## Valós idejű frissítési képesség

A Bigtable egyik legfontosabb sajátossága a gyors írás és frissítés.

- Nagyon kis késleltetéssel képes új értékeket beírni.
- Ez eltér a klasszikus relációs adatbázisok domináns optimalizálásától.
- Itt nem elsősorban a lekérdezés, hanem a gyors `update` a kulcs.

Ezért a Bigtable jól illik olyan helyzetekhez, ahol az adat folyamatosan és gyorsan változik.

## Adminisztráció és integráció

A szolgáltatás működtetése teljesen a szolgáltató oldalán zajlik.

- Automatikus frissítés,
- újraindítás,
- replikáció,
- klaszterátméretezés
  mind a háttérben történik.

Emellett a Bigtable szorosan integrálható más Google-szolgáltatásokkal és nyílt forráskódú rendszerekkel is.

## Tipikus alkalmazási területek

Az oktató több példát is említ, ahol gyorsan változó, idősoros vagy nagy gráfszerű adatok jelennek meg.

- rendszer- és infrastruktúramonitorozás,
- marketing- és pénzügyi idősorok,
- `IoT` és szenzoradatok,
- közlekedési és biztonsági megfigyelés,
- közösségi hálózati adatok elemzése.

Ezek közös jellemzője a nagy mennyiség és a gyors frissülés.

## Összegzés

Az `Epart_00.txt` fő témája a `Bigtable` bevezetése mint nagy méretű, gyors frissítésre optimalizált, menedzselt adattárolási szolgáltatás. A szöveg bemutatja a ritka, kulcs-érték alapú táblaformátumot, a valós idejű írási képességet és a tipikus alkalmazási területeket. A központi tanulság az, hogy a Bigtable nem általános relációs adatbázis-helyettesítő, hanem speciálisan nagy és dinamikus adatfolyamokhoz tervezett rendszer.
