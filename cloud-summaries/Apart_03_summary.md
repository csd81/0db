# Apart_03 összefoglaló

## Az erőforrás-megosztás alapgondolata

A szöveg központi kérdése az, hogyan lehet egy erőforrást több felhasználó számára elérhetővé tenni. Ez azért fontos, mert a felhő egyik alapelve is a közösen használt erőforrások hatékony kezelése.

- Az egyik legegyszerűbb modell a `sorban állás`.
- Ez ugyanúgy működik, mint egy pénztárnál:
  - mindenki vár,
  - sorban kerül kiszolgálásra,
  - ha túl hosszú a sor, a rendszer kényelmetlenné válik.
- A korai számítógépes rendszerek is hasonló logikával működtek.

Ez a rész azt mutatja meg, hogy a felhő szempontjából alapvető erőforrás-megosztási problémák már jóval korábban is léteztek.

## Mainframe korszak és foglalásos működés

Az oktató a `mainframe` rendszereket hozza fel történeti példaként.

- Egy nagy központi gépet sok felhasználó használt.
- A programok futtatásához gyakran időpontot kellett foglalni.
- Ha valaki:
  - elfelejtette a foglalást,
  - hibás programot futtatott,
  - vagy túl sok volt a felhasználó,
  akkor újra hosszasan várhatott.

Ez hatékony központosítást jelentett, de rugalmatlan használatot eredményezett.

## A multitasking operációs rendszerek előrelépése

A következő fejlődési lépés a `multitasking` operációs rendszerek megjelenése volt.

- Ezek látszólag egyszerre több programot tudtak futtatni.
- A valóságban ez `időszeleteléssel` történt.
  - egy program fut egy rövid ideig,
  - majd a rendszer átvált a következőre,
  - így minden folyamat halad valamennyit.
- Ez főleg interaktív programoknál volt fontos.
- A felhasználó úgy érzékelte, hogy a saját programja folyamatosan fut.

Ez a modell közelebb áll a mai megosztott számítási rendszerek logikájához.

## A személyi számítógépek forradalma

A `80-as években` a mikroprocesszorok megjelenésével teljes szemléletváltás következett be.

- A korábbi modell:
  - egy nagy gépet sokan használnak.
- Az új modell:
  - mindenkinek legyen saját számítógépe.
- Ez sokkal nagyobb szabadságot adott:
  - nem kellett sorban állni,
  - nem kellett foglalni,
  - mindenki akkor dolgozhatott, amikor akart.

Ez a változás decentralizálta a számítástechnikát, de újfajta pazarlásokat és hatékonysági problémákat is létrehozott.

## Az iroda mint sok kis elszigetelt rendszer

A személyi számítógépek kora kezdetben erősen elszigetelt világ volt.

- Minden felhasználónak saját gépe volt.
- Sokszor saját `nyomtató` is tartozott hozzá.
- Az adatcsere:
  - floppy lemezekkel,
  - később más hordozókkal történt.
- Ez gazdaságtalan volt:
  - sok külön eszköz kellett,
  - mindegyiket karban kellett tartani,
  - közben sokszor alig voltak kihasználva.

Ez megmutatja, hogy a személyi számítógépes modell sem volt önmagában optimális.

## A helyi hálózatok megjelenése

A `lokális hálózatok` fontos fordulópontot jelentettek.

- Lehetővé tették, hogy több gép közösen használjon egy erőforrást.
- Erre jó példa a `print server`.
- A nyomtatási feladatok ismét sorba rendezve futottak le.
- Itt a sorban állás ismét hasznos modell lett, mert:
  - nem lehet a nyomtatást időosztásosan keverni,
  - különben az oldalak összekeverednének.

A helyi hálózat tehát javította az erőforrás-kihasználást egy vállalaton belül.

## Központi adattárolás és adatbázisok

Ha már a nyomtató megosztható, a következő logikus lépés az adatok központosítása volt.

- A cél az volt, hogy ne hordozókon kelljen adatot vinni egyik gépről a másikra.
- Ennek eredményeként megjelentek:
  - a központi adattárolók,
  - az adatbázisok,
  - az adatbázis-szerverek.
- Ez hatalmas előrelépést jelentett:
  - egyszerűbb adatmegosztás,
  - rendezettebb működés,
  - közös vállalati adatkezelés.

Ez a modell nagyjából `1980 és 2000` között uralkodóvá vált.

## A mobiltelefonok megjelenése

A `2000-es évek közepén` újabb nagy váltás történt az okostelefonok elterjedésével.

- A korábbi jelszó az volt, hogy mindenkinek legyen számítógépe.
- Az új helyzetben inkább az lett fontos, hogy mindenkinek legyen mobiltelefonja.
- A mobil eszközök sok olyan feladatot kezdtek átvenni, amit korábban PC-n végeztünk.
- Az internet elérése egyre inkább:
  - vezeték nélküli,
  - folyamatos,
  - bárhonnan elérhető lett.

