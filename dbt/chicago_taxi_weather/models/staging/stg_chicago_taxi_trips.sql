
{{ config(materialized='table') }}

SELECT *
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE trip_start_timestamp BETWEEN '2023-06-01' AND '2023-12-31'


