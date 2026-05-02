# Apart_02 összefoglaló

## A felhőpiac mérete és jelentősége

A szöveg elején az oktató még a felhőpiac üzleti hátteréről beszél, hogy érzékeltesse, milyen súlyú területről van szó.

- A fő szereplők továbbra is:
  - `Amazon`
  - `Microsoft`
  - `Google`
- Az `Oracle` erősödik, az `Alibaba` visszaesik.
- A `Google` egyre jobban felzárkózik a vezetőkhöz.
- A piac óriási méretű:
  - több tíz- és százmilliárd dolláros üzlet,
  - rendkívül gyors növekedéssel.
- Az `AI` tovább növelte ennek a piacnak a jelentőségét.
- Ma már külön adatközpontok épülnek kifejezetten AI-futtatásra is.

Az oktató itt nem gazdasági elemzést akar adni, hanem azt mutatja meg, hogy a felhőtechnológia mögött komoly pénzügyi és technológiai erő koncentrálódik.

## Miért van szükség felhőre?

A szöveg fő technikai kérdése az, hogy miért volt szükség a felhőtechnológia kialakulására.

- A számítógépes rendszerek terhelése általában nem állandó.
- A legtöbb valós rendszerben:
  - vannak nyugodtabb időszakok,
  - és vannak csúcsidőszakok.
- Példák:
  - irodai rendszerek nappal terheltek, éjszaka kevésbé,
  - vállalati háttérrendszerek bizonyos időpontokban hirtelen sokkal több munkát kapnak,
  - például havi számfejtés vagy más időszakos feldolgozás idején.

A probléma tehát az, hogy a valóságban a terhelés `fluktuál`, nem pedig állandó.

## A szolgáltatásminőség kérdése

Egy vállalat számára nem elég, hogy a rendszer „legtöbbször” működjön.

- Biztosítani kell a `quality of service` szintet.
- Ez azt jelenti, hogy:
  - a szolgáltatásnak elérhetőnek kell lennie,
  - a feladatoknak időben le kell futniuk,
  - a csúcsidőszakokban sem omolhat össze a rendszer.
- Ez az informatikai vezetés felelőssége.

A felhő egyik legfontosabb szerepe éppen az, hogy ezt a szolgáltatásminőséget rugalmasabban lehessen biztosítani.

## Az állandó kapacitás problémája

Az oktató összehasonlít egy ideális és egy valós helyzetet.

- Ideális esetben a terhelés állandó lenne.
- Ilyenkor egyszerű lenne a tervezés:
  - megvesszük a szükséges kapacitást,
  - és azon stabilan fut minden.
- A valóságban azonban a terhelés hullámzik.
- Ha a rendszert csak az átlagos terhelésre méretezzük:
  - csúcsidőben nem fog tudni megfelelően működni,
  - lelassulhat,
  - akár le is állhat.

Ez a klasszikus túlterhelési probléma, amely sok ismert rendszerleállás mögött áll.

## A csúcsterhelésre méretezés hátránya

A másik lehetőség az, hogy a teljes rendszert a legnagyobb várható terhelésre tervezzük.

- Ilyenkor biztosított, hogy csúcsidőben is működjön.
- Ugyanakkor ez rendkívül drága.
- Az idő nagy részében ugyanis:
  - a gépek kihasználatlanul állnak,
  - túl sok erőforrás van fenntartva,
  - rossz lesz a fajlagos költség.

Ez gazdaságilag rossz modell, mert a vállalat olyan kapacitásért fizet folyamatosan, amelyre csak ritkán van szükség.

## Helyi rendszerrel ezt nem lehet rugalmasan megoldani

Az oktató hangsúlyozza, hogy hagyományos helyi infrastruktúrával a gyors bővítés gyakorlatilag lehetetlen.

- Nem lehet néhány perc alatt új szerverparkot létrehozni.
- Nem lehet azonnal plusz gépeket szerezni és üzembe állítani.
- Emiatt a helyi rendszereknél sokáig csak a túlméretezés maradt reális megoldás.

Ez az a pont, ahol a felhő értelmet nyer.

