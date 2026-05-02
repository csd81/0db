USE northwind;
GO

-------------------------------- LEKÉRDEZÉSEK ---------------------------

-- john barátai
select p2.name
from person p1, person p2, friendof
where match(p1-(friendof)->p2)
and p1.name = 'john';

-- john kedvelt éttermei
select restaurant.name
from person, likes, restaurant
where match (person-(likes)->restaurant)
and person.name = 'john';

-- john barátai kedvelt éttermei
select restaurant.name
from person person1, person person2, likes, friendof, restaurant
where match(person1-(friendof)->person2-(likes)->restaurant)
and person1.name = 'john';

-- azok a személyek, akik olyan éttermet kedvelnek, ami ugyanabban a városban van, ahol élnek
select person.id, person.name
from person, likes, restaurant, livesin, city, locatedin
where match (person-(likes)->restaurant-(locatedin)->city and person-(livesin)->city);

-- azok a személyek, akiknek legalább egy barátja olyan éttermet kedvel, ami ugyanabban a városban van, ahol a barát él
select distinct p1.id, p1.name
from person p1, person p2, friendof, likes, restaurant, livesin, city, locatedin
where match (p1-(friendof)->p2 and p2-(likes)->restaurant-(locatedin)->city and p2-(livesin)->city);

-- 2 olyan személy megkeresése, akiknek közös barátjuk van
-- a friendof IRÁNYÍTOTT él, noha a kapcsolat irányítatlan (kölcsönös)
-- az irányítatlan kapcsolatok kifejezésére csak két él használatával van mód
select p0.name person, p1.name Friend1, p2.name Friend2
from person p1, friendof f1, person p2, friendof f2, person p0
-- where match(p1-(f1)->p0<-(f2)-p2) and p1.id <> p2.id
where match(p1-(f1)->p0 and p2-(f2)->p0) and p1.id <> p2.id; -- egyenértékű

-- SHORTEST_PATH ----------------------------------------------
-- barátok: az összes legrövidebb út Johntól
select p1.name,
    p1.name + '->' + string_agg(p2.name, '->') within group (graph path) paths,
    last_value(p2.Name) within group (graph path) last_name,
    count(p2.name) within group (graph path) depth
from person p1, person for path as p2,
    friendof for path as friend
-- where match(shortest_path(p1(-(friend)->p2) {1,2})) and p1.name='john' -- nem tartalmazza a 3 hosszú john->mary->alice->tom utat
where match(shortest_path(p1(-(friend)->p2) +)) and p1.name = 'john'; -- mindet tartalmazza

-- barátok: a legrövidebb út John és Jacob között
select name, paths, depth
from (
    select p1.name,
        p1.name + '->' + string_agg(p2.name, '->') within group (graph path) paths,
        last_value(p2.Name) within group (graph path) last_name,
        count(p2.name) within group (graph path) depth
    from person p1, person for path as p2,
        friendof for path as friend
    where match(shortest_path(p1(-(friend)->p2)+)) and p1.name = 'john'
    -- and p2.name='jacob' -- HIBA: FOR PATH táblákból nem lehet oszlopokat szelektálni
) a where last_name = 'jacob';
