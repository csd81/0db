# Bpart_09 összefoglaló

## A MapReduce alapötlete

Ez a rész a `MapReduce` feldolgozási modell lényegét magyarázza el.

- Két alapfázisra épül:
  - `map`,
  - `reduce`.
- A programozó feladata ennek a két lépésnek a megadása.
- A párhuzamos végrehajtást maga a keretrendszer intézi.

Az oktató ezzel azt mutatja meg, hogy a nagy adatos párhuzamos feldolgozás mögött egy viszonylag egyszerű programozási modell áll.

## A programozó és a rendszer feladata

A `MapReduce` használatánál a fejlesztőnek nem kell a teljes klaszter működését vezérelnie.

- A programozó csak a saját feldolgozó logikáját írja meg.
- A keretrendszer osztja szét a munkát.
- A futtatás, koordináció és összegyűjtés már a háttérrendszer feladata.

Ez hasonló ahhoz, ahogy többszálú programozásnál a szálak futtatását az operációs rendszer kezeli.

## Fájlalapú működés

Az oktató kiemeli, hogy a `map` és a `reduce` fázisok fájlalapú környezetben dolgoznak.

- Az adatok a fájlrendszerből érkeznek.
- Az eredmények is fájlba kerülnek vissza.
- Nem közvetlen memóriabeli együttműködésről van szó.

Ez azért fontos, mert jól illeszkedik a nagy, megosztott klaszteres adattároláshoz.

## Klasszikus példa: szószámlálás

A működés szemléltetésére az oktató a jól ismert `word count` példát használja.

- A bemenő szöveget részekre bontják.
- A `map` fázis minden szóhoz egy `1` értéket rendel.
- Ezután az azonos kulcsok összegyűjtésre kerülnek.
- A `reduce` fázis megszámolja, hány darab érték tartozik az egyes szavakhoz.

Így a végén megkapjuk, hogy melyik szó hányszor fordult elő.

## Kulcs-érték szemlélet

A példa mögött egy általánosabb elv is látszik.

- A feldolgozás `kulcs-érték` párokra épül.
- A `map` kulcsokat és részértékeket állít elő.
- A `reduce` az azonos kulcsokhoz tartozó részértékeket egyesíti.

Ez a minta sokkal összetettebb feladatokra is alkalmazható, nemcsak szószámlálásra.

## Miért fontos a Hadoop-kompatibilitás?

Az oktató külön hangsúlyozza, hogy a `Hadoop` régóta használt, nyílt forráskódú rendszer.

- Sok szervezet már a felhő megjelenése előtt is használt hasonló klasztereket.
- Ezek a felhasználók nem akarnak teljesen új modellt tanulni.
- Ezért a felhőszolgáltatók kompatibilis megoldásokat kínálnak.

Ez teszi lehetővé, hogy meglévő programok és munkafolyamatok könnyebben átvihetők legyenek felhős környezetbe.

## A Google Dataproc szolgáltatás

A `Google Cloud` megfelelő szolgáltatása erre a célra a `Dataproc`.

- Ez egy menedzselt `Hadoop`- és `Spark`-környezet.
- Nem kell saját klasztert kézzel összerakni és adminisztrálni.
- A felhasználó létrehoz egy klasztert, és azon futtathatja a feldolgozó feladatokat.

Ez a rész azt mutatja meg, hogyan jelenik meg a korábban tárgyalt elosztott feldolgozás konkrét felhőszolgáltatás formájában.

## Dataproc klasztertípusok

Az oktató röviden a klaszterkonfigurációkat is megmutatja.

- Létezik egyszerű egycsomópontos megoldás.
- Van szabványos klaszter vezérlővel és worker node-okkal.
- Van nagyobb megbízhatóságú, több mesterrel rendelkező változat is.

Ez azt jelzi, hogy a skálázhatóság és a hibatűrés itt is konfigurálható szolgáltatás.

## Következő feladatok

A rész végén az oktató kijelöli az önálló munka irányát.

- Először a `gcloud`-os és programozott `VM`- illetve `Storage`-feladatokat kell begyakorolni.
- Ezután lehet a `Dataproc` és a `MapReduce` jellegű gyakorlatok felé továbblépni.
- A cél az, hogy mindenki lássa, hogyan érhető el a felhő kódból is.

Ez egy világos tanulási sorrendet ad: előbb infrastruktúra, aztán automatizálás, végül adatfeldolgozás.

## Összegzés

Az `Bpart_09.txt` fő témája a `MapReduce` modell működésének és a `Google Dataproc` szolgáltatás szerepének bemutatása. A szöveg megmagyarázza a `map` és `reduce` fázisok logikáját, a kulcs-érték alapú feldolgozást, valamint a `word count` példán keresztül a modell szemléletes működését. A rész végső tanulsága az, hogy a korábbi, nyílt forráskódú nagy adatos rendszerek logikája ma menedzselt felhőszolgáltatásként is elérhető, így a skálázható adatfeldolgozás a gyakorlatban is könnyebben használhatóvá válik.
