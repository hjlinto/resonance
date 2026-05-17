"""
Spotify ingestion service.

This module owns the responsibility of converting Spotify API responses into
normalized database records.

Routes should not contain data-normalization logic because that logic belongs
to the backend's data ingestion layer.
"""
import requests

from sqlalchemy.orm import Session

from app.models.artist import Artist
from app.models.track import Track
from app.models.user import User

from app.models.user_top_artist import UserTopArtist
from app.models.user_top_track import UserTopTrack

def upsert_user(db: Session, spotify_profile: dict) -> User:
    """
    Create or update an application user from a Spotify profile response.
    """

    spotify_user_id = spotify_profile["id"]

    user = db.query(User).filter(User.spotify_user_id == spotify_user_id).first()

    if user is None:
        user = User(
            spotify_user_id=spotify_user_id,
            display_name=spotify_profile.get("display_name")
        )
        db.add(user)

    else:
        user.display_name = spotify_profile.get("display_name")

    db.commit()
    db.refresh(user)

    return user

def upsert_artist(db: Session, spotify_artist: dict) -> Artist:
    """
    Create or update an artist from a Spotify artist response.
    """

    spotify_artist_id = spotify_artist["id"]
    images = spotify_artist.get("images", [])
    image_url = images[0].get("url") if images else None
    genres = ", ".join(spotify_artist.get("genres", []))
    
    artist = db.query(Artist).filter(Artist.spotify_artist_id == spotify_artist_id).first()

    if artist is None:
        artist = Artist(spotify_artist_id=spotify_artist_id)
        db.add(artist)

    artist.name = spotify_artist.get("name")
    artist.genres = genres
    artist.popularity = spotify_artist.get("popularity")
    artist.image_url = image_url

    db.commit()
    db.refresh(artist)

    return artist

def upsert_track(db: Session, track_data: dict) -> Track:
    """
    Create or update a track from a Spotify track response.
    """

    spotify_track_id = track_data["id"]

    track = db.query(Track).filter(Track.spotify_track_id == spotify_track_id).first()
    
    album = track_data.get("album", {})
    artists = track_data.get("artists", [])
    images = album.get("images", [])

    artist_name = artists[0].get("name") if artists else None
    album_name = album.get("name")
    album_image_url = images[0].get("url") if images else None
    
    if track is None:
        track = Track(spotify_track_id=spotify_track_id)
        db.add(track)

    track.name = track_data.get("name")
    track.artist_name = artist_name
    track.album_name = album_name
    track.album_image_url = album_image_url
    track.preview_url = track_data.get("preview_url")
    track.popularity = track_data.get("popularity")

    db.commit()
    db.refresh(track)

    return track

def save_user_top_artists(db: Session, user: User, spotify_top_artists: list[dict]) -> None:
    """
    Save a user's top artists from a Spotify API response.
    """

    for rank, spotify_artist in enumerate(spotify_top_artists, start=1):
        artist = upsert_artist(db, spotify_artist)

        user_top_artist = UserTopArtist(
            user_id=user.id,
            artist_id=artist.id,
            rank=rank
        )
        db.add(user_top_artist)

    db.commit()

def save_user_top_tracks(db: Session, user: User, spotify_top_tracks: list[dict]) -> None:
    """
    Save a user's top tracks from a Spotify API response.
    """

    for rank, spotify_track in enumerate(spotify_top_tracks, start=1):
        track = upsert_track(db, spotify_track)

        user_top_track = UserTopTrack(
            user_id=user.id,
            track_id=track.id,
            rank=rank
        )
        db.add(user_top_track)

    db.commit()

def update_track_audio_features(db: Session, track: Track, audio_features: dict) -> Track:
    """
    Update a track with Spotify audio feature data.

    This function goes unused in current version due to Spotify API revoking access to all audio features.
    """

    track.danceability = audio_features.get("danceability")
    track.energy = audio_features.get("energy")
    track.valence = audio_features.get("valence")
    track.tempo = audio_features.get("temp")
    track.acousticness = audio_features.get("acousticness")
    track.instrumentalness = audio_features.get("instrumentalness")

    db.commit()
    db.refresh(track)

    return track

def ingest_candidate_tracks_for_user(db: Session, access_token: str, user: User, market: str = "US") -> int:
    """
    Ingest candidate recommendation tracks from the user's top artists.

    These tracks are stored in the tracks table only.
    They are not saved as UserTopTrack rows.
    """

    top_artists = (
        db.query(UserTopArtist)
        .filter(UserTopArtist.user_id == user.id)
        .all()
    )

    inserted_or_updated_count = 0

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    for top_artist in top_artists:
        artist = (
            db.query(Artist)
            .filter(Artist.id == top_artist.artist_id)
            .first()
        )

        if artist is None:
            continue

        response = requests.get(
            f"https://api.spotify.com/v1/artists/{artist.spotify_artist_id}/top-tracks?market={market}",
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

        artist_top_tracks = response.json().get("tracks", [])

        for spotify_track in artist_top_tracks:
            upsert_track(db, spotify_track)
            inserted_or_updated_count += 1

    return inserted_or_updated_count