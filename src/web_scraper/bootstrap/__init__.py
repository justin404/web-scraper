"""
    All bootstrapping logic routed through here
    Creates and populates the Context object and populates with necessary common objects
"""

from web_scraper.context import Context
from typing import NoReturn

def bootstrap(**kwargs) -> NoReturn:
    Context()

