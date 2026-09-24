import duckdb
import os
import logging

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='load.log'
)
logger = logging.getLogger(__name__)


"""
This function loads the files from the NYC taxi site. I attempted to do years from 2015-2024, however, my computer ran very very slow, so I limited it to 2024 only. 
This can easily be changed to 2015-2024 by changing the range() in the for loop line 46. Also I print out and log very basic statistics of the number of rows loaded for each table.
"""
def load_parquet_files():

    con = None

    try:
        # Connect to local DuckDB instance
        con = duckdb.connect(database='emissions.duckdb', read_only=False)
        logger.info("Connected to DuckDB instance")


        #creating three tables; vehicle_emissions (8 rows), yellow_trips (2024, full year), green_trips (2024, full year)
        con.execute("""DROP TABLE IF EXISTS vehicle_emissions;
            CREATE TABLE vehicle_emissions AS 
            SELECT * FROM read_csv_auto('./data/vehicle_emissions.csv');
            """)

        url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet'
        con.execute("DROP TABLE IF EXISTS yellow_trips;")
        con.execute(f"CREATE TABLE yellow_trips AS SELECT * FROM read_parquet('{url}') LIMIT 0;")

        url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2024-01.parquet'
        con.execute("DROP TABLE IF EXISTS green_trips;")
        con.execute(f"CREATE TABLE green_trips AS SELECT * FROM read_parquet('{url}') LIMIT 0;")

        #Loading programmatically the parquet files looping over months 2-12 for both yellow and green trips

        for year in range(2024, 2025): #computer couldn't handle 2015-2024 data, so I limited to 2024 only for now.  Can be changed to range(2015, 2025) if needed.
            for month in range(1, 13):
                url = (f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:4d}-{month:02d}.parquet')
                con.execute(f'INSERT INTO yellow_trips SELECT * FROM read_parquet("{url}");')

            for month in range(1, 13):
                url = (f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year:4d}-{month:02d}.parquet')
                con.execute(f'INSERT INTO green_trips SELECT * FROM read_parquet("{url}");')


        #Basic row counting statistics for each table
        n = con.execute("SELECT COUNT(*) FROM vehicle_emissions").fetchone()[0]
        logger.info(f'vehicle_emissions: {n} rows loaded')
        print(f'vehicle_emissions: {n} rows loaded')

        n = con.execute("SELECT COUNT(*) FROM yellow_trips").fetchone()[0]
        logger.info(f'yellow_trips: {n} rows loaded')
        print(f'yellow_trips: {n} rows loaded')

        n = con.execute("SELECT COUNT(*) FROM green_trips").fetchone()[0]
        logger.info(f'green_trips: {n} rows loaded')
        print(f'green_trips: {n} rows loaded')


        logger.info("Dropped table if exists")

    #Exceptions logged when relevant
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")



if __name__ == "__main__":
    load_parquet_files()
