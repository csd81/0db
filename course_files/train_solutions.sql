--TRAINING QUERIES (SOLUTIONS)

--what are the missing skills for Peacock?
select e.LastName, s.skill_id, s.skill_name
from Employees e inner join skill_req sr on e.emp_categ_id=sr.emp_categ_id
inner join train_skill s on s.skill_id=sr.skill_id where e.LastName='Peacock'
except
select e.LastName, s.skill_id, s.skill_name
from Employees e inner join session_exam sx on e.EmployeeID=sx.emp_id
inner join train_skill s on s.skill_id=sx.skill_id where e.LastName='Peacock' and grade<>'fail'

--are there any sessions in the future that are still required for Peacock?
--When? Who is the organizer?
select distinct c.train_comp_name, s.session_code, s.date_start, s.date_end, ss.skill_id
from train_session s inner join session_skill ss on s.session_id=ss.session_id
inner join  train_comp c on c.train_comp_id=s.train_comp_id
where s.date_start > GETDATE() and ss.skill_id in (
	select sr.skill_id
	from Employees e inner join skill_req sr on e.emp_categ_id=sr.emp_categ_id
	where e.LastName='Peacock'
	except
	select sx.skill_id
	from Employees e inner join session_exam sx on e.EmployeeID=sx.emp_id
	where e.LastName='Peacock' and grade<>'fail')
go
--let's create a table-valued function that returns the missing skills for an employeeid
create function f_missing_skills(@emp_id int) returns table as
return
	select sr.skill_id
	from Employees e inner join skill_req sr on e.emp_categ_id=sr.emp_categ_id
	where e.EmployeeID=@emp_id
	except
	select sx.skill_id
	from Employees e inner join session_exam sx on e.EmployeeID=sx.emp_id
	where e.EmployeeID=@emp_id and grade<>'fail'
go
--using this new function, our query is much simpler
select distinct c.train_comp_name, s.session_code, s.date_start, s.date_end, ss.skill_id
from train_session s inner join session_skill ss on s.session_id=ss.session_id
inner join  train_comp c on c.train_comp_id=s.train_comp_id
where s.date_start > GETDATE() and ss.skill_id in (
	select skill_id from dbo.f_missing_skills(4)) --4 is Peacock

--What is the first and last training date and the average duration of trainings in days?
select min(date_start), max(date_start), avg(cast(DATEDIFF(dd, date_start, date_end) as decimal(3,1))) 
from train_session

--Which employee has the most skills with an exam result above ‘fail’?
select e.EmployeeID, e.LastName, COUNT(distinct skill_id) as no_of_skills
from Employees e inner join session_exam sx on e.EmployeeID=sx.emp_id
where  grade<>'fail'
group by e.EmployeeID, e.LastName
order by no_of_skills desc

--What is the total fee paid for all training sessions in which our most skilled employee (see above) participated?
select sum(fees_paid) as fee
from emp_session where emp_id=(
	select top 1 e.EmployeeID
	from Employees e inner join session_exam sx on e.EmployeeID=sx.emp_id
	where  grade<>'fail'
	group by e.EmployeeID
	order by COUNT(distinct skill_id) desc
)

--Which required skill(s) have not yet been addressed by any training session?
select distinct s.skill_id, s.skill_name
from skill_req sr inner join train_skill s on s.skill_id=sr.skill_id
except
select s.skill_id, s.skill_name
from session_skill ss inner join train_skill s on s.skill_id=ss.skill_id

--Using the training queries, create a stored procedure that returns 
--the missing skills for an employee name passed as a parameter. 
--The stored procedure should return a table with a single field 
--containing the missing skills. 
--If the employee cannot be identified, return an error message and no table
go
create procedure sp_missing_skills @name nvarchar(20)
as
declare @address nvarchar(max), @res_no int, @emp_id int
select @res_no=count(*) from Employees where LastName like @name + '%'
if @res_no=0 print 'No matching record.'
else if @res_no>1 print 'More than one matching record.'
else begin  --a single hit
	select e.LastName, s.skill_id, s.skill_name
	from Employees e inner join skill_req sr on e.emp_categ_id=sr.emp_categ_id
	inner join train_skill s on s.skill_id=sr.skill_id 
		where e.LastName=@name
	except
	select e.LastName, s.skill_id, s.skill_name
	from Employees e inner join session_exam sx on e.EmployeeID=sx.emp_id
	inner join train_skill s on s.skill_id=sx.skill_id 
		where e.LastName=@name and grade<>'fail'
end
go
--test
exec sp_missing_skills 'Leverling'

--Write a script that checks whether an employee needs any of the skills 
--offered by a future training session, and if yes, 
--enroll the employee for all such sessions (set status to 'enrolled')
set nocount on
declare @emp_id int, @i int
set @emp_id=7
select @i=count(distinct s.session_id)	
from train_session s inner join  session_skill ss on s.session_id=ss.session_id
where s.date_start > GETDATE() and skill_id in (	
	select skill_id from dbo.f_missing_skills(@emp_id))
and not exists (select 1 from emp_session es where es.emp_id=@emp_id and es.session_id=s.session_id)

if @i>0 print 'Enrolling Employee ' + cast(@emp_id as varchar(50)) + ' for ' + cast(@i as varchar(50))+ ' course(s)' 
else print 'No courses found for Employee ' + cast(@emp_id as varchar(50)) 

if @i>0 begin
	insert emp_session (emp_id, session_id, status)
	select distinct @emp_id, s.session_id, 'enrolled'	
	from train_session s inner join  session_skill ss on s.session_id=ss.session_id
	where s.date_start > GETDATE() and skill_id in (	
		select skill_id from dbo.f_missing_skills(@emp_id))
	print 'Employee successfully enrolled'
end
go
--test
select * from emp_session where emp_id=7
delete emp_session where emp_id=7
--note that the script should check whether the employee has already been enrolled for the future course

--let's make a stored procedure
--drop procedure sp_enrol_emp
go
create procedure sp_enrol_emp (@emp_id int)
as
begin tran
begin try
	declare @i int
	select @i=count(distinct s.session_id)	
	from train_session s inner join  session_skill ss on s.session_id=ss.session_id
	where s.date_start > GETDATE() and skill_id in (	
		select skill_id from dbo.f_missing_skills(@emp_id))
	and not exists (select 1 from emp_session es where es.emp_id=@emp_id and es.session_id=s.session_id)
	--comment out line above to make a logical error
	if @i>0 print 'Enrolling Employee ' + cast(@emp_id as varchar(50)) + ' for ' + cast(@i as varchar(50))+ ' course(s)' 
	else print 'No courses found for Employee ' + cast(@emp_id as varchar(50)) 

	if @i>0 begin
		insert emp_session (emp_id, session_id, status)
		select distinct @emp_id, s.session_id, 'enrolled'	
		from train_session s inner join  session_skill ss on s.session_id=ss.session_id
		where s.date_start > GETDATE() and skill_id in (	
			select skill_id from dbo.f_missing_skills(@emp_id))
		print 'Employee successfully enrolled'
	end
	if @i > 0 commit tran else begin
		print 'Rolling back transaction'
		rollback tran
	end
end try 
begin catch
	print 'OTHER ERROR: '+ ERROR_MESSAGE() + ' (' + cast(ERROR_NUMBER() as varchar(20)) + ')'
	print 'Rolling back transaction'
	rollback tran
end catch
go

--test
select * from emp_session where emp_id=7
delete emp_session where emp_id=7
set nocount on
exec sp_enrol_emp 7 