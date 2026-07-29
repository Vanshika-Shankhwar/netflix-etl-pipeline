# Netflix Titles ETL Pipeline

A small end-to-end ETL (Extract → Transform → Validate → Load) pipeline
built in Python that cleans the public Netflix titles dataset and loads
it into a SQL database, ready for analysis.

## Why this project

Raw datasets are rarely clean. This project takes ~7,800 real Netflix
title records — with missing directors/cast/country, free-text dates,
and inconsistent duration formats — and turns them into a clean,
query-ready SQL table, with data quality checks along the way.

## Pipeline steps

1. **Extract** (`etl/extract.py`) — reads the raw CSV and checks that
   all expected columns are present before continuing.
2. **Transform** (`etl/transform.py`) —
   - Fills missing `director`/`cast`/`country`/`rating` values explicitly
     instead of silently leaving nulls.
   - Parses `date_added` from free text (`"August 14, 2020"`) into a
     real datetime.
   - Splits the `duration` column, which mixes two units in one field
     (`"90 min"` for movies vs `"4 Seasons"` for TV shows), into a
     numeric `duration_value` + `duration_unit`.
   - Derives `primary_country` and `primary_genre` from the
     comma-separated `country` and `listed_in` fields.
3. **Validate** (`etl/validate.py`) — checks for duplicate IDs, missing
   titles, out-of-range release years, unparseable durations, and
   unexpected category values. Logs warnings rather than crashing, the
   way a real pipeline would flag issues without failing silently.
4. **Load** (`etl/load.py`) — writes the cleaned data into a SQLite
   database (swap the `db_url` for PostgreSQL/MySQL with no code
   changes elsewhere).

## How to run it

```bash
pip install -r requirements.txt
python run_pipeline.py
```

This single command runs the full pipeline and produces `netflix.db`,
a SQLite database with a `titles` table ready to query.

## Example queries against the output

```sql
-- Movies vs TV Shows
SELECT type, COUNT(*) FROM titles GROUP BY type;

-- Top genres
SELECT primary_genre, COUNT(*) c FROM titles
GROUP BY primary_genre ORDER BY c DESC LIMIT 5;

-- Top content-producing countries
SELECT primary_country, COUNT(*) c FROM titles
WHERE primary_country != 'Unknown'
GROUP BY primary_country ORDER BY c DESC LIMIT 5;
```

## Project structure

```
netflix_etl/
├── data/
│   └── netflix_titles.csv
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── validate.py
│   └── load.py
├── run_pipeline.py
├── requirements.txt
└── README.md
```

## Possible extensions

- Swap SQLite for PostgreSQL to demonstrate a production-style setup.
- Orchestrate with Apache Airflow (extract/transform/validate/load as
  separate DAG tasks).
- Add a scheduled run (cron) to simulate a recurring data refresh.

## Dataset source

Netflix titles dataset, originally from Kaggle, mirrored via the
[TidyTuesday project](https://github.com/rfordatascience/tidytuesday/tree/main/data/2021/2021-04-20).
