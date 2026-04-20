use northwind;
go

-- Stored procedure: enroll an employee into all training sessions
-- that teach at least one skill still needed by the employee.
create or alter procedure dbo.sp_enroll_employee_for_needed_trainings
    @employee_id int
as
begin
    set nocount on;

    begin try
        begin tran;

        declare @category_id int;

        select @category_id = ec.CategoryID
        from Employees e
        inner join EmploymentCategories ec
            on ec.Title = e.Title
        where e.EmployeeID = @employee_id;

        if @category_id is null
        begin
            print 'ERROR: employee not found or category not mapped.';
            rollback tran;
            return;
        end

        ;with missing_skills as (
            select distinct crs.SkillID
            from CategoryRequiredSkills crs
            where crs.CategoryID = @category_id
              and not exists (
                    select 1
                    from TrainingExamResults ter
                    where ter.EmployeeID = @employee_id
                      and ter.SkillID = crs.SkillID
                      and ter.ExamResult <> N'fail'
              )
        ),
        needed_sessions as (
            select distinct ts.SessionID
            from TrainingSessions ts
            inner join TrainingSessionSkills tss
                on tss.SessionID = ts.SessionID
            inner join missing_skills ms
                on ms.SkillID = tss.SkillID
            where not exists (
                select 1
                from TrainingParticipants tp
                where tp.SessionID = ts.SessionID
                  and tp.EmployeeID = @employee_id
            )
        )
        insert into TrainingParticipants (SessionID, EmployeeID, TrainingStatus)
        select
            ns.SessionID,
            @employee_id,
            N'enrolled'
        from needed_sessions ns;

        if @@rowcount = 0
            print 'No matching training sessions to enroll.';
        else
            print 'Employee enrolled into matching training sessions.';

        commit tran;
    end try
    begin catch
        if @@trancount > 0
            rollback tran;

        print 'OTHER ERROR: ' + error_message() + ' (' + cast(error_number() as varchar(20)) + ')';
    end catch
end
go

-- Test: try to enroll employee 1.
exec dbo.sp_enroll_employee_for_needed_trainings @employee_id = 1;
go

-- Verify enrollment records.
select *
from TrainingParticipants
where EmployeeID = 1
order by SessionID;
go
