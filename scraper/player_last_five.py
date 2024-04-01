import requests
from bs4 import BeautifulSoup
from base_stats_class.base_player_stat_class import BaseStatsClass

"""
NBA player's last five scraped stats class

Refactored to an abstract class, each table from the player's home page on basketball reference
(eg. https://www.basketball-reference.com/players/w/wembavi01.html for Victor Wembanyama will have
the same methods reused for each table, being last five, per 36, per 100 possesions...

Takes player name, modifies name for query string (in utility.py), stats come out.)
"""

class PlayerLastFiveStats(BaseStatsClass):

    def __init__(self, player_name) -> None:
        self.player_name = player_name

    """
    Returns none, for now. Useful for debugging. Runs all methods in class
    and returns a stat profile for the given player
    """
    def run(self) -> None:
        print(" --->  Scraping columns headers...")
        (x := self.get_player_column_headers())

        print(" ---> Scraping player data...")
        (y := self.get_player_row_data())

        print(" ---> Zipping stats...")
        print(self.parse_player_stats(x, y))


    """
    Returns a list of column headers for the given player's stat profile
    """
    def get_player_column_headers(self) -> list:
        html = requests.get(f"https://www.basketball-reference.com/players/{self.player_name[0]}/{self.player_name}01.html")
        soup = BeautifulSoup(html.text, 'html.parser')

        column_table = soup.find('table', id = 'last5')

        player_column_headers = [th.get_text(strip = True) for th in column_table.find_all('tr', limit = 1)[0].find_all('th')]

        #For testing
        #print(player_column_headers)

        return player_column_headers
    

    """
    Returns a list of stat rows for the given player's stat profile (Points, rebounds, assists, etc)
    """
    def get_player_row_data(self):
        html = requests.get(f"https://www.basketball-reference.com/players/{self.player_name[0]}/{self.player_name}01.html")
        soup = BeautifulSoup(html.text, 'html.parser')

        page = soup.find('table', class_ = 'sortable stats_table')

        stats = page.find_all(['th', 'td'], attrs= { 'data-stat' : any})

        #Test print
        #print([td.get_text(strip = True) for td in stats])

        #Hardcododed 27 due to length of headers - needed in zipping up to list of dicts
        stat_rows = [td.get_text(strip = True) for td in stats][27:]

        return stat_rows
    

    """
    Returns a list of dictionaries that contain each of the player's stats of last five games
    """
    def parse_player_stats(self, key_list, value_list) -> list:
        out = []

        out += [dict(zip(key_list, value_list[i: i + len(key_list)])) for i in range(0, len(value_list), len(key_list))]

        return out
    

#Test
stats = PlayerLastFiveStats("wembavi")
stats.run()