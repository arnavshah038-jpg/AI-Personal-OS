from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
)

from app.core.qdrant_client import (
    COLLECTION_NAME,
    qdrant,
)
from app.database.session import SessionLocal
from app.memory.embedding import EmbeddingGenerator
from app.repositories.memory_repository import (
    MemoryRepository,
)
from app.utils.logger import logger


class VectorSearch:

    @staticmethod
    def search(
        session_id: str,
        query: str,
        limit: int = 5,
        score_threshold: float = 0.15,
    ) -> list:

        embedding = EmbeddingGenerator.generate(
            query
        )

        results = qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=embedding,
            limit=limit,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="session_id",
                        match=MatchValue(
                            value=session_id,
                        ),
                    )
                ]
            ),
        ).points

        if not results:
            logger.info(
                "No vector search results found."
            )
            return []

        db = SessionLocal()

        try:

            memories = []

            for point in results:

                logger.debug(
                    f"Qdrant Result | Payload={point.payload} | Score={point.score}"
                )

                memory_id = point.payload.get(
                    "memory_id"
                )

                # ------------------------------------
                # Update access statistics
                # ------------------------------------

                if memory_id is not None:

                    logger.debug(
                        f"Updating memory access | ID={memory_id}"
                    )

                    MemoryRepository.touch_memory(
                        db=db,
                        memory_id=memory_id,
                    )

                else:

                    logger.warning(
                        "memory_id missing in Qdrant payload"
                    )

                # ------------------------------------
                # Filter by similarity
                # ------------------------------------

                if point.score < score_threshold:

                    logger.debug(
                        "Skipped vector result due to low similarity score"
                    )

                    continue

                memories.append(
                    {
                        "memory_id": memory_id,
                        "memory": point.payload.get(
                            "memory"
                        ),
                        "memory_type": point.payload.get(
                            "memory_type"
                        ),
                        "importance": point.payload.get(
                            "importance",
                            1,
                        ),
                        "score": point.score,
                        "created_at": point.payload.get(
                            "created_at"
                        ),
                        "access_count": 0,
                    }
                )

            return memories

        finally:

            db.close()

    @staticmethod
    def format_memories(
        memories: list,
    ) -> str:

        if not memories:
            return ""

        formatted = []

        for memory in memories:

            memory_type = memory.get(
                "memory_type",
                "general",
            )

            confidence = memory.get(
                "confidence",
                0,
            )

            importance = memory.get(
                "importance",
                1,
            )

            formatted.append(
                f"""
[{memory_type}]
Memory:
{memory['memory']}

Confidence:
{confidence}

Importance:
{importance}/10
"""
            )

        return "\n".join(
            formatted
        )