from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database.base import Base


class Memory(Base):
    __tablename__ = "memories"

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

    memory = Column(
        String,
        nullable=False,
    )

    # Memory Type
    memory_type = Column(
        String,
        nullable=False,
        default="fact",
    )

    # Importance Score
    importance = Column(
        Integer,
        default=1,
    )

    # Number of times this memory has been retrieved
    access_count = Column(
        Integer,
        default=0,
    )

    # Last time this memory was used
    last_accessed = Column(
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