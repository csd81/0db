-- Northwind bootstrap script.
-- Requires SQLCMD mode in SSMS because of the :r include below.
-- Place this file next to instnwnd.sql and run it in master or any database context.

IF DB_ID(N'Northwind') IS NULL
BEGIN
    CREATE DATABASE Northwind;
END
GO

USE Northwind;
GO

:r instnwnd.sql
