from base_stats_class.base_player_stat_class import BasePlayerStats
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

class PlayerSeasonTotalStats(BasePlayerStats):
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
        self.parse_player_stats(columns, rows)

    def get_player_column_headers(self) -> list:
        try:
            table = self.browser.find_element(By.ID, 'totals')
            headers = table.find_elements(By.XPATH, './thead/tr')
            column_headers = [header.text for header in headers[0].find_elements(By.XPATH, './th[not(contains(@data-stat, "DUMMY"))]')]

            print(column_headers)

            return column_headers

        except TimeoutException:
            self.browser.quit()

    def get_player_row_stats(self) -> list:
        try:
            table = self.browser.find_element(By.ID, 'totals')
            rows = table.find_elements(By.XPATH, './tbody')
            stat_rows = [row.text for row in rows[0].find_elements(By.XPATH, './tr')]

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

    def clean_player_stats(self, player_data_frame) -> None:
        pass

stats = PlayerSeasonTotalStats("lillada")
stats()