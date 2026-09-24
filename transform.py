import duckdb
import os
import logging

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='load.log'
)
logger = logging.getLogger(__name__)


"""
This function calculateCO2 calculates the co2 emissions for each trip and adds a new column called trip_co2_kgs.
"""

def calculateCO2(con, table, label):

    con.execute(f"""
        ALTER TABLE {table}
        ADD COLUMN IF NOT EXISTS trip_co2_kgs DOUBLE;
        """)

    con.execute(f""" 
        UPDATE {table}
        SET trip_co2_kgs = trip_distance * (vehicle_emissions.co2_grams_per_mile / 1000)
        FROM vehicle_emissions 
        WHERE vehicle_emissions.vehicle_type = '{label}';
        """)



"""
This function transformTables calculates average speed in mph and also extracts the date data from the pickup datetime and adds new columns for hour_of_day, day_of_week, week_of_year, and month_of_year.
"""


def transformTables(con, table, label):



    #calculating average speed in mph
    con.execute(f"""
        ALTER TABLE {table}
        ADD COLUMN IF NOT EXISTS avg_mph DOUBLE;
        """)

    con.execute(f"""
        UPDATE {table}
        SET avg_mph = trip_distance / (date_diff('second', {label}pep_pickup_datetime, {label}pep_dropoff_datetime) / 3600);
        """)


    #extracting date information
    con.execute(f"""
        ALTER TABLE {table}
        ADD COLUMN IF NOT EXISTS hour_of_day INTEGER;
        """)    
    
    con.execute(f""" 
    UPDATE {table}
    SET hour_of_day = date_part('hour', {label}pep_pickup_datetime);
    """)

    con.execute(f"""
        ALTER TABLE {table}
        ADD COLUMN IF NOT EXISTS day_of_week INTEGER;
        """)

    con.execute(f""" 
    UPDATE {table}
    SET day_of_week = date_part('dow', {label}pep_pickup_datetime);
    """)

    con.execute(f"""
        ALTER TABLE {table}
        ADD COLUMN IF NOT EXISTS week_of_year INTEGER;
        """)

    con.execute(f""" 
    UPDATE {table}
    SET week_of_year = date_part('week', {label}pep_pickup_datetime);
    """)


    con.execute(f"""
        ALTER TABLE {table}
        ADD COLUMN IF NOT EXISTS month_of_year INTEGER;
        """)

    con.execute(f""" 
    UPDATE {table}
    SET month_of_year = date_part('month', {label}pep_pickup_datetime);
    """)


""" 
THis function calls all the functions to extract the date data and calculate the co2 emissions for both yellow and green taxi trips.
"""

def transformations():
    con = None

    try:
        con = duckdb.connect(database='emissions.duckdb', read_only=False)
        logger.info("Connected to DuckDB instance")

        calculateCO2(con, 'yellow_trips', 'yellow_taxi')
        calculateCO2(con, 'green_trips', 'green_taxi')
        transformTables(con, 'yellow_trips', 't')
        transformTables(con, 'green_trips', 'l')


    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")


#calling transformations function to execute the transformations on the yellow and green taxi trips data.
if __name__ == "__main__":
    transformations()






