USE northwind;
GO

create table products_i --a szülőtábla virtuális, nem tárol adatot
      (productid int, productname varchar(40), unitprice money);
--drop table products_i_a_m cascade;
--drop table products_i_n_z cascade;
create table products_i_a_m () inherits (products_i);
alter table products_i_a_m add constraint df_a_m check (lower(left(productname, 1)) >=
    'a' and lower(left(productname, 1)) <= 'm');
create table products_i_n_z () inherits (products_i); --nincs átfedés!
alter table products_i_n_z add constraint df_n_z check (lower(left(productname, 1)) >
    'm' and lower(left(productname, 1)) <= 'z');

create rule products_insert_a_m as
      on insert to products_i where lower(left(productname, 1)) >= 'a' and
    lower(left(productname, 1)) <= 'm'
      do instead insert into products_i_a_m values (new.*);
create rule products_insert_n_z as
      on insert to products_i where lower(left(productname, 1)) > 'm' and
    lower(left(productname, 1))<= 'z'
      do instead insert into products_i_n_z values (new.*);

delete from products_i;
--a betöltött adatok a megfelelő partícióba kerülnek
insert into products_i (productid, productname, unitprice)
      select productid, productname, unitprice from products ;

--egy select az összes partícióban keres
select * from products_i --77
select * from only products_i --0
select * from products_i_a_m --41
select * from products_i_n_z --36
