# Epart_03 összefoglaló

## Terheléselosztás a Bigtable-ben

Ez a rész azt magyarázza el, hogyan oszlik el a terhelés egy `Bigtable` klaszterben.

- Nem lenne jó, ha egyetlen node lenne állandóan túlterhelve.
- A rendszer ezért a táblát kisebb részekre bontja.
- Ezek a részek a node-ok között szétoszthatók.

Ez statisztikailag segít egyenletesebbé tenni a terhelést.

## Tablet-szintű újraelosztás

Ha egy részhalmaz túl nagy vagy túl forróvá válik, a rendszer közbelép.

- A túlterhelt `tablet` tovább darabolható.
- A ritkán használt kis tabletek összevonhatók.
- Mindez automatikusan történik.

Ez a háttérfolyamat kulcsfontosságú a nagy rendszerek folyamatos kiegyensúlyozásában.

## A sorkulcs jelentősége

Az oktató itt eljut a `row key` kérdéséhez.

- A kulcs meghatározza, hogyan címezzük a sorokat.
- A kulcs eloszlása a teljesítményre is hatással van.
- Véletlenszerűbb kulcsok segíthetik az egyenletes eloszlást.

Ugyanakkor nem mindig ez a legjobb megoldás.

## Véletlen vs. rendezett kulcsok

Van egy fontos tradeoff.

- Véletlen kulcsok jobban szórják a kéréseket.
- Egymást követő kulcsok viszont egyszerűbbé teszik a tartományos lekérdezéseket.

Ezért a kulcs megtervezése mindig az alkalmazási mintától függ.

## Összegzés

Az `Epart_03.txt` fő témája a `Bigtable` terheléselosztási mechanizmusa és a sorkulcs megtervezésének jelentősége. A szöveg bemutatja a tabletek automatikus darabolását és összevonását, valamint azt, hogy a kulcsstratégia hogyan hat az elosztott teljesítményre. A központi tanulság az, hogy egy ilyen rendszerben a séma- és kulcstervezés nem csupán logikai kérdés, hanem közvetlenül befolyásolja a rendszer viselkedését.
