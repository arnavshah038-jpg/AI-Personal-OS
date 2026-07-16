from app.database.session import SessionLocal
from app.repositories.memory_repository import (
    MemoryRepository,
)
from app.utils.logger import logger


class MemoryBoostManager:

    @staticmethod
    def run():

        db = SessionLocal()

        try:

            updated = MemoryRepository.boost_memories(
                db=db,
            )

            logger.info(
                f"Memory Boost completed. Updated {updated} memories."
            )

        finally:

            db.close()