import sqlite3


class Database:
    __connection: sqlite3.Connection or None

    def __init__(self, connection_string: str) -> None:
        self.__connection_string = connection_string

    def connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.__connection_string)
