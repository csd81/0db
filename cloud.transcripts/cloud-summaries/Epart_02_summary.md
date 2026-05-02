# Epart_02 összefoglaló

## A Bigtable architektúrája

Ez a rész a `Bigtable` működésének belső architektúráját mutatja be.

- Fent a kliensek helyezkednek el.
- Ezek kérései frontendszerverekhez futnak be.
- A központi feldolgozó rész egy `Bigtable` klaszter.
- Az adattárolás ettől különálló rétegben történik.

Ez klasszikus felhős elosztott architektúra: a kliens, a kiszolgáló klaszter és a perzisztens tárolás szét van választva.

## A node-ok nem tárolnak adatot

Az oktató szerint ez az egyik legfontosabb architekturális elv.

- A klaszter node-jai nem magukat az adatokat tárolják.
- Csak mutatókat vagy hivatkozásokat tartanak az adattároló rétegre.
- Az adatok a háttérben külön fájlrendszerben vannak.

Ez a kialakítás nagyban növeli a hibatűrést és az átméretezhetőséget.

## Colossus és SSTable

Az adattárolás a Google háttérrendszerére épül.

- A fájlrendszer neve `Colossus`.
- A nagy táblák kisebb egységekre vannak darabolva.
- Ezek az egységek `SSTable` vagy `tablet` formában tárolódnak.

Ez teszi lehetővé a finomabb adatmozgatást, replikációt és részleges újraelosztást.

## Miért jó a szétválasztás?

A node-ok és az adattárolás elválasztásának több előnye is van.

- Egy node kiesése nem viszi magával az adatot.
- Új node gyorsan csatlakoztatható.
- A klaszter mérete rugalmasan növelhető vagy csökkenthető.
- A replikáció az adattárolási rétegben függetlenül kezelhető.

Ez a szerkezet teszi a Bigtable-t megbízható, nagy skálájú szolgáltatássá.

## Összegzés

Az `Epart_02.txt` fő témája a `Bigtable` architektúrájának bemutatása. A szöveg hangsúlyozza, hogy a feldolgozó node-ok és az adattárolás külön rétegben élnek, az adatok `Colossus` fájlrendszerben `SSTable`-ekben vannak, és ez biztosítja a skálázhatóságot valamint a hibatűrést. A központi tanulság az, hogy a nagy felhős adatplatformok ereje sokszor éppen abból fakad, hogy az adattárolás és a kiszolgálás logikája fizikailag és logikailag is szét van választva.
