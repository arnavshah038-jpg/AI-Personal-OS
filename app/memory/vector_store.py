from datetime import datetime
from uuid import uuid4

from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
    PointIdsList,
    PointStruct,
)

from app.core.qdrant_client import (
    COLLECTION_NAME,
    qdrant,
)
from app.memory.embedding import EmbeddingGenerator
from app.utils.logger import logger


class VectorStore:

    @staticmethod
    def save_memory(
        session_id: str,
        memory_id: int,
        memory: str,
        memory_type: str,
        importance: int = 1,
    ):

        embedding = EmbeddingGenerator.generate(
            memory
        )

        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "memory_id": memory_id,
                        "session_id": session_id,
                        "memory": memory,
                        "memory_type": memory_type,
                        "importance": importance,
                        "created_at": str(
                            datetime.utcnow()
                        ),
                        "access_count": 0,
                    },
                )
            ],
        )

        logger.info(
            "Memory vector saved to Qdrant."
        )

    @staticmethod
    def delete_memory(
        memory_id: int,
    ):

        points, _ = qdrant.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="memory_id",
                        match=MatchValue(
                            value=memory_id,
                        ),
                    )
                ]
            ),
            limit=100,
        )

        if not points:
            return

        ids = [
            point.id
            for point in points
        ]

        qdrant.delete(
            collection_name=COLLECTION_NAME,
            points_selector=PointIdsList(
                points=ids,
            ),
        )

        logger.info(
            "Memory vector deleted."
        )

    @staticmethod
    def update_memory(
        memory_id: int,
        session_id: str,
        memory: str,
        memory_type: str,
        importance: int = 1,
    ):

        VectorStore.delete_memory(
            memory_id=memory_id,
        )

        VectorStore.save_memory(
            session_id=session_id,
            memory_id=memory_id,
            memory=memory,
            memory_type=memory_type,
            importance=importance,
        )

        logger.info(
            "Memory vector updated."
        )

    @staticmethod
    def search_memories(
        session_id: str,
        query: str,
        limit: int = 5,
    ):

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
                ],
            ),
        )

        memories = []

        for point in results.points:

            memories.append(
                {
                    "memory_id": point.payload.get("memory_id"),
                    "memory": point.payload.get("memory", ""),
                    "memory_type": point.payload.get("memory_type", "fact"),
                    "importance": point.payload.get("importance", 1),
                    "score": point.score,
                }
            )

        return memories