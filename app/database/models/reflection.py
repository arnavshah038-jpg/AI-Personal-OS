from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.database.base import Base


class Reflection(Base):

    __tablename__ = "reflections"

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

    reflection = Column(
        Text,
        nullable=False,
    )

    importance = Column(
        Integer,
        default=5,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )