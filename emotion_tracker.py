"""
Mood & Emotion Analysis
Genre-based mood inference and emotional profiling
"""

import json
import pandas as pd
import numpy as np
import os
from collections import Counter, defaultdict
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = 'out'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================================
#  MOOD INFERENCE FROM GENRES & POPULARITY
# ============================================================================

class MoodAnalyzer:
    """Infer mood and energy from available metadata"""
    
    # Genre-based mood mapping
    MOOD_MAPPING = {
        # High energy genres
        'edm': {'energy': 0.9, 'valence': 0.7, 'danceability': 0.9},
        'dance': {'energy': 0.9, 'valence': 0.8, 'danceability': 0.9},
        'hip hop': {'energy': 0.8, 'valence': 0.6, 'danceability': 0.8},
        'punk': {'energy': 0.95, 'valence': 0.5, 'danceability': 0.7},
        'metal': {'energy': 0.95, 'valence': 0.4, 'danceability': 0.6},
        'pop': {'energy': 0.75, 'valence': 0.75, 'danceability': 0.8},
        'rock': {'energy': 0.8, 'valence': 0.5, 'danceability': 0.6},
        
        # Medium energy
        'indie': {'energy': 0.6, 'valence': 0.5, 'danceability': 0.5},
        'alternative': {'energy': 0.65, 'valence': 0.5, 'danceability': 0.55},
        'folk': {'energy': 0.5, 'valence': 0.6, 'danceability': 0.4},
        'country': {'energy': 0.6, 'valence': 0.65, 'danceability': 0.5},
        'blues': {'energy': 0.5, 'valence': 0.4, 'danceability': 0.5},
        'jazz': {'energy': 0.55, 'valence': 0.55, 'danceability': 0.6},
        
        # Low energy / emotional
        'ambient': {'energy': 0.2, 'valence': 0.5, 'danceability': 0.2},
        'classical': {'energy': 0.4, 'valence': 0.6, 'danceability': 0.3},
        'acoustic': {'energy': 0.4, 'valence': 0.55, 'danceability': 0.3},
        'sad': {'energy': 0.3, 'valence': 0.2, 'danceability': 0.3},
        'sleep': {'energy': 0.2, 'valence': 0.5, 'danceability': 0.2},
        'chill': {'energy': 0.35, 'valence': 0.6, 'danceability': 0.4},
        'lo-fi': {'energy': 0.3, 'valence': 0.6, 'danceability': 0.4},
        
        # Cultural/Regional
        'bollywood': {'energy': 0.75, 'valence': 0.7, 'danceability': 0.75},
        'bhajan': {'energy': 0.5, 'valence': 0.7, 'danceability': 0.4},
        'sufi': {'energy': 0.55, 'valence': 0.65, 'danceability': 0.5},
        'devotional': {'energy': 0.5, 'valence': 0.75, 'danceability': 0.4},
        'ghazal': {'energy': 0.4, 'valence': 0.5, 'danceability': 0.3},
        'qawwali': {'energy': 0.7, 'valence': 0.7, 'danceability': 0.6},
        
        # Default
        'default': {'energy': 0.5, 'valence': 0.5, 'danceability': 0.5}
    }
    
    def __init__(self, enriched_tracks):
        self.tracks = enriched_tracks
    
    def infer_mood_features(self):
        """Infer energy, valence, and danceability from genres"""
        print("=" * 80)
        print("🎭 MOOD INFERENCE ANALYSIS")
        print("=" * 80)
        
        if 'artist_genres' not in self.tracks.columns:
            print("⚠️  No genre data available for mood inference")
            return self.tracks
        
        # Add mood features
        mood_features = []
        
        for idx, row in self.tracks.iterrows():
            genres = row.get('artist_genres', [])
            
            if not genres or not isinstance(genres, list):
                # Use default
                mood_features.append(self.MOOD_MAPPING['default'].copy())
                continue
            
            # Average mood scores across all genres
            energy_scores = []
            valence_scores = []
            dance_scores = []
            
            for genre in genres:
                genre_lower = genre.lower()
                
                # Find matching mood mapping (partial match)
                matched = False
                for mood_key, mood_vals in self.MOOD_MAPPING.items():
                    if mood_key in genre_lower or genre_lower in mood_key:
                        energy_scores.append(mood_vals['energy'])
                        valence_scores.append(mood_vals['valence'])
                        dance_scores.append(mood_vals['danceability'])
                        matched = True
                        break
                
                if not matched:
                    # Use default for unknown genres
                    energy_scores.append(0.5)
                    valence_scores.append(0.5)
                    dance_scores.append(0.5)
            
            # Average the scores
            mood_features.append({
                'energy': np.mean(energy_scores) if energy_scores else 0.5,
                'valence': np.mean(valence_scores) if valence_scores else 0.5,
                'danceability': np.mean(dance_scores) if dance_scores else 0.5
            })
        
        # Add to dataframe
        self.tracks['inferred_energy'] = [m['energy'] for m in mood_features]
        self.tracks['inferred_valence'] = [m['valence'] for m in mood_features]
        self.tracks['inferred_danceability'] = [m['danceability'] for m in mood_features]
        
        # Calculate statistics
        avg_energy = self.tracks['inferred_energy'].mean()
        avg_valence = self.tracks['inferred_valence'].mean()
        avg_dance = self.tracks['inferred_danceability'].mean()
        
        print(f"✓ Inferred mood features for {len(self.tracks)} tracks")
        print(f"\n📊 Average Mood Profile:")
        print(f"   • Energy: {avg_energy:.2f} (0=calm, 1=intense)")
        print(f"   • Valence: {avg_valence:.2f} (0=sad, 1=happy)")
        print(f"   • Danceability: {avg_dance:.2f} (0=not danceable, 1=very danceable)")
        
        # Classify overall mood
        if avg_energy > 0.7 and avg_valence > 0.6:
            mood_type = "🎉 ENERGETIC & UPBEAT"
            description = "High energy, positive vibes. Party-ready playlist!"
        elif avg_energy < 0.4 and avg_valence < 0.5:
            mood_type = "🌙 MELLOW & INTROSPECTIVE"
            description = "Low energy, contemplative. Perfect for quiet moments."
        elif avg_energy > 0.6 and avg_valence < 0.5:
            mood_type = "⚡ INTENSE & EMOTIONAL"
            description = "High energy but emotional. Raw and powerful music."
        elif avg_energy < 0.5 and avg_valence > 0.6:
            mood_type = "☀️ CALM & HAPPY"
            description = "Relaxed but positive. Feel-good, easy listening."
        else:
            mood_type = "🎭 BALANCED & VERSATILE"
            description = "Well-balanced mood profile across the spectrum."
        
        print(f"\n{mood_type}")
        print(f"{description}")
        print()
        
        return self.tracks


