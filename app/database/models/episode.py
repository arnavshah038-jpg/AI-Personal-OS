from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database.base import Base


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    session_id = Column(
        String,
        nullable=False,
        index=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    event_type = Column(
        String,
        nullable=False,
        default="general",
    )

    importance = Column(
        Integer,
        default=5,
    )

    event_date = Column(
        DateTime,
        default=datetime.utcnow,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )