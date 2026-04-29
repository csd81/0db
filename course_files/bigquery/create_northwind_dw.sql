--select * from customers
--drop table  northwind_dw
create table northwind_dw as
SELECT (od.unitprice*od.quantity*(1-od.discount))::numeric::float value_numeric,        
case 
when (od.unitprice*od.quantity*(1-od.discount))::numeric::integer < 200 then 'L'
when (od.unitprice*od.quantity*(1-od.discount))::numeric::integer < 1200 then 'M'
when (od.unitprice*od.quantity*(1-od.discount))::numeric::integer >= 1200 then 'H'
else 'N/A' end value_nominal,  --ezt jósoljuk a country, categoryid, p_unitprice, discount, year alapján
c.CustomerID, c.CompanyName, c.Country, c.Balance, o.OrderID,  o.OrderDate, o.RequiredDate, extract(year from o.orderdate) pyear,
                         o.ShippedDate, o.ShipVia, o.Freight, o.ShipName, o.ShipAddress, o.ShipCity, o.ShipRegion, o.ShipPostalCode, o.ShipCountry, od.UnitPrice, od.Quantity, od.Discount,
						 p.ProductName, p.SupplierID, p.CategoryID, 
                         p.QuantityPerUnit, p.UnitPrice p_unitprice, p.UnitsInStock, p.UnitsOnOrder, p.ReorderLevel, p.Discontinued
FROM            Customers AS c INNER JOIN
                Orders AS o ON c.CustomerID = o.CustomerID INNER JOIN
                OrderDetails AS od ON o.OrderID = od.OrderID INNER JOIN
                Products AS p ON od.ProductID = p.ProductID
order by o.orderdate;

select * from northwind_dw -- ->download as csv gomb