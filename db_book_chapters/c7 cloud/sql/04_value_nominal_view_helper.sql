USE northwind;
GO

select od.unitprice*od.quantity*(1-od.discount) value,
case when (od.unitprice*od.quantity*(1-od.discount)) < 200 then 'L'
      when (od.unitprice*od.quantity*(1-od.discount)) < 1200 then 'M'
      when (od.unitprice*od.quantity*(1-od.discount)) >= 1200 then 'H'
else 'N/A' end value_nominal,
c.CustomerID, c.CompanyName, c.Country, c.Balance, o.OrderID,  o.OrderDate, o.RequiredDate,
year(o.orderdate) pyear,
o.ShippedDate, o.ShipVia, o.Freight, o.ShipName, o.ShipAddress, o.ShipCity, o.ShipRegion,
o.ShipPostalCode, o.ShipCountry, od.UnitPrice, od.Quantity, od.Discount,
p.ProductName, p.SupplierID, p.CategoryID,
p.QuantityPerUnit, p.UnitPrice p_unitprice, p.UnitsInStock, p.UnitsOnOrder, p.ReorderLevel,
p.Discontinued
from Customers AS c join Orders AS o ON c.CustomerID = o.CustomerID join
[Order Details] AS od ON o.OrderID = od.OrderID join
Products AS p ON od.ProductID = p.ProductID
