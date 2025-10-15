"""
    MySQL Manager
"""

from typing import NoReturn
from abc import ABC, abstractmethod


class DatabaseManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def connect(self) -> NoReturn:
        pass

    @abstractmethod
    def disconnect(self) -> NoReturn:
        pass

    def select(self, sql: str, ) -> NoReturn:
        pass

    def insert(self, sql: str) -> NoReturn:


class SQLAlchemyManager(DatabaseManager):
    def __init__(self):
        pass