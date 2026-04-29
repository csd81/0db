# Apart_07 összefoglaló

## A web service technológia eredete

A szöveg elején az oktató azt magyarázza, hogyan nőtt ki a korábbi elosztott rendszerekből a `web service` technológia.

- A web service-ek a korábbi:
  - `grid` rendszerek,
  - szolgáltatásorientált architektúrák,
  - távoli szolgáltatáshívási modellek
  továbbfejlődéséből jöttek létre.
- A cél az volt, hogy a grid világában megjelent szolgáltatáselvű gondolkodást átültessék az üzleti informatikába.
- A `2000-es évek elején` ez nagyon népszerű irány lett.
- Az `Amazon Web Services` korai formája is nagyon közel állt ehhez a világhoz.

A fő gondolat itt az, hogy a felhő üzleti oldala nem a semmiből jelent meg, hanem korábbi kutatási és elosztott rendszerszemléleti megoldásokra épült.

## A szolgáltatásorientált szemlélet megmaradt

Az oktató hangsúlyozza, hogy bár a konkrét technológia sokat változott, a mögötte álló alapötlet megmaradt.

- A legfontosabb gondolat az, hogy:
  - a felhasználót nem a fizikai infrastruktúra érdekli,
  - hanem az, hogy egy adott funkció elérhető legyen.
- A felhasználó szempontjából nem fontos:
  - melyik gépen fut a szolgáltatás,
  - milyen IP-címen van,
  - pontosan hogyan van implementálva.
- A fontos az, hogy az `interface` stabil legyen.
- Ha a kliens csak az interfészt látja, akkor a háttérben:
  - lehet szervereket cserélni,
  - lehet skálázni,
  - lehet a rendszert átszervezni
  anélkül, hogy a kliensoldali működés sérülne.

Ez a rész nagyon fontos, mert az oktató szerint csak ilyen absztrakcióval lehet igazán skálázható nagy rendszereket építeni.

## A web service alapmintája

A web service architektúra alapvetően ugyanarra a mintára épül, mint a korábbi elosztott szolgáltatási modellek.

- Három fő szereplő van:
  - `service consumer`
  - `service provider`
  - `registry`
- A `service consumer`:
  - lehet ember,
  - lehet kliensprogram,
  - lehet másik szolgáltatás vagy szerver.
- A `service provider` nyújtja a funkcionalitást.
- A `registry` nyilvántartja, hogy milyen szolgáltatások érhetők el.

A működés logikája ugyanaz marad:

- a szolgáltatás elindul,
- regisztrálja magát,
- a kliens keres,
- megtalálja a megfelelő szolgáltatást,
- majd kapcsolatba lép vele.

Ez tehát egy általános szolgáltatáskeresési és -használati modell.

## Minden XML-alapú volt

A web service-ek egyik központi jellemzője az volt, hogy gyakorlatilag minden `XML`-re épült.

- Az interfészleírás XML-ben történt.
- Az üzenetformátum XML-ben volt.
- A szolgáltatáskereséshez használt struktúrák is XML-alapúak voltak.
- Az egész rendszer célja az volt, hogy:
  - nyelvfüggetlen maradjon,
  - interoperábilis legyen,
  - ne kötődjön egyetlen programnyelvhez sem.

A korabeli gondolkodás szerint ez jó ötletnek tűnt, mert az XML semleges formátumnak számított, és gépi feldolgozásra is alkalmas volt.

## A fő technikai elemek

A szöveg több fontos rövidítést és réteget is említ, amelyek a klasszikus XML-alapú web service világ részei.

- `WSDL`
  - `Web Services Description Language`
  - XML-alapú szolgáltatásleíró nyelv
  - ez írja le, hogy a szolgáltatás mit tud
- `SOAP`
  - XML-alapú üzenetformátum és protokoll
  - ezen keresztül kommunikál a kliens és a szerver
- `UDDI`
  - registry jellegű komponens
  - a szolgáltatások nyilvántartására és keresésére szolgál

A szoftverstack rétegesen épült fel:

- legalul a `HTTP` volt mint szállítási réteg,
- fölötte az XML/SOAP üzenetkezelés,
- utána a szolgáltatásleírás,
- majd a discovery / registry réteg,
- fölé pedig további képességek épültek.

## A rendszer túlzott bonyolultsága

Az oktató egyik legerősebb kritikája az, hogy a web service világ a végére túlkomplikálttá vált.

- Az alaprétegeken felül további rétegek épültek rá:
  - `quality of service`
  - `security`
  - tranzakciókezelés
  - koordináció
  - kontextuskezelés
  - workflow
  - üzleti folyamatintegráció
  - menedzsment
