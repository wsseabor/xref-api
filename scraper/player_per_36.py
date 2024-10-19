#from base_stats_class.base_player_stat_class import BasePlayerStats
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

"""
Player per 36 minutes total stats

Takes player name and uses it to reference basketball reference's player stats page,
Inits selenium webdriver with options for headless browser and not loading images for faster performance

__call__ method performs like runtime script, aggregating columns and rows of stats table
and concatenates them to dictionary, then to pandas dataframe

Other helper methods retrieve columns headers and rows, and perform utility functions
to package data into format that can be output to a json-like format and then to dataframe
"""

class PlayerPer36Minutes():
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

    def __call__(self):
        try:
            print("Scraping per game column data...")
            (columns := self.get_player_column_headers())

            print("Scraping per game row data...")
            (rows := self.get_player_row_stats())

            print("Scrape ok...")
            print("Parsing data...")
            (player_dict := self.parse_player_stats(columns, rows))

            print("Constructing dataframe...")
            self.clean_player_stats(player_dict)


        #Multiple exception block, must be tuple
        except (SessionNotCreatedException, TimeoutException) as e:
            print("Selenium error: ", e)
            self.browser.quit()

    def get_player_column_headers(self) -> list[str]:
        """
        Scrapes page with selenium and xpath methods, returns list of column headers
        """

        try:
            table = self.browser.find_element(By.ID, 'per_minute')
            headers = table.find_elements(By.XPATH, './thead/tr')
            column_headers = [header.text for header in headers[0].find_elements(By.XPATH, './th')]

            #Test print
            print(column_headers)

            return column_headers

        except TimeoutException:
            self.browser.quit()
    
    def get_player_row_stats(self) -> list[str]:
        """
        Scrapes page with selenium and xpath methods, returns list of row stats for each row
        """
        try:
            table = self.browser.find_element(By.ID, 'per_minute')
            rows = table.find_elements(By.XPATH, './tbody')
            stat_rows = [row.text for row in rows[0].find_elements(By.XPATH, './tr')]

            player_data = [y for x in stat_rows for y in x.split(' ')]

            print(player_data)

            return player_data

        except TimeoutException:
            self.browser.quit()
    
    def parse_player_stats(self, key_list, value_list) -> list:
        """
        Parses both column headers and row values, packages them into list of dictionaries for each row

        Init empty list

        Append empty list as dictionary, zip the key_list (column headers), and value_list(rows), slices row
        list from zero to the length of the header list, for each value in range (0, start: length of row, step: length of 
        column headers)       
        """

        out = []

        out += [dict(zip(key_list, value_list[i: i + len(key_list)])) for i in range(0, len(value_list), len(key_list))]

        #Test print
        print(out)

        return out
    
    def clean_player_stats(self, player_data_dic) -> pd.DataFrame:
        player_df = pd.DataFrame(data=player_data_dic)

        #Test print
        #print(player_df.to_string())

        return player_df
    
stats = PlayerPer36Minutes("lillada")
stats()
