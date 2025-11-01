"""
Music Analysis Pipeline
Runs the complete analysis workflow
"""

import os
import json
from datetime import datetime

OUTPUT_DIR = 'out'
os.makedirs(OUTPUT_DIR, exist_ok=True)


def print_header(text):
    """Print a formatted header"""
    try:
        print("\n" + "=" * 80)
        print(f"  {text}")
        print("=" * 80 + "\n")
    except UnicodeEncodeError:
        # Fallback for Windows console
        text_ascii = text.encode('ascii', 'ignore').decode('ascii')
        print("\n" + "=" * 80)
        print(f"  {text_ascii}")
        print("=" * 80 + "\n")


def run_complete_analysis():
    """Run the complete analysis pipeline"""
    
    print_header("🎵 MUSIC PERSONALITY ANALYSIS")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Step 1: Data Loading & Analysis
    print_header("STEP 1: Data Preparation & Diversity Analysis")
    try:
        from analysis import run_analysis
        results_1 = run_analysis()
        print("✅ Step 1 Complete!\n")
    except Exception as e:
        print(f"❌ Error in Step 1: {e}\n")
        return False
    
    # Step 2: Mood & Emotion Analysis
    print_header("STEP 2: Mood & Emotion Analysis")
    try:
        from emotion_tracker import run_mood_emotion_analysis
        from analysis import SpotifyDataLoader
        
        loader = SpotifyDataLoader()
        unified_tracks, unified_artists = loader.load_and_normalize()
        enriched_tracks = loader.merge_track_artist_data()
        
        tracks_with_mood, emotional_metrics = run_mood_emotion_analysis(enriched_tracks)
        print("✅ Step 2 Complete!\n")
    except Exception as e:
        print(f"❌ Error in Step 2: {e}\n")
        return False
    
    # Step 3: Visualizations
    print_header("STEP 3: Creating Interactive Visualizations")
    try:
        try:
            import plotly
            from visualizations import create_visualizations
            create_visualizations()
            print("✅ Step 3 Complete!\n")
        except ImportError:
            print("⚠️  Plotly not installed. Skipping visualizations.")
            print("   Install with: pip install plotly wordcloud")
            print("✓ Step 3 Skipped\n")
    except Exception as e:
        print(f"⚠️  Error in Step 3: {e}")
        print("   Continuing...\n")
    
    # Step 4: Generate Summary Report
    print_header("STEP 4: Generating Summary Report")
    try:
        generate_summary_report()
        print("✅ Step 4 Complete!\n")
    except Exception as e:
        print(f"❌ Error in Step 4: {e}\n")
        return False
    
    # Completion
    print_header("✨ ANALYSIS COMPLETE ✨")
    print("📁 Generated Files in 'out' folder:")
    print("   • analysis_results.json")
    print("   • tracks_with_mood.json")
    print("   • emotional_results.json")
    print("   • personality_report.txt")
    print("   • radar_chart.html (if plotly installed)")
    print("   • genre_sunburst.html (if plotly installed)")
    print("   • mood_scatter.html (if plotly installed)")
    print("   • top_artists.html (if plotly installed)")
    print("   • artist_wordcloud.png (if wordcloud installed)")
    print()
    print("🌐 Open HTML files in your browser!")
    print()
    
    return True


