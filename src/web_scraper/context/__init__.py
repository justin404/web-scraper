"""
    Application Context
"""
from web_scraper.utils.decorators import Singleton
from typing import Iterator, Any, NoReturn, Optional


@Singleton
class Context:
    def __init__(self):
        self.__cache = {}

    def __contains__(self, item) -> bool:
        return item in self.__cache

    def __iter__(self) -> Iterator[tuple]:
        for key, value in self.__cache.items():
            yield key, value

    def __len__(self) -> int:
        return len(self.__cache)

    def __getitem__(self, item) -> Any:
        return self.__cache[item]

    def __setitem__(self, key, value) -> NoReturn:
        self.__cache[key] = value

    def __delitem__(self, key) -> NoReturn:
        del self.__cache[key]

    def __getattr__(self, item) -> Any:
        if item in self.__cache:
            return self.__cache.get(item)
        return None

    def __setattr__(self, key, value) -> NoReturn:
        """
        This is important for the construction of the context initially.
        Without this, we'll go into infinite recursion, since we'll try to cache the actual cache dictionary within itself.
        The format of the key is whatever the name of the context class + __cache (private member)
        """
        if "_Context__cache" in key:
            object.__setattr__(self, key, value)
        self.__cache[key] = value

    def empty(self) -> NoReturn:
        self.__cache = {}

    def get(self, key, default=None) -> Optional[Any]:
        if key in self.__cache:
            return self.__cache[key]
        return default

    def put(self, key, value) -> Optional[Any]:
        old_val = None
        if key in self.__cache:
            old_val = self.__cache[key]
        self.__cache[key] = value
        return old_val