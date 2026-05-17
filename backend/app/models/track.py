"""
Track database model.

This model owns normalized Spotify track records.

Tracks are stored independently from user rankings, so the
same track can be reused across different users and 
recommendation flows.
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Track(Base):
    """
    Repesents a Spotify track in the database.
    """

    __tablename__ = "tracks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    spotify_track_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    album_name: Mapped[str | None] = mapped_column(String, nullable=True)