## A felhő mint rugalmas erőforrásforrás

A felhő ott válik hasznossá, hogy lehetővé teszi távoli erőforrások ideiglenes bevonását.

- Ha a hálózat elég gyors és megbízható, akkor a vállalat:
  - csúcsidőben bérelhet plusz szervereket,
  - azokon futtathat extra feladatokat,
  - majd a csúcsidőszak után lemondhat róluk.
- Így:
  - nem kell mindig maximális helyi kapacitást fenntartani,
  - mégis biztosítható a szolgáltatásminőség.

Ez a felhő egyik legalapvetőbb gazdasági és technikai előnye.

## A felhő új problémákat is felvet

A távoli erőforrások használata ugyanakkor nem problémamentes.

- Felmerülnek technikai kérdések:
  - ki üzemelteti a távoli rendszert,
  - hogyan történik a menedzsment,
  - hogyan biztosítható a megbízható működés.
- Felmerülnek üzleti kérdések is:
  - kivel osztozunk az erőforráson,
  - milyen garanciákat kapunk,
  - mennyire kiszámítható a szolgáltatás.

A felhőtechnológia részben éppen ezekre a kérdésekre próbál megoldást adni.

## Teljesen felhős működés is lehetséges

Az oktató azt is kiemeli, hogy nemcsak hibrid módon lehet gondolkodni.

- Nem csak az lehetséges, hogy csúcsidőben veszünk igénybe plusz kapacitást.
- Az is lehet, hogy a helyi infrastruktúra gyakorlatilag nulla.
- Ilyenkor:
  - minden a felhőben fut,
  - a teljes kapacitásbiztosítást a szolgáltató végzi,
  - a változó terhelést is a felhő kezeli.

Ez már a teljesen felhőalapú működés logikája.

## Hibrid modellek is léteznek

A szöveg arra is utal, hogy a helyi és távoli infrastruktúra keverhető.

- Lehet:
  - részben helyi,
  - részben felhős
  rendszert használni.
- A későbbiekben szó lesz arról is, hogyan kombinálhatók ezek.

Ez a gondolat a hibrid felhő irányába mutat.

## Milyen technológiák kellettek a felhő létrejöttéhez?

A szöveg végén az oktató áttekintést ad arról, hogy a felhő nem egyetlen újításból jött létre, hanem több technológia összeéréséből.

- A bal oldali csoport inkább az alapokat mutatja:
  - `mainframe` világ,
  - hálózati technológiák fejlődése,
  - internet megjelenése,
  - kliens-szerver rendszerek.
- A jobb oldalon pedig a magasabb szintű modellek jelennek meg:
  - `web`,
  - `grid computing`,
  - szolgáltatásorientált architektúrák,
  - `web service`,
  - `peer-to-peer` rendszerek,
  - vállalati elosztott rendszerek.

Az oktató szerint ezek olyan alapfogalmak, amelyeket MSc-szinten legalább általános tájékozottsági szinten ismerni kell.

## Miért fontos ez az áttekintés?

Ez a technológiai „leltár” nem öncélú.

- A cél az, hogy a hallgató felismerje:
  - mit ismer jól,
  - mit ismer kevésbé,
  - miről nem hallott még.
- Ami teljesen ismeretlen, annak érdemes legalább utánanézni.
- A felhő megértése csak úgy lehetséges, ha a mögötte álló előzménytechnológiák fő logikáját is látjuk.

Ez a rész tehát inkább szemléleti és orientáló szerepet tölt be.

## Összegzés

Az `Apart_02.txt` fő témája az, hogy a felhőtechnológia miért vált szükségessé. A központi probléma a változó terhelés: a hagyományos helyi infrastruktúrák vagy túl gyengék csúcsidőben, vagy túl drágák, ha mindig a maximális terhelésre vannak méretezve. A felhő erre ad rugalmas megoldást az igény szerinti távoli erőforrás-használattal. Emellett a szöveg azt is hangsúlyozza, hogy a felhő több korábbi technológia, például a hálózatok, a kliens-szerver rendszerek és a szolgáltatásorientált architektúrák fejlődésének eredménye.
