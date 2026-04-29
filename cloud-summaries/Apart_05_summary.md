# Apart_05 összefoglaló

## A távoli függvényhívás alapötlete

A szöveg központi témája az, hogyan lehet egy távoli szerveren végrehajtani valamit úgy, mintha a kliens oldalon csak egy sima függvényhívás történne.

- Az ideális programozási modell az lenne, hogy:
  - a kliens oldalon meghívunk egy függvényt,
  - a függvény nem helyben fut le,
  - hanem egy távoli szerveren hajtódik végre,
  - az eredmény pedig automatikusan visszakerül a klienshez.
- Ez a modell nagyon elegáns, mert a programozó szemszögéből:
  - minden egyszerűnek tűnik,
  - a hálózati kommunikáció rejtve marad,
  - a távoli végrehajtás szinte úgy viselkedik, mint egy normál lokális függvényhívás.

A probléma az, hogy egy normál függvényhívás természeténél fogva helyben fut le. Ezért a rendszert valahogy "meg kell kerülni", hogy a távoli végrehajtás mégis ilyen egyszerű formában jelenhessen meg.

## A Remote Procedure Call lényege

Erre a problémára ad megoldást a `Remote Procedure Call`, röviden `RPC`.

- Az RPC célja:
  - a távoli hívást lokális függvényhívásnak álcázni.
- A programozó úgy írhatja meg a kódot, mintha csak egy normál függvényt használna.
- A háttérben azonban:
  - hálózati kapcsolat jön létre,
  - üzenetek készülnek,
  - adatküldés történik,
  - a szerver oldalon végrehajtják a műveletet,
  - majd visszaküldik az eredményt.

Vagyis az RPC nem azt jelenti, hogy a lokális függvény "átköltözik" a távoli gépre, hanem azt, hogy a rendszer létrehoz egy olyan köztes mechanizmust, amely ezt az illúziót kelti.

## A middleware szerepe

Az RPC egyik kulcsfogalma a `middleware`, vagyis egy köztes szoftverréteg.

- Ez a réteg a program és az operációs rendszer között helyezkedik el.
- Feladata, hogy:
  - elfogja a függvényhívást,
  - összegyűjtse a függvénynévhez tartozó paramétereket,
  - ezeket üzenetté alakítsa,
  - elküldje a hálózaton keresztül a szervernek,
  - majd a választ visszafordítsa a kliens számára használható formára.

A programozó ebből közvetlenül szinte semmit sem lát. Számára úgy tűnik, mintha egyszerűen meghívott volna egy függvényt, és kapott volna egy eredményt.

## Mi történik a kliens oldalon?

A kliens oldalon a távoli hívás mögött több rejtett lépés történik.

- A kliens meghív egy függvényt.
- A middleware ezt elfogja.
- A rendszer:
  - összeszedi a paramétereket,
  - létrehoz egy üzenetet,
  - átadja azt az operációs rendszernek,
  - elküldi a hálózaton át a szerver felé.

Tehát a függvényhívás valójában nem közvetlen végrehajtást indít, hanem egy üzenetküldési folyamatot.

## Mi történik a szerver oldalon?

A szerver oldalon a folyamat fordított irányban játszódik le.

- Az operációs rendszer fogadja az üzenetet.
- Az üzenet a szerveroldali middleware-hez kerül.
- A middleware:
  - kicsomagolja az adatokat,
  - megállapítja, melyik függvényt kell végrehajtani,
  - átadja a paramétereket a valódi implementációnak.
- A szerver ténylegesen végrehajtja a szükséges műveletet.
- Az eredményt a middleware újra becsomagolja.
- Ezután az operációs rendszer visszaküldi azt a kliens felé.

A kliens a végén ezt úgy kapja meg, mintha egyszerűen visszatért volna egy függvény eredménye.

## Marshalling és unmarshalling

A szöveg kiemel egy fontos technikai fogalmat is: a `marshalling` folyamatát.

- `Marshalling`:
  - az adatok átalakítása olyan bájtsorozattá, amely hálózaton keresztül elküldhető.
- `Unmarshalling`:
  - ennek a bájtsorozatnak visszaalakítása eredeti adatszerkezetekké.

Ez azért fontos, mert a hálózaton nem magas szintű programozási objektumok utaznak, hanem bináris adatok. Ezeket a rendszernek mindkét oldalon értelmezhető formába kell hoznia.

## Az RPC előnye

Az RPC egyik legnagyobb előnye az, hogy a sok apró hálózati lépést egyetlen logikai műveletté egyszerűsíti.

- A programozó számára:
  - a kommunikáció átláthatóbb,
  - a kód elegánsabb,
  - a távoli hívás jobban hasonlít a lokális programozásra.
- Hibakezelés szempontjából is előnyös:
  - nem öt különálló hálózati lépést kell figyelni,
  - hanem egyetlen művelet sikeres vagy sikertelen végrehajtását.

Ez tehát nemcsak kényelmesebb, hanem koncepcionálisan is sokkal tisztább modell.

## Az RPC történeti háttere

Az oktató hangsúlyozza, hogy az RPC nem új technológia.

