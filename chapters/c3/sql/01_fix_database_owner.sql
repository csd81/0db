USE northwind;
GO

EXEC sp_changedbowner 'sa';
ALTER AUTHORIZATION ON DATABASE::northwind TO sa;
