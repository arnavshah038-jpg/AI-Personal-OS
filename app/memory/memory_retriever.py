from app.database.session import SessionLocal

from app.memory.vector_search import VectorSearch
from app.memory.memory_ranker import MemoryRanker
from app.memory.memory_confidence import MemoryConfidence
from app.memory.episode_retriever import EpisodeRetriever
from app.memory.reflection_retriever import ReflectionRetriever

from app.repositories.memory_repository import MemoryRepository
from app.utils.logger import logger


class MemoryRetriever:

    MAX_MEMORIES = 5
    MAX_REFLECTIONS = 3

    MIN_CONFIDENCE = 0.45

    @staticmethod
    def retrieve(
        session_id: str,
        query: str,
    ) -> dict:

        db = SessionLocal()

        try:

            sections = []
            sources = []

            logger.info(
                f"Memory retrieval started | Session={session_id}"
            )

            # ==================================
            # 1. Semantic Search
            # ==================================

            memories = VectorSearch.search(
                session_id=session_id,
                query=query,
            )

            if memories:

                memories = MemoryRanker.rank(
                    memories
                )

                filtered = []

                for memory in memories:

                    if memory.get("memory_id"):

                        MemoryRepository.touch_memory(
                            db=db,
                            memory_id=memory["memory_id"],
                        )

                    confidence = (
                        MemoryConfidence.calculate(
                            memory
                        )
                    )

                    memory["confidence"] = confidence

                    if confidence >= MemoryRetriever.MIN_CONFIDENCE:

                        filtered.append(
                            memory
                        )

                filtered.sort(
                    key=lambda x: x["confidence"],
                    reverse=True,
                )

                filtered = filtered[
                    :MemoryRetriever.MAX_MEMORIES
                ]

                # ----------------------------------
                # Fallback Retrieval
                # ----------------------------------

                if not filtered and memories:

                    best_memory = max(
                        memories,
                        key=lambda x: x["confidence"],
                    )

                    logger.info(
                        "No memory passed confidence threshold. Using fallback memory."
                    )

                    filtered = [best_memory]

                if filtered:

                    formatted = (
                        VectorSearch.format_memories(
                            filtered
                        )
                    )

                    sections.append(
                        "Relevant Memories:\n"
                        + formatted
                    )

                    for memory in filtered:

                        sources.append(
                            {
                                "memory": memory["memory"],
                                "type": memory["memory_type"],
                                "score": round(
                                    memory["score"],
                                    3,
                                ),
                                "confidence": memory["confidence"],
                                "importance": memory["importance"],
                                "reason": "Semantic memory match",
                            }
                        )

            # ==================================
            # 2. Episodic Memory
            # ==================================

            episodes = EpisodeRetriever.retrieve(
                db=db,
                session_id=session_id,
                query=query,
            )

            if episodes:

                sections.append(
                    "Relevant Episodes:\n"
                    + episodes
                )

            # ==================================
            # 3. Reflection Memory
            # ==================================

            reflections = (
                ReflectionRetriever.retrieve(
                    session_id=session_id,
                    limit=MemoryRetriever.MAX_REFLECTIONS,
                )
            )

            if reflections:

                sections.append(
                    "Long Term Reflections:\n"
                    + reflections
                )

            if not sections:

                logger.info(
                    "No relevant memories found."
                )

                return {
                    "context": "",
                    "sources": [],
                }

            logger.info(
                f"Retrieved {len(sources)} semantic memories."
            )

            logger.info(
                "Memory retrieval completed."
            )

            return {
                "context": "\n\n".join(
                    sections
                ),
                "sources": sources,
            }

        except Exception as e:

            logger.exception(
                f"Memory retrieval failed: {e}"
            )

            return {
                "context": "",
                "sources": [],
            }

        finally:

            db.close()