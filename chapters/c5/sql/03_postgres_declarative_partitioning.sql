USE northwind;
GO

select * from products where productname <'N'
select * from products where productname >='N'

--drop table products_p
create table products_p --a szülőtábla virtuális, nem tárol adatot
      (productid int, productname varchar(40), part_key char(1), unitprice money)
partition by range(part_key)

create table products_p_a_m partition of products_p for values from ('a') to ('m');
--figyelj az átfedésre, 'm' a második partícióba fog kerülni
create table products_p_m_z partition of products_p for values from ('m') to ('z');
--create table products_p_n_z partition of products_p for values from ('n') to ('z')
tablespace very_fast_drive;

insert into products_p (productid, productname, part_key, unitprice)
      select productid, productname, substring(productname, 1,1), unitprice from
    products
--a lekérdezések a megfelelő partícióba irányítódnak
select * from products_p where productname <'d' --5
--a partíciók közvetlenül is lekérdezhetők
select * from products_p_a_m where productname <'d' --5
select * from products_p_m_z where productname <'d' --0

--a partíciók egymástól függetlenül kezelhetők
drop table products_p_a_m;
--eltávolítás a szülőtáblából, de az adatokat megtartjuk
alter table products_p detach partition products_p_a_m;
--betöltéshez az új partíció függetlenül létrehozható, majd csatolható a
--szülőtáblához
alter table products_p attach partition products_p_a_m for values from ('a') to ('m');
--érdemes check-megszorításokat létrehozni a partíciókon -> segíti a lekérdezés-
--optimalizálót
