"""
Spotify API Service.

This module owns outbound requests to Spotify's web API.

Routes should call this service instead of using requests
directly so Spotify communication stays centralized and 
reusable across the app.
"""

import requests
from fastapi import HTTPException

SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

def spotify_get(access_token: str, endpoint: str, params: dict | None = None) -> dict:
    """
    Send an authenticated GET request to the Spotify API.

    This helper centralizes headers, timeout behavior, and
    common error handling for all Spotify GET requests.
    """
    response = requests.get(
        f"{SPOTIFY_API_BASE_URL}{endpoint}",
        headers={"Authorization": f"Bearer {access_token}"},
        params=params,
        timeout=10,  # seconds
    )

    if response.status_code == 401:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized: Invalid Spotify access token."
        )
    
    response.raise_for_status()  # Raise for other HTTP errors

    return response.json()

def get_current_spotify_user(access_token: str) -> dict:
    """
    Fetch the current Spotify user's profile information.

    The profile gives us the stable Spotify user ID needed
    to associate tokens with a specific Spotify account in 
    our database.
    """
    return spotify_get(access_token, "/me")

def get_user_top_tracks(access_token: str, limit: int = 50) -> dict:
    """
    Fetch the current Spotify user's top tracks.
    
    This data becomes the first input for the recommendation engine.
    """

    return spotify_get(
        access_token, 
        "/me/top/tracks", 
        params={"limit": limit, "time_range": "medium_term"}
    )

def get_user_top_artists(access_token: str, limit: int = 50) -> dict:
    """
    Fetch the current Spotify user's top artists.
    
    This data becomes the second input for the recommendation engine.
    """

    return spotify_get(
        access_token, 
        "/me/top/artists", 
        params={"limit": limit, "time_range": "medium_term"}
    )

def get_track_audio_features(access_token: str, track_id: str) -> dict:
    """
    Fetch Spotify audio features for a single track.

    Audio Features provide numeric music attributes used by
    the recommendation engine.
    """

    return spotify_get(
        access_token,
        f"/audio-features/{track_id}"
    )