from abc import ABC, abstractmethod

"""
Structured base class for an NBA player's stat profiles on their home page 
(eg. https://www.basketball-reference.com/players/w/wembavi01.html)

Abstract class to scrape and parse player data, with selenium as basketball reference
now only loads dynamic data

Methods extract desired column header, row data, parses them and zips in one list of 
dictionaries, cleans and packages data with pandas
"""

class BasePlayerStats(ABC):

    @abstractmethod
    def get_player_column_headers(self) -> list:
        pass

    @abstractmethod
    def get_player_row_stats(self) -> list:
        pass

    @abstractmethod
    def parse_player_stats(self, key_list, value_list) -> list:
        pass

    @abstractmethod
    def clean_player_stats(self, player_data_dic) -> None:
        pass


"""

OLD

class BaseStatsClass(ABC):

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def get_player_column_headers(self) -> list:
        pass

    @abstractmethod
    def get_player_row_data(self) -> list:
        pass

    @abstractmethod
    def parse_player_stats(self, key_list, value_list) -> list:
        pass
        
"""