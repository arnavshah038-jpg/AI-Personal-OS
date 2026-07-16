from app.database.session import SessionLocal
from app.memory.reflection_generator import ReflectionGenerator
from app.repositories.memory_repository import MemoryRepository
from app.repositories.reflection_repository import (
    ReflectionRepository,
)
from app.utils.logger import logger


class ReflectionManager:

    @staticmethod
    def generate_if_needed(
        session_id: str,
    ):

        db = SessionLocal()

        try:

            logger.info("===== Reflection Manager Started =====")

            memories = MemoryRepository.get_memory_text(
                db=db,
                session_id=session_id,
            )

            if not memories:
                logger.info("No memories found.")
                return

            memory_count = len(memories.splitlines())

            logger.info(f"Memory Count: {memory_count}")
            logger.info(f"Memories:\n{memories}")

            # Generate reflections only after enough memories
            if memory_count < 5:
                logger.info("Not enough memories.")
                return

            reflection = ReflectionGenerator.generate(
                memories
            )

            logger.info(f"Generated Reflection: {reflection}")

            if not reflection:
                logger.info("Reflection is empty.")
                return

            recent = (
                ReflectionRepository.get_recent_reflections(
                    db=db,
                    session_id=session_id,
                    limit=1,
                )
            )

            # Skip duplicate reflection
            if (
                recent
                and recent[0].reflection == reflection
            ):
                logger.info("Duplicate reflection skipped.")
                return

            ReflectionRepository.save_reflection(
                db=db,
                session_id=session_id,
                reflection=reflection,
                importance=8,
            )

            logger.info("Reflection saved successfully.")

        except Exception as e:

            logger.exception(
                f"Reflection Manager Error: {e}"
            )

        finally:

            db.close()