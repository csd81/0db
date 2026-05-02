# Epart_04 összefoglaló

## Tárolási sajátosságok

Ez a rész a `Bigtable` adattárolási finomságairól szól.

- Az üres cellák nem foglalnak helyet.
- Az adatok alapvetően bájtfolyamként tárolódnak.
- Bizonyos speciális műveletekhez külön típuskezelés tartozik.

Ez azt mutatja, hogy a rendszer nem gazdag típusokkal dolgozó relációs adatbázis, hanem hatékony, nyers adattárolásra optimalizált struktúra.

## Törlés és késleltetett felszabadítás

A törlés nem feltétlenül azonnali fizikai törlést jelent.

- A rendszer először csak megjelöli az adatot töröltként.
- A tényleges eltávolítás későbbi háttérfolyamat során történik.
- Ez a folyamat egyfajta `compaction`.

Ez hasonlít a memóriakezelésnél ismert `garbage collection` logikájára.

## Tömörítés

Az oktató röviden kitér a tömörítésre is.

- Kisebb adatértékeket a rendszer automatikusan kezelhet.
- Nagyobb adatnál egyes esetekben a fejlesztőnek kell gondoskodnia megfelelő előkészítésről.

Ez bár itt nem központi téma, jelzi, hogy a fizikai adattárolás hatékonysága fontos része a működésnek.

## Titkosítás és adatbiztonság

Külön hangsúlyt kap, hogy a tárolt adatok titkosítva vannak.

- A felhőszolgáltató nem nyers formában tárolja az adatokat.
- Az adatszivárgások tipikusan nem a tárolórendszerből, hanem rosszul megírt alkalmazásokból vagy emberi hibákból származnak.

Ez fontos szemléleti pont: a felhővel szembeni bizalmatlanság sokszor nem a megfelelő helyre irányul.

## Átmenet a gyakorlathoz

Az elméleti rész után az oktató gyakorlati példát indít.

- A cél egy `Bigtable` példány és tábla létrehozása.
- Utána adatok beírása és lekérdezése következik.
- A gyakorlat parancssoros tutorial alapján történik.

Ez összeköti a szolgáltatás fogalmi megértését a tényleges használattal.

## Összegzés

Az `Epart_04.txt` fő témája a `Bigtable` tárolási és adatkezelési részleteinek lezárása, különösen a törlés, tömörítés és titkosítás kérdésköre. A szöveg hangsúlyozza, hogy a fizikai adatkezelés sokszor háttérfolyamatokkal történik, és a tárolás alapból biztonságos. A központi tanulság az, hogy a nagy felhős adattárolók használatához nem elég a logikai modellt ismerni; érteni kell a mögöttes működési kompromisszumokat is.
