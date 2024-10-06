from utility.utility import parse_player_formatted_name
#from scraper.player_last_five import PlayerLastFiveStats
from scraper.player_per_36 import PlayerPer36Minutes
from scraper.player_per_game import PlayerPerGameStats
from scraper.player_season_totals import PlayerSeasonTotalStats
import sys
if __name__ == "__main__":
    
    query_string = parse_player_formatted_name("james", "harden")
    per_36 = PlayerPer36Minutes(query_string)
    per_36()

    per_game = PlayerPerGameStats(query_string)
    per_season = PlayerSeasonTotalStats(query_string)

   
