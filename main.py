from utility.utility import parse_player_formatted_name
#from scraper.player_last_five import PlayerLastFiveStats
from scraper.player_per_36 import PlayerPer36Minutes
from scraper.player_per_game import PlayerPerGameStats
from scraper.player_season_totals import PlayerSeasonTotalStats
import sys
"""
Simple CLI interface - to change later
"""

if __name__ == "__main__":
    
    query_string = parse_player_formatted_name("Harden", "James")
    per_36 = PlayerPer36Minutes(query_string, None, None)
    per_36()
    


    """
    CLI with sys.arg, clean up later
    
    
    q_string = parse_player_formatted_name(sys.argv[1], sys.argv[2])
    player_season = PlayerSeasonTotalStats(q_string)
    player_season()
    """
    
