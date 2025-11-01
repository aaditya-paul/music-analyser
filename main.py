from fetchSpotifyData import FetchSpotifyData
from calculate_items import calculate_items as cal
from run_analysis import run_complete_analysis
from ai_summary import get_ai_summary
import json
import os

def main():
    print("Fetching Spotify Data...")
    FetchSpotifyData()
    print("Data fetched successfully.")
    print("Total Recently Played Tracks:", cal(data_file="spotify_data.json"))
    
    # Run music analysis
    print("\n" + "=" * 80)
    print("🎵 RUNNING MUSIC ANALYSIS")
    print("=" * 80 + "\n")
    
    success = run_complete_analysis()
    
    if not success:
        print("❌ Analysis failed. Please check the errors above.")
        return
    
    # Load analysis results for AI summary
    try:
        with open('out/analysis_results.json', 'r', encoding='utf-8') as f:
            enhanced_results = json.load(f)
        with open('out/emotional_results.json', 'r', encoding='utf-8') as f:
            emotional_results = json.load(f)
    except Exception as e:
        print(f"❌ Error loading analysis results: {e}")
        return
    
    # Extract key metrics
    data_summary = enhanced_results['data_summary']
    classification = enhanced_results['listener_classification']
    diversity = enhanced_results['diversity_metrics']
    nostalgia = enhanced_results['nostalgia_metrics']
    
    # Prepare prompt for AI
    prompt = f"""
You are an expert in music psychology and data-driven personality analysis, but you speak like a friend who knows the user really well — direct, funny, expressive, and brutally honest.

The user has provided comprehensive Spotify listening data and personality metrics.
You will use them to create a summary that feels personal, vibrant, and full of life — not robotic, not sugar-coated.

🧠 Analysis Results

LISTENER TYPE: {classification['category']}
Overall Diversity Score: {classification['overall_diversity']:.1f}/100
Description: {classification['description']}

DATA SUMMARY:
- Total Unique Tracks: {data_summary['total_unique_tracks']:,}
- Total Unique Artists: {data_summary['total_unique_artists']:,}
- Unique Genres: {diversity['unique_genres']}

DIVERSITY METRICS:
- Genre Diversity: {diversity['genre_diversity_score']:.1f}/100
- Shannon Entropy: {diversity['genre_entropy']:.2f} bits
- Artist Concentration (Top 10): {diversity['artist_concentration']:.1f}%

NOSTALGIA & LOYALTY:
- Consistency Score: {nostalgia.get('consistency_score', 0):.1f}%
- Return Rate: {nostalgia.get('return_rate', 0):.1f}%
- Artist Loyalty: {nostalgia.get('artist_loyalty', 0):.1f}%
- Resurgence Score: {nostalgia.get('resurgence_score', 0):.1f}%

EMOTIONAL PROFILE:
- Emotional Depth: {emotional_results['emotional_depth_score']:.1f}/100
- Emotional Range: {emotional_results['emotional_range']:.1f}/100
- Energy-Valence Correlation: {emotional_results.get('energy_valence_correlation', 0):.2f}

EMOTION DISTRIBUTION:
{chr(10).join([f"- {emotion.replace('_', ' ').title()}: {count} tracks" for emotion, count in emotional_results['emotion_distribution'].items()])}

TOP GENRES (by frequency):
{chr(10).join([f"- {genre}: {count} artists" for genre, count in list(diversity.get('genre_distribution', {}).items())[:10]])}

🧩 Your Tasks

Respond like a friend with strong opinions and a creative mind, not like a report generator. Keep it colorful, funny, vivid, and honest — if something’s chaotic, say it’s chaotic; if it’s beautiful, hype it up.

Provide:

🔥 A personalized summary (2–3 paragraphs) — explain what their music taste says about who they are, with personality and flair.

💡 Key insights — what makes their listening habits unique, strange, or surprisingly cool.

🧍 Personality interpretation — what kind of person listens like this (vibes, moods, emotional patterns).

🎯 Real-world recommendations — how they can use this taste in life (e.g., socializing, dating, creative work, or discovering new artists).

🎉 Fun or odd patterns — anything funny, unexpected, or revealing about their music data.

Tone guide:

Speak like a brutally honest, funny best friend.

Be descriptive and vivid, not robotic.

No unnecessary flattery.

Give honest reads and realistic advice.

Feel free to use colorful metaphors (e.g. “your playlists scream emotional main character energy” or “you have chaotic good taste”).
"""
    
    print("\n" + "=" * 80)
    print("🤖 GENERATING AI-POWERED INSIGHTS WITH GEMINI")
    print("=" * 80)
    print("\nAnalyzing your music personality with AI...\n")
    
    try:
        ai_summary = get_ai_summary(prompt)
        
        print("=" * 80)
        print("✨ AI-GENERATED PERSONALIZED INSIGHTS")
        print("=" * 80)
        print()
        print(ai_summary)
        print()
        print("=" * 80)
        
        # Save AI summary to file
        ai_insights_path = os.path.join("out", "ai_music_insights.txt")
        with open(ai_insights_path, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("AI-GENERATED MUSIC PERSONALITY INSIGHTS\n")
            f.write("=" * 80 + "\n\n")
            f.write(ai_summary)
            # f.write("\n\n" + "=" * 80 + "\n")
            # f.write("Generated using Google Gemini 2.5 Flash\n")
            # f.write("=" * 80 + "\n")
        
        print(f"💾 AI insights saved to: {ai_insights_path}")
        print()
        
    except Exception as e:
        print(f"❌ Error generating AI summary: {e}")
        print("Make sure you have set GEMINI_API_KEY in your .env file")

if __name__ == "__main__":
    main()  