import pandas as pd


def validate(df: pd.DataFrame) -> list:
    issues = []

    if df["title"].isnull().any() or df["show_id"].isnull().any():
        issues.append("Found rows with a missing title or show_id")

    dupe_ids = df["show_id"].duplicated().sum()
    if dupe_ids > 0:
        issues.append(f"Found {dupe_ids} duplicate show_id values")

    valid_types = {"Movie", "TV Show"}
    bad_types = set(df["type"].unique()) - valid_types
    if bad_types:
        issues.append(f"Found unexpected values in 'type': {bad_types}")

    current_year = pd.Timestamp.now().year
    bad_years = df[(df["release_year"] < 1900) | (df["release_year"] > current_year)]
    if len(bad_years) > 0:
        issues.append(f"Found {len(bad_years)} rows with an out-of-range release_year")

    null_duration = df["duration_value"].isnull().sum()
    if null_duration > 0:
        issues.append(f"Found {null_duration} rows where duration could not be parsed")

    if issues:
        print("[validate] Warnings found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("[validate] No data quality issues found")

    return issues
