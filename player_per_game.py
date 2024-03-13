from base_stats_class.base_player_stat_class import BasePlayerStats
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

DRIVER = "/usr/local/bin/chromedriver"

class PlayerPerGameStats(BasePlayerStats):
    
    def __init__(self, player_name):
        self.player_name = player_name

    def __call__(self):
        print("Scraping per game data...")
        self.get_player_column_headers()

        print("Scrape ok...")

    def get_player_column_headers(self) -> list:
        browser = webdriver.Chrome(DRIVER)
        url = "https://www.basketball-reference.com/players/{self.player_name[0]}/{self.player_name}01.html"

        delay = 5

        while True:
            try:
                browser.set_page_load_timeout(20)
                while True:
                    try:
                        browser.get(url)
                    except TimeoutException:
                        print("Timed out, retrying...")
                    else:
                        break

                WebDriverWait(browser, delay).until(ec.presence_of_element_located((By.ID, "per_game")))
            except TimeoutException:
                browser.quit()
                continue
            break

        browser.maximize_window()

        table = browser.find_element(By.ID, "per_game")
        head = table.find_element(By.TAG_NAME, "thead")

        head_row = head.find_element(By.TAG_NAME, "tr")[1]

        player_column_headers = [header.text.encode("utf8") for header in head_row.find_element((By.TAG_NAME, "th"))]
        player_column_headers = player_column_headers[1:]

        browser.quit()

        print(player_column_headers)

    def get_player_row_stats(self) -> list:
        pass

    def parse_player_stats(self) -> list:
        pass

    def clean_player_stats(self, player_data_frame) -> None:
        pass


stats = PlayerPerGameStats("wembavi")
