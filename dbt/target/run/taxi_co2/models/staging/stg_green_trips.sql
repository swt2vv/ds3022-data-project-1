
  
  create view "emissions"."main"."stg_green_trips__dbt_tmp" as (
    SELECT *
FROM green_trips
  );
