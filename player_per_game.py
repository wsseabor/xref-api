from base_stats_class.base_player_stat_class import BasePlayerStats
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

#Deprecated?
#DRIVER = "/usr/local/bin/chromedriver"

"""
Inherits from base player stat class
"""
class PlayerPerGameStats(BasePlayerStats):
    
    def __init__(self, player_name):
        self.player_name = player_name

    """
    Performs similar to a runtime script when class is called
    """
    def __call__(self):
        print("Scraping per game data...")
        self.get_player_column_headers()

        print("Scrape ok...")

    """
    Returns list of column headers in specified table
    """
    def get_player_column_headers(self) -> list:

        """
        Selenium webdriver boilerplate

        Has to use headless mode to work

        Experimental options - do not load images
        """
        options = Options()
        options.add_argument("--headless=new")
        options.add_experimental_option(
            "prefs", {
                "profile.managed_default_content_settings.images" : 2,
            }
        )

        browser = webdriver.Chrome(options=options)
        url = "https://www.basketball-reference.com/players/w/wembavi01.html"
        browser.get(url)

        try:
            table = browser.find_element(By.ID, 'per_game')
            headers = table.find_elements(By.XPATH, './thead/tr')
            column_headers = [header.text for header in headers[0].find_elements(By.TAG_NAME, 'th')]
            print(column_headers)
            browser.quit()
            
        except TimeoutException:
            pass

    def get_player_row_stats(self) -> list:
        pass

    def parse_player_stats(self) -> list:
        pass

    def clean_player_stats(self, player_data_frame) -> None:
        pass


stats = PlayerPerGameStats("wembavi")
stats()
