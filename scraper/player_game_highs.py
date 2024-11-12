from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd

class PlayerGameHighs():
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
        print("Scraping per game column data...")
        (columns := self.get_player_column_headers())

        print("Scraping per game row data...")
        (rows := self.get_player_row_stats())

        print("Scrape ok...\n")
        print("Parsing data...")
        (player_dict := self.parse_player_stats(columns, rows))

        print("Constructing dataframe...")
        self.clean_player_stats(player_dict)

    def get_player_column_headers(self) -> list:

        try:
            table = self.browser.find_element(By.ID, 'highs_reg_season')
            headers = table.find_elements(By.XPATH, './thead/tr')
            column_headers = [header.text for header in headers[0].find_elements(By.XPATH, './th[position() != last()]')]

        except TimeoutException:
            self.browser.quit()

        print(column_headers)

        return column_headers



    