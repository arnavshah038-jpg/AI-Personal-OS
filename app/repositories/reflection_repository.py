from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models.reflection import Reflection


class ReflectionRepository:

    @staticmethod
    def save_reflection(
        db: Session,
        session_id: str,
        reflection: str,
        importance: int = 5,
    ):

        reflection_obj = Reflection(
            session_id=session_id,
            reflection=reflection,
            importance=importance,
        )

        db.add(reflection_obj)
        db.commit()
        db.refresh(reflection_obj)

        return reflection_obj

    @staticmethod
    def get_latest_reflection(
        db: Session,
        session_id: str,
    ):

        return (
            db.query(Reflection)
            .filter(
                Reflection.session_id == session_id,
            )
            .order_by(
                Reflection.created_at.desc(),
            )
            .first()
        )

    @staticmethod
    def get_reflections(
        db: Session,
        session_id: str,
    ):

        return (
            db.query(Reflection)
            .filter(
                Reflection.session_id == session_id,
            )
            .order_by(
                Reflection.created_at.desc(),
            )
            .all()
        )

    @staticmethod
    def get_recent_reflections(
        db: Session,
        session_id: str,
        limit: int = 10,
    ):

        return (
            db.query(Reflection)
            .filter(
                Reflection.session_id == session_id,
            )
            .order_by(
                Reflection.created_at.desc(),
            )
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_reflection_by_id(
        db: Session,
        reflection_id: int,
    ):

        return (
            db.query(Reflection)
            .filter(
                Reflection.id == reflection_id,
            )
            .first()
        )

    @staticmethod
    def update_reflection(
        db: Session,
        reflection_id: int,
        reflection: str,
        importance: int,
    ):

        reflection_obj = (
            db.query(Reflection)
            .filter(
                Reflection.id == reflection_id,
            )
            .first()
        )

        if reflection_obj is None:

            return None

        reflection_obj.reflection = reflection
        reflection_obj.importance = importance
        reflection_obj.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(reflection_obj)

        return reflection_obj

    @staticmethod
    def delete_reflection(
        db: Session,
        reflection_id: int,
    ):

        reflection_obj = (
            db.query(Reflection)
            .filter(
                Reflection.id == reflection_id,
            )
            .first()
        )

        if reflection_obj is None:

            return False

        db.delete(reflection_obj)
        db.commit()

        return True

    @staticmethod
    def format_reflections(
        db: Session,
        session_id: str,
        limit: int = 10,
    ) -> str:

        reflections = (
            ReflectionRepository.get_recent_reflections(
                db=db,
                session_id=session_id,
                limit=limit,
            )
        )

        if not reflections:

            return ""

        return "\n\n".join(
            f"- {reflection.reflection}"
            for reflection in reflections
        )