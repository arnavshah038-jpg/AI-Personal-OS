from app.database.session import SessionLocal
from app.memory.forget_extractor import ForgetExtractor
from app.memory.vector_search import VectorSearch
from app.memory.vector_store import VectorStore
from app.repositories.memory_repository import MemoryRepository
from app.utils.logger import logger


def forget(
    session_id: str,
    message: str,
):

    extracted_memory = ForgetExtractor.extract(
        message
    )

    logger.info(
        f"Extracted Forget Memory: {extracted_memory}"
    )

    if (
        extracted_memory is None
        or extracted_memory == "NONE"
    ):

        return {
            "message": "No memory found to forget."
        }

    db = SessionLocal()

    try:

        # -------------------------------
        # Semantic Search in Qdrant
        # -------------------------------

        results = VectorSearch.search(
            session_id=session_id,
            query=extracted_memory,
            limit=1,
        )

        logger.info(
            f"Semantic Match: {results}"
        )

        if not results:

            logger.warning(
                "No similar memory found."
            )

            return {
                "message": "Memory not found."
            }

        # -------------------------------
        # Load PostgreSQL record
        # -------------------------------

        memory = MemoryRepository.get_memory_by_id(
            db=db,
            memory_id=results[0]["memory_id"],
        )

        logger.info(
            f"Database Match: {memory}"
        )

        if memory is None:

            logger.warning(
                "Memory ID not found in PostgreSQL."
            )

            return {
                "message": "Memory not found."
            }

        # -------------------------------
        # Delete PostgreSQL
        # -------------------------------

        MemoryRepository.delete_memory(
            db=db,
            session_id=session_id,
            memory=memory.memory,
        )

        # -------------------------------
        # Delete Qdrant
        # -------------------------------

        VectorStore.delete_memory(
            memory_id=memory.id,
        )

        logger.info(
            "Memory forgotten successfully."
        )

        return {
            "message": "Memory forgotten successfully."
        }

    finally:

        db.close()