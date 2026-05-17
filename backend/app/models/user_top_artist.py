"""
User top artist database model.

This model owns the relationship between users and their ranked Spotify artists.

The ranking is stored separately from the artist because "top artist" is a
user-specific property, while the artist itself is not.
"""

from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class UserTopArtist(Base):
    """User top artist database model."""

    __tablename__ = "user_top_artist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    artist_id: Mapped[int] = mapped_column(Integer, ForeignKey("artists.id"), nullable=False)

    rank: Mapped[int] = mapped_column(Integer, nullable=False)

    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc)
    )