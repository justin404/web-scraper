"""
    ESPN Web Scraper
    Scrapes player and team information

    ESPN URL Structures

    Schedule:  https://www.espn.com/nba/team/schedule/_/name/phi/season/2025
        There are various types of schedules -
            Preseason = https://www.espn.com/nba/team/schedule/_/name/okc/seasontype/1
            Regular season = https://www.espn.com/nba/team/schedule/_/name/okc/seasontype/2
            Post season = https://www.espn.com/nba/team/schedule/_/name/okc/seasontype/3
            play in = https://www.espn.com/nba/team/schedule/_/name/atl/seasontype/5

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

    Box Scores
        Box Score link --> https://www.espn.com/nba/boxscore/_/gameId/401704632
        Results Page Link --> https://www.espn.com/nba/game/_/gameId/401704632/bucks-76ers

        Box score tables are wrapped in a parent div
            div.Boxscore flex flex-column       :: parent of both teams box score tables
                div.Boxscore__Title         :: contains team image
                    div.BoxscoreItem__TeamName  :: content is the team name -- this should match the team name we have stored
                div.ResponsiveTable
                    div.flex
                        table :: this is the table which contains a single column for each player
                            tbody
                                tr  :: each row has data-idx -- can use this to link up player to stats
                                    td.Table__TD :: wraps player information
                                        div
                                            a
                                                span :: long name
                                                span :: short name
                                            span  :: player number in format of "#xx"
                                    OR - to split starters and bench
                                    td.Table__customHeader.Table__TD
                                        div.Table__customHeader
                                            starters or bench


                        div :: this div wraps the actual box scores
                            div :: ignore
                            div.Table__Scroller
                                table
                                    tbody
                                        tr :: first row is the header       each row has data-idx
                                            td :: min
                                            td :: fg        made-attempted
                                            td :: 3pt       made-attempted
                                            td :: ft        made-attempted
                                            td :: oreb
                                            td :: dreb
                                            td :: reb
                                            td :: ast
                                            td :: stl
                                            td :: blk
                                            td :: to
                                            td :: pf
                                            td :: +/-
                                            td :: pts

                                            if only a single td - this could be
                                                DNP-COACH'S DECISION (or likely other reasons)
                                        second to last row - totals
                                        last row - percentages


    Steps -
    1. Load the schedule page for the team
    2. Scrape the links for each game
    3. Load each game result page and retrieve statistics
    4. Load to the database

"""

import datetime
import typing
import time
from bs4 import BeautifulSoup, Tag
import web_scraper.loader.espn as espn_page_loader
from web_scraper.config.teams import Team
from web_scraper.config.teams.nba import NBATeams
from web_scraper.models.nba import BoxScore
from web_scraper.utils import files
from web_scraper.models.nba import Game



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

stat_mappings = [
    "minutes", "fg", "three_pt", "ft", "oreb", "dreb", "reb", "ast", "stl", "blk", "to", "pf", "plus_minus", "pts"
]

