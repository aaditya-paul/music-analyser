# 🎵 Enhanced Music Personality Analyzer

A comprehensive, data-driven music analysis tool that creates deep insights into your listening personality using advanced analytics, emotion detection, and interactive visualizations.

## ✨ Features

### 🧹 Advanced Data Processing

- **Unified Data Pipeline**: Normalizes and deduplicates tracks across all time periods
- **Smart Merging**: Combines track data with artist metadata for enriched analysis
- **Multi-Source Integration**: Aggregates data from top tracks, saved tracks, and recent plays

### 🎭 Emotional & Mood Analysis

- **Mood Inference**: Estimates energy, valence, and danceability from genre tags
- **Emotional Profiling**: Analyzes emotional depth and range across your library
- **Mood Mapping**: Classifies tracks into emotional quadrants (Happy/Sad × Calm/Energetic)

### 📊 Sophisticated Metrics

#### **Diversity Analysis**

- Shannon Entropy calculation for genre diversity
- Artist concentration and exploration metrics
- Popularity variance analysis

#### **Nostalgia & Loyalty**

- **Consistency Score**: How many long-term favorites remain in rotation
- **Return Rate**: Old favorites appearing in recent plays
- **Artist Loyalty**: Long-term artists still in your top rotation
- **Resurgence Detection**: Artists you rediscovered after a break

#### **Listener Classification**

Categorizes you into one of these types based on diversity metrics:

- 🌍 **MUSICAL EXPLORER** (75-100%): Extremely diverse taste
- 🎨 **ECLECTIC CURATOR** (60-75%): Well-balanced variety
- 🎯 **FOCUSED ENTHUSIAST** (40-60%): Clear preferences
- 💎 **NICHE SPECIALIST** (0-40%): Highly focused

### 📈 Interactive Visualizations

#### With Plotly (Optional):

- **Radar Chart**: 7-dimensional personality profile
- **Sunburst Chart**: Hierarchical genre distribution
- **Mood Scatter Plot**: Energy vs. Valence mapping
- **Popularity Timeline**: Track popularity across time periods
- **Top Artists Bar Chart**: Interactive horizontal bar chart

#### With Matplotlib:

