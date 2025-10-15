"""
    NBA Models
"""

from dataclasses import dataclass, field
import datetime


@dataclass
class Game:
    date: datetime.datetime
    result: bool
    result_score: str
    result_link: str
    game_id: int
    is_ot: bool
    win_loss: str = None
    opponent: str = None
    box_score_file: str = None


@dataclass
class BoxScore:
    player_name: str
    player_number: str
    player_id: str
    player_link: str
    data_index: int
    is_dnp: bool
    is_starter: bool
    game_id: int = None
    team_name: str = None
    minutes: int = None
    _fg: str = None
    _three_pt: str = None
    _ft: str = None
    fgm: int = None
    fga: int = None
    three_point_made: int = None
    three_point_attempted: int = None
    ftm: int = None
    fta: int = None
    oreb: int = None
    dreb: int = None
    reb: int = None
    ast: int = None
    stl: int = None
    blk: int = None
    to: int = None
    pf: int = None
    plus_minus: str = None
    pts: int = None

    @property
    def fg(self):
        return self._fg

    @fg.setter
    def fg(self, value):
        self._fg = value
        self.fgm, self.fga = self.fg.split("-")

    @property
    def three_pt(self):
        return self._three_pt

    @three_pt.setter
    def three_pt(self, value):
        self._three_pt = value
        self.three_point_made, self.three_point_attempted = self.three_pt.split("-")

    @property
    def ft(self):
        return self._ft

    @ft.setter
    def ft(self, value):
        self._ft = value
        self.ftm, self.fta = self.ft.split("-")