class EspnNBAGameResultsScraper:

    def __init__(self):
        pass

    def scrape_schedule_page(self, team: Team, season_year: str, output_dir: str = None) -> typing.List[Game]:
        if output_dir is None:
            output_dir = default_output_dir
        schedule_page_filename = espn_page_loader.get_nba_schedule_page(team, season_year, output_dir)
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
                is_win, link, score, is_ot, game_id = self._parse_result(results_td)
                game_results.append(Game(date=game_date, result=is_win, result_score=score, result_link=link,
                                         game_id=game_id, is_ot=is_ot))

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


            Link in the format of https://www.espn.com/nba/game/_/gameId/401704632/bucks-76ers
            We need to extract the gameId


        :param td:
        :return: Tuple (is_win, link, score, is_ot, game_id)
        """
        # If the game is postponed, then this will have a different structure.
        # Need to check

        def extract_game_id(link):
            game_id = link[link.find("gameId/")+7:]
            game_id = game_id[0:game_id.find("/")]
            return game_id

        is_win = td.contents[0].string.lower() == "w"
        anchor_tag = td.contents[1].contents[0]
        link = anchor_tag["href"]
        score = anchor_tag.text.strip()
        is_ot = score.find("OT") > 0
        game_id = extract_game_id(link)
        return is_win, link, score, is_ot, game_id



class EspnNBAGameStatisticsScraper:

    def __init__(self):
        pass

    def scrape_game_results(self, games: typing.List[Game], season_year: str, output_dir: str = None) -> typing.List[str]:
        if output_dir is None:
            output_dir = default_output_dir

        for game in games:
            # TODO: Check to see if we have the game first before running the query
            box_score_file = espn_page_loader.get_nba_box_score_page(game.game_id, season_year, output_dir)
            game.box_score_file = box_score_file
            # TODO: Randomize this so that it doesn't look so consistent
            time.sleep(5)

        game_files = ["D:\\workspace\\web-scraper\\output\\nba\\season_year\\401703373_box_score_501d551ea5f74c8e9896d12648974d95.html"]

        for game in games:
            content = files.read_all_content(game.box_score_file)
            parser = BeautifulSoup(content, "lxml")
            box_score_wrapper_selector = "div.Boxscore.Boxscore__ResponsiveWrapper > div.Wrapper"
            box_score_team_a_elem = parser.css.select(box_score_wrapper_selector)[0]
            box_score_team_b_elem = parser.css.select(box_score_wrapper_selector)[1]

            box_score_team_a = self._process_box_score(box_score_team_a_elem)
            box_score_team_b = self._process_box_score(box_score_team_b_elem)

            box_score_team_a.game_id = game.game_id
            box_score_team_b.game_id = game.game_id




        return game_files

    def _process_box_score(self, box_score_element: Tag) -> BoxScore:
        team_name_selector = "div.Boxscore > div.Boxscore__Title > div.BoxscoreItem__TeamName"
        player_names_selector = "div.Boxscore > div.ResponsiveTable > div > table.Table > tbody.Table__TBODY > tr"
        player_stats_selector = "div.Boxscore > div.ResponsiveTable > div > div.Table__ScrollerWrapper > div.Table__Scroller > table > tbody.Table__TBODY > tr"

        team_name = box_score_element.select(team_name_selector)[0].text.strip()

        player_names = box_score_element.select(player_names_selector)
        player_stats = box_score_element.select(player_stats_selector)

        if len(player_names) != len(player_stats):
            raise ValueError("Player names and player stats are not the same length")

        combined = zip(player_names, player_stats)

        is_starter = True

        for player_row, stats_row in combined:
            if self._is_non_player_row(player_row):
                is_starter = not self._is_bench_row(player_row)
                continue
            if player_row["data-idx"] != stats_row["data-idx"]:
                raise ValueError("Player and stats are not from the same index. Mismatched rows!")

            bs = self._initialize_player_box_score(player_row, stats_row, is_starter)
            self._extract_stats(bs, stats_row)
            bs.team_name = team_name

    def _initialize_player_box_score(self, player_row: Tag, stats_row: Tag, is_starter: bool) -> BoxScore:
        player_name = player_row.select("td > div > a > span:first-child")[0].text
        player_number = player_row.select("td > div > span.playerJersey")[0].text
        player_link = player_row.selecet("td > div > a")[0]["href"]
        player_id = self._extract_player_id(player_link)
        data_idx = player_row["data-idx"]

        bs = BoxScore(
            player_name=player_name,
            player_number=player_number,
            player_id=player_id,
            player_link=player_link,
            data_index=int(data_idx),
            is_dnp=self._is_dnp(stats_row),
            is_starter=is_starter
        )
        return bs


    def _extract_stats(self, box_score: BoxScore, stats_row: Tag):
        stats = list(map(lambda k: k.text, stats_row.select("td")))
        for stat_name, stat_value in zip(stat_mappings, stats):
            setattr(box_score, stat_name, stat_value)

    def _is_dnp(self, stats_elem: Tag) -> bool:
        td = stats_elem.select("td")[0]
        return "colspan" in td.attrs

    def _extract_player_id(self, player_link: str) -> str:
        player_id_name = player_link[player_link.find("/id/")+4:]
        return player_id_name[0:player_id_name.find("/")]

    def _is_non_player_row(self, row: Tag) -> bool:
        return row.select("td.Table__customHeader") is not None

    def _is_bench_row(self, row: Tag) -> bool:
        return row.select("td.Table__customHeader > div.Table__customHeader")[0].text.lower() == "bench"





