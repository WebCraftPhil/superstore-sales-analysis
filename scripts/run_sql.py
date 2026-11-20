"""Load the Superstore CSV into SQLite and run sql/key_metrics.sql.

Uses only the Python standard library, so no database server or extra
package is needed. Each query's result prints as a small table.

    python scripts/run_sql.py
    python scripts/run_sql.py --db superstore.db   # also save a .db file to explore
"""
import argparse
import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "raw" / "superstore.csv"
SQL_PATH = ROOT / "sql" / "key_metrics.sql"


def load_csv(conn: sqlite3.Connection) -> int:
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        cols = ", ".join(f'"{c}"' for c in header)
        marks = ", ".join("?" for _ in header)
        conn.execute("DROP TABLE IF EXISTS superstore")
        conn.execute(f"CREATE TABLE superstore ({cols})")
        rows = list(reader)
        conn.executemany(f"INSERT INTO superstore VALUES ({marks})", rows)
    conn.commit()
    return len(rows)


def split_statements(sql: str):
    """Yield (leading comment, statement) pairs, splitting on complete statements."""
    buf, comment = "", []
    for line in sql.splitlines(keepends=True):
        stripped = line.strip()
        if not buf.strip() and stripped.startswith("--"):
            comment.append(stripped.lstrip("- ").strip())
            continue
        buf += line
        if sqlite3.complete_statement(buf):
            yield (comment[-1] if comment else ""), buf.strip()
            buf, comment = "", []


def print_table(title, cursor):
    headers = [d[0] for d in cursor.description]
    rows = [["" if v is None else str(v) for v in r] for r in cursor.fetchall()]
    widths = [max(len(h), *(len(r[i]) for r in rows)) if rows else len(h)
              for i, h in enumerate(headers)]
    print(f"\n{title}")
    print("  ".join(h.ljust(w) for h, w in zip(headers, widths)))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print("  ".join(v.ljust(w) for v, w in zip(r, widths)))


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--db", default=":memory:",
                        help="SQLite file to write (default: in memory only)")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    n = load_csv(conn)
    print(f"Loaded {n:,} rows from {CSV_PATH.relative_to(ROOT)}")

    for title, stmt in split_statements(SQL_PATH.read_text(encoding="utf-8")):
        cur = conn.execute(stmt)
        if cur.description:  # SELECT statements return rows
            print_table(title, cur)
    conn.close()


if __name__ == "__main__":
    main()
