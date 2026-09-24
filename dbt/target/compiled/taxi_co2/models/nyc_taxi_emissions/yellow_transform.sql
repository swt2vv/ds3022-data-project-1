SELECT 
    y.*,
    y.trip_distance * (e.co2_grams_per_mile / 1000) AS trip_co2_kgs,
    y.trip_distance / (date_diff('second', y.tpep_pickup_datetime, y.tpep_dropoff_datetime) / 3600) AS avg_mph,
    date_part('hour', y.tpep_pickup_datetime) AS hour_of_day,
    date_part('dow', y.tpep_pickup_datetime) AS day_of_week,
    date_part('week', y.tpep_pickup_datetime) AS week_of_year,
    date_part('month', y.tpep_pickup_datetime) AS month_of_year
FROM "emissions"."main"."stg_yellow_trips" y
JOIN "emissions"."main"."stg_vehicle_emissions" e
    ON e.vehicle_type = 'yellow_taxi'