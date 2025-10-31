import json
def calculate_items(data_file):
    try:
        with open(data_file, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            # print("Total Recently Played Tracks:", len(data.get("items", [])))
            return len(data.get("recently_played", []))
    except FileNotFoundError:
        data = {}

    return 0

if __name__ == "__main__":
    total_items = calculate_items("spotify_data.json")
    print("Total Recently Played Tracks:", total_items)