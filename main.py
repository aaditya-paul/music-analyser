from fetchSpotifyData import FetchSpotifyData
from calculate_items import calculate_items as cal
from analyse import run_music_analysis
    
def main():
    print("Fetching Spotify Data...")
    FetchSpotifyData()
    print("Data fetched successfully.")
    print("Total Recently Played Tracks:", cal(data_file="spotify_data.json"))
    run_music_analysis(show_graphs=True)
    

if __name__ == "__main__":
    main()