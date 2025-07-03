
{{ config(materialized='table') }}

SELECT *
FROM `chicago-taxi-weather.raw.taxi_trips`
WHERE 'Trip Start Timestamp' BETWEEN '2023-06-01' AND '2023-12-31'


