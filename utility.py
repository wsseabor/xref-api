def parse_player_formatted_name(last_name, first_name):
    last = last_name[:5]
    first = first_name[:2]
    formatted_query_name = f"{last}{first}01"
    query_name = formatted_query_name.lower()
    return query_name