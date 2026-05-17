"""
Spotify ingestion service.

This module owns the responbility of converting Spotify API responses into
normalized database records.

Routes should not contain data-normalization logic because that logic belongs
to the backend's data ingestion layer.
"""

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

    artist = db.query(Artist).filter(Artist.spotify_artist_id == spotify_artist_id).first()

    if artist is None:
        artist = Artist(
            spotify_artist_id=spotify_artist_id,
            name=spotify_artist.get("name")
        )
        db.add(artist)

    else:
        artist.name = spotify_artist.get("name")

    db.commit()
    db.refresh(artist)

    return artist

def upsert_track(db: Session, track_data: dict) -> Track:
    """
    Create or update a track from a Spotify track response.
    """

    spotify_track_id = track_data["id"]

    track = db.query(Track).filter(Track.spotify_track_id == spotify_track_id).first()
    
    album_name = track_data.get("album", {}).get("name")
    
    if track is None:
        track = Track(
            spotify_track_id=spotify_track_id,
            name=track_data.get("name"),
            album_name=album_name
        )
        db.add(track)

    else:
        track.name = track_data.get("name")
        track.artist_name = track_data["artists"][0]["name"] if track_data.get("artists") else None
        track.album_name = album_name

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