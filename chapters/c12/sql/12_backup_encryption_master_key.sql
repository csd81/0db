USE northwind;
GO

use master
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'h6twqPNO'
go
--mentés készítése az új MK-ról
OPEN MASTER KEY DECRYPTION BY PASSWORD = 'h6twqPNO'
go
--a mentéshez eltérő jelszót használunk
BACKUP MASTER KEY TO FILE = 'C:\install\exportedmasterkey'
    ENCRYPTION BY PASSWORD = 'h6twqPNOh6twqPNO'
go
--létrehozunk egy privát-publikus kulcspárt és egy önaláírt tanúsítványt
CREATE CERTIFICATE backup_cert_master
--ezt az MK fogja titkosítani
WITH SUBJECT = 'NW DB backup',
    EXPIRY_DATE = '20301031'
--katasztrófa-helyreállítás céljából érdemes mentést készíteni róla
BACKUP CERTIFICATE backup_cert_master TO FILE = 'C:\install\exportedcert'
--visszaállítható a CREATE CERTIFICATE ... paranccsal
--mentést készítünk az adatbázisról
BACKUP DATABASE northwind TO DISK = 'C:\install\nw_enc.bak'
WITH COMPRESSION, ENCRYPTION (
    ALGORITHM = AES_256,
    SERVER CERTIFICATE = backup_cert_master
), STATS = 10
GO
