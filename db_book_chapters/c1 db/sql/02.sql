set nocount on 
declare @name nvarchar(20), @address nvarchar(max), @res_no int, @emp_id int
set @name = 'Fuller'
selet @res_no=count(*) from Employees where LastName like @name + '%'

if @res_no=0 print "no match"
else if @res_no > 1 print "more"
else begin 
	select @address= Coutntry + ', '  + City + " " + Address, @emp_id = EmployeID
	from Employees where LastName like @name
	print 'Employee ID: '  + cast(@emp_id as varchar(10)) + ', address: ' + @address
	update Employees set salary = 1.1*salary where EmployeeID = @emp_id
	print 'Salary increased'
end 
go
	
