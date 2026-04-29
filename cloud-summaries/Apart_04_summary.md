# Apart_04 összefoglaló

## A mai értelemben vett felhő megjelenése

A szöveg elején az oktató az idővonal végére ugrik, hogy összekösse a korábbi fejlődést a modern felhővel.

- A `2000-es években` megerősödik a `szolgáltatásorientált` technológia.
- Erre építve egyes cégek elkezdenek tényleges szolgáltatásokat fejleszteni.
- Az első nagy szereplő az `Amazon`.
- Később követi a `Google` és a `Microsoft`.
- `2005–2006` környékén jelennek meg az első valódi, publikus felhőrendszerek.
- Kezdetben ezek főként:
  - infrastruktúrát,
  - alap szolgáltatásokat,
  - futtató környezeteket kínáltak.

Az oktató szerint innen, a 2000-es évek közepétől beszélhetünk a mai értelemben vett felhőtechnológiáról.

## A piac stabilizálódása

A szöveg kiemeli, hogy a felhő gyorsan kinőtt az újdonság státuszból.

- `2008–2009` körül a Google és a Microsoft is belépett a piacra.
- `2010` óta ez a három szereplő vált meghatározóvá:
  - Amazon
  - Google
  - Microsoft
- Innentől a felhő már nem kísérleti technológia, hanem beérett üzletág.

A hangsúly tehát már nem az alapötlet újdonságán, hanem a folyamatos fejlesztésen és bővülésen van.

## A nagy felhőplatformok szolgáltatásgazdagsága

Az oktató megmutatja, hogy a nagy szolgáltatók mára mennyire széles portfóliót kínálnak.

- Tipikus kategóriák:
  - `compute`
  - `storage`
  - `database`
  - `network`
  - fejlesztői eszközök
  - menedzsment
  - biztonság
  - médiaszolgáltatások
  - gépi tanulás
  - mobil
  - integráció
  - üzleti alkalmazások
  - streaming
  - szenzoros / IoT megoldások
  - játék és egyéb speciális területek
- Az `Amazon`, `Microsoft` és `Google` kínálata szerkezetileg nagyon hasonló.

Ez a rész azt mutatja, hogy a felhő ma már nem pusztán virtuális szervereket jelent, hanem teljes szolgáltatási ökoszisztémát.

## A kurzus gyakorlati platformja

A szöveg alapján a kurzusban a `Google Cloud Platform` lesz a gyakorlati környezet.

- Először a `Compute Engine` kerül előtérbe.
- Ez lényegében egy virtuális gép.
- Később további szolgáltatások is szóba kerülnek:
  - adattárolás,
  - `Cloud Functions`,
  - big data feldolgozás,
  - AI-jellegű szolgáltatások.

Az oktató jelzi, hogy a hálózati rendszergazdai részletekkel nem fognak mélyen foglalkozni, inkább a használható, fejlesztői szempontból fontos szolgáltatásokra fókuszálnak.

## Mi az elosztott rendszer?

A következő nagy témakör az `elosztott rendszerek` világa, amely a felhő egyik technikai alapja.

- Egy elosztott rendszer nem egyetlen számítógépből áll.
- Több, hálózaton összekapcsolt gép működik együtt benne.
- Ezek a gépek:
  - nem feltétlenül ugyanazt csinálják,
  - különböző szerepköröket láthatnak el,
  - közösen oldanak meg nagyobb feladatokat.
- Lehetnek közöttük például:
  - adatbázis-szerverek,
  - számítási szerverek,
  - más speciális komponensek.

Az oktató ezt csapatmunkaként írja le: sok különálló gép együtt alkot egy működő rendszert.

## A kliens-szerver architektúra alapja

Az elosztott rendszerek legfontosabb alapmintája a `kliens-szerver` modell.

- A `kliens`:
  - a felhasználó gépe vagy eszköze,
  - például PC, laptop vagy mobiltelefon.
