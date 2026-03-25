CREATE OR REPLACE VIEW `ecommerce_data.training_view` AS
SELECT
  fullVisitorId,
  IF(totals.transactions IS NULL, 0, 1) AS label,
  IFNULL(device.operatingSystem, "Unknown") AS os,
  device.isMobile AS is_mobile,
  -- Clipping pageviews to avoid outliers/leakage
  IF(totals.pageviews > 50, 50, IFNULL(totals.pageviews, 0)) AS pageviews,
  IFNULL(totals.timeOnSite, 0) AS time_on_site,
  -- Adding Traffic Source as a new professional feature
  IFNULL(trafficSource.medium, "(none)") AS medium
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_*`
WHERE
  _TABLE_SUFFIX BETWEEN '20170101' AND '20170801';