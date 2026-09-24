
  
  create view "emissions"."main"."stg_yellow_trips__dbt_tmp" as (
    SELECT *
FROM yellow_trips
  );
