# Bpart_05 összefoglaló

## A virtuális gép elérése böngészőből

Ez a rész a már létrehozott virtuális gép gyakorlati használatát mutatja be.

- A `VM instance` többféleképpen is elérhető.
- A legegyszerűbb út most a böngészőből nyitott `SSH` kapcsolat.
- A Google automatikusan kezeli a szükséges kulcsokat.

Az oktató célja itt az, hogy a hallgatók gyorsan, helyi külön konfiguráció nélkül tudjanak belépni a saját gépükre.

## A böngészős terminál jellemzői

A megnyitott ablak egy egyszerű Linux terminált ad.

- Látszik a felhasználónév és a példány neve.
- A hallgatók egy valódi, „csupasz” Linux gépet kapnak.
- A felületen fájlfeltöltési és egyéb alapfunkciók is megjelennek.

Ez a rész megmutatja, hogy a felhőben létrehozott VM ténylegesen egy általános célú szerverként használható.

## A virtuális gép leállítása

Az oktató rögtön a belépés után hangsúlyozza a helyes gyakorlatot.

- A gépet a kipróbálás után le kell állítani.
- Nem szabad fölöslegesen futva hagyni.
- A leállítás állapota néha csak frissítés után látszik.

Ez megerősíti az előző rész egyik legfontosabb költségkezelési szabályát.

## További tutorialok

A gyors bemutató után az oktató röviden utal további gyakorlatokra is.

- Lehet fájlokat mozgatni,
- tartós diszket csatolni,
- illetve további VM-kezelési lépéseket gyakorolni.

Ezeket most nem futtatják végig, de a hallgatók később önállóan visszatérhetnek hozzájuk.

## Átmenet a Cloud Storage felé

A következő téma a `Cloud Storage` használata.

- A bal oldali menüből a `Cloud Storage` rész nyitható meg.
- A központi fogalom itt a `bucket`.
- Minden tárolási művelethez először ilyen tárolóegységet kell létrehozni.

Ez a rész arra szolgál, hogy a hallgatók megértsék: a felhőobjektumtárolás nem hagyományos fájlrendszerként működik.

## Bucket létrehozása

A bucket létrehozásakor több paramétert kell megadni.

- A névnek globálisan egyedinek kell lennie.
- Érdemes valamilyen egyedi azonosítót, például `Neptun`-kódot beleírni.
- Ki kell választani a régiót is.

Az oktató európai régió használatát javasolja, összhangban a korábbi elméleti résszel.

## Tárolási osztály és hozzáférés

A bucket létrehozásakor a tárolási osztály és az elérési beállítások is fontosak.

- Most `standard` tárolást választanak.
- Szóba kerül az `autoclass` funkció is.
- A publikus hozzáférés tiltása alapértelmezés szerint be van kapcsolva.

Az oktató ezt most módosítja, mert demonstrálni szeretné a külső elérést.

## Fájlok feltöltése és virtuális mappák

A létrehozott bucketbe ezután adatot töltenek fel.

- Lehet közvetlenül fájlt feltölteni.
- Lehet „mappát” is létrehozni, bár ez nem klasszikus fájlrendszerbeli könyvtár.
- A bucket tartalma később listázható és kezelhető.

Ez a rész megmutatja az objektumtárolás alapvető használati logikáját.

## Public URL és külső elérés

A bemutató végén az oktató megpróbálja lekérni egy feltöltött objektum nyilvános URL-jét.

- A konzol felajánlja a `copy public URL` lehetőséget.
- A cél annak ellenőrzése, hogy a fájl kívülről is elérhető-e.
- A demonstráció során ez nem fut teljesen simán, de a lényeg a működési elv bemutatása.

Ez a rész azt szemlélteti, hogy a bucket nemcsak tárolásra, hanem publikálásra is használható, ha a jogosultságok ezt lehetővé teszik.

## Összegzés

Az `Bpart_05.txt` fő témája a `Compute Engine` és a `Cloud Storage` első tényleges használata a konzolon keresztül. A szöveg bemutatja a böngészőből indított SSH-elérést, a virtuális gép leállítását, majd egy bucket létrehozását, konfigurálását és használatát. A rész központi tanulsága az, hogy a felhő erőforrásai néhány kattintással elérhetők, de a régió, az egyedi név, a tárolási osztály és a jogosultságok tudatos beállítása nélkül könnyen félremehet a használat.
