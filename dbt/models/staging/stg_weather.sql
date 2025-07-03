{{ config(materialized='view') }}

SELECT
    DATE(time) AS date,
    temperature_2m_max,
    temperature_2m_min,
    precipitation_sum
FROM `chicago-taxi-weather.raw.weather`