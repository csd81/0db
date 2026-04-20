use northwind;
go

-- Stored procedure: missing skills by employee name.
create or alter procedure dbo.sp_missing_skills_by_name
    @employee_name nvarchar(100)
as
begin
    set nocount on;

    declare
        @emp_id int,
        @category_id int,
        @res_no int;

    select @res_no = count(*)
    from Employees e
    where ltrim(rtrim(concat(
            coalesce(e.TitleOfCourtesy, N''),
            N' ',
            coalesce(e.LastName, N''),
            N' ',
            coalesce(e.FirstName, N'')
    ))) like N'%' + @employee_name + N'%';

    if @res_no = 0
    begin
        print 'ERROR: employee not found.';
        return;
    end

    if @res_no > 1
    begin
        print 'ERROR: employee name is ambiguous.';
        return;
    end

    select
        @emp_id = e.EmployeeID,
        @category_id = ec.CategoryID
    from Employees e
    inner join EmploymentCategories ec
        on ec.Title = e.Title
    where ltrim(rtrim(concat(
            coalesce(e.TitleOfCourtesy, N''),
            N' ',
            coalesce(e.LastName, N''),
            N' ',
            coalesce(e.FirstName, N'')
    ))) like N'%' + @employee_name + N'%';

    select distinct
        s.SkillName as MissingSkill
    from CategoryRequiredSkills crs
    inner join Skills s
        on s.SkillID = crs.SkillID
    where crs.CategoryID = @category_id
      and not exists (
            select 1
            from TrainingExamResults ter
            where ter.EmployeeID = @emp_id
              and ter.SkillID = crs.SkillID
              and ter.ExamResult <> N'fail'
      )
    order by s.SkillName;
end
go

-- Test of the stored procedure.
exec dbo.sp_missing_skills_by_name @employee_name = N'Peacock';
go

-- Table-valued function: missing skills by employee ID.
create or alter function dbo.fn_missing_skills
(
    @employee_id int
)
returns table
as
return
(
    select distinct
        s.SkillName as MissingSkill
    from Employees e
    inner join EmploymentCategories ec
        on ec.Title = e.Title
    inner join CategoryRequiredSkills crs
        on crs.CategoryID = ec.CategoryID
    inner join Skills s
        on s.SkillID = crs.SkillID
    where e.EmployeeID = @employee_id
      and not exists (
            select 1
            from TrainingExamResults ter
            where ter.EmployeeID = e.EmployeeID
              and ter.SkillID = crs.SkillID
              and ter.ExamResult <> N'fail'
      )
);
go

-- Test of the table-valued function.
select *
from dbo.fn_missing_skills(1);
go
