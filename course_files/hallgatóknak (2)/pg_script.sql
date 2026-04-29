--Demo postgres adatbázis a Northwind alapján
--Products, Orders/Details, Customers
--2021 tavasz

--Products
--drop table products
CREATE TABLE Products(
	ProductID int NOT NULL, --figyelem!
	ProductName varchar(40) NOT NULL,
	SupplierID int NULL,
	CategoryID int NULL,
	QuantityPerUnit varchar(20) NULL,
	UnitPrice money NULL,
	UnitsInStock smallint NULL check(UnitsInStock >= 0),
	UnitsOnOrder smallint NULL,
	ReorderLevel smallint NULL,
	Discontinued smallint NOT NULL, 
 CONSTRAINT PK_Products PRIMARY KEY  
(
	ProductID 
));
--10 termék
INSERT INTO  Products (ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued) 
VALUES (1, 'Chai', 1, 1, '10 boxes x 20 bags', 18.0000, 39, 0, 10, 0);
INSERT INTO  Products (ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
VALUES (2, 'Chang', 1, 1, '24 - 12 oz bottles', 19.0000, 17, 40, 25, 0);
INSERT INTO  Products (ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
VALUES (3, 'Aniseed Syrup', 1, 2, '12 - 550 ml bottles', 10.0000, 83, 0, 25, 0);
INSERT INTO  Products (ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
VALUES (4, 'Chef Anton''s Cajun Seasoning', 2, 2, '48 - 6 oz jars', 22.0000, 53, 0, 0, 0);
INSERT INTO  Products (ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
VALUES (5, 'Chef Anton''s Gumbo Mix', 2, 2, '36 boxes', 21.3500, 0, 0, 0, 1);
INSERT INTO  Products (ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
VALUES (6, 'Grandma''s Boysenberry Spread', 3, 2, '12 - 8 oz jars', 25.0000, 120, 0, 25, 0);
INSERT INTO  Products (ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
VALUES (7, 'Uncle Bob''s Organic Dried Pears', 3, 7, '12 - 1 lb pkgs.', 30.0000, 15, 0, 10, 0);
INSERT INTO  Products (ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
VALUES (8, 'Northwoods Cranberry Sauce', 3, 2, '12 - 12 oz jars', 40.0000, 6, 0, 0, 0);
INSERT INTO  Products (ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
VALUES (9, 'Mishi Kobe Niku', 4, 6, '18 - 500 g pkgs.', 97.0000, 9, 0, 0, 1);
INSERT INTO  Products (ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued)
VALUES (10, 'Ikura', 4, 8, '12 - 200 ml jars', 31.0000, 23, 0, 0, 0);
--select * from products;
------------------------------------
--drop table customers;
CREATE TABLE customers(
	customerid nchar(5) NOT NULL,
	companyname varchar(40) NOT NULL,
	country varchar(15) NOT NULL,
	balance money null check(balance >= '0.00'),
 CONSTRAINT PK_cust PRIMARY KEY  
(
	customerid 
));
--3 vásárló
INSERT INTO Customers  (CustomerID, CompanyName, Country, Balance) VALUES ('ALFKI', 'Alfreds Futterkiste', 'Germany', 20000.0);
INSERT INTO Customers  (CustomerID, CompanyName, Country, Balance) VALUES ('ANATR',	'Ana Trujillo Emparedados y helados', 'Mexico', 12000.0);
INSERT INTO Customers  (CustomerID, CompanyName, Country, Balance) VALUES ('AROUT',	'Around the Horn', 'UK', 10000.0);
--select * from customers;
---------------------------------------
--drop table orders
--drop sequence seq_orders
create sequence seq_orders start 1 increment 1;
CREATE TABLE Orders(
	OrderID integer NOT NULL, --identity helyett seq
	CustomerID nchar(5) NOT NULL references customers(customerid),
	OrderDate timestamp without time zone DEFAULT now()::timestamp NULL,
	RequiredDate date NULL,
	ShippedDate date NULL,
	ShipVia int NULL,
	Freight money NULL,
	ShipName varchar(40) NULL,
	ShipAddress varchar(60) NULL,
	ShipCity varchar(15) NULL,
	ShipRegion varchar(15) NULL,
	ShipPostalCode varchar(10) NULL,
	ShipCountry varchar(15) NULL,
 CONSTRAINT PK_Orders PRIMARY KEY  
(
	OrderID 
));
--nincs rendelésünk (üres a tábla)
--drop table OrderDetails
CREATE TABLE OrderDetails(
	orderid int NOT NULL references orders(orderid),
	productid int NOT NULL references products(productid),
	unitprice money NOT NULL,
	quantity smallint NOT NULL check(quantity >= 0),
	discount DOUBLE PRECISION NOT NULL,
 CONSTRAINT PK_Order_Details PRIMARY KEY  
(
	orderid ,    
	productid 
));
--(üres a tábla)
create or replace function new_order (var_productid integer, var_quantity integer, var_custid char(5)) returns integer as
$$
declare var_stock integer; var_unitprice money; var_balance money; var_orderid int;
begin  
	select unitsinstock, unitprice into var_stock, var_unitprice from products where productid = var_productid;
	select balance into var_balance from customers where customerid = var_custid;
	if var_quantity * var_unitprice > var_balance or var_stock < var_quantity then 
		raise notice 'Készlet vagy egyenleg hiba';
		return 1; --"the function either succeeds in its entirety or fails in its entirety"--no commit/rollback needed
	else 
		update customers set balance = balance - var_quantity * var_unitprice where customerid = var_custid;
		var_orderid := nextval('seq_orders');
		insert into orders (orderid, customerid) values (var_orderid, var_custid);
		insert into OrderDetails (orderid, productid, unitprice, quantity, discount) values (var_orderid, var_productid, var_unitprice, var_quantity, 0);
		update products set unitsinstock = unitsinstock - var_quantity where productid = var_productid;
		return 0;	
	end if;
end;
$$
language 'plpgsql';

--teszt
/*
select * from products where productid=1 --unitprice 18 unitsinstock 10 Chai
select * from customers where customerid='ALFKI' --balance 20000
select * from orders;
select * from orderdetails
update products set unitsinstock = 10 where productid=1
update customers set balance=2 where customerid='ALFKI'
--futtatás
select new_order(1, 1, 'ALFKI') --0 : OK
select new_order(1, 11, 'ALFKI') --1 NOTICE:  Készlet vagy egyenleg hiba: OK
*/
--lekérdezéshez egy view
--drop view last_orders;
create view last_orders as
select o.orderdate::timestamp(0) without time zone AS orderdate, c.companyname, c.country, c.balance, p.productname, od.quantity, od.quantity * od.unitprice AS value, p.unitsinstock
from products p join orderdetails od on p.productid=od.productid
	join orders o on o.orderid=od.orderid
	join customers c on c.customerid=o.customerid
order by orderdate desc limit 5;
--select * from last_orders;
