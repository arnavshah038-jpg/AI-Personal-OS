from app.database.session import SessionLocal
from app.repositories.episode_repository import EpisodeRepository
from app.repositories.memory_repository import MemoryRepository
from app.schemas.memory import MemoryDashboardResponse


class MemoryService:

    @staticmethod
    def get_dashboard(
        session_id: str,
    ) -> MemoryDashboardResponse:

        db = SessionLocal()

        try:

            identity = [
                m.memory
                for m in MemoryRepository.get_memories_by_type(
                    db,
                    session_id,
                    "identity",
                )
            ]

            preferences = [
                m.memory
                for m in MemoryRepository.get_memories_by_type(
                    db,
                    session_id,
                    "preference",
                )
            ]

            facts = [
                m.memory
                for m in MemoryRepository.get_memories_by_type(
                    db,
                    session_id,
                    "fact",
                )
            ]

            goals = [
                m.memory
                for m in MemoryRepository.get_memories_by_type(
                    db,
                    session_id,
                    "goal",
                )
            ]

            skills = [
                m.memory
                for m in MemoryRepository.get_memories_by_type(
                    db,
                    session_id,
                    "skill",
                )
            ]

            projects = [
                m.memory
                for m in MemoryRepository.get_memories_by_type(
                    db,
                    session_id,
                    "project",
                )
            ]

            episodes = EpisodeRepository.get_recent_episodes(
                db=db,
                session_id=session_id,
                limit=20,
            )

            return MemoryDashboardResponse(
                identity=identity,
                preferences=preferences,
                facts=facts,
                goals=goals,
                skills=skills,
                projects=projects,
                episodes=episodes,
            )

        finally:

            db.close()