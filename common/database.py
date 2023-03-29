from datetime import datetime

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import execute_values

from common.options import DatabaseOptions


def connect(db_options: DatabaseOptions):
    connection = None

    try:
        connection = psycopg2.connect(
            host=db_options.host,
            port=db_options.port,
            database=db_options.name,
            user=db_options.user,
            password=db_options.password,
        )
        print(f'[{datetime.now()}] INFO  – Connection to the database was established')
    except OperationalError as e:
        print(f'[{datetime.now()}] ERROR – An error occurred while trying to connect to the database: {e}')

    return connection


def create_mac_lookup_table_if_not_exists(connection):
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mac_lookup (
        prefix VARCHAR (17) NOT NULL PRIMARY KEY,
        vendor VARCHAR (256) NOT NULL
    )
    """)

    connection.commit()

    cursor.close()


def get_all_from_mac_lookup(connection):
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cursor.execute('SELECT * FROM mac_lookup')
    result = {}
    for row in cursor.fetchall():
        result[row[0]] = row[1]

    cursor.close()

    return result


def insert_mac_lookups(connection, records):
    cursor = connection.cursor()

    values = [[value for value in record.values()] for record in records]

    execute_values(cursor, """
    INSERT INTO mac_lookup (prefix, vendor)
    SELECT *
    FROM (VALUES %s) AS update_payload (prefix, vendor)
    """, values)

    connection.commit()

    cursor.close()


def update_mac_lookups(connection, records):
    cursor = connection.cursor()

    values = [[value for value in record.values()] for record in records]

    execute_values(cursor, """
    UPDATE mac_lookup
    SET vendor = update_payload.vendor
    FROM (VALUES %s) AS update_payload (prefix, vendor)
    WHERE mac_lookup.prefix = update_payload.prefix
    """, values)

    connection.commit()

    cursor.close()


def delete_mac_lookups(connection, records):
    cursor = connection.cursor()

    execute_values(cursor, """
    DELETE FROM mac_lookup
    INNER JOIN (VALUES %s) AS update_payload (prefix)
    WHERE mac_lookup.prefix = update_payload.prefix
    """, records)

    connection.commit()

    cursor.close()
