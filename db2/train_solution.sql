use northwind;
go

-- 1) Missing skills for Mrs. Peacock.
with peacock as (
    select top 1
        e.EmployeeID,
        ec.CategoryID
    from Employees e
    inner join EmploymentCategories ec
        on ec.Title = e.Title
    where e.TitleOfCourtesy = N'Mrs.'
      and e.LastName = N'Peacock'
)
select distinct
    s.SkillName as MissingSkill
from peacock p
inner join CategoryRequiredSkills crs
    on crs.CategoryID = p.CategoryID
inner join Skills s
    on s.SkillID = crs.SkillID
where not exists (
    select 1
    from TrainingParticipants tp
    inner join TrainingExamResults ter
        on ter.SessionID = tp.SessionID
       and ter.EmployeeID = tp.EmployeeID
    where tp.EmployeeID = p.EmployeeID
      and ter.SkillID = s.SkillID
      and ter.ExamResult <> N'fail'
)
order by s.SkillName;
go

-- 2) Future sessions Peacock still needs to attend because they teach missing skills.
with peacock as (
    select top 1
        e.EmployeeID,
        ec.CategoryID
    from Employees e
    inner join EmploymentCategories ec
        on ec.Title = e.Title
    where e.TitleOfCourtesy = N'Mrs.'
      and e.LastName = N'Peacock'
),
missing_skills as (
    select distinct crs.SkillID
    from peacock p
    inner join CategoryRequiredSkills crs
        on crs.CategoryID = p.CategoryID
    where not exists (
        select 1
        from TrainingParticipants tp
        inner join TrainingExamResults ter
            on ter.SessionID = tp.SessionID
           and ter.EmployeeID = tp.EmployeeID
        where tp.EmployeeID = p.EmployeeID
          and ter.SkillID = crs.SkillID
          and ter.ExamResult <> N'fail'
    )
)
select distinct
    ts.SessionID,
    ts.BeginDate,
    ts.EndDate,
    tc.CompanyName,
    ts.Location,
    s.SkillName
from peacock p
inner join missing_skills ms
    on 1 = 1
inner join TrainingSessionSkills tss
    on tss.SkillID = ms.SkillID
inner join TrainingSessions ts
    on ts.SessionID = tss.SessionID
inner join TrainingCompanies tc
    on tc.CompanyID = ts.CompanyID
inner join Skills s
    on s.SkillID = tss.SkillID
where ts.BeginDate > cast(getdate() as date)
order by ts.BeginDate, ts.SessionID, s.SkillName;
go

-- 3) First and last training date, plus average training duration in days.
select
    min(BeginDate) as FirstTrainingDate,
    max(EndDate) as LastTrainingDate,
    cast(avg(cast(datediff(day, BeginDate, EndDate) + 1 as decimal(10, 2))) as decimal(10, 2)) as AvgDurationDays
from TrainingSessions;
go

-- 4) Employee with the most skills that have an exam result above/following 'fail'.
select top 1
    e.EmployeeID,
    concat(e.TitleOfCourtesy, N' ', e.LastName, N' ', e.FirstName) as EmployeeName,
    count(distinct ter.SkillID) as SuccessfulSkills
from Employees e
inner join TrainingParticipants tp
    on tp.EmployeeID = e.EmployeeID
inner join TrainingExamResults ter
    on ter.SessionID = tp.SessionID
   and ter.EmployeeID = tp.EmployeeID
where ter.ExamResult <> N'fail'
group by e.EmployeeID, e.TitleOfCourtesy, e.LastName, e.FirstName
order by count(distinct ter.SkillID) desc, e.EmployeeID;
go

-- 5) Total fee paid for the training sessions attended by the most skilled employee.
with top_employee as (
    select top 1
        e.EmployeeID
    from Employees e
    inner join TrainingParticipants tp
        on tp.EmployeeID = e.EmployeeID
    inner join TrainingExamResults ter
        on ter.SessionID = tp.SessionID
       and ter.EmployeeID = tp.EmployeeID
    where ter.ExamResult <> N'fail'
    group by e.EmployeeID
    order by count(distinct ter.SkillID) desc, e.EmployeeID
),
employee_session_years as (
    select distinct
        ts.CompanyID,
        year(ts.BeginDate) as FeeYear
    from top_employee te
    inner join TrainingParticipants tp
        on tp.EmployeeID = te.EmployeeID
    inner join TrainingSessions ts
        on ts.SessionID = tp.SessionID
)
select
    sum(cyf.FeeAmount) as TotalFeePaid
from employee_session_years esy
inner join CompanyYearFees cyf
    on cyf.CompanyID = esy.CompanyID
   and cyf.FeeYear = esy.FeeYear;
go

-- 6) Required skills that have not yet been addressed by any training session.
select distinct
    s.SkillName
from CategoryRequiredSkills crs
inner join Skills s
    on s.SkillID = crs.SkillID
where not exists (
    select 1
    from TrainingSessionSkills tss
    where tss.SkillID = crs.SkillID
)
order by s.SkillName;
go
