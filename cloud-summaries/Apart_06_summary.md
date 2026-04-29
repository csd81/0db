# Apart_06 összefoglaló

## A szolgáltatás absztrakciója

A szöveg eleje továbbviszi az előző rész gondolatát: a kliens számára az a fontos, hogy ne alacsony szintű hálózati részletekkel kelljen foglalkoznia, hanem egy magasabb szintű szolgáltatást lásson.

- A kliens ideális esetben nem azt látja, hogy:
  - van egy `IP-cím`,
  - van egy `port`,
  - üzeneteket kell összeállítani,
  - kapcsolatokat kell menedzselni.
- Ehelyett azt látja, hogy van egy `interface`, amely leír egy szolgáltatást.
- Például egy nyomtató esetén az interface megadhatja:
  - be van-e kapcsolva,
  - milyen felbontásban dolgozzon,
  - színes vagy fekete-fehér nyomtatás történjen,
  - és végül egy `print` műveletet.

A lényeg az, hogy a kliensoldali program egyre magasabb absztrakciós szinten tudja leírni az üzleti logikát. Nem az átvitel technikai részleteire figyel, hanem a szolgáltatás használatára.

## Szervercsere és újracsatlakozás

A szöveg egy fontos gyakorlati problémát is megemlít: mi történik, ha a szerver leáll.

- Ha egy adott szerver elromlik, lehet indítani egy újat.
- Az új szerver első lépésként regisztrálja magát a `registry` rendszerben.
- A kliens, amikor újra keres egy adott szolgáltatást:
  - már az új szerver adatait kapja vissza,
  - és ahhoz tud kapcsolódni.

Ez azt mutatja, hogy a rendszer nem egyetlen fix géphez kötött, hanem a szolgáltatás új példányaival is képes tovább működni. Ez már a későbbi felhős gondolkodás egyik fontos előzménye.

## Továbblépés a platformfüggetlenség felé

Az oktató itt rámutat arra, hogy a Java-alapú megoldások hasznosak voltak, de túl szűkek.

- A probléma az volt, hogy a `Java RMI` Java-specifikus.
- Ez azt jelenti, hogy:
  - erősen kötődik egy nyelvhez,
  - nem elég rugalmas heterogén rendszerekhez.
- A következő cél tehát az lett, hogy a távoli szolgáltatások használata ne legyen egyetlen technológiához láncolva.

Ez a gondolat vezette tovább az elosztott rendszereket a webes, HTTP-alapú és szolgáltatásorientált megoldások felé.

## A Microsoft-vonal: DCOM

A szöveg röviden kitér a Microsoft saját technológiájára is.

- A Windows világában léteztek `COM` objektumok.
- Ezek moduláris komponensek voltak Windows-alkalmazások felépítéséhez.
- Ennek elosztott változata volt a `DCOM` (`Distributed COM`).
- A DCOM lényegében hasonló célt szolgált, mint a Java RMI:
  - objektumok és komponensek elosztott környezetben való használatát.

Ez jól mutatja, hogy több platform is saját módon próbálta megoldani az elosztott programozás problémáját.

## Áttérés a webre

Az oktató jelzi, hogy a következő fontos állomás a webes, `HTTP` alapú, szolgáltatásorientált kommunikáció lesz.

- Ez azt jelenti, hogy:
  - a távoli szolgáltatások már nem csak speciális RPC-rendszereken keresztül érhetők el,
  - hanem a web technológiáira épülnek.
- Ez a megközelítés sokkal jobban illeszkedik az internet világához.
- Egyben ez készíti elő a modern felhőszolgáltatások működését is.

Innen a fókusz részben eltolódik a programozási oldalról az infrastruktúra felé.

## Mi az a grid számítás?

A szöveg második nagy témája a `grid számítási rendszerek` világa.

- A grid az elosztott rendszerek egy speciális formája.
- Kifejezetten:
  - nagy számítási feladatokra,
  - nagy adatfeldolgozási igényekre,
  - nagy teljesítményű erőforrások összehangolt használatára találták ki.
- A történeti háttér a `szuperszámítógépekhez` kapcsolódik.

A grid tehát nem általános vállalati informatikai modellként indult, hanem nagy tudományos és műszaki számítások támogatására.

## A szuperszámítógépek problémája

A korai szuperszámítógépek nagyon erősek voltak, de elszigetelten működtek.

- A `80-as években` ezek:
  - rendkívül drága,
  - nagy teljesítményű,
  - központilag őrzött rendszerek voltak.
- A használatuk gyakran sorban állásos módon történt.
- Ha több központ létezett egy országban:
  - mindegyiket a helyi felhasználók használták,
  - de nem volt egyszerű átirányítani a terhelést egyik központból a másikba.

Ez erőforrás-kihasználási problémát okozott.

- Az egyik helyen túlterhelés lehetett.
- A másik helyen közben szabad kapacitás maradt.

A grid ötlete részben erre a problémára adott választ.

## A grid alapötlete

A fő elképzelés az volt, hogy a különálló nagy teljesítményű rendszereket hálózaton keresztül össze kell kötni.

- A felhasználónak ne kelljen megmondania:
  - melyik gépen fusson a feladat,
  - hol van szabad kapacitás,
  - melyik központot használja.
- Ehelyett csak azt kelljen mondania:
  - `ezt a feladatot szeretném lefuttatni`.
- A rendszer pedig:
  - megtalálja a megfelelő erőforrást,
  - kiválasztja a legalkalmasabb gépet,
  - elindítja rajta a feladatot.

Ez nagyon hasonlít a mai felhős gondolkodáshoz: a felhasználó szolgáltatást kér, nem konkrét hardvert.

