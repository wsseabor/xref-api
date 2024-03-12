from abc import ABC, abstractmethod


"""
Structured base class for an NBA player's stat profils on their home page 
(eg. https://www.basketball-reference.com/players/w/wembavi01.html)

Methods to extract column headers in table, specified stats rows in table, zip function
to package into list of dictionaries for parsing

"""
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
    def parse_player_stats(self) -> list:
        pass