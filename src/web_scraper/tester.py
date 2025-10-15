import web_scraper.loader.espn as espn_page_loader
from web_scraper.config.teams.nba import NBATeams
# from web_scraper.scraper.espn import EspnNBAGameResultsScraper, EspnNBAGameStatisticsScraper

output_dir = "D:\\workspace\\web-scraper\\output"

input_file = "D:\\workspace\\web-scraper\\output\\nba\\2025\\Philadelphia_76ers_schedule.html"


# filename = ESPNPageLoader.get_nba_schedule_page(team=NBATeams.Philadelphia76ers,
#                                                 season_year="2025",
#                                                 output_dir=output_dir)


# results_scraper = EspnNBAGameResultsScraper()
# box_score_scraper = EspnNBAGameStatisticsScraper()


# games = results_scraper.scrape_schedule_page(NBATeams.Philadelphia76ers, "2025", output_dir)

# files = box_score_scraper.scrape_game_results([], output_dir)



from web_scraper.context import Context

Context()