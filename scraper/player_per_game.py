from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

"""
Inits player per game stats class. Initializes all selenium boilerplate
"""

class PlayerPerGameStats():
    def __init__(self, player_name):
        self.player_name = player_name.lower()
        self.options = Options()

        #No popup window when called
        self.options.add_argument("--headless=new")

        #No image loading for performance
        self.options.add_experimental_option(
            "prefs", {
                "profile.managed_default_content_settings.images" : 2,
            }
        )
        self.browser = webdriver.Chrome(options=self.options)
        self.url = f"https://www.basketball-reference.com/players/{self.player_name[0]}/{self.player_name}01.html"
        self.browser.get(self.url)

        #Add wait for page load
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.ID, 'per_game_stats'))
        )

    """
    Performs similar to a runtime script when class is called

    Added more robust exception handling

    Added walrus operator for fun
    """
    def __call__(self):
        try:
            print("Scraping per game column data...")
            (columns := self.get_player_column_headers())
            if not columns:
                print("No columns found. Exiting.")
                return None

            print("Scraping per game row data...")
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
            table = self.browser.find_element(By.ID, 'per_game_stats')
            headers = table.find_elements(By.XPATH, './thead/tr')
            column_headers = [header.text for header in headers[0].find_elements(By.XPATH, './th[position() < last()]')]
            #print(column_headers)
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
            table = self.browser.find_element(By.ID, 'per_game_stats')
            rows = table.find_elements(By.XPATH, './tbody')
            stat_rows = [row.text for row in rows[0].find_elements(By.XPATH, './tr[position() < last()]')]

            #List split to get each stat as it's own index
            player_data = [y for x in stat_rows for y in x.split(' ')]

            #print(player_data)

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

            #print(out)

            return out

        except Exception as e:
            print(f"Error packing dictionary: {e}")
            return None
    
    """
    Returns a pandas dataframe from above dictionary packing method
    """
    def player_dataframe(self, player_data_dict) -> pd.DataFrame:
        try:
            player_df = pd.DataFrame(data=player_data_dict)

            #print(player_df.to_string())

            return player_df

        except Exception as e:
            print(f"Error constructing dataframe: {e}")
            return None

stats = PlayerPerGameStats("lillada")
stats()