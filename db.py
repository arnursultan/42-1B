import sqlite3

DB_NAME = "/tmp/database.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)


def add_server(name, server_type, status):
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO servers (name, type, status)
                VALUES (?, ?, ?)
                """,
                (name, server_type, status)
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False


def get_all_servers():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM servers ORDER BY id"
        ).fetchall()


def get_server_by_name(name):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM servers WHERE name = ?",
            (name,)
        ).fetchone()


def update_server_status(name, status):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE servers
            SET status = ?
            WHERE name = ?
            """,
            (status, name)
        )
        conn.commit()
        return cursor.rowcount > 0


def delete_server(name):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM servers WHERE name = ?",
            (name,)
        )
        conn.commit()
        return cursor.rowcount > 0