- **Word Cloud**: Visual representation of most-played artists
- **Static Charts**: Fallback visualizations

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Install base requirements
pip install -r requirements.txt
```

### Optional: Enhanced Features

```bash
# Install for interactive visualizations and advanced analytics
pip install -r requirements_enhanced.txt
```

### Running the Analysis

#### Full Pipeline (Recommended):

```bash
python run_complete_analysis.py
```

This runs:

1. Data preparation & diversity analysis
2. Mood & emotion analysis
3. Interactive visualizations (if libraries installed)
4. Summary report generation

#### Individual Modules:

**Basic Analysis:**

```bash
python analyse.py
```

**Enhanced Data Analysis:**

```bash
python enhanced_analysis.py
```

**Mood & Emotion Analysis:**

```bash
python mood_emotion_analysis.py
```

**Visualizations Only:**

```bash
python enhanced_visualizations.py
```

## 📁 Output Files

### JSON Data Files:

- `enhanced_analysis_results.json` - Diversity and nostalgia metrics
- `emotional_analysis_results.json` - Emotional depth analysis
- `tracks_with_mood_features.json` - Enriched track data with mood features
- `music_personality_match.json` - Compatibility scoring data

### Visualizations:

- `radar_chart_interactive.html` - Interactive personality radar
- `genre_sunburst_interactive.html` - Genre distribution sunburst
- `mood_scatter_interactive.html` - Mood map scatter plot
- `popularity_timeline_interactive.html` - Popularity boxes over time
- `top_artists_interactive.html` - Top artists bar chart
- `artist_wordcloud.png` - Word cloud of artists
- `music_personality_graphs.png` - Comprehensive static charts

### Reports:

- `music_personality_report.txt` - Complete text summary

## 📊 What Gets Analyzed

### Input Data (from `data/` folder):

- `top_tracks.json` - Your top tracks (short/medium/long term)
- `top_artists.json` - Your top artists (short/medium/long term)
- `saved_tracks.json` - Your saved library
- `recently_played.json` - Recent listening history

### Metrics Calculated:

#### **Diversity Metrics**

- Genre Diversity Score (Shannon Entropy)
- Unique genres and artists count
- Artist concentration (top 10%)
- Popularity variance

#### **Nostalgia Metrics**

- Consistency Score (0-100%)
- Return Rate (0-100%)
- Artist Loyalty (0-100%)
- Resurgence Score

#### **Emotional Metrics**

- Emotional Range (0-100)
- Emotional Depth Score (0-100)
- Energy-Valence Correlation
- Emotion Distribution (Very Sad → Very Happy)

#### **Mood Features** (Inferred per track)

- Energy (0-1)
- Valence (0-1)
- Danceability (0-1)

## 🛠️ Architecture

```
music-analyser/
│
├── fetchSpotifyData.py          # Data fetching from Spotify API
├── analyse.py                   # Original analysis (with fixes)
│
├── enhanced_analysis.py         # ✨ Advanced data processing
│   ├── SpotifyDataLoader        # Unified data loading
│   ├── NostalgiaAnalyzer        # Nostalgia metrics
│   └── DiversityAnalyzer        # Diversity & classification
│
├── mood_emotion_analysis.py     # 🎭 Mood & emotion
│   ├── MoodAnalyzer             # Genre-based mood inference
│   └── EmotionalAnalyzer        # Emotional depth analysis
│
├── enhanced_visualizations.py   # 📊 Interactive charts
│   └── EnhancedVisualizer       # Plotly visualizations
│
└── run_complete_analysis.py     # 🚀 Master pipeline
```

## 🎯 Key Insights Provided

1. **Your Listener Type**: Musical Explorer, Eclectic Curator, Focused Enthusiast, or Niche Specialist
2. **Diversity Profile**: How varied your music taste is across genres and artists
3. **Loyalty Analysis**: How consistent you are with your favorite artists
4. **Emotional Profile**: Your preference for different emotional tones
5. **Mood Preferences**: Your energy and valence preferences
6. **Discovery Patterns**: How much you explore vs. stick to favorites

## 📖 Technical Details

### Algorithms Used:

1. **Shannon Entropy**: Measures genre and artist diversity

   ```
   H = -Σ(p_i * log2(p_i))
   ```

2. **Mood Inference**: Genre-to-mood mapping based on music theory

   - Maps 50+ genres to energy/valence/danceability scores
   - Averages across all genres for each track

3. **Emotional Depth**: Composite score from:

   - Emotional range (valence variance)
   - Presence of emotional genres
   - Artist emotional diversity

4. **Listener Classification**: Weighted scoring:
   - Genre diversity: 50%
   - Artist exploration: 50%

### Data Flow:

```
Raw JSON → Normalize → Deduplicate → Enrich → Analyze → Visualize
```

## 🔧 Customization

### Adjust Genre-to-Mood Mapping:

Edit `MOOD_MAPPING` dict in `mood_emotion_analysis.py`:

```python
MOOD_MAPPING = {
    'your-genre': {'energy': 0.8, 'valence': 0.7, 'danceability': 0.9},
    ...
}
```

### Change Classification Thresholds:

Modify ranges in `DiversityAnalyzer.classify_listener_type()`:

```python
if overall_diversity >= 75:  # Adjust threshold
    category = "MUSICAL EXPLORER"
```

### Add Custom Metrics:

Extend analyzer classes with your own calculations.

## 🐛 Troubleshooting

### "No data available" errors:

- Ensure JSON files are in `./data/` directory
- Run `fetchSpotifyData.py` first to fetch your data
- Check that JSON files contain the expected structure

### Empty time periods (short_term/medium_term):

- The analyzer automatically falls back to long_term data
- This is expected if you haven't listened to enough music recently

### Unicode errors on Windows:

- Set environment variable: `$env:PYTHONIOENCODING="utf-8"`
- Or run with: `python -X utf8 run_complete_analysis.py`

### Missing visualizations:

- Install optional dependencies: `pip install plotly wordcloud`
- The analysis will work without them, just skip visualizations

## 📝 Future Enhancements

### Planned (Not Yet Implemented):

- [ ] Sentence transformer embeddings for semantic similarity
- [ ] Genius API integration for lyrics analysis
- [ ] Sentiment analysis on lyrics (distilbert)
- [ ] KMeans clustering for genre patterns
- [ ] Recommendation system based on cosine similarity
- [ ] Streamlit dashboard for interactive exploration
- [ ] Integration with MusicBrainz/Last.fm APIs
- [ ] Release year analysis for temporal diversity

### Contribute:

Feel free to implement any of these features and submit a PR!

## 🙏 Credits

Built with:

- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **matplotlib** - Static visualizations
- **plotly** (optional) - Interactive charts
- **wordcloud** (optional) - Artist word clouds
- **spotipy** - Spotify API wrapper

## 📄 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Areas to improve:

1. More sophisticated mood inference
2. Better visualization layouts
3. Additional metrics and insights
4. Performance optimizations
5. Testing suite

---

**Made with ❤️ for music lovers who want to understand their listening habits**

🎵 Happy Analyzing! 🎵
