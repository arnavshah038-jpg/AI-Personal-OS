from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

def _normalize(url: str) -> str:
    # Neon/Render "postgres://" ya "postgresql://" dete hain; psycopg3 driver chahiye
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


engine = create_engine(_normalize(settings.database_url), pool_pre_ping=True, pool_size=3, pool_recycle=300)
SessionLocal = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
