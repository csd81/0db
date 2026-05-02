# Dpart_03 összefoglaló

## Állapotmentesség mint alapkövetelmény

Ez a rész a felhőfüggvények működési korlátait és szemantikáját tárgyalja.

- A függvényeknek alapvetően `állapotmentesnek` kell lenniük.
- Nem tárolhatják a belső végrehajtási állapotukat a hívások között.
- Egy új hívásnak ugyanúgy kell viselkednie, mint bármelyik korábbinak.

Ez központi serverless alapelv, amely egyszerre teszi lehetővé a könnyű skálázást és korlátozza a közvetlen állapottartást.

## Workflow és külső állapottárolás

Az oktató felhívja a figyelmet arra, hogy sok alkalmazás mégis igényel állapotkezelést.

- Ilyenkor a függvény maga nem tarthatja fenn az állapotot.
- Ehelyett külső háttértárba kell menteni az állapotinformációkat.
- A workflow résztvevői induláskor ebből olvashatják ki, hol tart a folyamat.

Ez egy tipikus kerülőmegoldás, amely megőrzi a függvények állapotmentes természetét, miközben mégis lehet összetett folyamatokat építeni.

## Egy kérés per függvény példány

Az első generációs függvények egyik fontos jellemzője, hogy egyszerre egyetlen kérést szolgáltak ki.

- Ez erős izolációt biztosított.
- Biztonsági és adatszivárgási megfontolások álltak mögötte.
- Nagy terhelés esetén a rendszer automatikusan több példányt indított.

Ez egyszerű és tiszta végrehajtási modellt eredményezett.

## Végrehajtási szemantika

Az oktató különbséget tesz a `HTTP` és a `background` függvények megbízhatósági modellje között.

- A `HTTP` függvényeknél `at most once` szemantika érvényes.
- A `background` függvényeknél `at least once`.

Ez azt jelenti, hogy a háttérfüggvényeknél a rendszer szükség esetén újrapróbálja a végrehajtást.

## Miért különbözik a két modell?

A különbség oka a vezérelhetőség.

- HTTP-kérésnél nincs kontrollunk afelett, hogy a kliens újraküldi-e a kérést.
- Háttéreseményeknél a felhő eseménytovábbító rendszere tudja figyelni a kézbesítést.
- Ezért a háttéreseményeknél szorosabb megbízhatósági garancia adható.

Ez fontos tervezési különbség, különösen, ha az idempotencia vagy a többszöri végrehajtás számít.

## Lokális fájlrendszer és internetelérés

A rész még két gyakorlati tulajdonságot kiemel.

- A függvény futás közben használhat átmeneti lokális fájlrendszert.
- Ez csak a futás idejéig él.
- Emellett globális internetelérés is rendelkezésre állhat.

Ez azt mutatja, hogy a függvények kis, rövid életű futtatási környezetek, nem tartós szerverek.

## Összegzés

Az `Dpart_03.txt` fő témája a felhőfüggvények végrehajtási modelljének legfontosabb korlátai és garanciái. A szöveg bemutatja az állapotmentességet, az első generációs izolált végrehajtást, valamint a `HTTP` és `background` függvények eltérő szemantikáját. A központi tanulság az, hogy a `serverless` egyszerű használata mögött nagyon tudatos végrehajtási feltételek állnak, és ezek meghatározzák, hogyan lehet megbízható alkalmazásokat építeni rájuk.
