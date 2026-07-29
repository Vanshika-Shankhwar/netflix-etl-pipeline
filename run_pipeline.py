import time
from etl.extract import extract
from etl.transform import transform
from etl.validate import validate
from etl.load import load


def main():
    start = time.time()
    print("=== Netflix Titles ETL Pipeline ===")

    df_raw = extract("data/netflix_titles.csv")
    df_clean = transform(df_raw)
    issues = validate(df_clean)
    load(df_clean, table_name="titles", db_url="sqlite:///netflix.db")

    elapsed = time.time() - start
    print(f"=== Pipeline completed in {elapsed:.2f}s "
          f"({'with warnings' if issues else 'cleanly'}) ===")


if __name__ == "__main__":
    main()
