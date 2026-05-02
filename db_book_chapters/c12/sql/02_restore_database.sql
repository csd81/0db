USE northwind;
GO

USE [master]
RESTORE DATABASE [northwind] FROM DISK = N'C:\Program Files\Microsoft SQL Server\MSSQL14.PRIM\MSSQL\Backup\nw'
WITH FILE = 1, NOUNLOAD, REPLACE, STATS = 5
