from app.database.session import SessionLocal
from app.memory.episode_retriever import EpisodeRetriever
from app.memory.memory_ranker import MemoryRanker
from app.memory.reflection_retriever import ReflectionRetriever
from app.memory.vector_search import VectorSearch
from app.repositories.memory_repository import MemoryRepository


class HybridRetriever:

    @staticmethod
    def retrieve(
        session_id: str,
        query: str,
    ) -> str:

        db = SessionLocal()

        try:

            sections = []

            # ----------------------------------
            # Semantic Memory
            # ----------------------------------

            memories = VectorSearch.search(
                session_id=session_id,
                query=query,
            )

            # Update access statistics
            for memory in memories:

                MemoryRepository.touch_memory(
                    db=db,
                    memory_id=memory["memory_id"],
                )

            # Rank memories
            memories = MemoryRanker.rank(
                memories
            )

            # Keep only Top 5
            memories = memories[:5]

            formatted_memories = (
                VectorSearch.format_memories(
                    memories
                )
            )

            if formatted_memories:

                sections.append(
                    "Relevant Semantic Memories:\n"
                    + formatted_memories
                )

            # ----------------------------------
            # Episodic Memory
            # ----------------------------------

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

            # ----------------------------------
            # Reflection Memory
            # ----------------------------------

            reflections = ReflectionRetriever.retrieve(
                session_id=session_id,
                limit=3,
            )

            if reflections:

                sections.append(
                    "Long-Term Reflections:\n"
                    + reflections
                )

            if not sections:
                return ""

            return "\n\n".join(
                sections
            )

        finally:

            db.close()