USE northwind;
GO

insert my_table(image_column)
select * from openrowset(bulk 'c:\my_path\my_photo.png', single_blob);
