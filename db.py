import sqlite3

DB_NAME = "tg_bot.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                type TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'жив'
            )
        """)


def add_server(
    name: str,
    server_type: str,
    status: str = "жив"
) -> bool:
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO servers (name, type, status)
                VALUES (?, ?, ?)
                """,
                (name, server_type, status)
            )
        return True
    except sqlite3.IntegrityError:
        return False


def get_all_servers():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, name, type, status
            FROM servers
            ORDER BY id
            """
        ).fetchall()

    return rows


def get_server_by_name(name: str):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, name, type, status
            FROM servers
            WHERE name = ?
            """,
            (name,)
        ).fetchone()

    return row


def update_server_status(
    name: str,
    new_status: str
) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            UPDATE servers
            SET status = ?
            WHERE name = ?
            """,
            (new_status, name)
        )

    return cursor.rowcount > 0


def delete_server(name: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            DELETE FROM servers
            WHERE name = ?
            """,
            (name,)
        )

    return cursor.rowcount > 0