from sqlalchemy import create_engine


def load(df, table_name: str = "titles", db_url: str = "sqlite:///netflix.db"):
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"[load] Loaded {len(df):,} rows into table '{table_name}' ({db_url})")
    return engine
