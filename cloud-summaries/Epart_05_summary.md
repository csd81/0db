# Epart_05 összefoglaló

## Bigtable gyakorlati példa

Ez a rész a `Bigtable` első gyakorlati feladatáról szól.

- A hallgatók parancssori útmutató alapján dolgoznak.
- Létrehoznak egy Bigtable `instance`-t.
- Ezután táblát hoznak létre és adatot írnak bele.

Az oktató kifejezetten arra kéri őket, hogy önálló tempóban hajtsák végre a lépéseket.

## Jogosultsági problémák

A gyakorlat során többeknél `IAM` jellegű gond is előjön.

- A szükséges szerepkörök hiányozhatnak.
- A felhasználói email és a projektazonosító helyes beállítása kritikus.
- Szükség lehet a `Bigtable Administrator` szerepkör megadására.

Ez ismét azt mutatja, hogy a felhős gyakorlati feladatoknál a jogosultságok kezelése sokszor ugyanolyan fontos, mint maga a szolgáltatás használata.

## Időbélyeges értékek a gyakorlatban

Az oktató kiemeli, mit kell látni a sikeres futás után.

- Egy adott sorhoz és oszlophoz több érték is tartozhat.
- Ezek eltérő időbélyegekkel jelennek meg.
- Ez demonstrálja a Bigtable idősoros cellamodelljét.

Ez jó visszaigazolása annak, amit az elméleti részben már megmagyarázott.

## Cleanup

A gyakorlat lezárásához takarítani is kell.

- A létrehozott táblát törölni kell.
- A feleslegesen meghagyott erőforrás később költséget okozhat.
- A legvégén a hozzáférési jog visszavonása opcionális lehet.

Ez összhangban van a teljes tárgy egyik legfontosabb operatív tanulságával: a felhőben semmit nem szabad feleslegesen hátrahagyni.

## További források

Az oktató a dokumentáció és a további példák önálló átnézését is javasolja.

- Séma- és kulcstervezés.
- Programozott elérés különböző nyelvekből.
- Pythonos és más mintapéldák.

Ez különösen az adattudományos hátterű hallgatóknak lehet releváns.

## Átmenet a BigQuery felé

Miután elegen befejezték vagy legalább eljutottak a gyakorlat végére, az óra továbblép.

- A következő szolgáltatás a `BigQuery`.
- Az oktató külön rákérdez, hogy az adatbázisos tárgyban ez mennyire volt már téma.

Ez jelzi, hogy a következő blokk már inkább elemzési és vizualizációs jellegű lesz.

## Összegzés

Az `Epart_05.txt` fő témája a `Bigtable` gyakorlati kipróbálása és a hozzá kapcsolódó jogosultsági, adatírási és takarítási lépések. A szöveg bemutatja, hogyan jelenik meg a több időbélyeges cella a gyakorlatban, és mennyire fontosak a megfelelő szerepkörök. A központi tanulság az, hogy a `Bigtable` használata elméletben egyszerűnek tűnik, de a felhőn belüli jogosultságkezelés és erőforrásfegyelem a sikeres használat szerves része.
