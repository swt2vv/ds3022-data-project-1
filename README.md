# DS3022 - Data Project 1 (Fall 2025)

This project loads NYC taxi trip data, cleans it, adds emissions and time-based features, and analyzes CO2 output for yellow and green taxis in 2024.

## Project structure

- `load.py` — loads the vehicle emissions reference table and the 2024 yellow/green taxi Parquet files into DuckDB. Can be scaled to 2015-2024 if range() in for loop on line 46 is edited. Comments provided in the file. 
- `clean.py` — removes duplicates and invalid trips, including zero-passenger, zero-distance, >100 mile, and >1 day records. This is because these are invalid data entries for the purposes of logging true trip events. 
- `transform.py` — adds trip emissions (`trip_co2_kgs`), average speed (`avg_mph`), and date features like hour/day/week/month. It is very useful to have this date data extracted in such a way so we can use the date data to explore the relationship between the month, hour, year, etc. and other variables.  
- `analysis.py` — runs the CO2 summary questions and saves a monthly yellow vs green emissions chart. Outputs a png file which is located in the main folder of the project of the graph generated. 
- `main.py` — runs the full pipeline in order: load -> clean -> transform -> analysis. This makes it very ease to run without determining what to run and what to not run. 
- `dbt/` — contains dbt staging and transformation models for the same workflow. This is another approach to the transformation question not using python, but rather SQL's DBT. 

## How it works
0. Running main.py will do the following:
1. Load raw data into DuckDB
2. Clean the trip tables
3. Add transformed columns for CO2 and time-based calculations
4. Run analysis and save the plot

## Run the project

```bash
pip install -r requirements.txt
python main.py
```

## DBT Approach run

```bash
dbt clean
dbt compile
dbt run
```


## Outputs

- `emissions.duckdb` with cleaned taxi trip tables
- calculated CO2 and time features in the tables
- a monthly emissions comparison chart (`co2_by_month_2024.png`)


