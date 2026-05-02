USE northwind;
GO

select DP1.name as DatabaseRoleName, isnull (DP2.name, 'No members') as DatabaseUserName
from sys.database_role_members as DRM
    right outer join sys.database_principals as DP1 on DRM.role_principal_id = DP1.principal_id
    left outer join sys.database_principals as DP2 on DRM.member_principal_id = DP2.principal_id
where DP1.type = 'R' --R: adatbázis-szerepkör
order by DP1.name
