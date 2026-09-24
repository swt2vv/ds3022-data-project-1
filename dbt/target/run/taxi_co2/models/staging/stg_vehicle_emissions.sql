
  
  create view "emissions"."main"."stg_vehicle_emissions__dbt_tmp" as (
    SELECT *
FROM vehicle_emissions
  );
