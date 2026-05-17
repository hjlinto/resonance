"""
Recommendation service for Resonance.

This module owns recommendation business logic.

Routes should not calculate recommendations directly. Routes should receive an HTTP request, call this
service, and return the result as JSON.
"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.artist import Artist
from app.models.track import Track
from app.models import UserTopArtist, UserTopTrack


def generate_recommendations_for_user(db: Session, spotify_user_id: str, limit: int = 20) -> dict:
    """
    Generate recommendations for a Spotify user.

    Strategy:
    - Use ranks 1-10 as the user's strongest taste profile
    - Use ranks 11-50 as recommendation candidates
    - Score candidates higher when they match artists from the top 10
    """

    user = (
        db.query(User)
        .filter(User.spotify_user_id == spotify_user_id)
        .first()
    )

    if user is None:
        return {
            "spotify_user_id": spotify_user_id,
            "recommendations": [],
            "message": "No user found for this Spotify user ID.",
        }

    top_tracks = (
        db.query(UserTopTrack)
        .filter(UserTopTrack.user_id == user.id)
        .all()
    )

    top_artists = (
        db.query(UserTopArtist)
        .filter(UserTopArtist.user_id == user.id)
        .all()
    )

    profile_track_ids = {
        item.track_id
        for item in top_tracks
        if item.rank <= 10
    }

    candidate_track_ids = {
        item.track_id
        for item in top_tracks
        if item.rank > 10
    }

    favorite_artist_ids = {item.artist_id for item in top_artists}

    favorite_artists = (
        db.query(Artist)
        .filter(Artist.id.in_(favorite_artist_ids))
        .all()
        if favorite_artist_ids
        else []
    )

    favorite_genres = set()

    for artist in favorite_artists:
        if artist.genres:
            favorite_genres.update(
                genre.strip()
                for genre in artist.genres.split(",")
                if genre.strip()
            )

    profile_tracks = (
        db.query(Track)
        .filter(Track.id.in_(profile_track_ids))
        .all()
        if profile_track_ids
        else []
    )

    profile_artist_names = {
        profile_track.artist_name
        for profile_track in profile_tracks
        if profile_track.artist_name
    }

    candidate_tracks = (
        db.query(Track)
        .filter(Track.id.in_(candidate_track_ids))
        .all()
        if candidate_track_ids
        else []
    )

    scored_recommendations = []

    for track in candidate_tracks:
        score = 0
        reasons = []

        if track.artist_name in profile_artist_names:
            score += 50
            reasons.append("Matches an artist from your top tracks")

        if score == 0:
            score += max(1, 50 - track.id)
            reasons.append("Pulled from your broader Spotify listening history")

        scored_recommendations.append(
            {
                "track_id": track.id,
                "spotify_track_id": track.spotify_track_id,
                "name": track.name,
                "artist_name": track.artist_name,
                "album_name": track.album_name,
                "album_image_url": track.album_image_url,
                "preview_url": track.preview_url,
                "score": score,
                "reasons": reasons,
            }
        )

    scored_recommendations.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return {
        "spotify_user_id": spotify_user_id,
        "user_id": user.id,
        "recommendation_count": min(len(scored_recommendations), limit),
        "strategy": "Top 10 tracks used as taste profile; ranks 11-50 used as recommendation candidates.",
        "recommendations": scored_recommendations[:limit],
    }