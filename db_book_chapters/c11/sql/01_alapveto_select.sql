USE northwind;
GO

use NORTHWIND
select * from employees
select lastname, birthdate from employees

--a Londonban található ügyfelek neve
select companyname, city
from customers
--where city LIKE 'L%' and (city LIKE '%b%' or city LIKE '%n%') --részleges egyezés
where city IN ('London', 'Lander')
where city ='London' or city ='Lander'
where city IN ('London')
where city = 'London'
