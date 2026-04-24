USE northwind;
GO

use master
create login nw_user with password='...', default_database=northwind
use northwind --context switch
create user nw_user for login nw_user
alter role db_datareader add member nw_user
