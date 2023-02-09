import re
from asyncio import sleep
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from database import Database
from repositories import mac_lookups
from services.base_source_service import BaseSourceService


class MacLookupAppService(BaseSourceService):
    __host = 'https://maclookup.app'

    def __init__(self, database: Database) -> None:
        super().__init__(lambda response: response.json())
        self.__database = database

    def _get_link_to_download_file(self) -> str or None:
        response = requests.get(self.__host + '/downloads/json-database')
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            tag = soup.find('a', attrs={'href': re.compile(r'^/downloads/json-database/get-db.+$', flags=re.DOTALL)})
            if tag is not None:
                return self.__host + tag.attrs.get('href')

    def _save_records(self, file) -> None:
        connection = self.__database.connect()

        mac_lookups.truncate(connection)
        mac_lookups.add(connection, list(map(lambda x: (x['macPrefix'], x['vendorName']), file)))

        connection.commit()
        connection.close()

    async def background_task(self):
        while True:
            print(f'[{self.__class__.__name__}] {datetime.now()}: file importing...')
            self._import_file()
            print(f'[{self.__class__.__name__}] {datetime.now()}: the file was imported -> delay...')
            await sleep(60)
