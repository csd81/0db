go
create or alter function dbo.fn_employee_territories (@emp_id int)
returns table
as
return
(
    select
        r.RegionDescription,
        t.TerritoryDescription
    from EmployeeTerritories et
    inner join Territories t on t.TerritoryID = et.TerritoryID
    inner join Region r on r.RegionID = t.RegionID
    where et.EmployeeID = @emp_id
)
go

select *
from dbo.fn_employee_territories(1)
go
