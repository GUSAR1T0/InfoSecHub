import sqlite3


def create_table_if_not_exists(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mac_lookup
        (
            prefix TEXT NOT NULL PRIMARY KEY,
            vendor_name TEXT NOT NULL
        );
    """)


def get(connection: sqlite3.Connection, mac_address: str) -> list[(str, str)]:
    cursor = connection.cursor()
    return cursor.execute("""
        SELECT prefix, vendor_name
        FROM mac_lookup
        WHERE ? LIKE prefix || '%';
    """, (mac_address,)).fetchall()


def add(connection: sqlite3.Connection, records: list[(str, str)]) -> None:
    cursor = connection.cursor()
    cursor.executemany("""
        INSERT INTO mac_lookup (prefix, vendor_name)
        VALUES (?, ?);
    """, records)


def truncate(connection: sqlite3.Connection) -> None:
    cursor = connection.cursor()
    cursor.execute("DELETE FROM mac_lookup;")
