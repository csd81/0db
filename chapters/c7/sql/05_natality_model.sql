USE northwind;
GO

CREATE MODEL `us_dataset.natality_model`
OPTIONS
  (model_type='linear_reg',
    input_label_cols=['weight_pounds']) AS
SELECT
  weight_pounds,
  is_male,
  gestation_weeks,
  mother_age,
  CAST(mother_race AS string) AS mother_race
FROM
  `bigquery-public-data.samples.natality`
WHERE
  weight_pounds IS NOT NULL AND RAND() < 0.0001

SELECT  * FROM  ML.TRAINING_INFO(MODEL `dataset_nev.natality_model`)

SELECT * FROM ML.PREDICT(MODEL `dataset_nev.natality_model`,
(select true as is_male, 40 as gestation_weeks, 30 as mother_age,'38' as mother_race))
