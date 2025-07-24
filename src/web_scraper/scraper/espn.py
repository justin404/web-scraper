"""
    ESPN Web Scraper
    Scrapes player and team information

    ESPN URL Structures

        Schedule:  https://www.espn.com/nba/team/schedule/_/name/phi/season/2025
        Game results: https://www.espn.com/nba/game/_/gameId/401704632/bucks-76ers
        Selector to get to the tbody which contains game results:

        #fittPageContainer > div.pageContent > div
            > div.page-container.cf > div > div.layout__column.layout__column--1
            > section > div > section > section > div > div > div
            > div.Table__Scroller > table > tbody

        First tr is the table header
        Table cells:
            0 = DATE
            1 = OPPONENT
            2 = RESULT
                span = W or L
                span
                    a.href == game results link
                    a.text == score

            3 = W-L
            4 = Hi Points
            5 = Hi Rebounds
            6 = Hi Assists

    Steps -
    1. Load the schedule page for the team
    2. Scrape the links for each game
    3. Load each game result page and retrieve statistics
    4. Load to the database

"""

from bs4 import BeautifulSoup, Tag
from web_scraper.loader.espn import ESPNPageLoader
from web_scraper.config.teams import Team
from web_scraper.config.teams.nba import NBATeams
from web_scraper.utils import files
from web_scraper.models.nba import Game
import datetime
import typing


default_output_dir = "D:\\workspace\\web-scraper\\output"

game_results_selector = ("#fittPageContainer > div.pageContent > div > div.page-container.cf > div > "
                         "div.layout__column.layout__column--1 > section > div > section > section > div > "
                         "div > div > div.Table__Scroller > table > tbody")

DATE_TD = 0
OPPONENT_TD = 1
RESULT_TD = 2
WIN_LOSS_TD = 3

season_year_months = {"sep", "oct", "nov", "dec"}
next_year_months = {"jan", "feb", "mar", "apr", "may", "jun"}

# We'll make it this format
date_format = "%b %d %Y"

class EspnNBAGameResultsScraper:

    def __init__(self):
        pass

    def scrape_schedule_page(self, team: Team, season_year: str, output_dir: str = None) -> typing.List[Game]:
        if output_dir is None:
            output_dir = default_output_dir
        schedule_page_filename = ESPNPageLoader.get_nba_schedule_page(team, season_year, output_dir)
        content = files.read_all_content(schedule_page_filename)
        parser = BeautifulSoup(content, "lxml")
        results_tbody = parser.css.select(game_results_selector)
        game_results = []

        # Skip the first tr
        for tr in results_tbody[0].contents[2:]:
            tds = tr.contents
            game_date = self._parse_schedule_date(tds[DATE_TD], season_year)
            results_td = tds[RESULT_TD]
            if results_td.string != "Postponed":
                is_win, link, score, is_ot = self._parse_result(results_td)
                game_results.append(Game(date=game_date, result=is_win, result_score=score, result_link=link,
                                         is_ot=is_ot))

        return game_results

    def _parse_schedule_date(self, td: Tag, season_year) -> datetime.datetime:
        # Dates are formatted like this: Wed, Oct 23
        # We could use the datetime.strptime -- but it complains there is no year.
        # The year will be season_year when month < Jan, season_year+1 when month >= Jan
        raw_date = td.contents[0].string
        month, day = raw_date[raw_date.find(",")+1:].strip().split()
        year = season_year if month.lower() in season_year_months else  str(int(season_year) + 1)
        return datetime.datetime.strptime(f"{month} {day} {year}", date_format)

    def _parse_result(self, td: Tag) -> tuple:
        """
        Result cell formatted like this:
            td
                span -> W or L
                span
                    a.href = game link
                    a.text = score
            Can also be a td with inner text when postponed

        :param td:
        :return: Tuple (is_win, link, score, is_ot)
        """
        # If the game is postponed, then this will have a different structure.
        # Need to check

        is_win = td.contents[0].string.lower() == "w"
        anchor_tag = td.contents[1].contents[0]
        link = anchor_tag["href"]
        score = anchor_tag.text.strip()
        is_ot = score.find("OT") > 0
        return is_win, link, score, is_ot



class EspnNBAGameStatisticsScraper:

    def __init__(self):
        pass

    def scrape_game_results(self):
        pass








