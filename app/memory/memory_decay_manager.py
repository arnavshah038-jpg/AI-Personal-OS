from app.database.session import SessionLocal
from app.repositories.memory_repository import (
    MemoryRepository,
)
from app.utils.logger import logger


class MemoryDecayManager:

    @staticmethod
    def run():

        db = SessionLocal()

        try:

            updated = (
                MemoryRepository.decay_memories(
                    db=db,
                    days=30,
                )
            )

            logger.info(
                f"Memory Decay completed. Updated {updated} memories."
            )

        finally:

            db.close()