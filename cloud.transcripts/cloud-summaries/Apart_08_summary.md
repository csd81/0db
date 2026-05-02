# Apart_08 összefoglaló

## Átmenet a korai szolgáltatásoktól a modern API-kig

A szöveg elején az oktató röviden összefoglalja a szolgáltatáselérési modellek fejlődését.

- A legkorábbi megoldások még `XML`-alapúak voltak.
- Ezután megjelentek a `REST`-alapú, de még `RPC-szerű`, szinkron hívási modellek.
- Később ebből alakult ki a teljesebb, modernebb `REST API` szemlélet.
- A végrehajtás egyre inkább:
  - lazábban csatolt,
  - aszinkronabb,
  - szolgáltatásközpontúbb lett.

Ez a rész azt hangsúlyozza, hogy a felhőtechnológiák mai formája több fejlődési lépés eredménye, nem egyszerre jelent meg.

## Korai "konténertechnológia" mint infrastruktúraötlet

Az oktató egy érdekes történeti példát hoz a korai infrastruktúraszolgáltatásokra.

- A `Sun` egy fizikai konténeralapú megoldást talált ki.
- A cél az volt, hogy a vállalatok számára gyorsan biztosítható legyen extra számítási kapacitás.
- A modell lényege:
  - egy konténerbe szervereket építettek,
  - ezt fizikailag oda lehetett szállítani a céghez,
  - áramot és hálózatot kellett csak csatlakoztatni,
  - és máris működött a szerverpark.

Ez a megoldás a korábbi problémára adott választ: hogyan lehet gyorsan plusz infrastruktúrát adni csúcsidőszakban.

## A nagy felismerés: nem kell a céghez vinni

A valódi áttörés nem maga a szállítható konténer volt, hanem az a felismerés, hogy ezt nem feltétlenül kell az ügyfél telephelyére vinni.

- A konténereket lehetett volna egy központi helyen tartani.
- Az ügyfelek interneten keresztül kapcsolódhattak volna hozzájuk.
- Innentől a modell már nagyon közel került a mai felhőhöz:
  - az infrastruktúra távol van,
  - a felhasználó csak igénybe veszi,
  - a működtetés nem az ő feladata.

Ez lényegében a távoli, bérelhető számítási kapacitás egyik korai formája volt.

## Utility computing

Az oktató ezt a modellt a `utility computing` egyik első megjelenési formájaként mutatja be.

- A `utility` logika ugyanaz, mint a közüzemeknél:
  - víz,
  - villany,
  - gáz.
- Nem az infrastruktúrát vesszük meg, hanem a fogyasztás után fizetünk.
- A példában:
  - `CPU-óra` alapú elszámolás volt,
  - a tárolásnak is fix ára volt.
- A vállalat:
  - bérli az erőforrást,
  - használja, ameddig kell,
  - és utána csak a fogyasztást fizeti.

Ez a modell már nagyon közvetlen előképe a mai "pay as you go" felhős árazásnak.

## Üzleti felhasználási példa

A szöveg egy konkrét, üzleti világban megjelenő példát is hoz.

- Egy angol szakember a londoni pénzügyi szektorban használt ilyen infrastruktúrát.
- A probléma az volt, hogy hatalmas `Excel` modellek futottak, amelyek órákig tartó számításokat végeztek.
- Ő ezt úgy gyorsította fel, hogy:
  - a számítási részt kivitte a `Sun Grid Utility` rendszerre,
  - az Excel tábla megmaradt a megszokott formában,
  - a háttérben viszont párhuzamos számítás történt.
- Az eredmény:
  - a többórás feldolgozás percekre csökkent,
  - az ügyfelek nyertek vele,
  - és a szolgáltatás üzletileg is profitábilis volt.

Ez azt mutatja, hogy már a korai infrastruktúraszolgáltatások is komoly üzleti előnyöket adhattak.

## A virtualizáció szerepe

A szöveg következő nagy témája a `virtualizáció`, amely az egyik legfontosabb technológiai alapja a mai felhőnek.

- Korábban egy fizikai gépen:
  - egy operációs rendszer futott,
  - arra telepítették a programokat,
  - ezek erősen kötődtek az adott hardverhez.
- Ez sok problémát okozott nagy szerverparkoknál:
  - eltérő hardverek,
  - eltérő operációs rendszerek,
  - nehézkes áthelyezés,
  - rossz erőforrás-kihasználás.

A virtualizáció ezt a heterogenitást kezdte el kezelni.

## Mit old meg a virtualizáció?

Az oktató szerint a virtualizáció több kritikus problémát egyszerre old meg.

- Egységesebb környezetet ad.
- Elrejti a fizikai hardver és host operációs rendszer részleteit.
- Lehetővé teszi, hogy:
  - ugyanaz a virtuális gép többféle fizikai környezetben is fusson,
  - egy Windows-hoston Linux vendég fusson,
  - vagy fordítva.
- A felhasználó szempontjából sokkal kevésbé számít, milyen fizikai gép van alatta.

Ez üzemeltetési és skálázási szempontból is kulcsfontosságú.

## Több virtuális gép egy fizikai szerveren

A virtualizáció másik nagy előnye az erőforrások jobb kihasználása.

- Egy fizikai szerveren nem csak egy rendszer futhat.
- Több `virtuális gép` is elhelyezhető rajta.
- Ha egy feladat kis terhelést jelent:
  - több hasonló VM is elfér ugyanazon a gépen.
