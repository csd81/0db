--drop table r_friendof
--drop table r_person
--drop table r_restaurant
--drop table r_city
go
create table r_city (id int primary key, name varchar(100), statename varchar(100))
create table r_person (id int primary key, name varchar(100), city_id int references r_city)
create table r_restaurant (id int primary key, name varchar(100), city_id int references r_city)
go
create table r_likes (
	person_id int not null references r_person, 
	restaurant_id int not null references r_restaurant,
	rating int,
	constraint p_1 primary key (person_id, restaurant_id))
create table r_friendof (
	person1_id int not null references r_person, 
	person2_id int not null references r_person, 
	constraint p_21 primary key (person1_id, person2_id))
go
insert r_city values (1,'bellevue','wa'),(2,'seattle','wa'),(3,'redmond','wa') 
insert r_person values (1,'john', 1), (5,'julie', 1), (4,'jacob', 3), (3,'alice', 3), (2,'mary', 2)
insert r_restaurant values  (1,'taco dell', 1), (2,'ginger and spice', 2), (3,'noodle land', 3)

insert r_likes values (1,1,9),(2,2,9),(3,3,9),(4,3,9),(5,3,9)
insert r_friendof values (1,2),(1,5),(2,3),(3,5),(4,2),(5,4)
go
use db_vi
-- friends of john
select p2.Name
from r_person p1 join r_friendof f on p1.id=f.person1_id join r_person p2 on p2.id=f.person2_id
where p1.Name ='john'

-- find restaurants that john likes
select r.name
from r_restaurant r join r_likes l on r.id=l.restaurant_id join person p on p.id=l.person_id
where p.Name ='john'

-- find restaurants that john's friends like
select r.name
from r_person p1 join r_friendof f on p1.id=f.person1_id join r_person p2 on p2.id=f.person2_id
	join r_likes l on l.person_id=p2.id join r_restaurant r on r.id=l.restaurant_id
where p1.Name ='john'

--find people who like a restaurant in the same city they live in
select p.name
from r_restaurant r join r_likes l on r.id=l.restaurant_id join r_person p on p.id=l.person_id
where r.id=p.city_id

--find people who have at least one friend who likes a restaurant in the same city (s)he lives in
select p1.name
from r_person p1 join r_friendof f on p1.id=f.person1_id join r_person p2 on p2.id=f.person2_id
	join r_likes l on l.person_id=p2.id join r_restaurant r on r.id=l.restaurant_id 
where r.id=p2.city_id
