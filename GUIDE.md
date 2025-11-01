# 🚀 Quick Start Guide

## Installation & Setup (5 minutes)

### Step 1: Check Python

```bash
python --version
# Should be 3.8 or higher
```

### Step 2: Install Dependencies

```bash
# Core dependencies (required)
pip install -r requirements.txt

# Optional: For interactive visualizations
pip install plotly wordcloud
```

### Step 3: Verify Data Files

Make sure you have these files in the `data/` folder:

- `top_tracks.json`
- `top_artists.json`
- `saved_tracks.json`
- `recently_played.json`

If not, run:

```bash
python fetchSpotifyData.py
```

## Running the Analysis

### Option 1: Complete Analysis (Recommended)

```bash
python run_complete_analysis.py
```

**What it does:**

1. Loads and processes all your Spotify data
2. Calculates diversity metrics (genre entropy, artist concentration)
3. Analyzes nostalgia patterns (consistency, loyalty, resurgence)
4. Infers mood features (energy, valence, danceability)
5. Analyzes emotional depth and range
6. Generates interactive visualizations (if libraries installed)
7. Creates a comprehensive text report

**Time:** ~30 seconds - 1 minute

### Option 2: Step-by-Step

#### Basic Analysis (Original):

```bash
python analyse.py
```

- Generates personality scores
- Creates static charts
- Saves `music_personality_match.json`

#### Enhanced Analysis:

```bash
python enhanced_analysis.py
```

- Advanced diversity metrics
- Nostalgia analysis
- Listener classification
- Saves `enhanced_analysis_results.json`

#### Mood & Emotion:

```bash
python mood_emotion_analysis.py
```

- Mood inference from genres
- Emotional depth analysis
- Saves `emotional_analysis_results.json` and `tracks_with_mood_features.json`

#### Visualizations:

```bash
python enhanced_visualizations.py
```

- Creates interactive HTML charts
- Generates word cloud
- Requires previous steps to be run first

## Viewing Your Results

### Text Report

Open `music_personality_report.txt` in any text editor to see:

- Your listener type classification
- All diversity and nostalgia metrics
- Emotional profile
- Key insights

### Interactive Charts (if Plotly installed)

Open these HTML files in your browser:

1. `radar_chart_interactive.html` - Your music personality radar
2. `genre_sunburst_interactive.html` - Genre distribution
3. `mood_scatter_interactive.html` - Energy vs. emotion map
4. `top_artists_interactive.html` - Your top artists
5. `popularity_timeline_interactive.html` - Popularity over time

### Images

- `artist_wordcloud.png` - Word cloud of your artists
- `music_personality_graphs.png` - Comprehensive static charts

### Raw Data (JSON)

For developers/data scientists:

- `enhanced_analysis_results.json`
- `emotional_analysis_results.json`
- `tracks_with_mood_features.json`
- `music_personality_match.json`

## Understanding Your Results

### Listener Types

**🌍 Musical Explorer (75-100%)**

- Extremely diverse taste
- Always discovering new sounds
- Low artist concentration

**🎨 Eclectic Curator (60-75%)**

- Well-balanced variety
- Enjoys exploring but has favorites
- Moderate artist concentration

**🎯 Focused Enthusiast (40-60%)**

- Clear preferences
- Some exploration
- Moderate to high concentration

**💎 Niche Specialist (0-40%)**

- Highly focused
- Deep expertise in specific areas
- High artist concentration

### Key Metrics Explained

**Diversity Score (0-100%)**

- Based on Shannon entropy
- Higher = more diverse
- Considers both genres and artists

**Consistency Score (0-100%)**

- How many long-term favorites are still in your rotation
- High = loyal listener
- Low = always changing

**Artist Loyalty (0-100%)**

- Percentage of long-term artists still in top rotation
- High = stick to favorites
- Low = love discovering new artists

**Emotional Depth (0-100)**

- Measures emotional range and variety
- High = complex emotional engagement
- Low = lighter, more casual listening

**Energy Level (0-1)**

- 0 = Calm/Mellow (ambient, classical)
- 0.5 = Balanced
- 1 = Intense/Energetic (metal, EDM)

**Valence (0-1)**

- 0 = Sad/Melancholic
- 0.5 = Neutral
- 1 = Happy/Upbeat

## Troubleshooting

### "No data available"

- Check that JSON files exist in `./data/`
- Run `fetchSpotifyData.py` to get fresh data
- Ensure JSON files aren't empty

### "KeyError: 'popularity'"

- This is fixed in the latest version
- Re-run with: `python analyse.py`

### Unicode errors on Windows

```powershell
$env:PYTHONIOENCODING="utf-8"
python run_complete_analysis.py
```

### Missing visualizations

- Install optional dependencies:

```bash
pip install plotly wordcloud
```

- Analysis will still work without them

### Empty time periods

- Normal if you haven't listened much recently
- Analyzer automatically uses long-term data as fallback

## Next Steps

1. ✅ Run the analysis
2. 📊 Open the interactive charts in your browser
3. 📖 Read your personality report
4. 🔄 Re-run monthly to track changes
5. 🎯 Share results with friends!

## Tips

- **Track Changes**: Run the analysis monthly and compare results
- **Export Data**: JSON files can be imported into Excel/Tableau
- **Customize**: Edit `MOOD_MAPPING` in `mood_emotion_analysis.py` to adjust genre moods
- **Share**: Screenshots of HTML charts make great social media content

## Need Help?

- Check `ENHANCED_README.md` for detailed documentation
- See `IMPLEMENTATION_SUMMARY.md` for technical details
- Review error messages - they usually explain the issue

---

**Total Time: 5 minutes setup + 1 minute analysis = You're done!** 🎉

Enjoy exploring your music personality! 🎵
