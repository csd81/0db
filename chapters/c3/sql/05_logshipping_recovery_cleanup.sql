USE northwind;
GO

use master
alter database nw_ship set single_user with rollback immediate
restore database nw_ship with recovery
alter database nw_ship set multi_user