# ============================================================================
#  EMOTIONAL DEPTH ANALYSIS (WITHOUT LYRICS API FOR NOW)
# ============================================================================

class EmotionalAnalyzer:
    """Analyze emotional depth using available metadata"""
    
    def __init__(self, enriched_tracks_with_mood):
        self.tracks = enriched_tracks_with_mood
    
    def calculate_emotional_metrics(self):
        """Calculate emotional depth and variety metrics"""
        print("=" * 80)
        print("💫 EMOTIONAL DEPTH ANALYSIS")
        print("=" * 80)
        
        metrics = {}
        
        # 1. Emotional range (variance in valence)
        if 'inferred_valence' in self.tracks.columns:
            valence_scores = self.tracks['inferred_valence'].dropna()
            metrics['emotional_range'] = valence_scores.std() * 100
            metrics['emotional_variance'] = valence_scores.var()
            
            # Count emotional categories
            very_sad = len(valence_scores[valence_scores < 0.3])
            sad = len(valence_scores[(valence_scores >= 0.3) & (valence_scores < 0.5)])
            neutral = len(valence_scores[(valence_scores >= 0.5) & (valence_scores < 0.7)])
            happy = len(valence_scores[(valence_scores >= 0.7) & (valence_scores < 0.85)])
            very_happy = len(valence_scores[valence_scores >= 0.85])
            
            metrics['emotion_distribution'] = {
                'very_sad': very_sad,
                'sad': sad,
                'neutral': neutral,
                'happy': happy,
                'very_happy': very_happy
            }
            
            print(f"📊 Emotional Range: {metrics['emotional_range']:.1f}/100")
            print(f"   (Standard deviation in emotional tone)")
            
            print(f"\n📊 Emotion Distribution:")
            print(f"   😢 Very Sad: {very_sad} tracks ({very_sad/len(valence_scores)*100:.1f}%)")
            print(f"   😔 Sad: {sad} tracks ({sad/len(valence_scores)*100:.1f}%)")
            print(f"   😐 Neutral: {neutral} tracks ({neutral/len(valence_scores)*100:.1f}%)")
            print(f"   🙂 Happy: {happy} tracks ({happy/len(valence_scores)*100:.1f}%)")
            print(f"   😄 Very Happy: {very_happy} tracks ({very_happy/len(valence_scores)*100:.1f}%)")
        
        # 2. Artist emotional diversity
        if 'artists' in self.tracks.columns and 'inferred_valence' in self.tracks.columns:
            # Calculate valence variance per artist
            artist_valences = defaultdict(list)
            
            for idx, row in self.tracks.iterrows():
                artists = row.get('artists', [])
                valence = row.get('inferred_valence')
                
                if isinstance(artists, list) and pd.notna(valence):
                    for artist in artists:
                        artist_valences[artist].append(valence)
            
            # Calculate variance for artists with multiple tracks
            diverse_artists = []
            for artist, valences in artist_valences.items():
                if len(valences) >= 3:  # At least 3 tracks
                    variance = np.var(valences)
                    if variance > 0.05:  # Threshold for diversity
                        diverse_artists.append((artist, variance, len(valences)))
            
            diverse_artists.sort(key=lambda x: x[1], reverse=True)
            metrics['emotionally_diverse_artists'] = diverse_artists[:10]
            
            print(f"\n🎭 Emotionally Diverse Artists:")
            print(f"   (Artists with varied emotional tones)")
            for artist, variance, count in diverse_artists[:5]:
                print(f"   • {artist} ({count} tracks, variance: {variance:.3f})")
        
        # 3. Energy-Valence correlation
        if 'inferred_energy' in self.tracks.columns and 'inferred_valence' in self.tracks.columns:
            energy = self.tracks['inferred_energy'].dropna()
            valence = self.tracks['inferred_valence'].dropna()
            
            if len(energy) > 0 and len(valence) > 0:
                correlation = np.corrcoef(energy, valence)[0, 1]
                metrics['energy_valence_correlation'] = correlation
                
                print(f"\n📊 Energy-Emotion Correlation: {correlation:.2f}")
                if correlation > 0.5:
                    print(f"   → You prefer upbeat, energetic music")
                elif correlation < -0.3:
                    print(f"   → You like intense but melancholic music")
                else:
                    print(f"   → Your energy and emotion preferences are independent")
        
        # 4. Emotional depth score (composite)
        emotional_depth_score = 0
        
        if 'emotional_range' in metrics:
            # Higher range = more emotional depth
            emotional_depth_score += min(metrics['emotional_range'], 50)
        
        if 'emotionally_diverse_artists' in metrics:
            # More diverse artists = more emotional depth
            emotional_depth_score += min(len(metrics['emotionally_diverse_artists']) * 5, 30)
        
        # Check for presence of emotional genres
        emotional_genres = ['sad', 'melancholic', 'romantic', 'emotional', 'soul', 'blues']
        if 'artist_genres' in self.tracks.columns:
            all_genres = []
            for genres in self.tracks['artist_genres'].dropna():
                if isinstance(genres, list):
                    all_genres.extend([g.lower() for g in genres])
            
            emotional_count = sum(1 for g in all_genres if any(eg in g for eg in emotional_genres))
            emotional_depth_score += min(emotional_count / len(all_genres) * 20, 20) if all_genres else 0
        
        metrics['emotional_depth_score'] = min(emotional_depth_score, 100)
        
        print(f"\n🎭 Overall Emotional Depth Score: {metrics['emotional_depth_score']:.1f}/100")
        
        if metrics['emotional_depth_score'] >= 70:
            print(f"   → Deep emotional connection with music")
        elif metrics['emotional_depth_score'] >= 40:
            print(f"   → Moderate emotional engagement")
        else:
            print(f"   → Lighter, more casual listening")
        
        print()
        return metrics


