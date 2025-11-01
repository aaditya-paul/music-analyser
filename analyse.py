import json
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np


# ============================================================================
#  DATA LOADING FUNCTIONS
# ============================================================================

def load_spotify_data():
    """Load all Spotify data from JSON files."""
    print("=" * 80)
    print("LOADING DATA")
    print("=" * 80)
    
    with open('./data/top_tracks.json', 'r', encoding='utf-8') as f:
        top_tracks = json.load(f)
    with open('./data/top_artists.json', 'r', encoding='utf-8') as f:
        top_artists = json.load(f)
    with open('./data/saved_tracks.json', 'r', encoding='utf-8') as f:
        saved_tracks = json.load(f)
    with open('./data/recently_played.json', 'r', encoding='utf-8') as f:
        recently_played = json.load(f)
    
    print("✓ Successfully loaded all data files!")
    print()
    
    return top_tracks, top_artists, saved_tracks, recently_played


def create_dataframes(top_tracks, top_artists, saved_tracks, recently_played):
    """Convert loaded data into pandas DataFrames."""
    print("=" * 80)
    print("CREATING DATAFRAMES")
    print("=" * 80)
    
    # Top tracks for different time periods
    short_tracks = pd.DataFrame(top_tracks["data"]["short_term"])
    med_tracks = pd.DataFrame(top_tracks["data"]["medium_term"])
    long_tracks = pd.DataFrame(top_tracks["data"]["long_term"])
    
    # Top artists for different time periods
    short_artists = pd.DataFrame(top_artists["data"]["short_term"])
    med_artists = pd.DataFrame(top_artists["data"]["medium_term"])
    long_artists = pd.DataFrame(top_artists["data"]["long_term"])
    
    # Other data
    saved = pd.DataFrame(saved_tracks["items"])
    recent = pd.DataFrame(recently_played["items"])
    
    print(f"Short-term top tracks: {len(short_tracks)} tracks")
    print(f"Medium-term top tracks: {len(med_tracks)} tracks")
    print(f"Long-term top tracks: {len(long_tracks)} tracks")
    print(f"Saved tracks: {len(saved)} tracks")
    print(f"Recently played: {len(recent)} tracks")
    print()
    
    return short_tracks, med_tracks, long_tracks, short_artists, med_artists, long_artists, saved, recent


# ============================================================================
#  DATA INSPECTION AND ANALYSIS FUNCTIONS
# ============================================================================

def inspect_data(med_tracks, med_artists):
    """Display basic information about the data structure."""
    print("=" * 80)
    print("Inspecting Data")
    print("=" * 80)
    
    print("\n📊 MEDIUM-TERM TOP TRACKS - First 5 rows:")
    print(med_tracks.head())
    
    print("\n📋 Available columns in top tracks:")
    print(list(med_tracks.columns))
    
    print("\n🎤 MEDIUM-TERM TOP ARTISTS - First 5 rows:")
    print(med_artists.head())
    
    print("\n📋 Available columns in top artists:")
    print(list(med_artists.columns))
    print()


def analyze_statistics(med_tracks, med_artists):
    """Analyze and display statistical information about tracks and artists."""
    print("=" * 80)
    print("Analysis")
    print("=" * 80)
    
    # Check if we have data
    if len(med_tracks) == 0:
        print("\n⚠️  No medium-term track data available!")
        print("    Using long-term data as fallback if available.")
        return med_tracks
    
    print("\n📈 TRACK POPULARITY STATISTICS:")
    print(f"Average popularity (medium-term): {med_tracks['popularity'].mean():.2f}/100")
    print(f"Most popular track score: {med_tracks['popularity'].max()}/100")
    print(f"Least popular track score: {med_tracks['popularity'].min()}/100")
    
    if len(med_artists) > 0:
        print("\n📈 ARTIST POPULARITY STATISTICS:")
        print(f"Average artist popularity (medium-term): {med_artists['popularity'].mean():.2f}/100")
        print(f"Most popular artist score: {med_artists['popularity'].max()}/100")
    else:
        print("\n⚠️  No medium-term artist data available!")
    
    print("\n⏱️ TRACK DURATION STATISTICS:")
    med_tracks['duration_minutes'] = med_tracks['duration_ms'] / 60000
    print(f"Average track length: {med_tracks['duration_minutes'].mean():.2f} minutes")
    print(f"Longest track: {med_tracks['duration_minutes'].max():.2f} minutes")
    print(f"Shortest track: {med_tracks['duration_minutes'].min():.2f} minutes")
    print()
    
    return med_tracks  # Return with duration_minutes column added


