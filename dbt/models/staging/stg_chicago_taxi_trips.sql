
{{ config(materialized='view') }}

SELECT 
    `Trip ID` AS trip_id,
    `Taxi ID` AS taxi_id,
    PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', `Trip Start Timestamp`) AS trip_start_timestamp,
    PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', `Trip End Timestamp`) AS trip_end_timestamp,
    `Trip Seconds` AS trip_seconds,
    `Trip Miles` AS trip_miles,
    `Pickup Census Tract` AS pickup_census_tract,
    `Dropoff Census Tract` AS dropoff_census_tract,
    `Pickup Community Area` AS pickup_community_area,
    `Dropoff Community Area` AS dropoff_community_area,
    `Fare` AS fare,
    `Tips` AS tips,
    `Tolls` AS tolls,
    `Extras` AS extras,
    `Trip Total` AS trip_total,
    `Payment Type` AS payment_type,
    `Company` AS company,
    `Pickup Centroid Latitude` AS pickup_centroid_latitude,
    `Pickup Centroid Longitude` AS pickup_centroid_longitude,
    `Pickup Centroid Location` AS pickup_centroid_location,
    `Dropoff Centroid Latitude` AS dropoff_centroid_latitude,
    `Dropoff Centroid Longitude` AS dropoff_centroid_longitude,
    `Dropoff Centroid  Location` AS dropoff_centroid_location
FROM `chicago-taxi-weather.raw.taxi_trips`
WHERE PARSE_TIMESTAMP('%m/%d/%Y %I:%M:%S %p', `Trip Start Timestamp`) BETWEEN '2023-06-01' AND '2023-12-31'
AND `Trip Miles` IS NOT NULL
AND `Trip Miles` > 0

