from fetchSpotifyData import FetchSpotifyData
from calculate_items import calculate_items as cal

def main():
    print("Fetching Spotify Data...")
    FetchSpotifyData()
    print("Data fetched successfully.")
    print("Total Recently Played Tracks:", cal(data_file="spotify_data.json"))
    

if __name__ == "__main__":
    main()