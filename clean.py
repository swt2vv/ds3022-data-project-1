import duckdb
import os
import logging

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='clean.log'
)
logger = logging.getLogger(__name__)


""" 
This function I am dropping duplicates by selecting distinct rows from the tables. Then they are grouped by all the columns and when there is a count greater than one then it is tallyed. 
For dropping I have it so that it creates a new table with the distinct rows, drops the old table, and renames the new table to the old table name. 
I also print out and log the number of duplicates before and after the delete.
"""
# #dropping duplicates
def removeDups(con, table):
    before = con.execute(f"""
        SELECT COUNT(*)
        FROM (
            SELECT *
            FROM {table}
            GROUP BY *
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]
    print(f'Before delete: {before}')



    con.execute(f"""
        CREATE TABLE {table}_clean AS
        SELECT DISTINCT * FROM {table};
        DROP TABLE {table};
        ALTER TABLE {table}_clean RENAME TO {table};
        """)



    after = con.execute(f"""
        SELECT COUNT(*)
        FROM (
            SELECT *
            FROM {table}
            GROUP BY *
            HAVING COUNT(*) > 1
        )
    """).fetchone()[0]
    print(f'After delete (verify): {after}')


"""
This function removes rows with zero passengers from the specified table. This is done by deleting the rows with zero passengers and then counting the remaining rows.
"""

# all trips over 0 passengers
def removeZeroPassengers(con, table):

    before = con.execute(f"""
    SELECT COUNT(*)
    FROM {table}
    WHERE passenger_count = 0
    """).fetchone()[0]
    print(f'Before delete: {before}')

    con.execute(f'DELETE FROM {table} WHERE passenger_count = 0')

    after = con.execute(f"""
    SELECT COUNT(*)
    FROM {table}
    WHERE passenger_count = 0
    """).fetchone()[0]
    print(f'After delete (verify): {after}')


"""
This function removes rows with zero miles in a trip from the specified table. This is done by deleting the rows with zero miles and then counting the remaining rows.
"""

#all trips over 0 trip miles
def removeZeroTripMiles(con, table):
    before = con.execute(f"""
    SELECT COUNT(*)
    FROM {table}
    WHERE trip_distance = 0
    """).fetchone()[0]
    print(f'Before delete: {before}')

    con.execute(f'DELETE FROM {table} WHERE trip_distance = 0')

    after = con.execute(f"""
    SELECT COUNT(*)
    FROM {table}
    WHERE trip_distance = 0
    """).fetchone()[0]
    print(f'After delete (verify): {after}')


"""
This function removes rows with over 100 trip miles from the specified table. This is done by deleting the rows with over 100 miles and then counting the remaining rows.
"""


#all trips over under 100 trip miles
def remove100TripMiles(con, table):
    before = con.execute(f"""
    SELECT COUNT(*) 
    FROM {table}
    WHERE trip_distance > 100
    """).fetchone()[0]
    print(f'Before delete: {before}')

    con.execute(f'DELETE FROM {table} WHERE trip_distance > 100')

    after = con.execute(f"""
    SELECT COUNT(*) 
    FROM {table}
    WHERE trip_distance > 100
    """).fetchone()[0]
    print(f'After delete (verify): {after}')


"""
This function removes rows with trips over 1 day from the specified table. This is done by deleting the rows with trips over 1 day and then counting the remaining rows.
"""


#all trips under 1 day
def removeOverOneDay(con, table, letter):
    before = con.execute(f"""
    SELECT COUNT(*) 
    FROM {table}
    WHERE date_diff('second', {letter}pep_pickup_datetime, {letter}pep_dropoff_datetime) > 86400
    """).fetchone()[0]
    print(f'Before delete: {before}')

    con.execute(f"""DELETE FROM {table} WHERE date_diff('second', {letter}pep_pickup_datetime, {letter}pep_dropoff_datetime) > 86400""")

    after = con.execute(f"""
    SELECT COUNT(*) 
    FROM {table}
    WHERE date_diff('second', {letter}pep_pickup_datetime, {letter}pep_dropoff_datetime) > 86400
    """).fetchone()[0]
    print(f'After delete (verify): {after}')




"""
This final function is to call all the above functions to clean both tables. I needed to have a for look with 't' and 'l' for the yellow and green trips respectively because the column names are different for the two tables. 
I also print out and log the number of rows before and after each cleaning step.
"""

def cleanTables():
    con = None
    try:

        con = duckdb.connect(database='emissions.duckdb', read_only=False)
        logger.info("Connected to DuckDB instance")

        # fix code
        values = {'yellow_trips': 't', 'green_trips': 'l'}
        for i in ['yellow_trips', 'green_trips']:
            n = con.execute(f"""SELECT COUNT(*) FROM {i}""").fetchone()[0]
            logger.info(f'{i}: {n} rows loaded')
            removeDups(con, i)
            removeZeroPassengers(con, i)
            removeZeroTripMiles(con, i)
            remove100TripMiles(con, i)
            removeOverOneDay(con, i, values[i]) 

    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    cleanTables()

