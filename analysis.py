import duckdb
import logging
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
    filename='load.log'
)
logger = logging.getLogger(__name__)

DB_PATH = 'emissions.duckdb'
TABLES = {'YELLOW': {'table': 'yellow_trips', 'label': 't'},
        'GREEN': {'table': 'green_trips', 'label': 'l'}}

"""
Makes queries to the DuckDB database and generates a report of the results. Easier than repeatedly running queries in the DuckDB shell.
"""

def report(message):
    print(message)
    logger.info(message)


"""
This function organizes and selects the trips with the largest CO2 emissions as it is ordered by trip_co2_kgs in descending order and limited to 1. It also reports the trip distance and pickup time.
"""


# question 1: largest single-trip CO2 emission
def largest_trip(con, key, table, label):
    row = con.execute(f"""
        SELECT trip_co2_kgs, trip_distance, {label}pep_pickup_datetime
        FROM {table}
        ORDER BY trip_co2_kgs DESC LIMIT 1
        """).fetchone()
    report(f'[{key}] Largest single-trip CO2 of 2024 '
           f'{row[0]:.2f} kg ({row[1]:.2f} mi), picked up at {row[2]}')


"""
This function organizes the trips with the heaviest to lightest CO2 emissions by a specified column. It groups the data by the specified 
column and averages the trip_co2_kgs for each group. It then reports the group with the highest and lowest average CO2 emissions.
"""

# question 2-5: heaviest and lightest by column
def heaviest_lightest(con, key, table, column, description, names = None):
    rows = con.execute(f"""
        SELECT {column}, AVG(trip_co2_kgs) AS avg_co2
        FROM {table}
        GROUP BY {column}
        ORDER BY avg_co2 DESC
        """).fetchall()

    pretty = lambda v: names[int(v)] if names else v
    high, low = rows[0], rows[-1]
    report(f'[{key}] Most carbon-heavy {description}:'
           f' {pretty(high[0])} ({high[1]:.2f} kg avg/trip)')
    report(f'[{key}] Most carbon-light {description}:'
           f' {pretty(low[0])} ({low[1]:.2f} kg avg/trip)')

"""
This function generates graphs comparing the total CO2 emissions by month for both yellow and green taxis. It retrieves the tables' information for the total CO2 emissions for each month, 
and then plots the results on a graph with two y-axes, one for each taxi type. The resulting graph is saved as a PNG file.
"""


# question 6: monthly plot
def monthly_plot(con, filename = 'co2_by_month_2024.png'):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax2 = ax.twinx()
    for key, info in TABLES.items():
        table = info['table']
        rows = con.execute(f"""
            SELECT month_of_year, SUM(trip_co2_kgs) AS total_co2
            FROM {table}
            GROUP BY month_of_year
            ORDER BY 1
        """).fetchall()
        months = [r[0] for r in rows]
        totals = [r[1] / 1000.0 for r in rows]
        if key == 'YELLOW':
            ax.plot(months, totals, marker='o', color='gold', label='Yellow taxis')
        else:
            ax2.plot(months, totals, marker='o', color='green', label='Green taxis')

    ax.set_title('Total CO2 Emissions by Month (2024)')
    ax.set_xlabel('Month'); ax.set_ylabel('Total CO2 (tonnes)')
    ax.legend(loc='upper left'); ax2.legend(loc='upper right'); fig.savefig(filename, dpi = 150)
    report(f'Plot written to {filename}')



"""
This final function calls all the above functions to clean both tables. 
"""

def run_analysis():
    con = None

    try:
        con = duckdb.connect(database=DB_PATH, read_only=True)
        logger.info("Connected to DuckDB instance")

        for key, info in TABLES.items():
            table = info['table']
            label = info['label']
            largest_trip(con, key, table, label)
            heaviest_lightest(con, key, table, 'hour_of_day', 'hour of the day')
            heaviest_lightest(con, key, table, 'day_of_week', 'day of the week')
            heaviest_lightest(con, key, table, 'week_of_year', 'week of the year')
            heaviest_lightest(con, key, table, 'month_of_year', 'month of the year')
        monthly_plot(con)
        con.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    run_analysis()

















