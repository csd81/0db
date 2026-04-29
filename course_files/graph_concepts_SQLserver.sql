go
--use  graphdemo 
go
	--drop table likes
	--drop table friendof
	--drop table livesin
	--drop table locatedin
	--drop table person
	--drop table restaurant
	--drop table city

-- create node tables
create table person (
  id integer primary key,
  name varchar(100)
) as node 
create table restaurant (
  id integer not null,
  name varchar(100),
--  city varchar(100)
) as node 
create table city (
  id integer primary key,
  name varchar(100),
  statename varchar(100)
) as node 

-- create edge tables. 
create table likes (rating integer) as edge 
create table friendof as edge 
--we constrain the friendof edge type to connect ONLY persons:
alter table friendof add constraint ec_1 connection (person to person)

create table livesin as edge 
create table locatedin as edge 

-- insert data into node tables. inserting into a node table is same as inserting into a regular table
insert into person values (1,'john') 
insert into person values (2,'mary') 
insert into person values (3,'alice') 
insert into person values (4,'jacob') 
insert into person values (5,'julie') 
insert into person values (6,'tom') 

insert into restaurant values (1,'taco dell') 
insert into restaurant values (2,'ginger and spice') 
insert into restaurant values (3,'noodle land') 

insert into city values (1,'bellevue','wa') 
insert into city values (2,'seattle','wa') 
insert into city values (3,'redmond','wa') 
--select $node_id, * from city

-- insert into edge table. while inserting into an edge table,
-- you need to provide the $node_id from $from_id and $to_id columns.
insert into likes values ((select $node_id from person where id = 1), 
       (select $node_id from restaurant where id = 1),9) 
insert into likes values ((select $node_id from person where id = 2), 
      (select $node_id from restaurant where id = 2),9) 
insert into likes values ((select $node_id from person where id = 3), 
      (select $node_id from restaurant where id = 3),9) 
insert into likes values ((select $node_id from person where id = 4), 
      (select $node_id from restaurant where id = 3),9) 
insert into likes values ((select $node_id from person where id = 5), 
      (select $node_id from restaurant where id = 3),9) 
--select * from likes

insert into livesin values ((select $node_id from person where id = 1),
      (select $node_id from city where id = 1)) 
insert into livesin values ((select $node_id from person where id = 2),
      (select $node_id from city where id = 2)) 
insert into livesin values ((select $node_id from person where id = 3),
      (select $node_id from city where id = 3)) 
insert into livesin values ((select $node_id from person where id = 4),
      (select $node_id from city where id = 3)) 
insert into livesin values ((select $node_id from person where id = 5),
      (select $node_id from city where id = 1)) 

insert into locatedin values ((select $node_id from restaurant where id = 1),
      (select $node_id from city where id =1)) 
insert into locatedin values ((select $node_id from restaurant where id = 2),
      (select $node_id from city where id =2)) 
insert into locatedin values ((select $node_id from restaurant where id = 3),
      (select $node_id from city where id =3)) 

--delete friendof
-- insert data into the friendof edge.
insert into friendof values ((select $node_id from person where id = 1), (select $node_id from person where id = 2)) 
insert into friendof values ((select $node_id from person where id = 1), (select $node_id from person where id = 5)) 
insert into friendof values ((select $node_id from person where id = 2), (select $node_id from person where id = 3)) 
--friendof is a DIRECTED edge though friendship is undirected (mutual) --> no way to express undirected relationships except using two edges
insert into friendof values ((select $node_id from person where id = 3), (select $node_id from person where id = 2)) 
insert into friendof values ((select $node_id from person where id = 3), (select $node_id from person where id = 5)) 
--repeated edge:
insert into friendof values ((select $node_id from person where id = 3), (select $node_id from person where id = 6)) 
insert into friendof values ((select $node_id from person where id = 3), (select $node_id from person where id = 6)) 

insert into friendof values ((select $node_id from person where id = 4), (select $node_id from person where id = 2)) 
insert into friendof values ((select $node_id from person where id = 5), (select $node_id from person where id = 4)) 

--repeated edges:
select * from friendof where json_value($from_id, '$.id') = 2 and json_value($to_id, '$.id') = 5 
--the internal node id indexing starts from 0, so instead of the edge 3->6, we specify 2->5
--we delete the repeated edge:
delete friendof where json_value($edge_id, '$.id') = 8 

---------------------------------QUERIES--------------------------
-- friends of john
select p2.name 
from person p1, person p2, friendof
where match(p1-(friendof)->p2)
and p1.name='john' 

-- find restaurants that john likes
select restaurant.name
from person, likes, restaurant
where match (person-(likes)->restaurant)
and person.name = 'john' 

-- find restaurants that john's friends like
select restaurant.name 
from person person1, person person2, likes, friendof, restaurant
where match(person1-(friendof)->person2-(likes)->restaurant)
and person1.name='john' 

--find people who like a restaurant in the same city they live in
select person.id, person.name
from person, likes, restaurant, livesin, city, locatedin
where match (person-(likes)->restaurant-(locatedin)->city and person-(livesin)->city) 

--find people who have at least one friend who likes a restaurant in the same city (s)he lives in
select distinct p1.id, p1.name
from person p1, person p2, friendof, likes, restaurant, livesin, city, locatedin
where match (p1-(friendof)->p2 and p2-(likes)->restaurant-(locatedin)->city and p2-(livesin)->city) 

-- find 2 people who are both friends with same person
--friendof is a DIRECTED edge though the relationship is undirected (mutual) --no way to express undirected relationships except using two edges
select p0.name person, p1.name Friend1, p2.name Friend2
from person p1, friendof f1, person p2, friendof f2, person p0
--where match(p1-(f1)->p0<-(f2)-p2) and p1.id <> p2.id
where match(p1-(f1)->p0 and p2-(f2)->p0) and p1.id <> p2.id  --equivalent

--SHORTEST_PATH---------------------------------------------
--friends: all shortest paths from John
select p1.name,  p1.name+'->'+string_agg(p2.name, '->') within group (graph path) paths,
	last_value(p2.Name) within group (graph path) last_name
	,count(p2.name) within group (graph path) depth
from person p1, person for path as p2, 
    friendof for path as friend 
--where match(shortest_path(p1(-(friend)->p2) {1,2})) and p1.name='john' --does not contain the length 3 john->mary->alice->tom path
where match(shortest_path(p1(-(friend)->p2) +)) and p1.name='john' --contains all

--friends: the shortest path between John and Jacob
select name, paths, depth
from (
	select p1.name, p1.name+ '->'+string_agg(p2.name, '->') within group (graph path) paths,
		last_value(p2.Name) within group (graph path) last_name
		, count(p2.name) within group (graph path) depth
	from person p1, person for path as p2, 
		friendof for path as friend 
	where match(shortest_path(p1(-(friend)->p2)+)) and p1.name='john' --and p2.name='jacob' --ERROR: cannot select columns from FOR PATH tables
) a where last_name = 'jacob'


--Note:
--node query for Gephi
select json_value($node_id, '$.id') AS id, name label from person
--edge query for Gephi
select json_value($from_id, '$.id') source, json_value($to_id, '$.id') target 
from friendof where json_value($from_id, '$.table') = 'person' and json_value($to_id, '$.table') = 'person'


/* NORTHWIND AS A GRAPH DATABASE  */

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

--which way of modeling and querying do you prefer?