def show_music_graphs(show, personality_scores, personality_vector, artist_counts, 
                      genre_counts, med_tracks, short_tracks, long_tracks):
    """
    Create comprehensive visualizations of music personality data.
    
    Args:
        show (bool): If True, displays the graphs. If False, saves them without showing.
        personality_scores (dict): Dictionary of personality scores
        personality_vector (list): 7-dim vector for radar chart
        artist_counts (pd.Series): Artist counts
        genre_counts (pd.Series): Genre counts
        med_tracks, short_tracks, long_tracks (pd.DataFrame): DataFrames for time periods
    """
    if not show:
        return
    
    print("\n" + "=" * 80)
    print("📊 GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    # Set style for better looking plots
    plt.style.use('seaborn-v0_8-darkgrid' if 'seaborn-v0_8-darkgrid' in plt.style.available else 'default')
    
    # Create a large figure with multiple subplots
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle('🎵 Your Music Personality Analysis 🎵', fontsize=20, fontweight='bold', y=0.995)
    
    # ===== GRAPH 1: Personality Radar Chart =====
    ax1 = plt.subplot(2, 3, 1, projection='polar')
    
    # Prepare data for radar chart
    categories = ['Mainstream', 'Diversity', 'Nostalgia', 'Energy', 'Emotional\nDepth', 'Cultural', 'Explorer']
    values = personality_vector + [personality_vector[0]]  # Complete the circle
    
    # Calculate angles for each axis
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    
    # Plot
    ax1.plot(angles, values, 'o-', linewidth=2, color='#1DB954', label='Your Profile')
    ax1.fill(angles, values, alpha=0.25, color='#1DB954')
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(categories, size=9)
    ax1.set_ylim(0, 100)
    ax1.set_title('Personality Profile Radar', fontsize=12, fontweight='bold', pad=20)
    ax1.grid(True)
    
    # ===== GRAPH 2: Top 10 Artists Bar Chart =====
    ax2 = plt.subplot(2, 3, 2)
    top_10_artists = artist_counts.head(10)
    colors = plt.cm.Greens(np.linspace(0.4, 0.9, len(top_10_artists)))
    bars = ax2.barh(range(len(top_10_artists)), top_10_artists.values, color=colors)
    ax2.set_yticks(range(len(top_10_artists)))
    ax2.set_yticklabels(top_10_artists.index, fontsize=9)
    ax2.set_xlabel('Number of Tracks', fontsize=10)
    ax2.set_title('🎤 Top 10 Most Listened Artists', fontsize=12, fontweight='bold')
    ax2.invert_yaxis()
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, top_10_artists.values)):
        ax2.text(value, i, f' {value}', va='center', fontsize=9)
    
    # ===== GRAPH 3: Top 10 Genres Pie Chart =====
    ax3 = plt.subplot(2, 3, 3)
    if len(genre_counts) > 0:
        top_genres = genre_counts.head(10)
        colors_pie = plt.cm.Spectral(np.linspace(0.2, 0.8, len(top_genres)))
        wedges, texts, autotexts = ax3.pie(top_genres.values, labels=top_genres.index, 
                                             autopct='%1.1f%%', startangle=90, colors=colors_pie)
        for text in texts:
            text.set_fontsize(8)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(8)
            autotext.set_fontweight('bold')
        ax3.set_title('🎸 Top 10 Genres Distribution', fontsize=12, fontweight='bold')
    else:
        ax3.text(0.5, 0.5, 'No genre data available', ha='center', va='center')
        ax3.set_title('🎸 Genre Distribution', fontsize=12, fontweight='bold')
    
    # ===== GRAPH 4: Personality Dimensions Bar Chart =====
    ax4 = plt.subplot(2, 3, 4)
    dimensions = list(personality_scores.keys())
    dimension_labels = ['Mainstream', 'Diversity', 'Nostalgia', 'Energy', 
                        'Emotional', 'Cultural', 'Explorer']
    values_list = list(personality_scores.values())
    
    # Color bars based on score (red to green gradient)
    colors_bars = ['#1DB954' if v >= 70 else '#FFA500' if v >= 40 else '#FF6B6B' for v in values_list]
    bars = ax4.bar(dimension_labels, values_list, color=colors_bars, alpha=0.8, edgecolor='black')
    ax4.set_ylabel('Score (0-100)', fontsize=10)
    ax4.set_title('🎭 Personality Dimension Scores', fontsize=12, fontweight='bold')
    ax4.set_ylim(0, 100)
    ax4.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='Average (50)')
    ax4.legend(fontsize=8)
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=9)
    
    # Add value labels on bars
    for bar, value in zip(bars, values_list):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{int(value)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # ===== GRAPH 5: Popularity Distribution =====
    ax5 = plt.subplot(2, 3, 5)
    ax5.hist(med_tracks['popularity'], bins=20, color='#1DB954', alpha=0.7, edgecolor='black')
    ax5.axvline(med_tracks['popularity'].mean(), color='red', linestyle='--', 
                linewidth=2, label=f"Average: {med_tracks['popularity'].mean():.1f}")
    ax5.set_xlabel('Popularity Score', fontsize=10)
    ax5.set_ylabel('Number of Tracks', fontsize=10)
    ax5.set_title('📊 Track Popularity Distribution', fontsize=12, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(axis='y', alpha=0.3)
    
    # ===== GRAPH 6: Time Period Comparison =====
    ax6 = plt.subplot(2, 3, 6)
    periods = ['Short\n(4 weeks)', 'Medium\n(6 months)', 'Long\n(Years)']
    track_counts = [len(short_tracks), len(med_tracks), len(long_tracks)]
    avg_popularities = [
        short_tracks['popularity'].mean() if len(short_tracks) > 0 and 'popularity' in short_tracks.columns else 0,
        med_tracks['popularity'].mean() if len(med_tracks) > 0 and 'popularity' in med_tracks.columns else 0,
        long_tracks['popularity'].mean() if len(long_tracks) > 0 and 'popularity' in long_tracks.columns else 0
    ]
    
    x = np.arange(len(periods))
    width = 0.35
    
    bars1 = ax6.bar(x - width/2, track_counts, width, label='Track Count', color='#1DB954', alpha=0.8)
    ax6_twin = ax6.twinx()
    bars2 = ax6_twin.bar(x + width/2, avg_popularities, width, label='Avg Popularity', 
                         color='#FF6B6B', alpha=0.8)
    
    ax6.set_xlabel('Time Period', fontsize=10)
    ax6.set_ylabel('Number of Tracks', fontsize=10, color='#1DB954')
    ax6_twin.set_ylabel('Average Popularity', fontsize=10, color='#FF6B6B')
    ax6.set_title('⏰ Listening Trends Over Time', fontsize=12, fontweight='bold')
    ax6.set_xticks(x)
    ax6.set_xticklabels(periods, fontsize=9)
    ax6.tick_params(axis='y', labelcolor='#1DB954')
    ax6_twin.tick_params(axis='y', labelcolor='#FF6B6B')
    
    # Add value labels
    for bar, value in zip(bars1, track_counts):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height + 100,
                f'{int(value)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    for bar, value in zip(bars2, avg_popularities):
        height = bar.get_height()
        ax6_twin.text(bar.get_x() + bar.get_width()/2., height + 1,
                     f'{value:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Combine legends
    lines1, labels1 = ax6.get_legend_handles_labels()
    lines2, labels2 = ax6_twin.get_legend_handles_labels()
    ax6.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=8)
    
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    
    # Save the figure
    plt.savefig('music_personality_graphs.png', dpi=300, bbox_inches='tight')
    print("\n✅ Graphs saved to: music_personality_graphs.png")
    
    # Show the plots if requested
    plt.show()
    print("✅ Graphs displayed!")


# ============================================================================
#  PERSONALITY CALCULATION FUNCTIONS
# ============================================================================

def calculate_personality_scores(med_tracks, artist_counts, genre_counts):
    """
    Calculate 7-dimensional personality scores based on listening habits.
    
    Args:
        med_tracks (pd.DataFrame): Medium-term tracks data
        artist_counts (pd.Series): Count of tracks per artist
        genre_counts (pd.Series): Count of artists per genre
    
    Returns:
        tuple: (personality_scores dict, avg_popularity float)
    """
    print("=" * 80)
    print("🎭 YOUR MUSIC PERSONALITY PROFILE")
    print("=" * 80)
    
    # Initialize personality scores (0-100)
    personality_scores = {
        'mainstream_factor': 0,      # How mainstream vs indie your taste is
        'diversity_factor': 0,        # How diverse your music taste is
        'nostalgia_factor': 0,        # How much you listen to older/classic music
        'energy_factor': 0,           # Inferred energy level
        'emotional_depth': 0,         # How emotional/melancholic your music is
        'cultural_rootedness': 0,     # Connection to cultural music (Bollywood, regional)
        'explorer_factor': 0          # How much you explore new/obscure music
    }

    # ===== FACTOR 1: MAINSTREAM vs INDIE =====
    avg_popularity = med_tracks['popularity'].mean()
    if avg_popularity >= 70:
        personality_scores['mainstream_factor'] = 85
    elif avg_popularity >= 60:
        personality_scores['mainstream_factor'] = 65
    elif avg_popularity >= 50:
        personality_scores['mainstream_factor'] = 50
    elif avg_popularity >= 40:
        personality_scores['mainstream_factor'] = 35
    else:
        personality_scores['mainstream_factor'] = 20

    # ===== FACTOR 2: DIVERSITY =====
    unique_genres = len(genre_counts) if len(genre_counts) > 0 else 0
    unique_artists_count = len(artist_counts)
    artist_concentration = artist_counts.head(10).sum() / len(med_tracks) if len(med_tracks) > 0 else 0

    diversity_score = (
        (min(unique_genres / 30, 1.0) * 40) +
        (min(unique_artists_count / 500, 1.0) * 30) +
        ((1 - artist_concentration) * 30)
    )
    personality_scores['diversity_factor'] = int(diversity_score)

    # ===== FACTOR 3: NOSTALGIA =====
    nostalgia_genres = ['classic bollywood', 'ghazal', 'qawwali', 'classic hindi pop', 
                        'hindi retro', 'old bollywood', 'golden age']
    nostalgia_artists = ['Kishore Kumar', 'Lata Mangeshkar', 'Mohammed Rafi', 
                         'R. D. Burman', 'Asha Bhosle', 'Mukesh']

    nostalgia_genre_count = sum(1 for g in genre_counts.index[:20] 
                                if any(ng in g.lower() for ng in nostalgia_genres))
    nostalgia_artist_count = sum(1 for a in artist_counts.index[:20] 
                                 if a in nostalgia_artists)

    nostalgia_score = (
        (nostalgia_genre_count / 5 * 50) +
        (nostalgia_artist_count / 6 * 50)
    )
    personality_scores['nostalgia_factor'] = int(min(nostalgia_score, 100))

    # ===== FACTOR 4: ENERGY =====
    upbeat_genres = ['pop', 'dance', 'edm', 'hip hop', 'party', 'punjabi']
    mellow_genres = ['indie', 'sad', 'slow', 'acoustic', 'chill', 'lo-fi', 'ambient']

    upbeat_count = sum(1 for g in genre_counts.index[:30] 
                       if any(ug in g.lower() for ug in upbeat_genres))
    mellow_count = sum(1 for g in genre_counts.index[:30] 
                       if any(mg in g.lower() for mg in mellow_genres))

    if upbeat_count + mellow_count > 0:
        energy_ratio = upbeat_count / (upbeat_count + mellow_count)
        personality_scores['energy_factor'] = int(energy_ratio * 100)
    else:
        personality_scores['energy_factor'] = 50

    # ===== FACTOR 5: EMOTIONAL DEPTH =====
    emotional_artists = ['Cigarettes After Sex', 'Arijit Singh', 'Atif Aslam']
    emotional_genres = ['sad', 'romantic', 'melancholic', 'sufi', 'ghazal', 'indie']

    emotional_artist_count = sum(1 for a in artist_counts.index[:30] 
                                 if any(ea in a for ea in emotional_artists))
    emotional_genre_count = sum(1 for g in genre_counts.index[:30] 
                                if any(eg in g.lower() for eg in emotional_genres))

    emotional_score = (
        (emotional_artist_count / 10 * 50) +
        (emotional_genre_count / 10 * 50)
    )
    personality_scores['emotional_depth'] = int(min(emotional_score, 100))

    # ===== FACTOR 6: CULTURAL ROOTEDNESS =====
    cultural_genres = ['bollywood', 'hindi', 'bangla', 'desi', 'indian', 'punjabi', 
                       'tamil', 'marathi', 'telugu']
    cultural_count = sum(1 for g in genre_counts.index if any(cg in g.lower() for cg in cultural_genres))
    total_genres = len(genre_counts) if len(genre_counts) > 0 else 1

    cultural_ratio = cultural_count / total_genres
    personality_scores['cultural_rootedness'] = int(cultural_ratio * 100)

    # ===== FACTOR 7: EXPLORER =====
    low_popularity_tracks = len(med_tracks[med_tracks['popularity'] < 30])
    obscure_ratio = low_popularity_tracks / len(med_tracks) if len(med_tracks) > 0 else 0
    artist_variety = min(unique_artists_count / 1000, 1.0)

    explorer_score = (
        (obscure_ratio * 60) +
        (artist_variety * 40)
    )
    personality_scores['explorer_factor'] = int(explorer_score)
    
    return personality_scores, avg_popularity


def display_personality_profile(personality_scores):
    """
    Display personality scores with visual bars and labels.
    
    Args:
        personality_scores (dict): Dictionary of personality dimension scores
    
    Returns:
        tuple: (personality_type, description, avg_score)
    """
    def get_bar(score, width=30):
        filled = int((score / 100) * width)
        return '█' * filled + '░' * (width - filled)

    def get_label(score, labels):
        if score >= 80:
            return labels[4]
        elif score >= 60:
            return labels[3]
        elif score >= 40:
            return labels[2]
        elif score >= 20:
            return labels[1]
        else:
            return labels[0]
    
    print("\n🎯 YOUR PERSONALITY SCORES (0-100 scale):\n")

    print(f"1️⃣  MAINSTREAM vs INDIE: {personality_scores['mainstream_factor']}/100")
    print(f"   {get_bar(personality_scores['mainstream_factor'])}")
    print(f"   → {get_label(personality_scores['mainstream_factor'], ['Underground Explorer', 'Indie Lover', 'Balanced', 'Chart Follower', 'Mainstream Enthusiast'])}\n")

    print(f"2️⃣  MUSIC DIVERSITY: {personality_scores['diversity_factor']}/100")
    print(f"   {get_bar(personality_scores['diversity_factor'])}")
    print(f"   → {get_label(personality_scores['diversity_factor'], ['Very Focused', 'Somewhat Focused', 'Balanced', 'Diverse Listener', 'Musical Omnivore'])}\n")

    print(f"3️⃣  NOSTALGIA LEVEL: {personality_scores['nostalgia_factor']}/100")
    print(f"   {get_bar(personality_scores['nostalgia_factor'])}")
    print(f"   → {get_label(personality_scores['nostalgia_factor'], ['Modern Only', 'Mostly Modern', 'Balanced', 'Classic Lover', 'Vintage Soul'])}\n")

    print(f"4️⃣  ENERGY LEVEL: {personality_scores['energy_factor']}/100")
    print(f"   {get_bar(personality_scores['energy_factor'])}")
    print(f"   → {get_label(personality_scores['energy_factor'], ['Very Mellow', 'Chill Vibes', 'Balanced', 'Upbeat', 'High Energy'])}\n")

    print(f"5️⃣  EMOTIONAL DEPTH: {personality_scores['emotional_depth']}/100")
    print(f"   {get_bar(personality_scores['emotional_depth'])}")
    print(f"   → {get_label(personality_scores['emotional_depth'], ['Light & Fun', 'Mostly Upbeat', 'Balanced', 'Emotionally Rich', 'Deep Feels'])}\n")

    print(f"6️⃣  CULTURAL ROOTEDNESS: {personality_scores['cultural_rootedness']}/100")
    print(f"   {get_bar(personality_scores['cultural_rootedness'])}")
    print(f"   → {get_label(personality_scores['cultural_rootedness'], ['Global Listener', 'Mixed Tastes', 'Balanced', 'Culture-Connected', 'Deeply Rooted'])}\n")

    print(f"7️⃣  EXPLORER MINDSET: {personality_scores['explorer_factor']}/100")
    print(f"   {get_bar(personality_scores['explorer_factor'])}")
    print(f"   → {get_label(personality_scores['explorer_factor'], ['Comfort Zone', 'Mostly Familiar', 'Balanced', 'Adventurous', 'Music Archaeologist'])}\n")

    # ===== DETERMINE PERSONALITY TYPE =====
    print("=" * 80)
    print("🎭 YOUR MUSIC PERSONALITY TYPE")
    print("=" * 80)

    avg_score = sum(personality_scores.values()) / len(personality_scores)

    if personality_scores['cultural_rootedness'] > 70 and personality_scores['nostalgia_factor'] > 60:
        personality_type = "🏛️ THE CULTURAL GUARDIAN"
        description = "You have deep roots in your cultural music heritage and appreciate the classics. You're keeping traditions alive while enjoying contemporary sounds."
    
    elif personality_scores['diversity_factor'] > 70 and personality_scores['explorer_factor'] > 60:
        personality_type = "🌍 THE MUSICAL NOMAD"
        description = "You're constantly exploring new sounds and artists across genres. Your curiosity drives your music taste, and you're not afraid to venture into the unknown."
    
    elif personality_scores['emotional_depth'] > 70:
        personality_type = "💔 THE EMOTIONAL WANDERER"
        description = "Music is your emotional outlet. You connect deeply with lyrics and melodies that reflect complex feelings. You're introspective and sentimental."
    
    elif personality_scores['mainstream_factor'] > 70 and personality_scores['energy_factor'] > 60:
        personality_type = "🎉 THE VIBE CURATOR"
        description = "You love what's trending and know how to set the mood. Your playlist is perfect for parties, and you're always up-to-date with the latest hits."
    
    elif personality_scores['nostalgia_factor'] > 70:
        personality_type = "⏰ THE TIME TRAVELER"
        description = "You find comfort in the golden oldies and timeless classics. Modern music is fine, but nothing beats the magic of the past for you."
    
    elif personality_scores['mainstream_factor'] < 40 and personality_scores['explorer_factor'] > 60:
        personality_type = "🔍 THE INDIE ARCHAEOLOGIST"
        description = "Mainstream is not your thing. You dig deep to find hidden gems and obscure artists that others haven't discovered yet. You're a true music connoisseur."
    
    elif personality_scores['diversity_factor'] > 70:
        personality_type = "🎨 THE ECLECTIC COLLECTOR"
        description = "Your music taste is wonderfully unpredictable. From Bollywood to indie rock, ghazals to pop - you appreciate good music regardless of genre boundaries."
    
    else:
        personality_type = "🎵 THE BALANCED LISTENER"
        description = "You have a well-rounded music taste that doesn't lean too heavily in any direction. You appreciate variety while maintaining your favorites."

    print(f"\n{personality_type}")
    print(f"\n{description}")
    print(f"\n📊 OVERALL SCORE: {int(avg_score)}/100")
    
    def get_bar_large(score, width=40):
        filled = int((score / 100) * width)
        return '█' * filled + '░' * (width - filled)
    
    print(f"   {get_bar_large(int(avg_score), 40)}")
    
    return personality_type, description, avg_score


# ============================================================================
#  MAIN ANALYSIS FUNCTION
# ============================================================================

def run_music_analysis(show_graphs=True):
    """
    Run the complete music personality analysis.
    
    Args:
        show_graphs (bool): If True, displays and saves graphs. If False, skips visualization.
    
    Returns:
        dict: Match data containing personality scores and metadata
    """
    # Load data
    top_tracks, top_artists, saved_tracks, recently_played = load_spotify_data()
    
    # Create dataframes
    short_tracks, med_tracks, long_tracks, short_artists, med_artists, long_artists, saved, recent = create_dataframes(
        top_tracks, top_artists, saved_tracks, recently_played
    )
    
    # Use fallback data if medium-term is empty
    if len(med_tracks) == 0 and len(long_tracks) > 0:
        print("\n⚠️  Medium-term data not available. Using long-term data as primary source.")
        med_tracks = long_tracks.copy()
        med_artists = long_artists.copy()
    elif len(med_tracks) == 0 and len(short_tracks) > 0:
        print("\n⚠️  Medium and long-term data not available. Using short-term data as primary source.")
        med_tracks = short_tracks.copy()
        med_artists = short_artists.copy()
    elif len(med_tracks) == 0:
        print("\n❌ ERROR: No track data available in any time period!")
        return None
    
    # Inspect data
    # inspect_data(med_tracks, med_artists)
    
    # Analyze statistics
    med_tracks = analyze_statistics(med_tracks, med_artists)
    
    print("=" * 80)
    print("YOUR TOP FAVORITES (Sorting and filtering)")
    print("=" * 80)

    print("\n🎵 YOUR TOP 10 MOST POPULAR TRACKS (Medium-term):")
    top_popular = med_tracks.sort_values('popularity', ascending=False).head(10)
    for idx, row in top_popular.iterrows():
        print(f"  {row['popularity']}/100 - {row['name']} by {', '.join(row['artists'])}")

    print("\n🎤 YOUR TOP 10 MOST POPULAR ARTISTS (Medium-term):")
    top_artists_popular = med_artists.sort_values('popularity', ascending=False).head(10)
    for idx, row in top_artists_popular.iterrows():
        print(f"  {row['popularity']}/100 - {row['name']} | Followers: {row['followers']:,}")

    print()



    print("=" * 80)
    print(" PATTERNS IN YOUR MUSIC (Grouping and counting)")
    print("=" * 80)

    # Count tracks per artist (medium-term)
    med_tracks_exploded = med_tracks.explode('artists')
    artist_counts = med_tracks_exploded['artists'].value_counts()

    print("\n🎤 ARTISTS YOU LISTEN TO MOST (by track count, medium-term):")
    for artist, count in artist_counts.head(15).items():
        print(f"  {artist}: {count} tracks")

    # Genre analysis
    print("\n🎸 YOUR TOP GENRES (Medium-term artists):")
    med_artists_exploded = med_artists.explode('genres')
    genre_counts = med_artists_exploded['genres'].value_counts()

    if len(genre_counts) > 0:
        for genre, count in genre_counts.head(15).items():
            print(f"  {genre}: {count} artists")
    else:
        print("  (Genre data not available)")

    print()


    print("=" * 80)
    print(" HOW YOUR TASTE CHANGES OVER TIME")
    print("=" * 80)

    print("\n⏰ TRACK COUNT BY TIME PERIOD:")
    print(f"  Short-term (last 4 weeks): {len(short_tracks)} tracks")
    print(f"  Medium-term (last 6 months): {len(med_tracks)} tracks")
    print(f"  Long-term (several years): {len(long_tracks)} tracks")

    print("\n📊 AVERAGE POPULARITY BY TIME PERIOD:")
    if len(short_tracks) > 0 and 'popularity' in short_tracks.columns:
        print(f"  Short-term: {short_tracks['popularity'].mean():.2f}/100")
    else:
        print(f"  Short-term: N/A (no data)")
    
    if len(med_tracks) > 0 and 'popularity' in med_tracks.columns:
        print(f"  Medium-term: {med_tracks['popularity'].mean():.2f}/100")
    else:
        print(f"  Medium-term: N/A (no data)")
    
    if len(long_tracks) > 0 and 'popularity' in long_tracks.columns:
        print(f"  Long-term: {long_tracks['popularity'].mean():.2f}/100")
    else:
        print(f"  Long-term: N/A (no data)")

    print()


    print("=" * 80)
    print(" YOUR RECENT LISTENING HABITS")
    print("=" * 80)

    if len(recent) > 0:
        print(f"\n🎧 Last {len(recent)} tracks you played:")
        for idx, row in recent.head(10).iterrows():
            print(f"  {row['track_name']} by {', '.join(row['artists'])}")
    else:
        print("\n⚠️  No recent listening history available.")

    print()


    print("=" * 80)
    print(" YOUR MUSIC LIBRARY")
    print("=" * 80)

    print(f"\n💾 You have {len(saved)} saved tracks in your library")

    # Most saved artists
    saved_exploded = saved.explode('artists')
    saved_artist_counts = saved_exploded['artists'].value_counts()

    print("\n🎤 MOST SAVED ARTISTS IN YOUR LIBRARY:")
    for artist, count in saved_artist_counts.head(10).items():
        print(f"  {artist}: {count} tracks saved")

    print()

    #  Insight

    print("=" * 80)
    print("🎯 KEY INSIGHTS ABOUT YOUR MUSIC TASTE")
    print("=" * 80)

    total_listening_minutes = med_tracks['duration_minutes'].sum()
    unique_artists = len(artist_counts)
    avg_track_popularity = med_tracks['popularity'].mean()

    print(f"""
    📊 SUMMARY:
      - You have {len(long_tracks):,} top tracks over all time
      - Your medium-term top tracks total {total_listening_minutes:.0f} minutes ({total_listening_minutes/60:.1f} hours)
      - You listen to {unique_artists} different artists regularly (medium-term)
      - Your average track popularity: {avg_track_popularity:.1f}/100
      - Your music library has {len(saved):,} saved tracks
      - You follow {len(med_artists)} artists currently
    """)

    if len(genre_counts) > 0:
        print(f"🎸 Your #1 genre: {genre_counts.index[0]}")
    print(f"🎤 Your #1 artist (by track count): {artist_counts.index[0]} ({artist_counts.iloc[0]} tracks)")

    # Calculate personality scores
    personality_scores, avg_popularity = calculate_personality_scores(
        med_tracks, artist_counts, genre_counts
    )
    
    # Display personality profile
    personality_type, description, avg_score = display_personality_profile(personality_scores)

    # ============================================================================
    #  MUSIC PERSONALITY MATCH SCORE (For future  Dating App ) (●'◡'●)
    # ============================================================================

    print("\n" + "=" * 80)
    print("💕 MUSIC PERSONALITY MATCH SCORE")
    print("=" * 80)

    # Create a comprehensive single score for matching
    # Each dimension contributes to different aspects of compatibility

    # Weighted scoring for dating app matching
    # Higher weight = more important for personality matching
    weights = {
        'diversity_factor': 0.20,      # Important: shows openness to new experiences
        'emotional_depth': 0.18,       # Important: emotional compatibility
        'explorer_factor': 0.15,       # Moderate: shows curiosity and adventure
        'energy_factor': 0.15,         # Moderate: lifestyle compatibility (party vs chill)
        'mainstream_factor': 0.12,     # Moderate: cultural alignment
        'cultural_rootedness': 0.12,   # Moderate: shared cultural values
        'nostalgia_factor': 0.08       # Lower: less critical for matching
    }

    # Calculate weighted personality score
    weighted_sum = sum(personality_scores[key] * weights[key] for key in weights)

    # Normalize to 0-100 scale
    music_personality_score = int(weighted_sum)

    # Create a unique personality fingerprint (for exact matching algorithm)
    # This encodes all 7 dimensions into a comparable format
    personality_vector = [
        personality_scores['mainstream_factor'],
        personality_scores['diversity_factor'],
        personality_scores['nostalgia_factor'],
        personality_scores['energy_factor'],
        personality_scores['emotional_depth'],
        personality_scores['cultural_rootedness'],
        personality_scores['explorer_factor']
    ]

    # Helper function for bar display
    def get_bar(score, width=50):
        filled = int((score / 100) * width)
        return '█' * filled + '░' * (width - filled)
    
    print(f"\n🎯 YOUR MUSIC PERSONALITY SCORE: {music_personality_score}/100")
    print(f"   {get_bar(music_personality_score, 50)}")

    print("\n📊 WHAT THIS SCORE MEANS:")
    if music_personality_score >= 70:
        compatibility_tier = "PREMIUM TIER"
        description = "Highly diverse, emotionally rich, and adventurous music taste. Great conversation starter!"
    elif music_personality_score >= 55:
        compatibility_tier = "HIGH COMPATIBILITY"
        description = "Well-rounded and balanced music personality. Easy to connect with diverse people."
    elif music_personality_score >= 40:
        compatibility_tier = "MODERATE COMPATIBILITY"
        description = "Defined preferences with room for exploration. Best matched with similar tastes."
    else:
        compatibility_tier = "NICHE PERSONALITY"
        description = "Specific and focused music taste. Best matched with highly compatible partners."

    print(f"   Tier: {compatibility_tier}")
    print(f"   {description}")

    # Generate personality vector string (for database storage)
    personality_fingerprint = ','.join(map(str, personality_vector))

    print(f"\n🔢 PERSONALITY VECTOR (for matching algorithm):")
    print(f"   [{personality_fingerprint}]")

    print("\n💡 HOW TO USE THIS FOR MATCHING:")
    print("""
       1. Store the 7-dimensional vector for each user
       2. Calculate Euclidean distance between user vectors:
          distance = sqrt(sum((user1[i] - user2[i])² for each dimension))
       3. Lower distance = better match!
       4. Perfect match = distance 0, Very different = distance ~100+
   
       Example match formula:
       match_score = 100 - min(distance, 100)
   
       Or use cosine similarity for direction-based matching:
       similarity = dot(vector1, vector2) / (|vector1| * |vector2|)
    """)

    # Save to JSON for easy integration
    match_data = {
        "music_personality_score": music_personality_score,
        "personality_type": personality_type.split(" ", 1)[1] if " " in personality_type else personality_type,
        "compatibility_tier": compatibility_tier,
        "vector": personality_vector,
        "dimensions": {
            "mainstream_vs_indie": personality_scores['mainstream_factor'],
            "diversity": personality_scores['diversity_factor'],
            "nostalgia": personality_scores['nostalgia_factor'],
            "energy": personality_scores['energy_factor'],
            "emotional_depth": personality_scores['emotional_depth'],
            "cultural_rootedness": personality_scores['cultural_rootedness'],
            "explorer": personality_scores['explorer_factor']
        },
        "top_genre": genre_counts.index[0] if len(genre_counts) > 0 else "unknown",
        "top_artist": artist_counts.index[0] if len(artist_counts) > 0 else "unknown",
        "avg_popularity": round(avg_popularity, 2),
        "total_artists": len(artist_counts)
    }

    with open("music_personality_match.json", "w", encoding="utf-8") as f:
        json.dump(match_data, f, ensure_ascii=False, indent=2)

    print("\n✅ Match data saved to: music_personality_match.json")


    # ============================================================================
    #  VISUALIZATION FUNCTION
    # ============================================================================


    # ===== VISUALIZATION =====
    show_music_graphs(show_graphs, personality_scores, personality_vector,
                     artist_counts, genre_counts, med_tracks, short_tracks, long_tracks)

    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    
    # Prepare comprehensive data summary for return
    analysis_summary = {
        "match_data": match_data,
        "statistics": {
            "total_listening_minutes": total_listening_minutes,
            "unique_artists": unique_artists,
            "avg_track_popularity": avg_track_popularity,
            "track_counts": {
                "short_term": len(short_tracks),
                "medium_term": len(med_tracks),
                "long_term": len(long_tracks)
            },
            "saved_tracks_count": len(saved),
            "followed_artists": len(med_artists)
        },
        "top_items": {
            "top_genre": genre_counts.index[0] if len(genre_counts) > 0 else "unknown",
            "top_artist": artist_counts.index[0] if len(artist_counts) > 0 else "unknown",
            "top_tracks": [
                {"name": row['name'], "artists": ', '.join(row['artists']), "popularity": int(row['popularity'])}
                for _, row in top_popular.head(5).iterrows()
            ],
            "top_artists": [
                {"name": row['name'], "popularity": int(row['popularity']), "followers": int(row['followers'])}
                for _, row in top_artists_popular.head(5).iterrows()
            ],
            "top_genres": [
                {"genre": genre, "count": int(count)}
                for genre, count in genre_counts.head(10).items()
            ]
        },
        "personality_profile": {
            "personality_type": personality_type,
            "personality_description": description,
            "scores": personality_scores,
            "overall_score": int(avg_score),
            "compatibility_tier": compatibility_tier
        }
    }
    
    return analysis_summary


# ============================================================================
#  STANDALONE EXECUTION
# ============================================================================

if __name__ == "__main__":
    run_music_analysis(show_graphs=True)