# ============================================================================
#  INTEGRATION FUNCTION
# ============================================================================

def run_mood_emotion_analysis(enriched_tracks):
    """Run complete mood and emotion analysis"""
    
    # Step 1: Infer mood features
    mood_analyzer = MoodAnalyzer(enriched_tracks)
    tracks_with_mood = mood_analyzer.infer_mood_features()
    
    # Step 2: Emotional depth analysis
    emotional_analyzer = EmotionalAnalyzer(tracks_with_mood)
    emotional_metrics = emotional_analyzer.calculate_emotional_metrics()
    
    # Save tracks
    tracks_path = os.path.join(OUTPUT_DIR, 'tracks_with_mood.json')
    tracks_with_mood.to_json(tracks_path, orient='records', indent=2)
    print(f"📄 Tracks: {tracks_path}")
    
    # Save metrics
    metrics_path = os.path.join(OUTPUT_DIR, 'emotional_results.json')
    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(emotional_metrics, f, indent=2, ensure_ascii=False, default=str)
    print(f"📄 Metrics: {metrics_path}")
    print()
    
    return tracks_with_mood, emotional_metrics


if __name__ == "__main__":
    print("Loading tracks...")
    
    from analysis import SpotifyDataLoader
    
    loader = SpotifyDataLoader()
    unified_tracks, unified_artists = loader.load_and_normalize()
    enriched_tracks = loader.merge_track_artist_data()
    
    run_mood_emotion_analysis(enriched_tracks)
