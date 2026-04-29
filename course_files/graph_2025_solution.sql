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

/***************************************** Solutions to problems ******************************/

/* PROBLEM 1  */
/* Implement the Orders, Order Details and Products tables of the Northwind database as a graph and write a T-SQL script that copies the contents into the new graph tables. Query the income by year and product name. 
Compare the relational version to the graph-based version of the same query.
 */

--***SOLUTION BEGIN:***

go
create table g_products (productid int primary key, productname nvarchar(40) not null) as node
create table g_orders (orderid int primary key, orderdate date not null) as node
create table g_details (quantity smallint not null, value money not null) as edge
go
alter table g_details add constraint ec_2 connection (g_orders to g_products)
go
insert g_orders (orderid, orderdate) 
	select OrderID, orderdate from northwind..Orders --830
insert g_products (productid, productname) 
	select ProductID, ProductName from northwind..Products --77
insert g_details ($from_id, $to_id, quantity, value)
	select o.$node_id, p.$node_id, od.Quantity, od.Quantity*od.UnitPrice*(1-od.Discount)
	from g_orders o join northwind..[Order Details] od on o.orderid=od.OrderID
		join g_products p on od.ProductID=p.productid --2155
go
--query the value by the year and product:
select p.productname, year(o.orderdate) year, sum(d.value) value
from g_products p, g_orders o, g_details d
where match(o-(d)->p)
group by p.productname, year(o.orderdate) 
order by year, value desc --227

--this should return exactly the same record set as the relational query:
select p.productname, year(o.orderdate) year, sum(od.Quantity*od.UnitPrice*(1-od.Discount)) value
from northwind..Orders o join northwind..[Order Details] od on o.OrderID=od.OrderID
	join northwind..Products p on p.ProductID=od.ProductID
group by p.productname, year(o.orderdate) 
order by year, value desc --227
go
--cleaning up
drop table g_details
drop table g_orders
drop table g_products
go
--which way of modeling and querying do you prefer?
--***SOLUTION END***


--MIGRATE Northwind to Neo4j
--prepare csv files
create view vi_products as select productid, productname from products
go
create view vi_orders as select orderid, cast(orderdate as date) odate from orders
go
create view vi_orders_products as
select o.orderid, p.productid, od.Quantity quantity, od.Quantity*od.UnitPrice*(1-od.Discount) price
from orders o join [Order Details] od on o.orderid=od.OrderID
		join products p on od.ProductID=p.productid 
go --use the export data wizard, copy csv files into the Import directory of Neo4j

--import data in Neo4j
load csv with headers from 'file:///products.csv' as line 
create (p:product {id: line.productid, name: line.productname}) 
return p.id, p.name

load csv with headers from 'file:///orders.csv' as line 
create (o:orders {id: line.orderid, odate: date(line.odate)}) 
return o.id, o.odate;

load csv with headers from 'file:///orders_products.csv' as line 
match (p:product {id: line.productid}), (o:orders {id: line.orderid}) 
merge (o) -[c:CONTAINS 
{quantity: toInteger(line.quantity), price: toFloat(line.price)}]-> (p) 
return c;

--PROBLEM: query the value by the year and product in Cypher:
--***SOLUTION BEGIN:***

match  (p:product)-[c:CONTAINS]-(o:orders)
return p.name, o.odate.year,  sum(c.price*c.quantity)

--***SOLUTION END***


--Write Neo4j QUERIES--------------------------
--***SOLUTION BEGIN:***

•	Query those persons who directed a movie in which they acted
match (p:Person)-[:DIRECTED]-(m:Movie), (p:Person)-[:ACTED_IN]-(m:Movie) 
return p.name,m .title

•	Find all the followers of the persons above
match (p:Person)-[:DIRECTED]-(m:Movie), (p:Person)-[:ACTED_IN]-(m:Movie) , (p2:Person)-[:FOLLOWS]->(p:Person) 
return p.name,m .title, p2.name

•	Find the person who acted in the most movies which have a rating above 50
match (p:Person)-[:ACTED_IN]-(m:Movie)-[r:REVIEWED]-() where r.rating>50 
return p.name, count(*), avg(r.rating) order by count(*) desc limit 1

•	Add a new hypothetical film to the graph that was directed by Ron Howard
--
--***SOLUTION END***


/* PROBLEM 2  */
/* TEST SQL SERVER GRAPH PERFORMANCE */
--2.	Write a T-SQL script to generate a random graph with 1000 nodes and 500 edges in SQL Server 
--and measure the time needed to calculate the diameter

--***SOLUTION BEGIN:***

use test
create table friends (id int primary key) as node
create table knows as edge
go
set nocount on
delete friends
delete knows
declare @i int = 0, @e int = 2, @n int = 350 --size of graph
declare @j int, @k int
while @i < @n begin
	insert friends values (@i)
	set @i = @i+1
end
set  @i = 0
while @i < @e*@n begin --everybody has e friends
	set @j = @n*rand()
	set @k = @n*rand()
	if @j = @k set @k = (@k+1) % @n
	insert knows values ((select $node_id from friends where id = @j), (select $node_id from friends where id = @k))
	set @i = @i+1
end
go
--select * from knows
--select * from friends
go
set statistics time on
set statistics io on

--find the maximum of all the shortest paths (the diameter of the graph)
select MAX(depth) from (
	select p1.id,  --p1.id+'->'+string_agg(p2.name, '->') within group (graph path) paths,
		last_value(p2.id) within group (graph path) last_id,
		count(p2.id) within group (graph path) depth
	from friends p1, friends for path as p2, knows for path as friend 
	where match(shortest_path(p1(-(friend)->p2) +)) ) a
--e=3 n=350 : 5s (depth 13), n=700: 22s (14)
--e=2 n=350 : 4s (26), n=700: 17s (21), n=900: 36s (24)
--it seems we hit a hard limit at around 1000 nodes
--n=1000, edges=500 -> depth=20, runtime 33 sec

--MIGRATE TO Neo4j
--we must create new tables to get rid of hidden fields
select json_value($from_id, '$.id') p1 ,json_value($to_id, '$.id') p2 into vknows from knows
select json_value($node_id, '$.id') p into vfriends from friends

--> export to knows.txt, friends.txt

load csv with headers from 'file:///friends.txt' as line
create (p:friends {id: line.p})
return p.id

load csv with headers from 'file:///knows.txt' as line
match (p_1:friends {id: line.p1}), (p_2:friends {id: line.p2})
merge (p_1) -[c:knows]-> (p_2)
return c

match (p1:friends), (p2:friends) where id(p1)>(id(p2)) 
match p=shortestPath((p1:friends)-[:knows*]-(p2:friends))
return p, length(p) as length order by length desc limit 1

--n=1000, edges=500 -> depth=9, runtime 2 sec
--***SOLUTION END***


