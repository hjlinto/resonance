"""
Artist database model.

This model owns the normalized artist records imported from Spotify.

Artists are stored once and reused across tracks, top-artist rankings, and
future recommendation features.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Artist(Base):
    """
    Represent a Spotify artist in our database.
    """

    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    spotify_artist_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)