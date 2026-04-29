# Bpart_07 összefoglaló

## A klienskönyvtárak szerepe

Ez a rész azt mutatja meg, hogyan lehet a `Google Cloud` szolgáltatásait programkódból elérni.

- Erre a Google `client library` csomagokat biztosít.
- Ezek több programozási nyelvhez elérhetők.
- A cél az, hogy a felhő műveletei magasabb szintű absztrakción keresztül legyenek használhatók.

Az oktató hangsúlyozza, hogy ez sokkal kényelmesebb, mint mindent alacsony szinten, kézzel vagy saját protokollkezeléssel megoldani.

## Kétféle fejlesztési környezet

A programozott elérésnek két fő módja van.

- Az egyik a saját helyi fejlesztőkörnyezet.
- A másik a `Cloud Shell`, amely már eleve hitelesített.

A helyi fejlesztéshez külön kulcsok és autentikációs beállítások kellenének, ezért az oktató most az egyszerűbb, felhőn belüli megoldást választja.

## Node.js és Python tutorialok

Az oktató megmutatja, hogy a dokumentációban nyelvspecifikus tutorialok is vannak.

- Külön anyag tartozik a `Node.js`-hez.
- Külön anyag tartozik a `Python`-hoz.
- Ezeket a saját `project ID`-val kell használni.

Ez a rész arra ösztönzi a hallgatókat, hogy a felhőelérést ne csak nézzék, hanem valamelyik támogatott nyelven ki is próbálják.

## Példakód: virtuális gépek listázása

Az oktató egy `Node.js` példán keresztül mutatja be a klienskönyvtár használatát.

- A kódban meg kell adni a projektet és a zónát.
- Létrejön egy kliensobjektum.
- Ezen keresztül egy listázó metódust hívnak meg.
- Az eredmény a példányok listája lesz.

Ez a példa jól mutatja, hogy a klienskönyvtárak a felhő műveleteit egyszerű függvényhívások formájában teszik elérhetővé.

## A magasabb absztrakció előnye

Az oktató kiemeli, hogy ez a programozási forma emberbarátabb.

- Nem kell közvetlenül az alacsony szintű kommunikációval foglalkozni.
- A könyvtár elrejti a bonyolultabb háttérrészleteket.
- A fejlesztő inkább a logikára koncentrálhat.

Ez a gondolat szorosan kapcsolódik a korábban tárgyalt `RPC`-jellegű működéshez.

## A dokumentáció használata programozáshoz

Felmerül a kérdés, hogyan lehet megtalálni a szükséges metódusokat és objektumokat.

- Ehhez a referenciadokumentációt kell használni.
- A dokumentáció azonban nem mindig könnyen áttekinthető.
- A példakódok sokszor gyorsabb belépési pontot jelentenek.

Ez ismét megerősíti, hogy a felhőprogramozás egyik kulcskészsége a dokumentációban való keresés.

## A Terraform mint magasabb szintű eszköz

Az oktató röviden megemlíti a `Terraform` használatát is.

- Nagyobb rendszereknél az infrastruktúrát nem kézzel vagy egyesével kezelik.
- Ehelyett leíró jellegű keretrendszereket használnak.
- A `Terraform` tipikusan ilyen infrastruktúra-kód megoldás.

Ez a rész azt mutatja, hogy a most bemutatott alacsonyabb szintű kezelési módok mögött léteznek még magasabb szintű ipari eszközök is.

## Továbblépés az adatfeldolgozás felé

A rész végén az oktató átvezeti a témát a következő szintre.

- A puszta infrastruktúra-kezelés után az igazi kérdés az, mire használható a felhő.
- Az első nagyobb alkalmazási terület az `adatfeldolgozás`.
- Ezzel a tárgy elmozdul az infrastruktúra-szintről a platformszolgáltatások irányába.

Ez tartalmi váltást jelez a kurzusban: a gépek létrehozásától az érdemi számítási feladatok felé.

## Összegzés

Az `Bpart_07.txt` fő témája a `Google Cloud` programozott elérése klienskönyvtárakon keresztül. A szöveg bemutatja a `Cloud Shell`-ből futtatható `Node.js` és `Python` tutorialokat, a kliensobjektumok használatát és a magasabb szintű absztrakció előnyeit. A rész másik fontos tanulsága, hogy a kézi infrastruktúra-kezelés felett már léteznek ipari szintű leíró eszközök is, és a következő lépés a felhő tényleges alkalmazása lesz nagyobb adatfeldolgozási feladatokra.
