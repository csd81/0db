USE northwind;
GO

-- forrás: https://docs.microsoft.com/en-us/sql/relational-databases/graphs/sql-graph-sample?view=sql-server-ver15
go
-- use graphdemo
go
-- drop table likes
-- drop table friendof
-- drop table livesin
-- drop table locatedin
-- drop table person
-- drop table restaurant
-- drop table city

-- csomóponttáblák létrehozása
create table person (
    id integer primary key,
    name varchar(100)
) as node;

create table restaurant (
    id integer not null,
    name varchar(100)
    -- city varchar(100)
) as node;

create table city (
    id integer primary key,
    name varchar(100),
    statename varchar(100)
) as node;

-- éltáblák létrehozása
create table likes (rating integer) as edge;
create table friendof as edge;

-- a friendof éltípust úgy szorítjuk meg, hogy CSAK személyeket köthessen össze:
alter table friendof add constraint ec_1 connection (person to person);

create table livesin as edge;
create table locatedin as edge;

-- adatok beszúrása a csomóponttáblákba. egy csomóponttáblába való beszúrás ugyanúgy történik, mint egy szokásos táblába
insert into person values (1, 'john');
insert into person values (2, 'mary');
insert into person values (3, 'alice');
insert into person values (4, 'jacob');
insert into person values (5, 'julie');
insert into person values (6, 'tom');

insert into restaurant values (1, 'taco dell');
insert into restaurant values (2, 'ginger and spice');
insert into restaurant values (3, 'noodle land');

insert into city values (1, 'bellevue', 'wa');
insert into city values (2, 'seattle', 'wa');
insert into city values (3, 'redmond', 'wa');

-- select $node_id, * from city

-- beszúrás az éltáblába. éltáblába való beszúráskor
-- meg kell adnod a $node_id-ket a $from_id és $to_id oszlopokhoz.
insert into likes values ((select $node_id from person where id = 1),
    (select $node_id from restaurant where id = 1), 9);
insert into likes values ((select $node_id from person where id = 2),
    (select $node_id from restaurant where id = 2), 9);
insert into likes values ((select $node_id from person where id = 3),
    (select $node_id from restaurant where id = 3), 9);
insert into likes values ((select $node_id from person where id = 4),
    (select $node_id from restaurant where id = 3), 9);
insert into likes values ((select $node_id from person where id = 5),
    (select $node_id from restaurant where id = 3), 9);
-- select * from likes

insert into livesin values ((select $node_id from person where id = 1),
    (select $node_id from city where id = 1));
insert into livesin values ((select $node_id from person where id = 2),
    (select $node_id from city where id = 2));
insert into livesin values ((select $node_id from person where id = 3),
    (select $node_id from city where id = 3));
insert into livesin values ((select $node_id from person where id = 4),
    (select $node_id from city where id = 3));
insert into livesin values ((select $node_id from person where id = 5),
    (select $node_id from city where id = 1));

insert into locatedin values ((select $node_id from restaurant where id = 1),
    (select $node_id from city where id = 1));
insert into locatedin values ((select $node_id from restaurant where id = 2),
    (select $node_id from city where id = 2));
insert into locatedin values ((select $node_id from restaurant where id = 3),
    (select $node_id from city where id = 3));

-- delete friendof
-- adatok beszúrása a friendof élbe.
insert into friendof values ((select $node_id from person where id = 1),
    (select $node_id from person where id = 2));
insert into friendof values ((select $node_id from person where id = 1),
    (select $node_id from person where id = 5));
insert into friendof values ((select $node_id from person where id = 2),
    (select $node_id from person where id = 3));

-- a friendof IRÁNYÍTOTT él, noha a barátság irányítatlan (kölcsönös) --> az irányítatlan
-- kapcsolatok kifejezésére csak két él használatával van mód
insert into friendof values ((select $node_id from person where id = 3),
    (select $node_id from person where id = 2));
insert into friendof values ((select $node_id from person where id = 3),
    (select $node_id from person where id = 5));

-- ismétlődő él:
insert into friendof values ((select $node_id from person where id = 3),
    (select $node_id from person where id = 6));
insert into friendof values ((select $node_id from person where id = 3),
    (select $node_id from person where id = 6));
insert into friendof values ((select $node_id from person where id = 4),
    (select $node_id from person where id = 2));
insert into friendof values ((select $node_id from person where id = 5),
    (select $node_id from person where id = 4));

-- ismétlődő élek:
select * from friendof
where json_value($from_id, '$.id') = 2 and json_value($to_id, '$.id') = 5;
-- a belső csomópont-id indexelés 0-tól indul, ezért a 3->6 él helyett 2->5-öt adunk meg

-- töröljük az ismétlődő élt:
delete friendof where json_value($edge_id, '$.id') = 8;
