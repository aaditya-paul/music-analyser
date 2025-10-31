import os
import json
import sys
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SCOPES = "user-read-recently-played user-top-read user-library-read user-follow-read playlist-read-private"

# Use an absolute cache path so running the script from other working directories still finds the cache
CACHE_PATH = os.path.join(os.path.dirname(__file__), ".spotify_cache")


def require_env(var_name):
        print(f"Environment variable {var_name} is set to: {os.getenv(var_name)}")

        if not os.getenv(var_name):
                print(f"Error: Environment variable {var_name} is not set.")
                sys.exit(1)


def iso_now():
        return datetime.utcnow().isoformat() + "Z"


def fetch_recently_played(sp, limit=50):
        results = sp.current_user_recently_played(limit=limit)
        items = []
        for item in results.get("items", []):
                track = item.get("track", {})
                items.append(
                        {
                                "played_at": item.get("played_at"),
                                "track_id": track.get("id"),
                                "track_name": track.get("name"),
                                "artists": [a.get("name") for a in track.get("artists", [])],
                                "album": track.get("album", {}).get("name"),
                                "duration_ms": track.get("duration_ms"),
                        }
                )
        return items


def fetch_top_items(sp, item_type="artists", time_range="medium_term", limit=20):
        # item_type: "artists" or "tracks"
        # This function will page through results using offset to collect all available items.
        # Spotify limits `limit` to 50 per request; we'll request in pages of up to 50.
        page_limit = min(50, max(1, limit))
        items = []
        offset = 0
        total = None

        while True:
                if item_type == "artists":
                        res = sp.current_user_top_artists(limit=page_limit, time_range=time_range, offset=offset)
                        batch = [
                                {
                                        "id": a.get("id"),
                                        "name": a.get("name"),
                                        "genres": a.get("genres", []),
                                        "popularity": a.get("popularity"),
                                        "followers": a.get("followers", {}).get("total"),
                                }
                                for a in res.get("items", [])
                        ]
                else:
                        res = sp.current_user_top_tracks(limit=page_limit, time_range=time_range, offset=offset)
                        batch = [
                                {
                                        "id": t.get("id"),
                                        "name": t.get("name"),
                                        "artists": [ar.get("name") for ar in t.get("artists", [])],
                                        "album": t.get("album", {}).get("name"),
                                        "duration_ms": t.get("duration_ms"),
                                        "popularity": t.get("popularity"),
                                }
                                for t in res.get("items", [])
                        ]

                items.extend(batch)

                # total is provided by the API; use it to stop paging when we've collected everything
                if total is None:
                        total = res.get("total")

                offset += page_limit
                # Stop when we've collected all items or the batch was smaller than requested
                if (total is not None and offset >= total) or len(batch) < page_limit:
                        break

        return items


def fetch_saved_tracks(sp, limit=50):
        # Page through the user's saved tracks until none remain.
        items = []
        page_limit = min(50, max(1, limit))
        offset = 0

        while True:
                res = sp.current_user_saved_tracks(limit=page_limit, offset=offset)
                batch = []
                for it in res.get("items", []):
                        t = it.get("track", {})
                        batch.append(
                                {
                                        "added_at": it.get("added_at"),
                                        "track_id": t.get("id"),
                                        "track_name": t.get("name"),
                                        "artists": [a.get("name") for a in t.get("artists", [])],
                                        "album": t.get("album", {}).get("name"),
                                }
                        )

                items.extend(batch)
                if len(batch) < page_limit:
                        break
                offset += page_limit

        return items


def fetch_followed_artists(sp, limit=50):
        # Spotify returns followed artists via a cursor'd endpoint. Use the `after` cursor to page.
        items = []
        after = None
        page_limit = min(50, max(1, limit))

        while True:
                if after:
                        res = sp.current_user_followed_artists(limit=page_limit, after=after)
                else:
                        res = sp.current_user_followed_artists(limit=page_limit)

                artists_block = res.get("artists", {})
                for a in artists_block.get("items", []):
                        items.append({"id": a.get("id"), "name": a.get("name"), "genres": a.get("genres", [])})

                cursors = artists_block.get("cursors", {})
                after = cursors.get("after")
                # If there's no `after` cursor, we've reached the end
                if not after:
                        break

        return items


