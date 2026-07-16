from app.database.session import SessionLocal
from app.repositories.reflection_repository import (
    ReflectionRepository,
)


class ReflectionRetriever:

    @staticmethod
    def retrieve(
        session_id: str,
        limit: int = 5,
    ) -> str:

        db = SessionLocal()

        try:

            reflections = (
                ReflectionRepository.get_recent_reflections(
                    db=db,
                    session_id=session_id,
                    limit=limit,
                )
            )

            if not reflections:
                return ""

            return "\n".join(
                f"- {reflection.reflection}"
                for reflection in reflections
            )

        finally:

            db.close()