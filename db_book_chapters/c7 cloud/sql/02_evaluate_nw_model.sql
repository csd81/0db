USE northwind;
GO

SELECT * FROM ML.EVALUATE(MODEL `northwind.nw_model`, (
  SELECT value_numeric, country, categoryid, p_unitprice, discount, pyear
  FROM `northwind.nw`
))
