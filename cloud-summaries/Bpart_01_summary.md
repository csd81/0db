# Bpart_01 összefoglaló

## A virtuális gépek konfigurációs lehetőségei

Ez a rész a `virtuális gépek` részletesebb paraméterezéséről szól a `Google Cloud` környezetében.

- Többféle gépkategória választható:
  - `standard`,
  - `high CPU`,
  - `high memory`.
- A `vCPU` virtuális processzormagot jelent.
- A memória mennyisége a választott géptípushoz és magszámhoz igazodik.

Az oktató célja itt az, hogy a hallgatók lássák: egy virtuális gép nem egyszerűen „egy gép”, hanem sokféle hardverprofilból állítható össze.

## Processzor- és háttértár-választás

A konfiguráció nem áll meg a magszámnál és a memóriánál.

- Kiválasztható a processzorgyártó:
  - `Intel`,
  - `AMD`,
  - `ARM` alapú megoldás.
- Meghatározható a háttértár típusa és mérete is.
- További tárolókat is hozzá lehet csatolni.

Ez a rész azt hangsúlyozza, hogy a felhőben az infrastruktúra sokkal rugalmasabban alakítható, mint egy előre rögzített fizikai gépnél.

## Shared és isolated virtuális gépek

Az oktató kitér a virtuális gépek elkülönítési szintjeire is.

- A `shared` VM megosztott fizikai hardveren fut.
- Ez olcsóbb, de kevésbé stabil és kevésbé kiszámítható.
- Az `isolated` VM ezzel szemben jobban elszigetelt.
- Ilyenkor garantáltabb, hogy más ügyfelek nem osztoznak ugyanazon a fizikai erőforráson.

Ez a különbség főként teljesítmény, megbízhatóság és biztonság szempontjából fontos.

## A virtuális gép életciklusa

A szöveg másik fontos témája a VM-ek állapotgépe és életciklusa.

- A létrehozás után először `provisioning` történik.
- Ezt követi a `staging`, vagyis az indulási folyamat.
- Ezután kerül a gép `running` állapotba.
- Később leállítható vagy teljesen megszüntethető.

Az oktató felhívja a figyelmet arra, hogy a háttérben több átmeneti állapot és hibakezelési ág is létezhet, de a hallgatók számára a legfontosabb a létrehozás, futás és leállítás logikája.

## Számlázás és a leállítás jelentősége

Ebben a részben kiemelt figyelmet kap a költség.

- A számlázás nem attól függ, fut-e rajta program,
  hanem attól, hogy maga a virtuális gép fut-e.
- A gépet mindig le kell állítani, ha már nincs rá szükség.
- Ellenkező esetben folyamatosan fogy a kredit.

Ez a gyakorlat szempontjából az egyik legfontosabb operatív szabály.

## Másodperc alapú elszámolás

Az oktató összeveti a régi és a mai számlázási modellt.

- Korábban órás elszámolás volt jellemző.
- Ma már a rendszer jellemzően `másodperc alapon` számláz.
- Az első egy percet mindenképpen ki kell fizetni.

Ez finomabb, igazságosabb használatalapú modellt jelent, de a pazarlás veszélye továbbra is fennáll.

## Az árak és a méretválasztás kérdése

Az ár nagyban függ a kiválasztott konfigurációtól.

- Az óradíj néhány centtől több dollárig is terjedhet.
- A nagy gépek nagyon gyorsan elvihetik az egész kreditet.
- Az oktató azt javasolja, hogy mindig a lehető legkisebb megfelelő gépet válasszák a hallgatók.

Ez a rész arra tanít, hogy a felhőben a technikai döntések közvetlen pénzügyi következményekkel járnak.

## Havi költségek és kedvezmények

A szöveg példákat is ad arra, mennyibe kerülne egy gép tartós, folyamatos használata.

- A legolcsóbb konfiguráció akár egy hónapig is futhatna a kapott keretből.
- Egy nagyobb gép viszont nagyon rövid idő alatt elviheti a teljes összeget.
- Léteznek különféle kedvezmények is, de ezek nem teszik jelentéktelenné a költségkérdést.

Az oktató ezzel érzékelteti, hogy a felhő rugalmassága együtt jár a folyamatos költségtudatosság igényével.

## Összegzés

Az `Bpart_01.txt` fő témája a virtuális gépek részletes konfigurációja és gazdaságos használata a `Google Cloud` környezetében. A szöveg bemutatja a géptípusokat, a processzor- és háttértár-opciókat, a megosztott és elszigetelt VM-ek közötti különbséget, valamint a virtuális gépek életciklusát. A központi tanulság az, hogy a felhőben minden erőforrás-választás közvetlenül hat a költségekre, ezért a leállítás és a tudatos méretezés alapvető gyakorlat.
