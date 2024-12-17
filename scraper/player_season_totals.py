from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import itertools
import pandas as pd

"""
Inits player season totals stats class. Initializes all selenium boilerplate
"""
class PlayerSeasonTotalStats():
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
        self.url = f"https://www.basketball-reference.com/players/{self.player_name[0]}/{self.player_name}01.html"
        self.browser.get(self.url)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'totals_stats'))
        )
        

    def __call__(self):
        try:
            print("Scraping season totals column data...")
            (columns := self.get_player_column_headers())
            if not columns:
                print("No columns found. Exiting.")
                return None

            print("Scraping season totals row data...")
            (rows := self.get_player_row_stats())
            if not rows:
                print("No rows found. Exiting.")
                return None

            print("Scrape ok...\n")
            print("Parsing data...")
            (player_dict := self.parse_player_stats(columns, rows))
            if not player_dict:
                print("Player stats dicitonary not constructed. Exiting.")
                return None

            print("Constructing dataframe...")
            self.player_dataframe(player_dict)
        
        finally:
            self.browser.quit()

    """
    Returns list of column headers in specified table

    Added exception handling
    """
    def get_player_column_headers(self) -> list:
        try:
            table = self.browser.find_element(By.ID, 'totals_stats')
            headers = table.find_elements(By.XPATH, './thead/tr')
            column_headers = [header.text for header in headers[0].find_elements(By.XPATH, './th[not(contains(@data-stat, "awards"))]')]

            return column_headers

        except NoSuchElementException:
            print(f"Could not find player {self.player_name}")
            return None

        except Exception as e:
            print(f"Exception: Error occurred: {e}")
            return None

    """
    Returns list of row data for each column
    """
    def get_player_row_stats(self) -> list:
        try:
            wait = WebDriverWait(self.browser, 1)
            player_data = list(itertools.chain(*[[cell.text for cell in row.find_elements(By.CSS_SELECTOR, "th,td")[:-1]]
            for row in wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "#totals_stats tbody tr")))]))

            return player_data

        except Exception as e:
            print(f"Error extracting row stats: {e}")
            return None

    """
    Parses data and packs into list of dictionaries

        Key : Season
        Items : Stat rows

    Added exception handling
    """
    def parse_player_stats(self, key_list, value_list) -> list:
        try:
            out = []

            out += [dict(zip(key_list, value_list[i: i + len(key_list)])) for i in range(0, len(value_list), len(key_list))]

            return out

        except Exception as e:
            print(f"Error packing dictionary: {e}")
            return None

    """
    Returns a pandas dataframe from above dictionary packing method
    """
    def player_dataframe(self, player_data_dict) -> None:
        try:
            player_df = pd.DataFrame(data=player_data_dict)

            return player_df

        except Exception as e:
            print(f"Error constructing dataframe: {e}")
            return None

stats = PlayerSeasonTotalStats("lillada")
stats()
