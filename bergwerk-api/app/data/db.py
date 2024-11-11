"""
This module provides functionality to interact with the database for tracking text data.

Functions:
    track_text(uid, role, text, buttons, ts):
        Inserts a new record into the tracker database with the provided user ID, role, text, buttons, and timestamp.

Classes:
    DatabaseSession:
        Manages database connections and cursors.

"""

import mariadb
from .connections import DatabaseSession

dbs = DatabaseSession()

def track_text(uid, role, text, buttons, ts):
    """
    Inserts a new record into the tracker database with the provided user ID, role, text, buttons, and timestamp.
    """

    cur, conn = dbs.get_cursor_conn()

    row = (uid, ts, role, text, buttons)

    insert_query = """
    INSERT INTO tracker_db.tracker (id, ts, role, text, buttons)
    VALUES (?, ?, ?, ?, ?);
    """

    try:
        cur.execute(insert_query, row)
        conn.commit()

    except mariadb.Error as err:
        print(f"Error inserting data into the table: {err}")
        conn.rollback()