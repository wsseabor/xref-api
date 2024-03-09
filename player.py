import requests
from bs4 import BeautifulSoup


"""
NBA player class

Takes player name (Modified in utility file for basketball reference's query params, 
player name like James Harden would shorted to hardeja1), csv output file name if specified
"""
class NbaPlayerStats:

    #Init method
    def __init__(self, player, csv_file_name = None):
        self.player = player
        self.csv_file_name = csv_file_name

    """
    Initially wanted to use the dunder call method, but that didn't end up working too well.
    Unsure why - will research later.

    Also the repeated function calls should probably be cleaned up. But I did get to use
    the walrus operator, which should take precedence over best practices

    Run method scrapes all relevant class data, packages it to list of dictionaries, 
    outputs to specified file type.

    TO DO:
        Add json 
    """
    def run(self):
        print(" --->  Scraping columns headers...")
        (x := self.get_player_column_header())

        print(" ---> Scraping player data...")
        (y := self.get_player_row_data())

        print(" ---> Zipping stats...")
        print(self.parse_player_stats(x, y))
        
    """
    Method gets column headers per player

    Returns list of column headers
    """
    def get_player_column_header(self):
        html = requests.get(f"https://www.basketball-reference.com/players/w/{self.player}.html")
        soup = BeautifulSoup(html.text, 'html.parser')

        column_table = soup.find('table', id = 'last5')

        player_column_headers = [th.get_text(strip = True) for th in column_table.find_all('tr', limit = 1)[0].find_all('th')]

        #For testing
        #print(player_column_headers)

        return player_column_headers
    

    """
    Gets player row data

    Returns list of row data for last five games
    """
    def get_player_row_data(self):
        html = requests.get(f"https://www.basketball-reference.com/players/w/{self.player}.html")
        soup = BeautifulSoup(html.text, 'html.parser')

        page = soup.find('table', id = 'last5')

        stats = page.find_all(['th', 'td'], attrs= { 'data-stat' : any})

        #Test print
        #print([td.get_text(strip = True) for td in stats])

        return [td.get_text(strip = True) for td in stats][27:]
    

    """
    Returns list of dictionaries

    Each dict represents one of the last five games played
    """
    def parse_player_stats(self, key_list, value_list):
        out = []

        out += [dict(zip(key_list, value_list[i: i + len(key_list)])) for i in range(0, len(value_list), len(key_list))]

        return out

stats = NbaPlayerStats("wembavi01")
stats.run()