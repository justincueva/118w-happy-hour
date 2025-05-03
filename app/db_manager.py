import sqlite3
import os


def connect():
    """
    Create a connection to the SQLite database. Assumes 'happy_hour.db' is one level up from this module.
    Returns a sqlite3.Connection with ROW factory to access columns by name.
    """
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'happy_hour.db'))
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn


def insert_pending(name: str, url: str, email: str, comments: str = '') -> None:
    """
    Insert a new user-submitted URL into the pending_urls table.
    """
    conn = connect()
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO pending_urls (name, url, email, comments)
        VALUES (?, ?, ?, ?)
        """,
        (name, url, email, comments)
    )
    conn.commit()
    conn.close()


def get_pending() -> list[dict]:
    """
    Retrieve all pending URL submissions.
    Returns a list of dicts with keys: id, name, url, email, comments, submitted_at.
    """
    conn = connect()
    c = conn.cursor()
    c.execute(
        """
        SELECT id, name, url, email, comments, submitted_at
        FROM pending_urls
        WHERE status = 'pending'
        ORDER BY submitted_at ASC
        """
    )
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_pending_by_id(pending_id: int) -> dict | None:
    """
    Retrieve a single pending submission by its ID.
    Returns a dict or None if not found.
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM pending_urls WHERE id = ?", (pending_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None


def set_pending_status(pending_id: int, status: str, status_msg: str | None = None) -> None:
    """
    Update the status (and optional message) of a pending submission.
    status should be one of: 'approved', 'rejected', 'error'.
    """
    conn = connect()
    c = conn.cursor()
    c.execute(
        """
        UPDATE pending_urls
        SET status = ?, status_msg = ?
        WHERE id = ?
        """,
        (status, status_msg, pending_id)
    )
    conn.commit()
    conn.close()


def insert_restaurant(name: str, url: str, latest_hh_raw: str = '', weekdays: str = '', weekends: str = '') -> None:
    """
    Insert a new approved restaurant into the restaurants table.
    Uses INSERT OR IGNORE to avoid duplicate URLs.
    """
    conn = connect()
    c = conn.cursor()
    c.execute(
        """
        INSERT OR IGNORE INTO restaurants
            (name, url, latest_hh_raw, weekdays, weekends, last_scraped)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (name, url, latest_hh_raw, weekdays, weekends)
    )
    conn.commit()
    conn.close()


def get_all_restaurants() -> list[dict]:
    """
    Retrieve all restaurants for display.
    Returns a list of dicts with restaurant data and timestamps.
    """
    conn = connect()
    c = conn.cursor()
    c.execute(
        """
        SELECT id, name, url, latest_hh_raw, weekdays, weekends, last_scraped, created_at
        FROM restaurants
        ORDER BY name ASC
        """
    )
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_restaurant_info(restaurant_id: int, latest_hh_raw: str, weekdays: str, weekends: str) -> None:
    """
    Update scrape results for an existing restaurant and refresh the last_scraped timestamp.
    """
    conn = connect()
    c = conn.cursor()
    c.execute(
        """
        UPDATE restaurants
        SET latest_hh_raw = ?, weekdays = ?, weekends = ?, last_scraped = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (latest_hh_raw, weekdays, weekends, restaurant_id)
    )
    conn.commit()
    conn.close()
