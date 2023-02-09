import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from threading import Thread

import requests


def _download_file(link: str, transformer):
    response = requests.get(link)
    if response.ok:
        return transformer(response)

    raise Exception('Failed to download the file')


class BaseSourceService(ABC):

    def __init__(self, transformer) -> None:
        self.__transformer = transformer

    @abstractmethod
    def _get_link_to_download_file(self) -> str or None:
        pass

    @abstractmethod
    def _save_records(self, file) -> None:
        pass

    def _import_file(self) -> None:
        link = self._get_link_to_download_file()
        if link is not None:
            file = _download_file(link, self.__transformer)
            self._save_records(file)
        else:
            raise Exception('Failed to get a link to the file')

    @abstractmethod
    def background_task(self):
        pass

    def launch(self) -> None:
        print(f'[{self.__class__.__name__}] {datetime.now()}: the process has been launched')
        daemon = Thread(name=self.__class__.__name__, daemon=True, target=lambda: asyncio.run(self.background_task()))
        daemon.start()
