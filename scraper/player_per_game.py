#from base_stats_class.base_player_stat_class import BasePlayerStats
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

"""
Inherits from base player stat class
"""
class PlayerPerGameStats():
    
    def __init__(self, player_name):
        self.player_name = player_name
        self.options = Options()
        self.options.add_argument("--headless=new")
        self.options.add_experimental_option(
            "prefs", {
                "profile.managed_default_content_settings.images" : 2,
            }
        )
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.get(f"https://www.basketball-reference.com/players/{self.player_name[0]}/{self.player_name}01.html")

    """
    Performs similar to a runtime script when class is called
    """
    def __call__(self):
        print("Scraping per game column data...")
        (columns := self.get_player_column_headers())

        print("Scraping per game row data...")
        (rows := self.get_player_row_stats())

        print("Scrape ok...\n")
        print("Parsing data...")
        (player_dict := self.parse_player_stats(columns, rows))

        print("Constructing dataframe...")
        self.clean_player_stats(player_dict)

    """
    Returns list of column headers in specified table
    """
    def get_player_column_headers(self) -> list:

        """
        Scrapes pages with selenium and xpath methods, returns list of column headers
        """

        try:
            table = self.browser.find_element(By.ID, 'per_game')
            headers = table.find_elements(By.XPATH, './thead/tr')
            column_headers = [header.text for header in headers[0].find_elements(By.XPATH, './th[not(contains(@data-stat, "award_summary"))]')]

        except TimeoutException:
            self.browser.quit()


        return column_headers
    
    def get_player_row_stats(self) -> list:

        """
        Selenium webdriver boilerplate

        OLD:

        TO DO:
            Exclude player awards in given season - selenium xpath scraping includes column data with 
            awards but skips columns without - leaving no blank string for an empty column, making
            zipping in dictionary

        try:
            table = self.browser.find_element(By.ID, 'per_game')
            rows = table.find_elements(By.XPATH, './tbody/tr')

            #31 rows in player per game data, needed to parse list to zip to list of dicts
            player_data = [row.text for row in rows][:31]

            return player_data

        except TimeoutException:
            self.browser.quit()


        """

        try:
            table = self.browser.find_element(By.ID, 'per_game')
            rows = table.find_elements(By.XPATH, './tbody')
            stat_rows = [row.text for row in rows[0].find_elements(By.XPATH, './tr[not(contains(@data-stat, "award_summary"))]')]

            #List split to get each stat as it's own index
            player_data = [y for x in stat_rows for y in x.split(' ')]

            print(player_data)

            return player_data

        except TimeoutException:
            self.browser.quit()
        

    def parse_player_stats(self, key_list, value_list) -> list:
        out = []

        out += [dict(zip(key_list, value_list[i: i + len(key_list)])) for i in range(0, len(value_list), len(key_list))]

        print(out)

        return out

    def clean_player_stats(self, player_data_dic) -> pd.DataFrame:
        player_df = pd.DataFrame(data = player_data_dic)
        

        #print(player_df.to_string())
        return player_df

stats = PlayerPerGameStats("lillada")
stats()
