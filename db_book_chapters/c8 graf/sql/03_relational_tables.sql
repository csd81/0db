USE northwind;
GO

-- drop table r_friendof
-- drop table r_person
-- drop table r_restaurant
-- drop table r_city
go

create table r_city (id int primary key, name varchar(100), statename varchar(100));
create table r_person (id int primary key, name varchar(100),
    city_id int references r_city);
create table r_restaurant (id int primary key, name varchar(100),
    city_id int references r_city);
go

create table r_likes (
    person_id int not null references r_person,
    restaurant_id int not null references r_restaurant,
    rating int,
    constraint p_1 primary key (person_id, restaurant_id));

create table r_friendof (
    person1_id int not null references r_person,
    person2_id int not null references r_person,
    constraint p_21 primary key (person1_id, person2_id));
go

insert r_city values (1, 'bellevue', 'wa'), (2, 'seattle', 'wa'), (3, 'redmond', 'wa');
insert r_person values (1, 'john', 1), (5, 'julie', 1), (4, 'jacob', 3), (3, 'alice', 3), (2, 'mary', 2);
insert r_restaurant values (1, 'taco dell', 1), (2, 'ginger and spice', 2), (3, 'noodle land', 3);
insert r_likes values (1, 1, 9), (2, 2, 9), (3, 3, 9), (4, 3, 9), (5, 3, 9);
insert r_friendof values (1, 2), (1, 5), (2, 3), (3, 5), (4, 2), (5, 4);
