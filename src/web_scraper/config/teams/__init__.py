
from dataclasses import dataclass

@dataclass
class Team:
    name: str
    espn_abbreviation: str

    @property
    def clean_name(self):
        return self.name.replace(" ", "_")