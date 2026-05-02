USE northwind;
GO

SELECT * FROM ML.PREDICT(MODEL `northwind.nw_model`, (
  SELECT value_numeric, country, categoryid, p_unitprice, discount, pyear
  FROM `northwind.nw`
)) where abs((predicted_value_numeric-value_numeric))/value_numeric<0.4
