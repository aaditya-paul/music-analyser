"""
Music Analysis Module
Listener profiling with diversity and nostalgia metrics
"""

import json
import pandas as pd
import numpy as np
import os
from collections import Counter, defaultdict
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'out'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================================
#  1. ENHANCED DATA PREPARATION
# ============================================================================

class SpotifyDataLoader:
    """Enhanced data loader with normalization and deduplication"""
    
    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir
        self.unified_tracks = None
        self.unified_artists = None
        
    def load_and_normalize(self):
        """Load all JSON files and create normalized, deduplicated datasets"""
        print("=" * 80)
        print("🔄 ENHANCED DATA LOADING")
        print("=" * 80)
        
        # Load raw data
        with open(f'{self.data_dir}/top_tracks.json', 'r', encoding='utf-8') as f:
            top_tracks_raw = json.load(f)
        with open(f'{self.data_dir}/top_artists.json', 'r', encoding='utf-8') as f:
            top_artists_raw = json.load(f)
        with open(f'{self.data_dir}/saved_tracks.json', 'r', encoding='utf-8') as f:
            saved_tracks_raw = json.load(f)
        with open(f'{self.data_dir}/recently_played.json', 'r', encoding='utf-8') as f:
            recently_played_raw = json.load(f)
            
        # Normalize tracks from all time periods
        all_tracks = []
        
        for period, period_name in [
            ('short_term', 'short'), 
            ('medium_term', 'medium'), 
            ('long_term', 'long')
        ]:
            tracks = top_tracks_raw['data'][period]
            for track in tracks:
                track['time_period'] = period_name
                track['source'] = 'top_tracks'
            all_tracks.extend(tracks)
        
        # Add saved tracks
        saved_items = saved_tracks_raw.get('items', [])
        for track in saved_items:
            track['time_period'] = 'saved'
            track['source'] = 'saved_tracks'
        all_tracks.extend(saved_items)
        
        # Add recently played
        recent_items = recently_played_raw.get('items', [])
        for track in recent_items:
            track['time_period'] = 'recent'
            track['source'] = 'recently_played'
        all_tracks.extend(recent_items)
        
        # Create normalized DataFrame
        if all_tracks:
            self.unified_tracks = pd.json_normalize(all_tracks)
            
            # Deduplicate by track ID while keeping time_period info
            # Keep the first occurrence and aggregate time_periods
            if 'id' in self.unified_tracks.columns:
                self.unified_tracks = self.unified_tracks.groupby('id', as_index=False).agg({
                    col: 'first' if col not in ['time_period', 'source'] else lambda x: '|'.join(set(x))
                    for col in self.unified_tracks.columns if col != 'id'
                })
            
            print(f"✓ Loaded {len(all_tracks)} tracks (before deduplication)")
            print(f"✓ Unified to {len(self.unified_tracks)} unique tracks")
        else:
            self.unified_tracks = pd.DataFrame()
            print("⚠️  No track data available")
        
        # Normalize artists from all time periods
        all_artists = []
        
        for period, period_name in [
            ('short_term', 'short'),
            ('medium_term', 'medium'),
            ('long_term', 'long')
        ]:
            artists = top_artists_raw['data'][period]
            for artist in artists:
                artist['time_period'] = period_name
            all_artists.extend(artists)
        
        if all_artists:
            self.unified_artists = pd.json_normalize(all_artists)
            
            # Deduplicate artists
            if 'id' in self.unified_artists.columns:
                self.unified_artists = self.unified_artists.groupby('id', as_index=False).agg({
                    col: 'first' if col not in ['time_period'] else lambda x: '|'.join(set(x))
                    for col in self.unified_artists.columns if col != 'id'
                })
            
            print(f"✓ Loaded {len(all_artists)} artists (before deduplication)")
            print(f"✓ Unified to {len(self.unified_artists)} unique artists")
        else:
            self.unified_artists = pd.DataFrame()
            print("⚠️  No artist data available")
        
        print()
        return self.unified_tracks, self.unified_artists
    
    def merge_track_artist_data(self):
        """Merge track data with artist metadata"""
        if self.unified_tracks is None or self.unified_artists is None:
            return None
        
        print("🔗 MERGING TRACK-ARTIST DATA")
        
        # Explode artists array in tracks
        if 'artists' in self.unified_tracks.columns:
            tracks_exploded = self.unified_tracks.copy()
            
            # Create artist-track mapping
            enriched_tracks = []
            
            for idx, track_row in tracks_exploded.iterrows():
                track_dict = track_row.to_dict()
                
                # Get artist names from track
                if isinstance(track_dict.get('artists'), list):
                    artist_names = track_dict['artists']
                    
                    # Find matching artists in artist dataset
                    matching_artists = []
                    for artist_name in artist_names:
                        artist_match = self.unified_artists[
                            self.unified_artists['name'] == artist_name
                        ]
                        if not artist_match.empty:
                            matching_artists.append(artist_match.iloc[0].to_dict())
                    
                    # Aggregate artist info
                    if matching_artists:
                        track_dict['artist_genres'] = list(set([
                            genre for artist in matching_artists 
                            for genre in artist.get('genres', [])
                        ]))
                        track_dict['artist_avg_popularity'] = np.mean([
                            artist.get('popularity', 0) for artist in matching_artists
                        ])
                        track_dict['artist_total_followers'] = sum([
                            artist.get('followers', 0) for artist in matching_artists
                        ])
                
                enriched_tracks.append(track_dict)
            
            enriched_df = pd.DataFrame(enriched_tracks)
            print(f"✓ Enriched {len(enriched_df)} tracks with artist metadata")
            print()
            
            return enriched_df
        
        return self.unified_tracks


