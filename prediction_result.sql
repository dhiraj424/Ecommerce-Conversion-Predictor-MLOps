SELECT
  fullVisitorId,
  predicted_label,
  ROUND(p.predicted_label_probs[OFFSET(0)].prob, 4) AS purchase_probability
FROM
  ML.PREDICT(MODEL `ecommerce_data.conversion_model`, (
    SELECT * FROM `ecommerce_data.training_view`
  )) AS p
LIMIT 10;