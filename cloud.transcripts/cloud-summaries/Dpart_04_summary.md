# Dpart_04 összefoglaló

## Első és második generációs függvények

Ez a rész a `Cloud Functions` két generációja közötti különbségeket tárgyalja.

- Az első generáció szigorúbb és egyszerűbb modellre épült.
- A második generáció több erőforrást és nagyobb rugalmasságot adott.
- A háttérben megjelent a kibővített eseménykezelés is.

Ez azt mutatja, hogy a serverless platform maga is fejlődött, reagálva a gyakorlati igényekre.

## Futási időkorlátok

Az egyik fontos különbség a maximális futási idő.

- Az első generációban a korlát egységesen rövidebb volt.
- A második generációban a `HTTP` függvények akár hosszabb ideig is futhatnak.
- A háttérfüggvényeknél továbbra is szigorúbb időkorlát marad.

Ez különösen olyan feladatoknál fontos, ahol a válasz vagy feldolgozás több időt vehet igénybe.

## Erőforrások

A második generáció erősebb futtatási környezetet is kínál.

- Több memória.
- Több CPU-mag.
- Nagyobb teljesítményigényű feladatok támogatása.

Ez részben magyarázza, miért nyílt meg az út összetettebb serverless use case-ek felé.

## Konkurencia

Az egyik legérdekesebb változás a `konkurencia` kezelése.

- Az első generációban egy függvénypéldány csak egyetlen kérést szolgált ki.
- A második generációban egy példány több kérést is kiszolgálhat.
- Ez jobb erőforrás-kihasználást és költséghatékonyságot eredményez.

Az oktató hangsúlyozza, hogy ez az állapotmentes függvényeknél természetes továbbfejlődés.

## Eseménykezelés kiterjesztése

A második generációban az eseményrendszer is kibővült.

- Az első verzió csak korlátozott számú eseményt támogatott.
- A második verzió `Eventarc` alapokon sokkal több eseményforrást kezel.
- Ez a serverless integrációs lehetőségeket jelentősen megnöveli.

Ez közelebb viszi a modellt az általános, nagy skálájú eseményvezérelt architektúrákhoz.

## Első gyakorlati példa: HTTP függvény

A rész második fele az első konkrét kódpéldát vezeti be.

- `JavaScript`,
- `Python`,
- `Java`
  megvalósítások jelennek meg.

Mindegyik ugyanazt a logikát mutatja: egy egyszerű HTTP kérésre `Hello World` vagy paraméterezett válasz adása.

## Összegzés

Az `Dpart_04.txt` fő témája a felhőfüggvények első és második generációjának összehasonlítása, majd egy egyszerű `HTTP` függvény bevezetése. A szöveg bemutatja a futási idő, az erőforrások, a konkurencia és az eseménytámogatás fejlődését, majd egy triviális példával átvezeti ezt a gyakorlatba. A központi tanulság az, hogy a modern serverless platformok már jóval rugalmasabbak és erősebbek, mint a korai, nagyon szigorúan izolált modellek.