# ============================================================================
#  2. ADVANCED NOSTALGIA METRICS
# ============================================================================

class NostalgiaAnalyzer:
    """Calculate sophisticated nostalgia and loyalty metrics"""
    
    def __init__(self, unified_tracks, unified_artists):
        self.tracks = unified_tracks
        self.artists = unified_artists
    
    def calculate_nostalgia_metrics(self):
        """Comprehensive nostalgia analysis"""
        print("=" * 80)
        print("🕰️  ADVANCED NOSTALGIA ANALYSIS")
        print("=" * 80)
        
        metrics = {}
        
        # 1. Track overlap analysis
        if 'time_period' in self.tracks.columns:
            long_term_tracks = set(
                self.tracks[self.tracks['time_period'].str.contains('long', na=False)]['id']
            )
            short_term_tracks = set(
                self.tracks[self.tracks['time_period'].str.contains('short', na=False)]['id']
            )
            recent_tracks = set(
                self.tracks[self.tracks['time_period'].str.contains('recent', na=False)]['id']
            )
            
            # Consistency score: how many long-term favorites appear in short-term
            if long_term_tracks and short_term_tracks:
                overlap = long_term_tracks & short_term_tracks
                metrics['consistency_score'] = len(overlap) / len(long_term_tracks) * 100
            else:
                metrics['consistency_score'] = 0
            
            # Return rate: old favorites in recent plays
            if long_term_tracks and recent_tracks:
                returning = long_term_tracks & recent_tracks
                metrics['return_rate'] = len(returning) / len(long_term_tracks) * 100
            else:
                metrics['return_rate'] = 0
            
            print(f"📊 Track Consistency: {metrics['consistency_score']:.1f}%")
            print(f"   (Long-term favorites still in short-term rotation)")
            print(f"📊 Return Rate: {metrics['return_rate']:.1f}%")
            print(f"   (Old favorites appearing in recent plays)")
        
        # 2. Artist loyalty analysis
        if 'time_period' in self.artists.columns and 'name' in self.artists.columns:
            long_artists = set(
                self.artists[self.artists['time_period'].str.contains('long', na=False)]['name']
            )
            short_artists = set(
                self.artists[self.artists['time_period'].str.contains('short', na=False)]['name']
            )
            
            if long_artists and short_artists:
                loyal_artists = long_artists & short_artists
                metrics['artist_loyalty'] = len(loyal_artists) / len(long_artists) * 100
                metrics['loyal_artist_list'] = list(loyal_artists)[:10]
            else:
                metrics['artist_loyalty'] = 0
                metrics['loyal_artist_list'] = []
            
            print(f"📊 Artist Loyalty: {metrics['artist_loyalty']:.1f}%")
            print(f"   (Long-term artists still in rotation)")
            
            if metrics['loyal_artist_list']:
                print(f"\n🎤 Your Most Loyal Artists:")
                for artist in metrics['loyal_artist_list']:
                    print(f"   • {artist}")
        
        # 3. Resurgence detection
        # Artists who were in long-term but NOT in medium, but ARE in short
        if 'time_period' in self.artists.columns:
            medium_artists = set(
                self.artists[self.artists['time_period'].str.contains('medium', na=False)]['name']
            )
            
            if long_artists and medium_artists and short_artists:
                # Stopped listening: in long but not medium
                stopped = long_artists - medium_artists
                # Returned: stopped + now in short
                resurgent = stopped & short_artists
                
                metrics['resurgence_score'] = len(resurgent)
                metrics['resurgent_artists'] = list(resurgent)
                
                print(f"\n📊 Resurgence Score: {metrics['resurgence_score']} artists")
                print(f"   (Artists you rediscovered after a break)")
                
                if metrics['resurgent_artists']:
                    print(f"   Artists: {', '.join(metrics['resurgent_artists'][:5])}")
        
        print()
        return metrics


