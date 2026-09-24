
  
  create view "emissions"."main"."green_transform__dbt_tmp" as (
    SELECT g.*,
    g.trip_distance * (e.co2_grams_per_mile / 1000) AS trip_co2_kgs,
    g.trip_distance / (date_diff('second', g.lpep_pickup_datetime, g.lpep_dropoff_datetime) / 3600) AS avg_mph,
    date_part('hour', g.lpep_pickup_datetime) AS hour_of_day,
    date_part('dow', g.lpep_pickup_datetime) AS day_of_week,
    date_part('week', g.lpep_pickup_datetime) AS week_of_year,
    date_part('month', g.lpep_pickup_datetime) AS month_of_year
FROM "emissions"."main"."stg_green_trips" g
JOIN "emissions"."main"."stg_vehicle_emissions" e
    ON e.vehicle_type = 'green_taxi'
  );