## A "grid" elnevezés jelentése

A `grid` elnevezés az elektromos hálózat analógiájából származik.

- Ahogy az elektromos hálózatnál:
  - bedugunk egy eszközt a konnektorba,
  - és nem foglalkozunk vele, melyik erőmű termeli az áramot,
- ugyanígy a grid esetén:
  - csatlakozunk a hálózathoz,
  - és a számítási kapacitást szolgáltatásként kapjuk.

Ez a hasonlat nagyon fontos, mert jól megfogja az egész koncepció lényegét: az erőforrás háttere el van rejtve a felhasználó elől.

## Magas szintű felhasználói kérések

A szöveg szerint a grid egyik nagy célja az volt, hogy a felhasználó ne technikai nyelven fogalmazza meg az igényeit.

- A felhasználó mondhat például ilyesmit:
  - egy nagy részecskeszimulációt szeretne futtatni,
  - sok paraméterkombinációval akar vizsgálatot végezni,
  - virtuális együttműködési teret szeretne egy interaktív alkalmazáshoz.
- Ezek a kérések nem tartalmaznak konkrét infrastruktúra-adatokat.
- A rendszer feladata, hogy ezeket lefordítsa technikai követelményekké:
  - mekkora számítási kapacitás kell,
  - mennyi memória kell,
  - mekkora késleltetés fogadható el,
  - milyen egyéb erőforrás-feltételek szükségesek.

Ez a szemlélet nagyon közel áll a modern szolgáltatásalapú rendszerekhez.

## A broker és az erőforráskezelés

A gridben egy központi szereplő értelmezi ezeket a magas szintű igényeket.

- Ez a komponens a `broker`.
- Feladata:
  - a kérés értelmezése,
  - annak átalakítása informatikai követelményekké,
  - megfelelő erőforrások keresése,
  - a futás megszervezése.
- Ehhez szükség van egy folyamatosan frissülő információs rendszerre is.
- Ennek tudnia kell:
  - hány gép van a rendszerben,
  - ezek milyen paraméterekkel rendelkeznek,
  - mennyire terheltek,
  - milyen erőforrások szabadok.

Ez tulajdonképpen már erőforrás-virtualizációs és szolgáltatásmenedzsment gondolkodás.

## A technikai megvalósítás: Globus

A szöveg konkrét példaként a `Globus` rendszert említi.

- Ez egy szoftverkörnyezet volt grid számítási rendszerekhez.
- Alul helyi `batch` végrehajtási rendszerek működtek.
  - Ezek kezelték a helyi futási sorokat.
- Fölöttük helyezkedett el a `GRAM`
  - `Globus Resource Allocation Manager`.
- A GRAM feladata:
  - helyi információk gyűjtése,
  - kommunikáció a magasabb szintű grid rendszerrel,
  - helyi futtatások végrehajtásának kezelése.
- Legfelül a `broker` dolgozta fel a kliens kérését.
- A kliens kérését egy `RSL` (`Resource Specification Language`) írta le.
- A broker:
  - ezt értelmezte,
  - megkereste a megfelelő gépeket,
  - lefoglalta az erőforrásokat,
  - majd elindította a programot.

Ez már nagyon hasonlít a mai felhő egyik alaplogikájára: a felhasználó leírja, mit szeretne, a rendszer pedig megszervezi a végrehajtást.

## Kapcsolat a modern felhővel

Az oktató külön ki is emeli, hogy ha a grid technikai részleteit félretesszük, akkor a mögötte levő gondolat nagyon közel áll a mai felhő működéséhez.

- A felhasználó ma sem konkrét gépeket akar kiválasztani.
- Inkább magas szintű műveleteket kér.
- Például a `Gmail` használatakor:
  - nem szervert választunk,
  - nem IP-címet adunk meg,
  - nem adatközpontot választunk,
  - csak megírjuk az emailt és elküldjük.
- A háttérben a rendszer:
  - kiválasztja a szükséges erőforrásokat,
  - tárolja az adatokat,
  - kezeli a kiszolgálást,
  - végrehajtja a műveleteket.

Ugyanez a logika jelenik meg később a `serverless` modellekben is.

- A felhasználó egyszerűen beküld egy programot vagy függvényt.
- A rendszer gondoskodik arról, hogy az hol és hogyan fusson le.

## A grid korlátja

A szöveg végén az oktató arra utal, hogy bár a grid technológia fontos előfutár volt, alapvetően speciális feladatokra összpontosított.

- Főként:
  - nagy tudományos számításokra,
  - nagy adatfeldolgozási munkákra,
  - speciális kutatási igényekre készült.
- Ilyen feladatból viszont a világban viszonylag kevés van.
- Az üzleti világ tipikus problémái sokszor más jellegűek.

Vagyis a grid fontos technikai és gondolati előkép volt, de a modern felhő ennél szélesebb, általánosabb és üzletileg sokkal jobban hasznosítható modellé vált.

## Összegzés

Az `Apart_06.txt` két fontos témát kapcsol össze. Egyrészt továbbviszi a kliens-szerver és szolgáltatásorientált gondolkodást azzal, hogy a kliens már nem gépeket és portokat lát, hanem magas szintű szolgáltatásokat. Másrészt bemutatja a `grid számítási rendszereket`, amelyek a szuperszámítógépek világából indultak, és azt a célt tűzték ki, hogy a számítási kapacitás hálózaton keresztül, szolgáltatásként legyen elérhető. A rész legfontosabb tanulsága, hogy a mai felhő alapötletei közül sok már a grid rendszerekben megjelent: a felhasználó igényt fogalmaz meg, a rendszer pedig elrejti előle az infrastruktúra konkrét működését és megszervezi a végrehajtást.
