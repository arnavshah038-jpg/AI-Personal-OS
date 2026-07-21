from app.core.config import settings
from app.core.openai_client import client
from app.database.session import SessionLocal
from app.repositories.memory_repository import MemoryRepository
from app.memory.memory_importance import MemoryImportance
from app.memory.memory_type_classifier import MemoryTypeClassifier
from app.memory.vector_store import VectorStore
from app.utils.logger import logger


class MemoryConsolidator:

    @staticmethod
    def consolidate(session_id: str):

        db = SessionLocal()

        try:

            memories = MemoryRepository.get_memories(
                db=db,
                session_id=session_id,
            )

            if len(memories) < 5:

                logger.info(
                    "Not enough memories to consolidate."
                )

                return []

            memory_text = "\n".join(
                memory.memory
                for memory in memories
            )

            prompt = f"""
You are an AI memory consolidation engine.

Merge duplicate and similar memories.

Rules:
- Remove duplicate memories.
- Merge related memories.
- Keep only useful information.
- Return ONE memory per line.
- No numbering.
- No explanation.

Memories:

{memory_text}
"""

            response = client.responses.create(
                model=settings.OPENAI_MODEL,
                input=prompt,
            )

            consolidated = response.output_text.strip()

            logger.info(
                "Consolidated Memories:\n%s",
                consolidated,
            )

            new_memories = [
                m.strip()
                for m in consolidated.split("\n")
                if m.strip()
            ]

            logger.info(
                "Parsed Memories: %s",
                new_memories,
            )

            # -----------------------------
            # Delete old memories
            # -----------------------------

            for memory in memories:

                MemoryRepository.delete_memory_by_id(
                    db=db,
                    memory_id=memory.id,
                )

                VectorStore.delete_memory(
                    memory_id=memory.id,
                )

            logger.info(
                "Old memories removed."
            )

            # -----------------------------
            # Save consolidated memories
            # -----------------------------

            for memory in new_memories:

                importance = MemoryImportance.score(
                    memory
                )

                memory_type = MemoryTypeClassifier.classify(
                    memory
                )

                saved = MemoryRepository.save_memory(
                    db=db,
                    session_id=session_id,
                    memory=memory,
                    importance=importance,
                    memory_type=memory_type,
                )

                VectorStore.save_memory(
                    session_id=session_id,
                    memory_id=saved.id,
                    memory=memory,
                    memory_type=memory_type,
                    importance=importance,
                )

            logger.info(
                "Memory consolidation completed successfully."
            )

            return new_memories

        except Exception as e:

            logger.exception(
                "Memory consolidation failed: %s",
                e,
            )

            raise

        finally:

            db.close()