- A rendszerből gyakorlatilag egy programozási nyelv nélküli „programozási világ” lett.
- Az XML köré teljes infrastruktúrát kellett építeni:
  - feldolgozók,
  - parser-ek,
  - értelmező rétegek,
  - végrehajtási logikák.

Az oktató ezt elrettentő példaként mutatja: ha túl sok mindent akarunk egyetlen univerzális technológiával megoldani, az végül kezelhetetlenné válhat.

## A teljesítményprobléma

A másik nagy gond a hatékonyság hiánya volt.

- A bináris adatokat XML-re kellett átkódolni.
- Ez azt jelentette, hogy:
  - a tényleges adatméret nagyon megnőtt,
  - sok extra strukturális információ utazott a hálózaton,
  - a kódolás és dekódolás is lassú volt.
- Egy kis adatból könnyen sokkal nagyobb XML-struktúra lett.
- Emiatt:
  - az internetes forgalom jelentősen nőtt,
  - a rendszerek lassabbak lettek,
  - a feldolgozás költségesebbé vált.

Az oktató szerint a túlzott interoperabilitási törekvés miatt a hatékonysági szempontokat gyakorlatilag háttérbe szorították.

## Mi maradt meg belőle?

A szöveg szerint a klasszikus XML-alapú web service modell ma már nagyrészt háttérbe szorult.

- Ma már főként `legacy` rendszerekben jelenik meg.
- Régebbi vállalati rendszerek még ma is használhatják.
- Példaként említésre kerül:
  - `NAV` rendszerek,
  - bizonyos Microsoft üzleti rendszerek.
- Új rendszereknél viszont ez a technológia jellemzően már nem számít elsődleges választásnak.

A tanulság az, hogy a koncepció fontos volt, de a konkrét megvalósítás túl nehézkesnek bizonyult.

## A REST megjelenése

Amikor a klasszikus web service modell túl bonyolulttá vált, megjelent egy egyszerűbb alternatíva: a `REST`.

- A REST lényege, hogy:
  - nem funkcionális interfészekben gondolkodik,
  - hanem erőforrásokban és végpontokban (`URL`).
- Nem olyan műveleteket írunk le, mint:
  - `getStatus`
  - `setResolution`
  - `print`
- Ehelyett azt mondjuk:
  - van egy URL,
  - azon keresztül `HTTP` műveletekkel lehet dolgozni.
- Például:
  - `GET` lekérdez információt,
  - `POST` adatot küld,
  - a válasz tipikusan `JSON` formában érkezik.

Ez sokkal egyszerűbb, könnyebb és hatékonyabb modellt adott a szolgáltatások elérésére.

## Miért lett a REST sikeres?

A szöveg alapján a REST több okból is legyőzte a korábbi XML-es web service világot.

- Egyszerűbb volt.
- Könnyebb volt fejleszteni rá.
- Kisebb adatforgalmat generált.
- Jobban illeszkedett a web eredeti működéséhez.
- Nem igényelt olyan nehéz és bonyolult infrastruktúrát, mint a SOAP/WSDL/UDDI világ.

Bár kezdetben sokan bírálták, főleg azok, akik sok pénzt fektettek az XML-es rendszerekbe, idővel világossá vált, hogy a REST gyakorlati szempontból sokkal életképesebb.

## A REST korlátja

Az oktató arra is utal, hogy a REST nem mindenben „tökéletesebb”.

- Funkcionalitásban bizonyos értelemben egyszerűbb, szegényesebb lehet.
- Nem ad olyan teljes absztrakciót, mint a klasszikus szolgáltatásleíró modellek.
- Egy URL például már tartalmaz elérési információt, tehát részben közelebb van a konkrét szerverhez.

Ennek ellenére a gyakorlatban ez a kompromisszum elfogadhatónak bizonyult, mert az egyszerűség és a hatékonyság sokkal fontosabb lett.

## Összegzés

Az `Apart_07.txt` fő témája a klasszikus XML-alapú `web service` technológia kialakulása, működése és háttérbe szorulása. A szöveg bemutatja, hogyan épült ez a modell a szolgáltatásorientált gondolkodásra, hogyan használt `WSDL`, `SOAP` és `UDDI` elemeket, majd miért vált túl bonyolulttá és lassúvá. A rész második nagy tanulsága a `REST` megjelenése: ez egy egyszerűbb, HTTP- és URL-alapú szolgáltatáselérési modell, amely végül sokkal sikeresebbnek bizonyult, és ma a modern API-k világának egyik alapja.
