import sqlite3
from pathlib import Path

for db in Path(__file__).parent.glob("*.db"):
    print(f"\n=== {db.name} ===")
    con = sqlite3.connect(db)
    tables = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")]
    if not tables:
        print("No tables (empty database)")
    for t in tables:
        rows = con.execute(f'SELECT * "{t}"').fetchall() if False else con.execute(f'SELECT * FROM "{t}"').fetchall()
        print(f"Table '{t}': {len(rows)} row(s)")
        for r in rows:
            print(r)
    con.close()