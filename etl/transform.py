import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    before = len(df)
    df = df.drop_duplicates(subset="show_id")
    print(f"[transform] Dropped {before - len(df)} duplicate rows")

    df["type"] = df["type"].str.strip()
    df["title"] = df["title"].str.strip()

 
    df["director"] = df["director"].fillna("Unknown")
    df["cast"] = df["cast"].fillna("Unknown")
    df["country"] = df["country"].fillna("Unknown")
    df["rating"] = df["rating"].fillna("Not Rated")

    df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")

    duration_split = df["duration"].str.extract(r"(?P<duration_value>\d+)\s*(?P<duration_unit>\w+)")
    df["duration_value"] = pd.to_numeric(duration_split["duration_value"])
    df["duration_unit"] = duration_split["duration_unit"].replace(
        {"Season": "Season(s)", "Seasons": "Season(s)", "min": "Minutes"}
    )

    df["primary_country"] = df["country"].apply(lambda x: x.split(",")[0].strip())
    df["primary_genre"] = df["listed_in"].apply(lambda x: x.split(",")[0].strip())

    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").astype("Int64")

    print(f"[transform] Produced {df.shape[0]:,} rows, {df.shape[1]} columns")
    return df