- Ha egy feladat nagy terhelést jelent:
  - akár egyedül is elfoglalhatja az egész szervert.

Ez azt teszi lehetővé, hogy a rendelkezésre álló hardvert sokkal rugalmasabban használják ki.

## Mozgathatóság és üzemeltetési előny

A virtualizáció nemcsak futtatási, hanem menedzsmentelőnyt is ad.

- A virtuális gépek:
  - előre telepített állapotban tárolhatók,
  - image formában menthetők,
  - egyik fizikai gépről a másikra vihetők.
- Nem kell mindent újratelepíteni.
- Egy adott futtatási környezet gyorsan újraindítható másik szerveren is.

Ez az egyik oka annak, hogy a modern adatközpontok működése elképzelhetetlen virtualizáció nélkül.

## A felhő három fő szolgáltatási szintje

A szöveg végére az oktató eljut a valódi felhőszolgáltatási modellekhez.

- Három fő szint jelenik meg:
  - `Infrastructure as a Service` (`IaaS`)
  - `Platform as a Service` (`PaaS`)
  - `Software as a Service` (`SaaS`)

Ezek azt mutatják meg, hogy a szolgáltató és a felhasználó hogyan osztja meg egymás között a felelősséget.

## On-premises modell

A kiindulópont a helyi infrastruktúra, vagyis az `on-premises` működés.

- Ebben a modellben mindent a vállalat csinál:
  - hardver beszerzés,
  - telepítés,
  - üzemeltetés,
  - operációs rendszer,
  - futtatókörnyezet,
  - alkalmazások,
  - biztonság,
  - működtetés.
- Ez sok helyen szükséges lehet, de általában:
  - drága,
  - bonyolult,
  - nem a legtöbb cég fő tevékenysége.

Az oktató szerint ahol a vállalat fő profilja nem informatika, ott ez gyakran inkább szükséges teher.

## IaaS: infrastruktúra mint szolgáltatás

Az első felhős szint az `IaaS`.

- Itt a felhasználó virtualizált hardverkörnyezetet kap.
- Például:
  - virtuális gépeket,
  - tárolási lehetőséget,
  - alapinfrastruktúrát.
- Viszont a felhasználó feladata marad:
  - operációs rendszer telepítése,
  - middleware,
  - futtatókörnyezet,
  - saját szoftverek kezelése.

Ez azoknak előnyös, akik saját informatikai architektúrával rendelkeznek, de nem helyben akarják futtatni azt.

## PaaS: platform mint szolgáltatás

A következő szint a `PaaS`.

- Itt a szolgáltató már futtatókörnyezetet is ad.
- A felhasználónak nem kell az alaprendszert üzemeltetni.
- Neki főleg ezek maradnak:
  - az alkalmazás fejlesztése,
  - saját adatok kezelése,
  - saját üzleti logika biztosítása.
- Példák:
  - adatbázis-platform,
  - webszerver-platform,
  - alkalmazásfuttató környezetek.

Ez már jelentősen csökkenti az üzemeltetési terhet.

## SaaS: szoftver mint szolgáltatás

A legmagasabb absztrakciós szint a `SaaS`.

- Itt a felhasználó már kész szoftvert kap.
- Nem fejleszt, nem üzemeltet, nem menedzsel infrastruktúrát.
- Egyszerűen használja a szolgáltatást.
- Tipikus példák:
  - `Gmail`
  - `Teams`
  - `Netflix`
  - `Facebook`

Ebben a modellben a technológiai háttér szinte teljesen láthatatlan a végfelhasználó számára.

## Kinek mi a feladata?

A szöveg egyik kulcsfontosságú üzenete az, hogy a három modell közti fő különbség a felelősségmegosztásban van.

- `On-premises`: szinte minden a felhasználóé.
- `IaaS`: az infrastruktúrát a szolgáltató adja, a felsőbb rétegek a felhasználónál maradnak.
- `PaaS`: a szolgáltató a futtatókörnyezetet is biztosítja.
- `SaaS`: szinte mindent a szolgáltató kezel.

Ez a felhőszolgáltatások egyik legalapvetőbb értelmezési kerete.

## PaaS valós architektúrában

A szöveg végén az oktató elkezd mutatni egy konkrét, valós `PaaS` jellegű architektúrát is.

- A szolgáltató adja:
  - a platformot,
  - a futtatási környezetet,
  - az adatközponti infrastruktúrát,
  - a kiszolgáló réteget.
- A megrendelő főként az alkalmazást szolgáltatja.
- Megjelenik egy `load balancing` réteg is.
- Ez lehetővé teszi, hogy:
  - normál esetben a forgalom egy fő adatközpontba menjen,
  - hiba esetén vagy csúcsterhelésnél másik központ is bevonható legyen.

Ez már közvetlenül a magas rendelkezésre állás és a felhős skálázás világába vezet át.

## Összegzés

Az `Apart_08.txt` fő témája az, hogyan jutunk el a korai szolgáltatáselérési modellektől és infrastruktúraötletektől a mai felhőszolgáltatási modellekig. A szöveg bemutatja a `utility computing` korai megjelenését, a `virtualizáció` kulcsszerepét, majd a három alapvető felhőszintet: `IaaS`, `PaaS`, `SaaS`. A legfontosabb tanulság az, hogy a felhő nem egyetlen technológia, hanem több korábbi megoldás összeérő eredménye, amelynek lényege a rugalmas erőforrás-használat, az absztrakció és a felelősség fokozatos átrendezése a felhasználó és a szolgáltató között.
