{{ config(materialized='table') }}

WITH trips AS (
    SELECT
        DATE(trip_start_timestamp) AS date,
        AVG(trip_seconds) / 60 AS avg_trip_duration_min,
        AVG(trip_total) AS avg_trip_total,
        AVG(trip_miles) AS avg_trip_miles,
        COUNT(*) AS trip_count
    FROM {{ ref('stg_chicago_taxi_trips') }}
    GROUP BY date
),

weather AS (
    SELECT
        date,
        temperature_2m_max,
        temperature_2m_min,
        precipitation_sum
    FROM {{ ref('stg_weather') }}
)

SELECT
    t.date,
    t.avg_trip_duration_min,
    t.avg_trip_total,
    t.avg_trip_miles,
    t.trip_count,
    w.temperature_2m_max,
    w.temperature_2m_min,
    w.precipitation_sum
FROM trips t
LEFT JOIN weather w
    ON t.date = w.date