Ez a változás még jobban megerősítette a hálózaton keresztüli szolgáltatásfogyasztást.

## A kör bezárul: vissza a központi adatközpontokhoz

Az oktató egyik legfontosabb gondolata, hogy a fejlődés végül részben visszatért a kezdeti központosított modellhez.

- Elindultunk a nagy központi számítógépektől.
- Eljutottunk a személyi számítógépekig.
- Onnan a mobiltelefonokig.
- Végül ismét központi adatközpontokhoz jutottunk vissza.

A különbség az, hogy ma ezek nem egyetlen nagy gépből állnak.

- Hanem:
  - szerverek ezreiből,
  - rackszekrényekbe szervezett gépekből,
  - elosztott adatközpontokból.
- A végfelhasználók pedig kis kliensekről kapcsolódnak ezekhez:
  - PC-ről,
  - laptopról,
  - mobilról.

Ez nagyon közel áll a modern felhő alapelvéhez: a számítás központilag történik, a felhasználó pedig távoli kliensként kapcsolódik.

## A web és az internet üzleti jelentősége

A szöveg második felében a `90-es évek` internetes robbanása jelenik meg.

- Kezdetben az internet a vállalatok számára nem volt különösebben érdekes.
- Az áttörést a böngészők megjelenése hozta.
- Először a böngészők egyszerűek voltak:
  - karakteresek,
  - fekete-fehérek,
  - korlátozott képességűek.
- A grafikus, majd színes böngészők megjelenésével a cégek rájöttek, hogy az internet üzleti lehetőség.

Innentől kezdve tömegesen kezdtek céges honlapokat készíteni.

## A „minden vállalatnak weboldalt” korszak

A böngészők fejlődésével kialakult az a szemlélet, hogy minden cégnek jelen kell lennie a weben.

- A cégek honlapokat készítettek:
  - termékbemutatásra,
  - szolgáltatásismertetésre,
  - marketingcélokra.
- Ez nagyon gyorsan elterjedt.
- Még olyan cégek is webes jelenlétet akartak, amelyeknek ez nem volt közvetlenül informatikai profiljuk.

Ez új üzemeltetési problémákat hozott létre.

## A helyi webszerverek problémája

A `90-es évek közepén` sok vállalat saját gépen futtatott webszervert.

- Egy cégnek nemcsak a fő tevékenysége volt jelen,
  hanem külön számítógépet is fenn kellett tartania a weboldalhoz.
- Ehhez gyakran külön informatikust kellett alkalmazni.
- Sok helyen ennek a rendszergazdának lényegében az volt a feladata, hogy:
  - figyelje a gépet,
  - újraindítsa, ha gond van,
  - biztosítsa, hogy a weboldal működjön.

Ez tipikus példa arra, amikor egy technikai szükséglet túl nagy helyi terhet rak a vállalatra.

## A hosting mint első kiszervezési lépés

Erre a problémára válaszként megjelentek a `hosting` szolgáltatók.

- A hosting cégek azt mondták:
  - ne a saját irodában tartsátok a webszervert,
  - vigyétek be hozzánk,
  - mi biztosítjuk az áramot, hálózatot és az alapüzemeltetést.
- Az ügyfél gépe továbbra is az ő gépe volt,
  de már nem neki kellett helyben őrizni és folyamatosan működtetni.

Ez fontos átmeneti lépés volt a felhő felé.

- A számítás még nem teljesen vált szolgáltatássá,
- de az üzemeltetés már kezdett kiszerveződni.

## Az egységesítés iránya

A szöveg végén az oktató arra utal, hogy a hosting cégek következő természetes lépése az infrastruktúra egységesítése lett.

- Nem hatékony, ha minden ügyfél teljesen eltérő saját gépet hoz.
- Az üzemeltetés sokkal egyszerűbb, ha a háttérrendszerek szabványosítottak.
- Ez már közvetlenül a modern, központilag kezelt felhőinfrastruktúra felé vezet.

Itt kezd kialakulni az a logika, hogy az ügyfél már ne saját fizikai gépet vigyen be, hanem szolgáltatásként kapjon egységes erőforrásokat.

## Összegzés

Az `Apart_03.txt` fő témája az erőforrás-megosztás történeti fejlődése a mainframe rendszerektől a személyi számítógépeken, helyi hálózatokon és mobil eszközökön át a központi adatközpontokhoz való visszatérésig. A szöveg egyik legfontosabb tanulsága, hogy a mai felhő nem teljesen új jelenség, hanem a korábbi központosított számítás modern, hálózati és elosztott formája. Emellett a rész azt is megmutatja, hogyan vezetett a web üzleti elterjedése és a webszerverek üzemeltetési terhe a hosting szolgáltatások megjelenéséhez, ami már közvetlen előfutára a felhőnek.
