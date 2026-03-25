SELECT
  -- Model Quality Indicators
  ROUND(precision, 4) AS precision,
  ROUND(recall, 4)    AS recall,
  ROUND(accuracy, 4)  AS accuracy,
  ROUND(f1_score, 4)  AS f1_score,
  ROUND(log_loss, 4)  AS log_loss,
  ROUND(roc_auc, 4)   AS roc_auc
FROM
  ML.EVALUATE(MODEL `ecommerce_data.conversion_model`, (
    SELECT
      *
    FROM
      `ecommerce_data.training_view`
  ));