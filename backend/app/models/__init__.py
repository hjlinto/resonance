"""
Model registry.

Import ORM models here so SQLAlchemy can find them when creating tables.
"""

from app.models.spotify_token import SpotifyToken
from app.models.user import User
from app.models.artist import Artist
from app.models.track import Track
from app.models.user_top_artist import UserTopArtist
from app.models.user_top_track import UserTopTrack