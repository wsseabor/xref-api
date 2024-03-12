from utility.utility import parse_player_formatted_name
from player_last_five import PlayerLastFiveStats

"""
Simple CLI interface - to change later
"""

if __name__ == "__main__":
    
    running = True

    while running:
        print("Basketball reference API v0.01\n")
        print("Enter player name to receive updated last five games stats\n")

        print("Enter player last name:")
        last = input()
        print("Enter player first name:")
        first = input()

        query_string = parse_player_formatted_name(last, first)
        last_five = PlayerLastFiveStats(query_string, None, None)
        last_five.run()


    """
    CLI with sys.arg, clean up later
    
    """

    """
    if __name__ == "__main__":
        q_string = parse_player_formatteda_name(sys.argv[1], sys.argv[2])
        last_five = PlayerLastFive(q_string, None, None)
        last_five.run()
    
    """
