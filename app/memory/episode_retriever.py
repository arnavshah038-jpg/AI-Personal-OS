from sqlalchemy.orm import Session

from app.repositories.episode_repository import EpisodeRepository


class EpisodeRetriever:

    @staticmethod
    def retrieve(
        db: Session,
        session_id: str,
        query: str,
    ) -> str:

        episodes = EpisodeRepository.search_episodes(
            db=db,
            session_id=session_id,
            keyword=query,
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