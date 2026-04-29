

--declarative table partitioning
--==============================
select * from products where productname <'N'
select * from products where productname >='N'

--drop table products_p
create table products_p --the parent table is virtual, does not store data
	(productid int, productname varchar(40), part_key char(1), unitprice money)
partition by range(part_key)

create table products_p_a_m partition of products_p for values from ('a') to ('m');  --mind the overlap: inclusive on lower, exclusive upper
create table products_p_m_z partition of products_p for values from ('m') to (MAXVALUE); 
	--to ('z') would result in an error when inserting a product starting with a Z

--put the partition where you want:	
--create table products_p_m_z partition of products_p for values from ('m') to (MAXVALUE) tablespace very_fast_drive;

insert into products_p (productid, productname, part_key, unitprice)
	select productid, productname, lower(substring(productname, 1,1)), unitprice from products order by productname
--queries are redirected to the right partition
select * from products_p where productname <'d' --5
--the partitions can be queried also directly
select * from products_p_a_m where productname <'d' --5
select * from products_p_m_z where productname <'d' --0
--partitons can be managed independently
drop table products_p_a_m;
--remove from the parent table but keep the data
alter table products_p detach partition products_p_a_m;
--for loading, the new partiton can be created independently, then attached to the parent table
alter table products_p attach partition products_p_a_m for values from ('a') to ('m');
--it is recommended to create check constraints on partitions -> helps the query optimizer


--inheritance for the same purpose
--================================
create table products_i --the parent table is virtual, does not store data
	(productid int, productname varchar(40), unitprice money);
--drop table products_i_a_m cascade;
--drop table products_i_n_z cascade;
create table products_i_a_m () inherits (products_i);
alter table products_i_a_m add constraint df_a_m check (lower(left(productname, 1)) >= 'a' and lower(left(productname, 1)) <= 'm');
create table products_i_n_z () inherits (products_i);  --no overlap!
alter table products_i_n_z add constraint df_n_z check (lower(left(productname, 1)) > 'm' and lower(left(productname, 1)) <= 'z');

create rule products_insert_a_m as 
	on insert to products_i where lower(left(productname, 1)) >= 'a' and lower(left(productname, 1)) <= 'm' 
	do instead insert into products_i_a_m values (new.*);
create rule products_insert_n_z as 
	on insert to products_i where lower(left(productname, 1)) > 'm' and lower(left(productname, 1))<= 'z'
	do instead insert into products_i_n_z values (new.*);

delete from products_i;
--loaded data will end up in the right partition
insert into products_i (productid, productname, unitprice)
	select productid, productname, unitprice from products ;

--a select will look up all the partitions
select * from products_i --77
select * from only products_i --0
select * from products_i_a_m --41
select * from products_i_n_z --36



