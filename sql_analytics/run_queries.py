import sqlite3
import re
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).parent.parent / "netflix.db"
SQL_PATH = Path(__file__).parent / "queries.sql"


def load_queries(path: Path) -> list[tuple[str, str]]:

    text = path.read_text()
    blocks = re.split(r"-- Query \d+: ", text)[1:]  
    queries = []
    for block in blocks:
        title_line, _, rest = block.partition("\n")

        sql_lines = [
            line for line in rest.splitlines()
            if not line.strip().startswith("--") and line.strip() != ""
        ]
        sql = "\n".join(sql_lines).strip().rstrip(";")
        queries.append((title_line.strip(), sql))
    return queries


def main():
    conn = sqlite3.connect(DB_PATH)
    queries = load_queries(SQL_PATH)

    for title, sql in queries:
        print("=" * 70)
        print(title)
        print("=" * 70)
        df = pd.read_sql(sql, conn)
        
        print(df.to_string(index=False, max_rows=15))
        print()

    conn.close()


if __name__ == "__main__":
    main()
