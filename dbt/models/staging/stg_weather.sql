{{ config(
    materialized='incremental',
    unique_key='date'
) }}


SELECT
    DATE(time) AS date,
    temperature_2m_max,
    temperature_2m_min,
    precipitation_sum
FROM `chicago-taxi-weather.raw.weather`

{% if is_incremental() %}
WHERE DATE(time) > (SELECT MAX(date) FROM {{ this }})
{% endif %}