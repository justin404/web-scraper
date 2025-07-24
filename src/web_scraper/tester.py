from web_scraper.loader.espn import ESPNPageLoader
from web_scraper.config.teams.nba import NBATeams
from web_scraper.scraper.espn import EspnNBAScraper

output_dir = "D:\\workspace\\web-scraper\\output"

input_file = "D:\\workspace\\web-scraper\\output\\nba\\2025\\Philadelphia_76ers_schedule.html"


# filename = ESPNPageLoader.get_nba_schedule_page(team=NBATeams.Philadelphia76ers,
#                                                 season_year="2025",
#                                                 output_dir=output_dir)


scraper = EspnNBAScraper()


games = scraper.scrape_schedule_page(NBATeams.AtlantaHawks, "2025", output_dir)

games
