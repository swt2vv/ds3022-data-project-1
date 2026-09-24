/* This is the SQL dbt version of the transform for green taxi trips */
/* In this model, I am transforming the raw green taxi trip data by adding 
CO2 emissions and other derived metrics. */
/* This is useful to do instead of python because it is more efficient and allows for easier maintenance. */
SELECT g.*,
    g.trip_distance * (e.co2_grams_per_mile / 1000) AS trip_co2_kgs,
    g.trip_distance / (date_diff('second', g.lpep_pickup_datetime, g.lpep_dropoff_datetime) / 3600) AS avg_mph,
    date_part('hour', g.lpep_pickup_datetime) AS hour_of_day,
    date_part('dow', g.lpep_pickup_datetime) AS day_of_week,
    date_part('week', g.lpep_pickup_datetime) AS week_of_year,
    date_part('month', g.lpep_pickup_datetime) AS month_of_year
FROM {{ ref('stg_green_trips') }} g
JOIN {{ ref('stg_vehicle_emissions') }} e
    ON e.vehicle_type = 'green_taxi'