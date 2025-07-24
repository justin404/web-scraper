"""
    ESPN Data Loader

    Retrieves a teams schedule page or a team roster page and dumps to a file

    Schedule:
        https://www.espn.com/nba/team/schedule/_/name/phi/season/2025
        There are preseason, regular season, play-in, post season links
        We want the regular season for now
        Preseason = https://www.espn.com/nba/team/schedule/_/name/okc/seasontype/1
        Regular season = https://www.espn.com/nba/team/schedule/_/name/okc/seasontype/2
        Post season = https://www.espn.com/nba/team/schedule/_/name/okc/seasontype/3
        play in = https://www.espn.com/nba/team/schedule/_/name/atl/seasontype/5

    Game results: https://www.espn.com/nba/game/_/gameId/401704632/bucks-76ers

"""

import requests
from web_scraper.config.teams import Team
from web_scraper.config import uris
from web_scraper.config import constants
import os


from web_scraper.utils.files import make_temp_file


class ESPNPageLoader:
    def __init__(self):
        pass

    @staticmethod
    def get_nba_schedule_page(team: Team, season_year: str, output_dir: str) -> str:
        uri = uris.espn_nba_regular_season_uri.format(abbreviation=team.espn_abbreviation, season_year=season_year)
        response = requests.get(url=uri, headers=constants.spoof_chrome_headers)

        out = os.path.join(output_dir, "nba", season_year)
        filename = make_temp_file(out, f"{team.clean_name}_schedule", "html")

        with open(filename, "w") as of:
            of.write(response.content.decode("utf-8"))

        return filename