# ============================================================================
#  3. GENRE DIVERSITY & BALANCED LISTENER ANALYSIS
# ============================================================================

class DiversityAnalyzer:
    """Analyze music diversity using Shannon entropy and clustering"""
    
    def __init__(self, enriched_tracks):
        self.tracks = enriched_tracks
    
    def calculate_shannon_entropy(self, genre_counts):
        """Calculate Shannon entropy for genre diversity"""
        total = sum(genre_counts.values())
        if total == 0:
            return 0
        
        entropy = 0
        for count in genre_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * np.log2(p)
        
        return entropy
    
    def analyze_diversity(self):
        """Comprehensive diversity analysis"""
        print("=" * 80)
        print("🎨 DIVERSITY ANALYSIS")
        print("=" * 80)
        
        metrics = {}
        
        # 1. Genre diversity (Shannon entropy)
        if 'artist_genres' in self.tracks.columns:
            all_genres = []
            for genres in self.tracks['artist_genres'].dropna():
                if isinstance(genres, list):
                    all_genres.extend(genres)
            
            genre_counts = Counter(all_genres)
            metrics['genre_entropy'] = self.calculate_shannon_entropy(genre_counts)
            metrics['unique_genres'] = len(genre_counts)
            
            # Normalize entropy (max entropy = log2(n))
            max_entropy = np.log2(len(genre_counts)) if len(genre_counts) > 1 else 1
            metrics['genre_diversity_score'] = (
                metrics['genre_entropy'] / max_entropy * 100 if max_entropy > 0 else 0
            )
            
            print(f"📊 Genre Diversity Score: {metrics['genre_diversity_score']:.1f}/100")
            print(f"   (Based on Shannon Entropy)")
            print(f"   • Unique genres: {metrics['unique_genres']}")
            print(f"   • Entropy: {metrics['genre_entropy']:.2f} bits")
        
        # 2. Release year variance (if available)
        # This would require additional data from Spotify API
        # For now, we'll use a placeholder
        metrics['temporal_diversity'] = 50  # Placeholder
        
        # 3. Artist diversity
        if 'artists' in self.tracks.columns:
            all_artists = []
            for artists in self.tracks['artists'].dropna():
                if isinstance(artists, list):
                    all_artists.extend(artists)
            
            artist_counts = Counter(all_artists)
            metrics['artist_entropy'] = self.calculate_shannon_entropy(artist_counts)
            metrics['unique_artists'] = len(artist_counts)
            
            # Calculate concentration (top 10 artists)
            top_10_count = sum([count for _, count in artist_counts.most_common(10)])
            total_count = sum(artist_counts.values())
            metrics['artist_concentration'] = (
                top_10_count / total_count * 100 if total_count > 0 else 0
            )
            
            print(f"\n📊 Artist Diversity:")
            print(f"   • Unique artists: {metrics['unique_artists']}")
            print(f"   • Top 10 concentration: {metrics['artist_concentration']:.1f}%")
        
        # 4. Popularity diversity
        if 'popularity' in self.tracks.columns:
            pop_scores = self.tracks['popularity'].dropna()
            if len(pop_scores) > 0:
                metrics['popularity_std'] = pop_scores.std()
                metrics['popularity_range'] = pop_scores.max() - pop_scores.min()
                
                print(f"\n📊 Popularity Diversity:")
                print(f"   • Standard deviation: {metrics['popularity_std']:.1f}")
                print(f"   • Range: {metrics['popularity_range']:.0f} points")
        
        print()
        return metrics
    
    def classify_listener_type(self, diversity_metrics):
        """Classify listener based on diversity metrics"""
        print("=" * 80)
        print("🏷️  LISTENER CLASSIFICATION")
        print("=" * 80)
        
        # Score components
        genre_score = diversity_metrics.get('genre_diversity_score', 50)
        concentration = diversity_metrics.get('artist_concentration', 50)
        
        # Invert concentration (lower is better for diversity)
        artist_diversity_score = 100 - concentration
        
        # Weighted average
        overall_diversity = (genre_score * 0.5 + artist_diversity_score * 0.5)
        
        # Classification
        if overall_diversity >= 75:
            category = "🌍 MUSICAL EXPLORER"
            description = "Extremely diverse taste spanning many genres and artists. You're always discovering new sounds."
        elif overall_diversity >= 60:
            category = "🎨 ECLECTIC CURATOR"
            description = "Well-balanced taste with good variety. You enjoy exploring but have favorites."
        elif overall_diversity >= 40:
            category = "🎯 FOCUSED ENTHUSIAST"
            description = "Clear preferences with moderate exploration. You know what you like."
        else:
            category = "💎 NICHE SPECIALIST"
            description = "Highly focused on specific genres/artists. Deep expertise in your domain."
        
        print(f"{category}")
        print(f"Overall Diversity: {overall_diversity:.1f}/100")
        print(f"\n{description}")
        print()
        
        return {
            'category': category,
            'overall_diversity': overall_diversity,
            'description': description
        }


