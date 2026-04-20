# 0db

## Northwind adatbázis - rövid összefoglaló

A jegyzet példáinak egy része a Northwind nevű, képzeletbeli kereskedőcég adatbázisán alapul. Az adatbázis tipikus rendeléskezelési struktúrát mutat be: az alkalmazottak ügyfelekkel vesznek fel rendeléseket, a rendelésekhez rendelési tételek tartoznak, a kiszállítást futárcégek végzik, a készletet pedig a terméktábla tartja nyilván.

Az adatbázis másolásához a SQL Server Management Studio `Tasks -> Generate scripts` parancsa használható. Az `Advanced` beállításoknál a `Types of Data to script` opciónál a `Schema and data` értéket kell választani, így a séma, a kulcsok és a kényszerek is átkerülnek. A script futtatásához a forrásadatbázison `db_owner` jogosultság szükséges.

### Főbb táblák

- `Categories`: termékkategóriák.
- `Products`: termékek.
- `Employees`: alkalmazottak, köztük az ügynökök és a főnök-hierarchia.
- `EmployeeTerritories`: az egyes alkalmazottakhoz tartozó területek.
- `Orders`: a rendelések fejadatai, például dátum, ügyfél, alkalmazott és szállító.
- `Order Details`: a rendelések tételei, vagyis a rendelt termék, mennyiség, egységár és kedvezmény.
- `Customers`: vevők.
- `Shippers`: futárcégek.
- `Suppliers`: beszállítók.

### Fontos mezők

- `Categories.CategoryID`: kategória-azonosító, kulcs.
- `Categories.CategoryName`: a kategória neve, például `Beverages`, vagyis italok.
- `Products.ProductID`: termék-azonosító, kulcs.
- `Products.SupplierID`: a beszállítóra mutató külső kulcs.
- `Products.CategoryID`: a termék-kategóriára mutató külső kulcs, a `Categories` táblára hivatkozik.
- `Products.ProductName`: a termék neve.
- `Products.UnitPrice`: a termék aktuális egységára.
- `Products.UnitsInStock`: a termék aktuális raktárkészlete.
- `Products.ReorderLevel`: ha a készlet ez alá csökken, új rendelést kell küldeni a beszállítónak.
- `Products.UnitsOnOrder`: a beszállítói rendelésen lévő, még be nem érkezett egységek száma.
- `Products.Discontinued`: ha `1`, akkor a terméket már nem forgalmazzák, és új rendelésen nem szerepelhet.
- `Orders.OrderID`: a rendelés azonosítója, kulcs.
- `Orders.OrderDate`: a rendelés dátuma.
- `Orders.EmployeeID`: az alkalmazottra mutató külső kulcs.
- `Orders.CustomerID`: a megrendelőre mutató külső kulcs, a `Customers` táblára hivatkozik.
- `Orders.ShipVia`: a rendelés kiszállítójára mutató külső kulcs, a `Shippers` táblára hivatkozik.
- `Order Details.OrderID`, `ProductID`: két mezős kulcs, illetve külön-külön külső kulcsok a `Orders` és `Products` táblára.
- `Order Details.UnitPrice`: a tételen szereplő termékért a rendelés időpontjában fizetendő egységár, amely eltérhet a `Products` táblában aktuálisan szereplő ártól.
- `Order Details.Quantity`: darabszám.
- `Order Details.Discount`: árengedmény. Ha például az értéke `0.05`, akkor a tétel értéke 5%-kal csökkentendő.
- `Employees.EmployeeID`: alkalmazott-azonosító, kulcs.
- `Employees.LastName`: vezetéknév.
- `Employees.Title`: beosztás, például `Sales Manager`.
- `Employees.Country`, `City`: az illető címe.
- `Employees.ReportsTo`: ugyanezen tábla `EmployeeID` mezőjére mutató külső kulcs, vagyis az illető főnöke.
- `Employees.Emp_categ_id`: a beosztás alapján számított beosztásazonosító.
- `Employees.Salary`: az alkalmazott fizetése.
- `EmployeeTerritories.EmployeeID`: alkalmazottra mutató külső kulcs.
- `EmployeeTerritories.TerritoryID`: területre mutató külső kulcs.

### Lényeg

A Northwind példaadatbázis jól szemlélteti az OLTP jellegű, kapcsolt relációs adatmodell működését, és később erre épülnek a jegyzet adatmodellezési, T-SQL és tranzakciókezelési példái.
