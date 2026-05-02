USE northwind;
GO

go
use db_vi

-- john barátai
select p2.Name
from r_person p1 join r_friendof f on p1.id = f.person1_id
    join r_person p2 on p2.id = f.person2_id
where p1.Name = 'john';

-- john kedvelt éttermei
select r.name
from r_restaurant r join r_likes l on r.id = l.restaurant_id
    join person p on p.id = l.person_id
where p.Name = 'john';

-- john barátai kedvelt éttermei
select r.name
from r_person p1 join r_friendof f on p1.id = f.person1_id
    join r_person p2 on p2.id = f.person2_id
    join r_likes l on l.person_id = p2.id
    join r_restaurant r on r.id = l.restaurant_id
where p1.Name = 'john';

-- azok a személyek, akik olyan éttermet kedvelnek, ami ugyanabban a városban van, ahol élnek
select p.name
from r_restaurant r join r_likes l on r.id = l.restaurant_id
    join r_person p on p.id = l.person_id
where r.id = p.city_id;

-- azok a személyek, akiknek legalább egy barátja olyan éttermet kedvel, ami ugyanabban a városban van, ahol ő él
select p1.name
from r_person p1 join r_friendof f on p1.id = f.person1_id
    join r_person p2 on p2.id = f.person2_id
    join r_likes l on l.person_id = p2.id
    join r_restaurant r on r.id = l.restaurant_id
where r.id = p2.city_id;