# ============================================================================
#  4. MAIN ENHANCED ANALYSIS RUNNER
# ============================================================================

def run_analysis():
    """Run comprehensive analysis"""
    
    # Load and prepare data
    loader = SpotifyDataLoader()
    unified_tracks, unified_artists = loader.load_and_normalize()
    
    if unified_tracks is None or len(unified_tracks) == 0:
        print("❌ No data available")
        return None
    
    # Merge and enrich
    enriched_tracks = loader.merge_track_artist_data()
    
    # Nostalgia analysis
    nostalgia_analyzer = NostalgiaAnalyzer(unified_tracks, unified_artists)
    nostalgia_metrics = nostalgia_analyzer.calculate_nostalgia_metrics()
    
    # Diversity analysis
    diversity_analyzer = DiversityAnalyzer(enriched_tracks)
    diversity_metrics = diversity_analyzer.analyze_diversity()
    
    # Step 5: Listener classification
    listener_type = diversity_analyzer.classify_listener_type(diversity_metrics)
    
    # Compile results
    results = {
        'nostalgia_metrics': nostalgia_metrics,
        'diversity_metrics': diversity_metrics,
        'listener_classification': listener_type,
        'data_summary': {
            'total_unique_tracks': len(unified_tracks),
            'total_unique_artists': len(unified_artists),
            'enriched_tracks': len(enriched_tracks)
        }
    }
    
    # Save results
    output_path = os.path.join(OUTPUT_DIR, 'analysis_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"📄 Results: {output_path}")
    print()
    
    return results


if __name__ == "__main__":
    run_analysis()
