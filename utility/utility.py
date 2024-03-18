import csv
from data.data import player_last_five_fields, player_per_game_fields

def parse_player_formatted_name(last_name, first_name):
    last = last_name[:5]
    first = first_name[:2]
    formatted_query_name = f"{last}{first}01"
    query_name = formatted_query_name.lower()
    print(query_name)
    return query_name

def output(values, output_type, output_file_path, output_write_option, csv_writer):
    if output_type is None:
        return values
    
    if output_type == "CSV":
        if output_file_path is None:
            raise ValueError("CSV output must contain file path.")
        else:
            return csv_writer(rows = values, output_file_path = output_file_path, 
                              output_write_option = output_write_option)
        
    raise ValueError(f"Unknown output: {output_type}")

def player_last_five_to_csv(rows, output_file_path, output_write_option):
    with open(output_file_path, output_write_option, newline = "") as f:
        writer = csv.DictWriter(f, fieldnames = player_last_five_fields)
        writer.writeheader()
        writer.writerows(
            rows
        )

def player_per_game_to_csv(rows, output_file_path, output_write_option):
    with open(output_file_path, output_write_option, newline = "") as f:
        writer = csv.DictWriter(f, fieldnames = player_per_game_fields)
        writer.writeheader()
        writer.writerows(
            rows
        )
