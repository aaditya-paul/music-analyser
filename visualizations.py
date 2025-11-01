"""
Interactive Visualizations
Charts using Plotly and matplotlib
"""

import json
import pandas as pd
import numpy as np
import os
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'out'
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("⚠️  Plotly not installed. Install with: pip install plotly")

try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    print("⚠️  WordCloud not installed. Install with: pip install wordcloud")


# ============================================================================
#  ENHANCED VISUALIZATIONS
# ============================================================================

class Visualizer:
    """Create interactive visualizations with Plotly"""
    
    def __init__(self, tracks_with_mood, diversity_metrics, nostalgia_metrics, emotional_metrics):
        self.tracks = tracks_with_mood
        self.diversity = diversity_metrics
        self.nostalgia = nostalgia_metrics
        self.emotional = emotional_metrics
    
    def create_radar_chart(self):
        """Create an interactive radar chart for listener profile"""
        if not PLOTLY_AVAILABLE:
            return None
        
        print("📊 Creating enhanced radar chart...")
        
        # Prepare data
        categories = [
            'Genre Diversity',
            'Artist Exploration',
            'Emotional Range',
            'Energy Level',
            'Danceability',
            'Artist Loyalty',
            'Consistency'
        ]
        
        values = [
            self.diversity.get('genre_diversity_score', 50),
            100 - self.diversity.get('artist_concentration', 50),
            min(self.emotional.get('emotional_range', 0) * 2, 100),
            self.tracks['inferred_energy'].mean() * 100 if 'inferred_energy' in self.tracks.columns else 50,
            self.tracks['inferred_danceability'].mean() * 100 if 'inferred_danceability' in self.tracks.columns else 50,
            self.nostalgia.get('artist_loyalty', 50),
            self.nostalgia.get('consistency_score', 50)
        ]
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the polygon
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(29, 185, 84, 0.3)',
            line=dict(color='rgb(29, 185, 84)', width=2),
            name='Your Profile'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    tickfont=dict(size=10)
                ),
                angularaxis=dict(
                    tickfont=dict(size=11)
                )
            ),
            showlegend=False,
            title=dict(
                text="🎵 Your Music Personality Radar",
                font=dict(size=20, color='#1DB954'),
                x=0.5,
                xanchor='center'
            ),
            height=600,
            template='plotly_dark'
        )
        
        fig.write_html(os.path.join(OUTPUT_DIR, 'radar_chart.html'))
        print("✓ Saved: radar_chart.html")
        
        return fig
    
    def create_genre_sunburst(self):
        """Create a sunburst chart for genre distribution"""
        if not PLOTLY_AVAILABLE:
            return None
        
        print("📊 Creating genre sunburst chart...")
        
        if 'artist_genres' not in self.tracks.columns:
            print("⚠️  No genre data available")
            return None
        
        # Collect all genres
        all_genres = []
        for genres in self.tracks['artist_genres'].dropna():
            if isinstance(genres, list):
                all_genres.extend(genres)
        
        genre_counts = Counter(all_genres)
        top_genres = dict(genre_counts.most_common(30))
        
        # Prepare data for sunburst
        labels = ['Music'] + list(top_genres.keys())
        parents = [''] + ['Music'] * len(top_genres)
        values = [sum(top_genres.values())] + list(top_genres.values())
        
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            marker=dict(
                colorscale='Viridis',
                cmid=np.mean(values)
            ),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br><extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text="🎸 Your Genre Universe",
                font=dict(size=20, color='#1DB954'),
                x=0.5,
                xanchor='center'
            ),
            height=700,
            template='plotly_dark'
        )
        
        fig.write_html(os.path.join(OUTPUT_DIR, 'genre_sunburst.html'))
        print("✓ Saved: genre_sunburst.html")
        
        return fig
    
    def create_mood_scatter(self):
        """Create an energy vs valence scatter plot"""
        if not PLOTLY_AVAILABLE:
            return None
        
        print("📊 Creating mood scatter plot...")
        
        if 'inferred_energy' not in self.tracks.columns or 'inferred_valence' not in self.tracks.columns:
            print("⚠️  No mood data available")
            return None
        
        # Prepare data
        df_plot = self.tracks[['name', 'artists', 'inferred_energy', 'inferred_valence', 'popularity']].copy()
        df_plot = df_plot.dropna()
        
        # Convert artists list to string
        df_plot['artist_str'] = df_plot['artists'].apply(
            lambda x: ', '.join(x[:2]) if isinstance(x, list) else str(x)
        )
        
        # Create quadrant labels
        def get_quadrant(row):
            energy = row['inferred_energy']
            valence = row['inferred_valence']
            
            if energy >= 0.5 and valence >= 0.5:
                return '🎉 Energetic & Happy'
            elif energy >= 0.5 and valence < 0.5:
                return '⚡ Energetic & Melancholic'
            elif energy < 0.5 and valence >= 0.5:
                return '☀️ Calm & Happy'
            else:
                return '🌙 Calm & Sad'
        
        df_plot['mood_quadrant'] = df_plot.apply(get_quadrant, axis=1)
        
        # Create scatter plot
        fig = px.scatter(
            df_plot,
            x='inferred_valence',
            y='inferred_energy',
            color='mood_quadrant',
            size='popularity',
            hover_data=['name', 'artist_str'],
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={
                'inferred_valence': 'Emotional Tone (Sad → Happy)',
                'inferred_energy': 'Energy Level (Calm → Intense)'
            }
        )
        
        fig.update_traces(marker=dict(opacity=0.6, line=dict(width=0.5, color='white')))
        
        fig.update_layout(
            title=dict(
                text="🎭 Your Music Mood Map",
                font=dict(size=20, color='#1DB954'),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(range=[0, 1], gridcolor='rgba(128,128,128,0.2)'),
            yaxis=dict(range=[0, 1], gridcolor='rgba(128,128,128,0.2)'),
            height=700,
            template='plotly_dark',
            legend=dict(
                title='Mood Category',
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        
        # Add quadrant lines
        fig.add_hline(y=0.5, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_vline(x=0.5, line_dash="dash", line_color="gray", opacity=0.5)
        
        fig.write_html(os.path.join(OUTPUT_DIR, 'mood_scatter.html'))
        print("✓ Saved: mood_scatter.html")
        
        return fig
    
    def create_artist_wordcloud(self):
        """Create a word cloud of most listened artists"""
        if not WORDCLOUD_AVAILABLE:
            return None
        
        print("📊 Creating artist word cloud...")
        
        if 'artists' not in self.tracks.columns:
            print("⚠️  No artist data available")
            return None
        
        # Count artists
        all_artists = []
        for artists in self.tracks['artists'].dropna():
            if isinstance(artists, list):
                all_artists.extend(artists)
        
        artist_counts = Counter(all_artists)
        
        # Create word cloud
        wordcloud = WordCloud(
            width=1200,
            height=600,
            background_color='#191414',  # Spotify dark
            colormap='Greens',
            relative_scaling=0.5,
            min_font_size=10
        ).generate_from_frequencies(artist_counts)
        
        # Plot
        plt.figure(figsize=(15, 7))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('🎤 Your Artist Universe', fontsize=24, color='#1DB954', pad=20)
        plt.tight_layout(pad=0)
        plt.savefig(os.path.join(OUTPUT_DIR, 'artist_wordcloud.png'), dpi=300, bbox_inches='tight', facecolor='#191414')
        plt.close()
        
        print("✓ Saved to: artist_wordcloud.png")
    
    def create_popularity_timeline(self):
        """Create a timeline showing popularity distribution over time periods"""
        if not PLOTLY_AVAILABLE:
            return None
        
        print("📊 Creating popularity timeline...")
        
        if 'time_period' not in self.tracks.columns or 'popularity' not in self.tracks.columns:
            print("⚠️  No time period or popularity data available")
            return None
        
        # Prepare data by time period
        time_periods = ['short', 'medium', 'long']
        period_names = ['Short-term\n(4 weeks)', 'Medium-term\n(6 months)', 'Long-term\n(All time)']
        
        fig = go.Figure()
        
        for period, period_name in zip(time_periods, period_names):
            period_tracks = self.tracks[self.tracks['time_period'].str.contains(period, na=False)]
            
            if len(period_tracks) > 0:
                popularity_vals = period_tracks['popularity'].dropna()
                
                fig.add_trace(go.Box(
                    y=popularity_vals,
                    name=period_name,
                    marker_color='rgb(29, 185, 84)',
                    boxmean='sd'
                ))
        
        fig.update_layout(
            title=dict(
                text="📈 Popularity Distribution Across Time Periods",
                font=dict(size=20, color='#1DB954'),
                x=0.5,
                xanchor='center'
            ),
            yaxis_title="Popularity Score (0-100)",
            xaxis_title="Time Period",
            height=600,
            template='plotly_dark',
            showlegend=False
        )
        
        fig.write_html(os.path.join(OUTPUT_DIR, 'popularity_timeline.html'))
        print("✓ Saved: popularity_timeline.html")
        
        return fig
    
    def create_top_artists_bar(self):
        """Create an interactive bar chart of top artists"""
        if not PLOTLY_AVAILABLE:
            return None
        
        print("📊 Creating top artists bar chart...")
        
        if 'artists' not in self.tracks.columns:
            print("⚠️  No artist data available")
            return None
        
        # Count artists
        all_artists = []
        for artists in self.tracks['artists'].dropna():
            if isinstance(artists, list):
                all_artists.extend(artists)
        
        artist_counts = Counter(all_artists).most_common(20)
        
        artists = [a[0] for a in artist_counts]
        counts = [a[1] for a in artist_counts]
        
        fig = go.Figure(data=[
            go.Bar(
                x=counts,
                y=artists,
                orientation='h',
                marker=dict(
                    color=counts,
                    colorscale='Greens',
                    showscale=False
                ),
                text=counts,
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Tracks: %{x}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=dict(
                text="🎤 Your Top 20 Artists",
                font=dict(size=20, color='#1DB954'),
                x=0.5,
                xanchor='center'
            ),
            xaxis_title="Number of Tracks",
            yaxis=dict(autorange='reversed'),
            height=800,
            template='plotly_dark',
            showlegend=False
        )
        
        fig.write_html(os.path.join(OUTPUT_DIR, 'top_artists.html'))
        print("✓ Saved: top_artists.html")
        
        return fig
    
    def generate_all_visualizations(self):
        """Generate all visualizations"""
        print("\n" + "=" * 80)
        print("🎨 GENERATING VISUALIZATIONS")
        print("=" * 80 + "\n")
        
        results = {}
        
        results['radar'] = self.create_radar_chart()
        results['sunburst'] = self.create_genre_sunburst()
        results['mood_scatter'] = self.create_mood_scatter()
        results['wordcloud'] = self.create_artist_wordcloud()
        results['popularity'] = self.create_popularity_timeline()
        results['top_artists'] = self.create_top_artists_bar()
        
        print("\n" + "=" * 80)
        print("✅ VISUALIZATIONS COMPLETE!")
        print("=" * 80)
        print("\n📂 Open HTML files in browser!")
        print("📂 View PNG files!\n")
        
        return results


# ============================================================================
#  MAIN EXECUTION
# ============================================================================

def create_visualizations():
    """Load data and create visualizations"""
    
    print("Loading results...")
    
    try:
        tracks_with_mood = pd.read_json(os.path.join(OUTPUT_DIR, 'tracks_with_mood.json'))
    except Exception as e:
        print(f"❌ Error loading tracks: {e}")
        return
    
    try:
        with open(os.path.join(OUTPUT_DIR, 'analysis_results.json'), 'r', encoding='utf-8') as f:
            enhanced_results = json.load(f)
        diversity_metrics = enhanced_results['diversity_metrics']
        nostalgia_metrics = enhanced_results['nostalgia_metrics']
    except Exception as e:
        print(f"❌ Error loading analysis: {e}")
        return None
    
    try:
        with open(os.path.join(OUTPUT_DIR, 'emotional_results.json'), 'r', encoding='utf-8') as f:
            emotional_results = json.load(f)
    except Exception as e:
        print(f"❌ Error loading emotions: {e}")
        return None
    
    print("✓ Data loaded!\n")
    
    # Create visualizations
    visualizer = Visualizer(
        tracks_with_mood,
        diversity_metrics,
        nostalgia_metrics,
        emotional_results
    )
    
    visualizer.generate_all_visualizations()


if __name__ == "__main__":
    create_visualizations()
