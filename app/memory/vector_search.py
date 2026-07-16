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
            print("No vector search results found.")
            return []

        db = SessionLocal()

        try:

            memories = []

            for point in results:

                print("=" * 60)
                print("Payload:", point.payload)
                print("Score:", point.score)

                memory_id = point.payload.get(
                    "memory_id"
                )

                print("Memory ID:", memory_id)

                # ------------------------------------
                # Update access statistics
                # ------------------------------------

                if memory_id is not None:

                    print(
                        f"Touching memory {memory_id}"
                    )

                    MemoryRepository.touch_memory(
                        db=db,
                        memory_id=memory_id,
                    )

                else:

                    print(
                        "memory_id NOT FOUND in payload!"
                    )

                # ------------------------------------
                # Filter by similarity
                # ------------------------------------

                if point.score < score_threshold:

                    print(
                        "Skipped (score below threshold)"
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

            formatted.append(
                f"[{memory_type}] {memory['memory']}"
            )

        return "\n".join(
            formatted
        )