import pandas as pd


EXPECTED_COLUMNS = [
    "show_id", "type", "title", "director", "cast", "country",
    "date_added", "release_year", "rating", "duration",
    "listed_in", "description",
]


def extract(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Source file is missing expected columns: {missing_cols}")

    print(f"[extract] Read {len(df):,} rows and {len(df.columns)} columns from {path}")
    return df
