# Cpart_01 összefoglaló

## Források, nyelők és transzformációk

Ez a rész tovább bontja a `Beam`-szerű adatfolyamrendszerek felépítését.

- Sokféle helyről lehet adatot olvasni.
- Sokféle célba lehet adatot írni.
- A feldolgozás középpontjában továbbra is a `transzformációk` állnak.

Az oktató azt hangsúlyozza, hogy az ilyen rendszerek egyik nagy előnye az, hogy rengeteg külső rendszerrel tudnak összekapcsolódni.

## Időablakok kezelése

Az egyik legfontosabb streamfeldolgozási fogalom az `ablakolás`.

- Lehet fix méretű ablakot definiálni.
- Lehet csúszó vagy mozgó ablakot megadni.
- Lehet naptári vagy más logika szerint tagolt időablakokat használni.

Ez azért fontos, mert folyamatos adatsornál a rendszernek valahogy mégis el kell döntenie, mely adatelemeket tekint egy adott számítás szempontjából összetartozónak.

## Triggerelés

A szöveg kitér arra is, hogy önmagában az ablak még nem elég.

- Kell valamilyen `trigger`, amely eldönti, mikor kell ténylegesen lefuttatni a számítást.
- Ez történhet idő alapján.
- Történhet adatvezérelt feltételek alapján is.

Ez a rész arra mutat rá, hogy streamfeldolgozásnál a „mikor számolunk?” kérdése legalább olyan fontos, mint az, hogy „mit számolunk?”.

## Eseményidő és feldolgozási idő

Az oktató megkülönbözteti az idő két fontos fogalmát.

- Az egyik az adat vagy esemény saját ideje.
- A másik a feldolgozórendszer belső ideje.

Ez a kettő nem mindig esik egybe, ezért a streamrendszereknek mindkettővel külön kell tudniuk dolgozni.

## Dataflow és példaalkalmazások

A szövegben megjelenik a `Google Dataflow` mint konkrét felhős környezet.

- Ez a `Beam`-jellegű pipeline-ok futtatásának egyik fontos platformja.
- A hallgatók számára példaprogramok is elérhetők.
- Az oktató azt javasolja, hogy a Google-felhő dokumentációjában keressenek rá a `Dataflow` témára.

Ez a rész a deklaratív programozási modellt egy konkrét menedzselt felhőszolgáltatáshoz köti.

## Szószámlálás Beam-stílusban

Megjelenik egy klasszikus `word count` példa is.

- A program beolvassa a szöveget.
- Kiszedi a szavakat.
- Csoportosítja és megszámolja őket.
- A végén formázza és elmenti az eredményt.

Ez a példa párhuzamot mutat a korábbi `MapReduce` szemlélettel, de modernebb, adatfolyam-orientált formában.

## A deklaratív pipeline előnye

Az oktató szerint az ilyen rendszerek egyik ereje az, hogy a programozó nem a futtatás minden részletét kezeli.

- A pipeline szerkezetét írjuk le.
- A rendszer maga gondoskodik a végrehajtásról.
- Ugyanarra a logikára többféle futtatókörnyezet is illeszthető.

Ez sokkal magasabb szintű absztrakció, mint a közvetlen klaszterkezelés.

## Összegzés

Az `Cpart_01.txt` fő témája a `Beam`- és `Dataflow`-jellegű streamfeldolgozás gyakorlati fogalmainak bevezetése. A szöveg tárgyalja az időablakokat, a triggerek szerepét, az eseményidő és feldolgozási idő különbségét, valamint egy `word count` jellegű pipeline felépítését. A központi tanulság az, hogy az adatfolyam-feldolgozásban a számításokat deklaratív gráfként írjuk le, miközben a futtatási részleteket a rendszerrejtezi el előlünk.