def generate_summary_report():
    """Generate a text summary report"""
    
    # Load results
    try:
        with open(os.path.join(OUTPUT_DIR, 'analysis_results.json'), 'r', encoding='utf-8') as f:
            enhanced = json.load(f)
        with open(os.path.join(OUTPUT_DIR, 'emotional_results.json'), 'r', encoding='utf-8') as f:
            emotional = json.load(f)
    except Exception as e:
        print(f"❌ Could not load results: {e}")
        return
    
    # Create report
    report = []
    report.append("=" * 80)
    report.append("          🎵 YOUR MUSIC PERSONALITY REPORT 🎵")
    report.append("=" * 80)
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Data Summary
    report.append("-" * 80)
    report.append("📊 DATA SUMMARY")
    report.append("-" * 80)
    data_summary = enhanced['data_summary']
    report.append(f"Total Unique Tracks: {data_summary['total_unique_tracks']:,}")
    report.append(f"Total Unique Artists: {data_summary['total_unique_artists']:,}")
    report.append("")
    
    # Listener Classification
    report.append("-" * 80)
    report.append("🏷️  YOUR LISTENER TYPE")
    report.append("-" * 80)
    classification = enhanced['listener_classification']
    report.append(f"{classification['category']}")
    report.append(f"Diversity Score: {classification['overall_diversity']:.1f}/100")
    report.append(f"\n{classification['description']}")
    report.append("")
    
    # Diversity Metrics
    report.append("-" * 80)
    report.append("🎨 DIVERSITY ANALYSIS")
    report.append("-" * 80)
    diversity = enhanced['diversity_metrics']
    report.append(f"Genre Diversity: {diversity['genre_diversity_score']:.1f}/100")
    report.append(f"  • Unique Genres: {diversity['unique_genres']}")
    report.append(f"  • Shannon Entropy: {diversity['genre_entropy']:.2f} bits")
    report.append(f"\nArtist Diversity:")
    report.append(f"  • Unique Artists: {diversity['unique_artists']}")
    report.append(f"  • Top 10 Concentration: {diversity['artist_concentration']:.1f}%")
    report.append("")
    
    # Nostalgia Metrics
    report.append("-" * 80)
    report.append("🕰️  NOSTALGIA & LOYALTY")
    report.append("-" * 80)
    nostalgia = enhanced['nostalgia_metrics']
    report.append(f"Consistency Score: {nostalgia.get('consistency_score', 0):.1f}%")
    report.append(f"  (How many long-term favorites are still in rotation)")
    report.append(f"\nReturn Rate: {nostalgia.get('return_rate', 0):.1f}%")
    report.append(f"  (Old favorites appearing in recent plays)")
    report.append(f"\nArtist Loyalty: {nostalgia.get('artist_loyalty', 0):.1f}%")
    report.append(f"  (Long-term artists still in your top rotation)")
    
    if nostalgia.get('loyal_artist_list'):
        report.append(f"\nYour Most Loyal Artists:")
        for artist in nostalgia['loyal_artist_list'][:5]:
            report.append(f"  • {artist}")
    
    if nostalgia.get('resurgent_artists'):
        report.append(f"\nResurgent Artists (Rediscovered): {nostalgia['resurgence_score']}")
        for artist in nostalgia['resurgent_artists'][:5]:
            report.append(f"  • {artist}")
    report.append("")
    
    # Emotional Analysis
    report.append("-" * 80)
    report.append("💫 EMOTIONAL PROFILE")
    report.append("-" * 80)
    report.append(f"Emotional Depth Score: {emotional['emotional_depth_score']:.1f}/100")
    report.append(f"Emotional Range: {emotional['emotional_range']:.1f}/100")
    report.append(f"Energy-Valence Correlation: {emotional.get('energy_valence_correlation', 0):.2f}")
    
    report.append(f"\nEmotion Distribution:")
    dist = emotional['emotion_distribution']
    total = sum(dist.values())
    for emotion, count in dist.items():
        pct = (count / total * 100) if total > 0 else 0
        report.append(f"  • {emotion.replace('_', ' ').title()}: {count} tracks ({pct:.1f}%)")
    report.append("")
    
    # Key Insights
    report.append("-" * 80)
    report.append("💡 KEY INSIGHTS")
    report.append("-" * 80)
    
    # Insight 1: Diversity
    if classification['overall_diversity'] >= 75:
        report.append("🌍 You're a true musical explorer with exceptionally diverse taste!")
    elif classification['overall_diversity'] >= 60:
        report.append("🎨 You have a well-balanced, eclectic music taste.")
    else:
        report.append("💎 You have focused preferences and know exactly what you like.")
    
    # Insight 2: Loyalty
    if nostalgia.get('artist_loyalty', 0) >= 70:
        report.append("❤️  You're very loyal to your favorite artists!")
    elif nostalgia.get('artist_loyalty', 0) >= 40:
        report.append("🔄 You balance loyalty with exploration.")
    else:
        report.append("🆕 You love discovering new artists!")
    
    # Insight 3: Emotion
    corr = emotional.get('energy_valence_correlation', 0)
    if corr > 0.5:
        report.append("☀️  You prefer upbeat, energetic music.")
    elif corr < -0.3:
        report.append("🌙 You appreciate intense, emotionally complex music.")
    else:
        report.append("🎭 Your music taste spans all emotional spectrums.")
    
    report.append("")
    report.append("=" * 80)
    report.append("          Thank you for using Enhanced Music Analyzer!")
    report.append("=" * 80)
    
    # Save report
    report_text = '\n'.join(report)
    report_path = os.path.join(OUTPUT_DIR, 'personality_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"✓ Generated report: {report_path}")
    
    # Also print to console
    print("\n" + report_text + "\n")


if __name__ == "__main__":
    success = run_complete_analysis()
    
    if success:
        print("\n🎉 Analysis complete!")
        print("💡 Tip: Install optional dependencies:")
        print("   pip install -r requirements_optional.txt\n")
    else:
        print("\n⚠️  Some errors occurred.")
        print("    Check error messages above.\n")