def FetchSpotifyData():
        # Ensure env vars exist
        require_env("SPOTIPY_CLIENT_ID")
        require_env("SPOTIPY_CLIENT_SECRET")
        require_env("SPOTIPY_REDIRECT_URI")

        auth_manager = SpotifyOAuth(
                scope=SCOPES,
                cache_path=CACHE_PATH,
                client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
                show_dialog=True,  # force re-auth if you want to switch accounts
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)

        # Print cached token info (if any) to help debug 401/No token issues
        try:
                token_info = auth_manager.get_cached_token()
        except Exception:
                token_info = None

        if token_info and token_info.get("access_token"):
                expires_at = token_info.get("expires_at")
                print(f"Cached token present, expires_at: {expires_at}")
        else:
                print("No cached token found (or access_token missing). The auth flow may need to run.")

        out = {"fetched_at": iso_now(), "recently_played": [], "top_artists": {}, "top_tracks": {}, "saved_tracks": [], "followed_artists": []}

        # Recently played
        try:
                out["recently_played"] = fetch_recently_played(sp, limit=50)
        except spotipy.SpotifyException as e:
                print("Error fetching recently played:", e)

        # Top artists and tracks for short/medium/long term
        for tr in ("short_term", "medium_term", "long_term"):
                try:
                        out["top_artists"][tr] = fetch_top_items(sp, item_type="artists", time_range=tr, limit=50)
                        out["top_tracks"][tr] = fetch_top_items(sp, item_type="tracks", time_range=tr, limit=50)
                except spotipy.SpotifyException as e:
                        print(f"Error fetching top items ({tr}):", e)

        # Saved tracks (library)
        try:
                out["saved_tracks"] = fetch_saved_tracks(sp, limit=50)
        except spotipy.SpotifyException as e:
                print("Error fetching saved tracks:", e)

        # Followed artists
        try:
                out["followed_artists"] = fetch_followed_artists(sp, limit=50)
        except spotipy.SpotifyException as e:
                print("Error fetching followed artists:", e)

        # Print summary of fetched data
        print("\n=== Fetch Summary ===")
        print(f"Recently played: {len(out['recently_played'])} tracks")
        for tr in ("short_term", "medium_term", "long_term"):
                print(f"Top artists ({tr}): {len(out['top_artists'].get(tr, []))}")
                print(f"Top tracks ({tr}): {len(out['top_tracks'].get(tr, []))}")
        print(f"Saved tracks: {len(out['saved_tracks'])}")
        print(f"Followed artists: {len(out['followed_artists'])}")
        print("=====================\n")

        # Save combined data to single file
        out_path = "./data/spotify_data.json"
        with open(out_path, "w", encoding="utf-8") as fh:
                json.dump(out, fh, ensure_ascii=False, indent=2)
        print(f"Saved combined data to {out_path}")

        # Save separate files for each category
        print("\nSaving separate files...")
        
        with open("./data/recently_played.json", "w", encoding="utf-8") as fh:
                json.dump({"fetched_at": out["fetched_at"], "items": out["recently_played"]}, fh, ensure_ascii=False, indent=2)
        print("  - recently_played.json")

        with open("./data/top_artists.json", "w", encoding="utf-8") as fh:
                json.dump({"fetched_at": out["fetched_at"], "data": out["top_artists"]}, fh, ensure_ascii=False, indent=2)
        print("  - top_artists.json")

        with open("./data/top_tracks.json", "w", encoding="utf-8") as fh:
                json.dump({"fetched_at": out["fetched_at"], "data": out["top_tracks"]}, fh, ensure_ascii=False, indent=2)
        print("  - top_tracks.json")

        with open("./data/saved_tracks.json", "w", encoding="utf-8") as fh:
                json.dump({"fetched_at": out["fetched_at"], "items": out["saved_tracks"]}, fh, ensure_ascii=False, indent=2)
        print("  - saved_tracks.json")

        with open("./data/followed_artists.json", "w", encoding="utf-8") as fh:
                json.dump({"fetched_at": out["fetched_at"], "items": out["followed_artists"]}, fh, ensure_ascii=False, indent=2)
        print("  - followed_artists.json")

        print("\nAll files saved successfully!")


if __name__ == "__main__":
        FetchSpotifyData()