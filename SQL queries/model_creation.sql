CREATE OR REPLACE MODEL `ecommerce_data.conversion_model`
OPTIONS (
    MODEL_TYPE          = 'LOGISTIC_REG',
    INPUT_LABEL_COLS    = ['label'],
    AUTO_CLASS_WEIGHTS  = TRUE, -- Essential for 1.0 prob issues
    DATA_SPLIT_METHOD   = 'RANDOM'
) AS
SELECT
    * EXCEPT(fullVisitorId)
FROM
    `ecommerce_data.training_view`;