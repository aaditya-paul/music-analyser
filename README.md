
![WhatsApp Image 2025-10-31 at 22 43 03_391f985e](https://github.com/user-attachments/assets/70c0789c-5bc3-42d9-aea9-38bf48079e8d)
![WhatsApp Image 2025-10-31 at 22 43 02_3f4b666b](https://github.com/user-attachments/assets/d86914e1-9f33-4489-a3d9-632d8decd139)
![WhatsApp Image 2025-10-31 at 22 43 50_563020a4](https://github.com/user-attachments/assets/d9fdeb38-8594-4f6b-b510-dcfea91ab230)

# Video Output
https://github.com/user-attachments/assets/a1709ea3-cdc4-4c5f-9457-d5e7fd5d16ac

# 🎵 Spotify Music Personality Analyzer

A comprehensive Python application that analyzes your Spotify listening habits and generates a detailed music personality profile. The tool fetches your listening data, performs statistical analysis, and creates beautiful visualizations to reveal insights about your musical taste.

## ✨ Features

### 📊 Data Analysis

- **Multi-timeframe Analysis**: Analyzes your listening habits across three time periods:
  - Short-term (last 4 weeks)
  - Medium-term (last 6 months)
  - Long-term (several years)
- **Comprehensive Metrics**: Tracks popularity scores, artist counts, genre distribution, and listening duration
- **Library Insights**: Analyzes your saved tracks and recently played music

### 🎭 Music Personality Profile

The analyzer calculates a **7-dimensional personality vector** based on your listening habits:

1. **Mainstream vs Indie** (0-100): How mainstream or underground your taste is
2. **Diversity Factor** (0-100): How varied your music taste is across genres and artists
3. **Nostalgia Level** (0-100): Your preference for classic/retro music
4. **Energy Factor** (0-100): Whether you prefer upbeat or mellow music
5. **Emotional Depth** (0-100): Connection to emotional/melancholic music
6. **Cultural Rootedness** (0-100): Connection to cultural music (Bollywood, regional)
7. **Explorer Mindset** (0-100): How much you explore new/obscure music

### 📈 Visualizations

Generates a comprehensive dashboard with **6 graphs**:

- 🕸️ **Radar Chart**: Your personality profile visualization
- 📊 **Top 10 Artists Bar Chart**: Most listened artists by track count
- 🎨 **Genre Pie Chart**: Top 10 genres distribution
- 📉 **Personality Dimensions**: Color-coded bar chart of all 7 factors
- 📊 **Popularity Histogram**: Distribution of track popularity scores
- ⏰ **Time Period Comparison**: Dual-axis chart comparing listening trends

### 💕 Match Score (Future Dating App Feature)

Calculates a weighted **Music Personality Match Score** (0-100) designed for matching users based on musical compatibility. Includes:

- Personality type classification (e.g., "The Musical Nomad", "The Cultural Guardian")
- Compatibility tier ranking
- 7-dimensional vector for distance-based matching algorithms
- Exportable JSON data for integration

## 🚀 Setup

### Prerequisites

- Python 3.8 or higher
- Spotify Developer Account
- Active Spotify Premium or Free account

### Installation

1. **Clone the repository**

   ```bash
   cd music-analyzer/backend
   ```

2. **Create and activate a virtual environment**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Spotify API credentials**

   a. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

   b. Create a new app and note down:

   - Client ID
   - Client Secret

   c. In your app settings, add redirect URI: `http://127.0.0.1:8888/callback`

   d. Copy `.example.env` to `.env`:

   ```bash
   cp .example.env .env
   ```

   e. Edit `.env` and add your credentials:

   ```properties
   SPOTIPY_CLIENT_ID=your_client_id_here
   SPOTIPY_CLIENT_SECRET=your_client_secret_here
   SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
   ```

## 📖 Usage

### Basic Usage

Run the complete analysis pipeline:

```bash
python main.py
```

This will:

1. Fetch your Spotify data (top tracks, artists, saved tracks, recently played)
2. Save raw data to `./data/` directory
3. Perform comprehensive personality analysis
4. Generate visualizations (saved as `music_personality_graphs.png`)
5. Export match data to `music_personality_match.json`

### Module Usage

You can also use individual components:

```python
# Fetch data only
from fetchSpotifyData import FetchSpotifyData
FetchSpotifyData()

# Run analysis with graphs
from analyse import run_music_analysis
match_data = run_music_analysis(show_graphs=True)

# Run analysis without showing graphs
match_data = run_music_analysis(show_graphs=False)
```

### First-Time Authentication

On first run, the application will:

1. Open your browser for Spotify authorization
2. Ask you to grant permissions (read-only access)
3. Redirect you to `localhost:8888/callback`
4. Save authentication token in `.spotify_cache`

**Note**: You only need to authenticate once. The token is automatically refreshed.

## 📁 Project Structure

```
backend/
├── main.py                          # Main entry point
├── fetchSpotifyData.py              # Spotify API data fetching
├── analyse.py                       # Music personality analysis engine
├── calculate_items.py               # Utility functions
├── requirements.txt                 # Python dependencies
├── .env                             # Environment variables (create this)
├── .example.env                     # Environment template
├── .spotify_cache                   # OAuth token cache (auto-generated)
├── data/                            # Raw Spotify data (auto-generated)
│   ├── top_tracks.json
│   ├── top_artists.json
│   ├── saved_tracks.json
│   └── recently_played.json
├── music_personality_graphs.png     # Generated visualization (output)
└── music_personality_match.json     # Match data export (output)
```

## 📊 Output Files

### `music_personality_graphs.png`

High-resolution (300 DPI) dashboard with 6 visualization charts saved automatically.

### `music_personality_match.json`

Contains your music personality data in JSON format:

```json
{
  "music_personality_score": 75,
  "personality_type": "THE MUSICAL NOMAD",
  "compatibility_tier": "PREMIUM TIER",
  "vector": [65, 82, 45, 70, 60, 55, 78],
  "dimensions": {
    "mainstream_vs_indie": 65,
    "diversity": 82,
    "nostalgia": 45,
    "energy": 70,
    "emotional_depth": 60,
    "cultural_rootedness": 55,
    "explorer": 78
  },
  "top_genre": "indie rock",
  "top_artist": "Artist Name",
  "avg_popularity": 62.5,
  "total_artists": 247
}
```

## 🔧 Configuration

### Graph Display Control

Control whether graphs are displayed:

```python
# Show graphs in window + save PNG
run_music_analysis(show_graphs=True)

# Only save PNG without displaying
run_music_analysis(show_graphs=False)
```

### API Timeout Settings

If you experience timeout errors with Spotify API, you can adjust the timeout in `fetchSpotifyData.py`:

```python
# Line 165
sp = spotipy.Spotify(auth_manager=auth_manager, requests_timeout=10)  # Increase from default 5
```

## 🎯 Use Cases

### Personal Music Discovery

- Understand your listening patterns and preferences
- Discover which genres and artists dominate your taste
- Track how your musical taste evolves over time

### Music-Based Social Features

The personality vector and match score are designed for:

- **Dating Apps**: Match users based on music compatibility
- **Social Networks**: Find people with similar music taste
- **Playlist Collaboration**: Connect users for collaborative playlists
- **Concert Buddies**: Find companions for live music events

### Data Analysis & Research

- Study music consumption patterns
- Analyze genre trends and popularity
- Research cultural music preferences

## 🛠️ Troubleshooting

### `ModuleNotFoundError: No module named 'spotipy'`

Ensure you've activated the virtual environment and installed dependencies:

```bash
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### `TimeoutError: The read operation timed out`

Your internet connection might be slow. Increase the timeout value in `fetchSpotifyData.py` (see Configuration section).

### `FileNotFoundError: [Errno 2] No such file or directory: './data/top_tracks.json'`

Run the data fetching first:

```bash
python fetchSpotifyData.py
```

### Authentication Issues

1. Delete `.spotify_cache` file
2. Verify credentials in `.env` file
3. Check redirect URI matches exactly: `http://127.0.0.1:8888/callback`
4. Ensure your Spotify app is not in Development Mode restrictions

## 📦 Dependencies

Main libraries:

- **spotipy** (2.25.1): Spotify Web API wrapper
- **pandas** (2.3.3): Data manipulation and analysis
- **matplotlib** (3.10.7): Visualization and plotting
- **numpy** (2.3.4): Numerical computing
- **python-dotenv** (1.2.1): Environment variable management

See `requirements.txt` for complete list.

## 🔒 Privacy & Data

- **Read-Only Access**: The app only reads your Spotify data (never modifies)
- **Local Storage**: All data is stored locally on your machine
- **No External Sharing**: Your data is never sent to external servers
- **OAuth Security**: Uses official Spotify OAuth2 authentication

### Required Spotify Scopes

- `user-read-recently-played`: Access recently played tracks
- `user-top-read`: Read top artists and tracks
- `user-library-read`: Read saved tracks
- `user-follow-read`: Read followed artists
- `playlist-read-private`: Read private playlists

## 🚧 Future Enhancements

- [ ] Web dashboard interface
- [ ] Historical trend tracking (save snapshots over time)
- [ ] Playlist generation based on personality
- [ ] Social features (share profiles, compare with friends)
- [ ] Integration with dating app APIs
- [ ] Machine learning-based recommendations
- [ ] More personality dimensions and metrics
- [ ] Export to PDF/Instagram-ready formats

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is open source and available for personal use.

## 👤 Author

**Aaditya Paul**

## 🙏 Acknowledgments

- Spotify Web API for providing comprehensive music data
- The open-source community for excellent Python libraries
- Music lovers worldwide for inspiring this project

---

**Note**: This tool is for personal analysis and educational purposes. It is not affiliated with or endorsed by Spotify.

## 🎵 Happy Analyzing! 🎵
