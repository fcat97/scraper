import sqlite3
from abc import ABC, abstractmethod
from sqlite3 import Cursor


class Database(ABC):

    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def insert_record(self, rec: dict):
        pass

    @abstractmethod
    def save_status(self, url: str, status: str, msg: str|None):
        pass

    @abstractmethod
    def close(self):
        pass