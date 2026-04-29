--Source:
--https://github.com/microsoft/sql-server-samples/blob/master/samples/features/in-memory-database/in-memory-oltp/t-sql-scripts/enable-in-memory-oltp.sql
set nocount on;
set xact_abort on;

-- 1. validate that in-memory oltp is supported 
if serverproperty('isxtpsupported') = 0
begin
    print 'error: in-memory oltp is not supported for this server edition or database pricing tier.';
end
if db_id() < 5
begin
    print 'error: in-memory oltp is not supported in system databases. connect to a user database.';
end
else
begin
	begin try; 
-- 2. add memory_optimized_data filegroup when not using azure sql db
	if serverproperty('engineedition') != 5
	begin
		declare @sqldatafolder nvarchar(max) = cast(serverproperty('instancedefaultdatapath') as nvarchar(max))
		declare @modname nvarchar(max) = db_name() + '_mod';
		declare @memoryoptimizedfilegroupfolder nvarchar(max) = @sqldatafolder + @modname;

		declare @sql nvarchar(max) = '';

		-- add filegroup 
		if not exists (select 1 from sys.filegroups where type = 'fx')
		begin
			set @sql = '
alter database current
add filegroup ' + quotename(@modname) + ' contains memory_optimized_data;';
			print @sql
			execute (@sql);
		end;
		-- add container in the filegroup
		if not exists (select * from sys.database_files where data_space_id in (select data_space_id from sys.filegroups where type = 'fx'))
		begin
			set @sql = '
alter database current
add file (name = ''' + @modname + ''', filename = '''
						+ @memoryoptimizedfilegroupfolder + ''')
to filegroup ' + quotename(@modname);
			print @sql
			execute (@sql);
		end
	end

	-- 3. set compat level to 130 if it is lower
	if (select compatibility_level from sys.databases where database_id=db_id()) < 130
		alter database current set compatibility_level = 130

	-- 4. enable memory_optimized_elevate_to_snapshot for the database
	alter database current set memory_optimized_elevate_to_snapshot = on;

    end try
    begin catch
        print 'error enabling in-memory oltp';
		if xact_state() != 0
			rollback;
        throw;
    end catch;
end;
