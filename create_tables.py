# create_tables.py
from app.db_manager import connect

def init_db():
    sql = """
    CREATE TABLE IF NOT EXISTS pending_urls (
      id           INTEGER PRIMARY KEY AUTOINCREMENT,
      name         TEXT    NOT NULL,
      url          TEXT    NOT NULL,
      email        TEXT    NOT NULL,
      comments     TEXT,
      submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      status       TEXT    DEFAULT 'pending',
      status_msg   TEXT
    );
    CREATE TABLE IF NOT EXISTS restaurants (
      id            INTEGER PRIMARY KEY AUTOINCREMENT,
      name          TEXT    NOT NULL,
      url           TEXT    NOT NULL UNIQUE,
      latest_hh_raw TEXT,
      weekdays      TEXT,
      weekends      TEXT,
      last_scraped  DATETIME,
      created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn = connect()
    conn.executescript(sql)
    conn.close()
    print("✅ Database initialized.")

if __name__ == "__main__":
    init_db()
