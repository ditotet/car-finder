import sqlite3

from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS seen_lots (
            lot TEXT PRIMARY KEY,
            first_seen_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    return conn


def filter_new_lots(conn, lots):
    rows = conn.execute("SELECT lot FROM seen_lots").fetchall()
    seen = {row[0] for row in rows}
    return [lot for lot in lots if lot["lot"] not in seen]


def mark_seen(conn, lots):
    conn.executemany(
        "INSERT OR IGNORE INTO seen_lots (lot) VALUES (?)",
        [(lot["lot"],) for lot in lots],
    )
    conn.commit()