- A szabványosított RPC-megoldás `1995-ben` vált hivatalossá.
- Eredetileg a `Sun Microsystems` dolgozta ki.
- C nyelven implementált rendszer volt.
- Főként lokális hálózatokon működő elosztott rendszerekre tervezték, nem az internetre.

Ez azért fontos, mert megmutatja, hogy a felhőhöz vezető technológiák egy része jóval a modern web előtt megszületett.

## Az objektumorientált világ problémája

Az RPC eredeti formája nem objektumorientált, ami a 90-es évek végére egyre nagyobb korlát lett.

- Időközben elterjedtek:
  - a `C++`,
  - a `Java`,
  - más objektumorientált nyelvek.
- Az objektumorientált rendszerekben:
  - osztályok vannak,
  - példányok vannak,
  - metódusok és állapot is tartozik az objektumokhoz.
- Ez bonyolultabbá teszi a távoli végrehajtást.
  - Nem elég adatot küldeni.
  - A viselkedés, a típusok és az implementáció kérdése is megjelenik.

Ez új technológiák felé terelte az elosztott programozási modelleket.

## A CORBA megjelenése

Erre a kihívásra adott válasz volt a `CORBA` (`Common Object Request Broker Architecture`).

- A CORBA lényegében:
  - egy objektumorientált RPC-rendszer.
- Fő jellemzői:
  - nyelvfüggetlen megközelítés,
  - interfészalapú leírás,
  - többféle programozási nyelv támogatása.
- A szerver funkcionalitását egy `IDL` (`Interface Description Language`) segítségével lehet leírni.
- Ebből fordítás során automatikusan generálhatók kliensoldali elemek különböző nyelveken.

A cél tehát az volt, hogy heterogén rendszerek is együtt tudjanak működni, és a távoli szolgáltatások használata szabványos formát kapjon.

## Miért lett problémás a CORBA?

Bár a CORBA fontos technológiai lépés volt, az oktató szerint végül túl bonyolulttá vált.

- A rendszer célja nagyon nagy volt:
  - szinte minden elosztott rendszerszintű problémát kezelni akart.
- Emiatt:
  - a specifikáció hatalmas lett,
  - a megvalósítás bonyolulttá vált,
  - a különböző gyártók nem teljesen ugyanazt implementálták.
- A gyakorlatban ez azt jelentette, hogy:
  - az egyik cég kliensoldali rendszere,
  - és egy másik cég szerveroldali rendszere
  nem mindig működött tökéletesen együtt.
- További gondot okozott az internet elterjedése is.
  - A web `HTTP` alapú kommunikációt használt.
  - Megjelentek a `tűzfalak`.
  - Ezek gyakran blokkolták a közvetlen TCP portokat, amelyekre a CORBA és hasonló rendszerek építettek.

Ennek következtében a CORBA fokozatosan háttérbe szorult, és ma már gyakorlatilag nem számít általánosan használt megoldásnak.

## A Java RMI

A szövegben röviden megjelenik a `Java RMI` (`Remote Method Invocation`) is.

- Ez lényegében az RPC objektumorientált, Java-specifikus változata.
- A Java világában lehetővé teszi, hogy:
  - objektumokat küldjünk át egyik virtuális gépből a másikba,
  - és a távoli oldalon ezeket használni lehessen.
- Ez különösen érdekes, mert:
  - a Java egységes futtatási környezetet ad,
  - így bizonyos dolgok egyszerűbben megoldhatók, mint nyelvfüggetlen rendszereknél.

A Java RMI egy fontos köztes lépés volt az elosztott objektumorientált rendszerek fejlődésében.

## A szolgáltatásorientáltság megjelenése

A szöveg vége felé az oktató arra utal, hogy ezekben a technológiákban már megjelenik a `szolgáltatásorientált` szemlélet.

- A hagyományos kliens-szerver modell egyik problémája az, hogy a kliensnek tudnia kell:
  - a szerver címét,
  - IP-címét,
  - portszámát.
- Ez kis rendszereknél még kezelhető.
- Nagyobb rendszereknél azonban ez már nehézkessé válik.
- A Java RMI-ben megjelenik egy `registry`, vagyis névszolgáltatás-jellegű komponens.
- Ez már abba az irányba mutat, hogy:
  - a kliens ne közvetlenül gépeket keressen,
  - hanem szolgáltatásokat tudjon megtalálni és használni.

Ez a gondolat később a modern szolgáltatásorientált és felhős architektúrákban válik igazán meghatározóvá.

## Összegzés

Az `Apart_05.txt` fő témája a távoli eljáráshívás, vagyis az, hogyan lehet a hálózati kommunikációt úgy elrejteni, hogy a programozó számára egy távoli művelet is egyszerű függvényhívásnak tűnjön. A szöveg bemutatja az `RPC` működését, a middleware szerepét, a marshalling folyamatát, majd kitér az objektumorientált továbbfejlődésre a `CORBA` és a `Java RMI` példáján keresztül. Az egész rész lényege, hogy a felhőhöz vezető út egyik alapvető állomása az volt, amikor a távoli rendszerek használatát programozási szinten egyre természetesebbé és átláthatóbbá tudták tenni.
