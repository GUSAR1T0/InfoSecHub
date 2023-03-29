import asyncio
import os
from asyncio import sleep
from datetime import datetime

from common.database import connect, \
    create_mac_lookup_table_if_not_exists, \
    get_all_from_mac_lookup, \
    insert_mac_lookups, \
    update_mac_lookups, \
    delete_mac_lookups
from common.options import DatabaseOptions
from service.mac_lookup import download_file

options = DatabaseOptions(
    host=os.environ.get('DATABASE_HOST', '127.0.0.1'),
    port=os.environ.get('DATABASE_PORT', '5432'),
    name=os.environ.get('DATABASE_NAME', 'database'),
    user=os.environ.get('DATABASE_USER', 'postgres'),
    password=os.environ.get('DATABASE_PASSWORD', 'qwerty')
)
delay = 60 * 60 * 24  # 1 day of delay


def try_init() -> bool:
    connection = connect(options)
    if not connection:
        return False

    try:
        print(f'[{datetime.now()}] INFO  – Started to initialize the database')
        create_mac_lookup_table_if_not_exists(connection)
        print(f'[{datetime.now()}] INFO  – Initialization was completed')
        return True
    except Exception as e:
        print(f'[{datetime.now()}] ERROR – An error occurred while trying to initialize the database: {e}')
        return False
    finally:
        connection.close()


async def launch():
    while True:
        print(f'[{datetime.now()}] INFO  – Started to download the file')
        content = download_file()

        print(f'[{datetime.now()}] INFO  – Started to query records from DB')
        connection = connect(options)
        records = get_all_from_mac_lookup(connection)

        print(f'[{datetime.now()}] INFO  – Started to search changes')
        keys = set(map(lambda item_key: item_key, content)) \
            .union(map(lambda record_key: record_key, records))

        insert = []
        update = []
        delete = []

        for key in keys:
            if key in content and key not in records:
                insert.append({'prefix': key, 'vendor': content[key]})
            elif key not in content and key in records:
                delete.append(key)
            elif content[key] != records[key]:
                update.append({'prefix': key, 'vendor': content[key]})

        if len(insert) > 0:
            print(f'[{datetime.now()}] INFO  – Started to insert records to DB')
            insert_mac_lookups(connection, insert)

        if len(update) > 0:
            print(f'[{datetime.now()}] INFO  – Started to update records to DB')
            update_mac_lookups(connection, update)

        if len(delete) > 0:
            print(f'[{datetime.now()}] INFO  – Started to delete records to DB')
            delete_mac_lookups(connection, delete)

        connection.close()

        print(f'[{datetime.now()}] INFO  – The process was completed, delay is started ({delay} secs)')
        await sleep(delay)


def main():
    if try_init():
        asyncio.run(launch())


if __name__ == '__main__':
    main()
