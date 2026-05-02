USE northwind;
GO

use master
dbcc shrinkdatabase(northwind, 10)
