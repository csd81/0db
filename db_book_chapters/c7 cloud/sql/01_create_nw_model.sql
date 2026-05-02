USE northwind;
GO

CREATE MODEL `northwind.nw_model` OPTIONS (model_type='linear_reg', input_label_cols=['value_numeric']) AS
SELECT value_numeric, country, categoryid, p_unitprice, discount, pyear
-- ha a select lista nem tartalmazza az osztálycímkét, a következő hibaüzenetet kapod:
-- 'Unable to identify the label column'
FROM `northwind.nw`
WHERE value_numeric is not null
