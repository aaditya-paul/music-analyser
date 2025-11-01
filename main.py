from fetchSpotifyData import FetchSpotifyData
from calculate_items import calculate_items as cal
from analyse import run_music_analysis
from ai_summary import get_ai_summary
import json

def main():
    print("Fetching Spotify Data...")
    FetchSpotifyData()
    print("Data fetched successfully.")
    print("Total Recently Played Tracks:", cal(data_file="spotify_data.json"))
    
    # Run analysis and get comprehensive results
    analysis_results = run_music_analysis(show_graphs=False)
    
    # Prepare detailed prompt for Gemini
    prompt = f"""
You are an expert in music psychology and data-driven personality analysis, but you speak like a friend who knows the user really well — direct, funny, expressive, and brutally honest.

The user has provided comprehensive Spotify listening data and personality metrics.
You will use them to create a summary that feels personal, vibrant, and full of life — not robotic, not sugar-coated.

🧠 Input Data

Personality Type: {analysis_results['personality_profile']['personality_type']}
Description: {analysis_results['personality_profile']['personality_description']}

Overall Personality Score: {analysis_results['personality_profile']['overall_score']}/100
Compatibility Tier: {analysis_results['personality_profile']['compatibility_tier']}

Personality Dimension Scores (0–100):

Mainstream vs Indie: {analysis_results['personality_profile']['scores']['mainstream_factor']}/100

Music Diversity: {analysis_results['personality_profile']['scores']['diversity_factor']}/100

Nostalgia Level: {analysis_results['personality_profile']['scores']['nostalgia_factor']}/100

Energy Level: {analysis_results['personality_profile']['scores']['energy_factor']}/100

Emotional Depth: {analysis_results['personality_profile']['scores']['emotional_depth']}/100

Cultural Rootedness: {analysis_results['personality_profile']['scores']['cultural_rootedness']}/100

Explorer Mindset: {analysis_results['personality_profile']['scores']['explorer_factor']}/100

Listening Stats:

Total listening time: {analysis_results['statistics']['total_listening_minutes']:.0f} min ({analysis_results['statistics']['total_listening_minutes']/60:.1f} hrs)

Unique artists: {analysis_results['statistics']['unique_artists']}

Average track popularity: {analysis_results['statistics']['avg_track_popularity']:.1f}/100

Saved tracks: {analysis_results['statistics']['saved_tracks_count']}

Followed artists: {analysis_results['statistics']['followed_artists']}

Track Counts by Time Period:

Short-term: {analysis_results['statistics']['track_counts']['short_term']}

Medium-term: {analysis_results['statistics']['track_counts']['medium_term']}

Long-term: {analysis_results['statistics']['track_counts']['long_term']}

Top Items:

#1 Genre: {analysis_results['top_items']['top_genre']}
#1 Artist: {analysis_results['top_items']['top_artist']}

Top 5 Tracks:
{chr(10).join([f" - {track['name']} by {track['artists']} (Popularity: {track['popularity']}/100)" for track in analysis_results['top_items']['top_tracks']])}

Top 5 Artists:
{chr(10).join([f" - {artist['name']} (Popularity: {artist['popularity']}/100, Followers: {artist['followers']:,})" for artist in analysis_results['top_items']['top_artists']])}

Top 10 Genres:
{chr(10).join([f" - {genre['genre']}: {genre['count']} artists" for genre in analysis_results['top_items']['top_genres']])}

Match Data:

Music Personality Score: {analysis_results['match_data']['music_personality_score']}/100

Personality Vector: {analysis_results['match_data']['vector']}

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
        with open("ai_music_insights.txt", "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("AI-GENERATED MUSIC PERSONALITY INSIGHTS\n")
            f.write("=" * 80 + "\n\n")
            f.write(ai_summary)
            # f.write("\n\n" + "=" * 80 + "\n")
            # f.write("Generated using Google Gemini 2.5 Flash\n")
            # f.write("=" * 80 + "\n")
        
        print("💾 AI insights saved to: ai_music_insights.txt")
        print()
        
    except Exception as e:
        print(f"❌ Error generating AI summary: {e}")
        print("Make sure you have set GEMINI_API_KEY in your .env file")

if __name__ == "__main__":
    main()  