from sqlalchemy import text
from database import engine, init_db

def run_sqlquery(query: str):
    """Run a raw SQL query on the same DB used by database.py."""
    # init_db() ensures the appointments table exists
    init_db()
    with engine.begin() as conn:
        result = conn.execute(text(query))
        return result.fetchall() if result.returns_rows else result.rowcount

query = """SELECT * FROM appointments"""
print(run_sqlquery(query))