"""
    NBA Models
"""

from dataclasses import dataclass
import datetime


@dataclass
class Game:
    date: datetime.datetime
    result: bool
    result_score: str
    result_link: str
    is_ot: bool
    win_loss: str = None
    opponent: str = None