- A `szerver`:
  - a távoli rendszer,
  - amely funkcionalitást nyújt.
- A kliens feladata:
  - kapcsolatot kezdeményezni,
  - elküldeni a kérést,
  - fogadni a választ.
- A szerver feladata:
  - várni a kéréseket,
  - feldolgozni azokat,
  - visszaküldeni az eredményt.

Az oktató a `Teams` rendszerét hozza fel példának: a böngésző kliensként viselkedik, a háttérben működő Teams-szerver pedig kiszolgálja a kéréseket.

## Request-response működés

A kliens-szerver rendszer lényege a kérés-válasz modell.

- A kliens először `requestet` küld.
- A szerver ezt feldolgozza.
- Ezután `response` formájában választ küld vissza.
- Webes környezetben ez tipikusan:
  - egy `HTTP request`,
  - majd egy `HTTP response`.

A válasz lehet például:

- HTML oldal,
- adat,
- üzenet,
- vagy más tartalom.

Ez az alapminta a legtöbb modern hálózati alkalmazás működésének középpontjában áll.

## Miért fontos a központi szerver?

Az oktató kiemeli, hogy a szerver célja nem az, hogy egyetlen felhasználót szolgáljon ki.

- A szerver funkcionalitását sok kliens között osztják meg.
- Példa:
  - egy pénzügyi osztályon 20 ember ugyanazt a rendszert használja,
  - ugyanazt a központi adatbázist érik el,
  - nem különálló, széttagolt rendszerekben dolgoznak.

Ez előnyös, mert:

- központi adatkezelést ad,
- egyszerűbb a karbantartás,
- elkerülhető az adatduplikáció,
- jobban kontrollálható a működés.

Ugyanakkor technikai problémákat is felvet, például párhuzamos írás és konzisztencia kérdését.

## A kliens-szerver programozás alacsony szinten

A szöveg végén az oktató a programozási oldal felé fordul, és megmutatja, hogyan történik mindez alacsony szinten.

- A kliensnek először kapcsolatot kell létrehoznia a szerverrel.
- Ez tipikusan `TCP` kapcsolaton keresztül történik.
- A programban ezt `socket` segítségével lehet megvalósítani.
- A kapcsolat létrejötte után:
  - létre kell hozni az üzenetet,
  - bele kell csomagolni a parancsot vagy adatot,
  - el kell küldeni a szervernek.
- A szerver:
  - fogadja,
  - kicsomagolja,
  - végrehajtja a műveletet,
  - majd újra becsomagolva visszaküldi az eredményt.
- A kliens ezután:
  - megvárja a választ,
  - kicsomagolja,
  - értelmezi.

Ez egy teljes hálózati kommunikációs ciklus.

## Miért problémás ez a modell?

Az oktató szerint ez a megközelítés rendkívül alacsony szintű.

- Minden egyes kérésnél újra és újra végig kell csinálni ugyanazokat a lépéseket.
- A programozónak minden kommunikációs helyzetre külön kell kezelnie:
  - az üzenet felépítését,
  - a válasz értelmezését,
  - a kapcsolatkezelést.
- Ez:
  - fárasztó,
  - ismétlődő,
  - hibalehetőségekkel teli munka.

Ráadásul ez a programozási modell nem hasonlít a hagyományos, kényelmes lokális függvényhívásos gondolkodásra, ezért természetellenesebb és nehezebben kezelhető.

## Összegzés

Az `Apart_04.txt` összekapcsolja a modern felhő kialakulását az elosztott rendszerek és a kliens-szerver architektúra alapjaival. A szöveg bemutatja, hogyan jelent meg a mai értelemben vett felhő a 2000-es évek közepén, majd rátér arra, hogy a felhő technikai értelemben hálózaton együttműködő gépek rendszere. A rész második fő tanulsága, hogy a kliens-szerver kommunikáció alacsony szinten nagyon bonyolult és ismétlődő programozási feladat, ami később indokolja a magasabb absztrakciós szintű megoldások megjelenését.
