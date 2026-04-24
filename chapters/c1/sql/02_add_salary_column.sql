IF COL_LENGTH('dbo.Employees', 'Salary') IS NULL
BEGIN
    ALTER TABLE dbo.Employees ADD Salary money NULL;
END
GO

UPDATE dbo.Employees
SET Salary = 1000
WHERE Salary IS NULL;
GO
