from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models.episode import Episode


class EpisodeRepository:

    @staticmethod
    def save_episode(
        db: Session,
        session_id: str,
        title: str,
        description: str,
        event_type: str,
        importance: int = 5,
        event_date=None,
    ):

        episode = Episode(
            session_id=session_id,
            title=title,
            description=description,
            event_type=event_type,
            importance=importance,
            event_date=event_date,
        )

        db.add(episode)
        db.commit()
        db.refresh(episode)

        return episode

    @staticmethod
    def get_episodes(
        db: Session,
        session_id: str,
    ):

        return (
            db.query(Episode)
            .filter(
                Episode.session_id == session_id,
            )
            .order_by(
                Episode.created_at.desc(),
            )
            .all()
        )

    @staticmethod
    def get_recent_episodes(
        db: Session,
        session_id: str,
        limit: int = 10,
    ):

        return (
            db.query(Episode)
            .filter(
                Episode.session_id == session_id,
            )
            .order_by(
                Episode.created_at.desc(),
            )
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_episode_by_id(
        db: Session,
        episode_id: int,
    ):

        return (
            db.query(Episode)
            .filter(
                Episode.id == episode_id,
            )
            .first()
        )

    @staticmethod
    def update_episode(
        db: Session,
        episode_id: int,
        title: str,
        description: str,
        event_type: str,
        importance: int,
    ):

        episode = (
            db.query(Episode)
            .filter(
                Episode.id == episode_id,
            )
            .first()
        )

        if episode is None:
            return None

        episode.title = title
        episode.description = description
        episode.event_type = event_type
        episode.importance = importance
        episode.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(episode)

        return episode

    @staticmethod
    def delete_episode(
        db: Session,
        episode_id: int,
    ):

        episode = (
            db.query(Episode)
            .filter(
                Episode.id == episode_id,
            )
            .first()
        )

        if episode is None:
            return False

        db.delete(episode)
        db.commit()

        return True

    @staticmethod
    def format_episodes(
        db: Session,
        session_id: str,
        limit: int = 10,
    ) -> str:

        episodes = EpisodeRepository.get_recent_episodes(
            db=db,
            session_id=session_id,
            limit=limit,
        )

        if not episodes:
            return ""

        return "\n\n".join(
            (
                f"Title: {episode.title}\n"
                f"Type: {episode.event_type}\n"
                f"Description: {episode.description}"
            )
            for episode in episodes
        )

    @staticmethod
    def search_episodes(
        db: Session,
        session_id: str,
        keyword: str,
    ):

        return (
            db.query(Episode)
            .filter(
                Episode.session_id == session_id,
                Episode.description.ilike(f"%{keyword}%"),
            )
            .order_by(
                Episode.created_at.desc(),
            )
            .all()
        )