from load import load_parquet_files
from clean import cleanTables
from transform import transformations
from analysis import run_analysis

def main():
    load_parquet_files()
    cleanTables()
    transformations()
    run_analysis()

if __name__ == "__main__":
    main()



