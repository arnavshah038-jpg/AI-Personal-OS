from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.database.models.memory import Memory


class MemoryRepository:

    @staticmethod
    def save_memory(
        db: Session,
        session_id: str,
        memory: str,
        importance: int = 1,
        memory_type: str = "fact",
    ):

        memory_obj = Memory(
            session_id=session_id,
            memory=memory,
            importance=importance,
            memory_type=memory_type,
        )

        db.add(memory_obj)
        db.commit()
        db.refresh(memory_obj)

        return memory_obj

    @staticmethod
    def get_memories(
        db: Session,
        session_id: str,
    ):

        return (
            db.query(Memory)
            .filter(
                Memory.session_id == session_id,
            )
            .order_by(
                Memory.importance.desc(),
            )
            .all()
        )

    @staticmethod
    def get_memories_by_type(
        db: Session,
        session_id: str,
        memory_type: str,
    ):

        return (
            db.query(Memory)
            .filter(
                Memory.session_id == session_id,
                Memory.memory_type == memory_type,
            )
            .order_by(
                Memory.importance.desc(),
            )
            .all()
        )

    @staticmethod
    def format_memories(
        db: Session,
        session_id: str,
    ) -> str:

        memories = MemoryRepository.get_memories(
            db=db,
            session_id=session_id,
        )

        if not memories:
            return ""

        return "\n".join(
            f"- [{memory.memory_type}] {memory.memory}"
            for memory in memories
        )

    @staticmethod
    def get_memory_text(
        db: Session,
        session_id: str,
    ) -> str:

        memories = MemoryRepository.get_memories(
            db=db,
            session_id=session_id,
        )

        if not memories:
            return ""

        return "\n".join(
            memory.memory
            for memory in memories
        )

    @staticmethod
    def get_memory_by_id(
        db: Session,
        memory_id: int,
    ):

        return (
            db.query(Memory)
            .filter(
                Memory.id == memory_id,
            )
            .first()
        )

    @staticmethod
    def update_memory(
        db: Session,
        memory_id: int,
        memory: str,
        memory_type: str,
        importance: int,
    ):

        memory_obj = (
            db.query(Memory)
            .filter(
                Memory.id == memory_id,
            )
            .first()
        )

        if memory_obj is None:
            return None

        memory_obj.memory = memory
        memory_obj.memory_type = memory_type
        memory_obj.importance = importance
        memory_obj.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(memory_obj)

        return memory_obj

    @staticmethod
    def find_memory(
        db: Session,
        session_id: str,
        memory: str,
    ):

        return (
            db.query(Memory)
            .filter(
                Memory.session_id == session_id,
                Memory.memory == memory,
            )
            .first()
        )

    @staticmethod
    def memory_exists(
        db: Session,
        session_id: str,
        memory: str,
    ) -> bool:

        existing_memory = (
            db.query(Memory)
            .filter(
                Memory.session_id == session_id,
                Memory.memory == memory,
            )
            .first()
        )

        return existing_memory is not None

    @staticmethod
    def update_memory_by_text(
        db: Session,
        session_id: str,
        old_memory: str,
        new_memory: str,
        importance: int,
        memory_type: str = "fact",
    ):

        memory = (
            db.query(Memory)
            .filter(
                Memory.session_id == session_id,
                Memory.memory == old_memory,
            )
            .first()
        )

        if memory:

            memory.memory = new_memory
            memory.importance = importance
            memory.memory_type = memory_type
            memory.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(memory)

            return memory

        return None

    @staticmethod
    def delete_memory(
        db: Session,
        session_id: str,
        memory: str,
    ) -> bool:

        memory_obj = (
            db.query(Memory)
            .filter(
                Memory.session_id == session_id,
                Memory.memory == memory,
            )
            .first()
        )

        if memory_obj:

            db.delete(memory_obj)
            db.commit()

            return True

        return False

    @staticmethod
    def delete_memory_by_id(
        db: Session,
        memory_id: int,
    ):

        memory = (
            db.query(Memory)
            .filter(
                Memory.id == memory_id,
            )
            .first()
        )

        if memory is None:
            return None

        db.delete(memory)
        db.commit()

        return memory

    @staticmethod
    def touch_memory(
        db: Session,
        memory_id: int,
    ):

        memory = (
            db.query(Memory)
            .filter(
                Memory.id == memory_id,
            )
            .first()
        )

        if memory is None:
            return None

        memory.access_count += 1
        memory.last_accessed = datetime.utcnow()

        db.commit()
        db.refresh(memory)

        return memory

    @staticmethod
    def decay_memories(
        db: Session,
        days: int = 30,
    ):

        threshold = datetime.utcnow() - timedelta(days=days)

        memories = (
            db.query(Memory)
            .filter(
                Memory.last_accessed.is_not(None),
                Memory.last_accessed < threshold,
            )
            .all()
        )

        updated = 0

        for memory in memories:

            # Frequently used memories ko skip karo
            if memory.access_count >= 5:
                continue

            # Recently updated memories ko skip karo
            if (
                memory.updated_at is not None
                and memory.updated_at > threshold
            ):
                continue

            # Importance minimum 1 tak hi aaye
            if memory.importance > 1:

                memory.importance -= 1
                updated += 1

        db.commit()

        return updated

    @staticmethod
    def get_memory_stats(
        db: Session,
        session_id: str,
    ):

        memories = (
            db.query(Memory)
            .filter(
                Memory.session_id == session_id,
            )
            .all()
        )

        if not memories:

            return {
                "total_memories": 0,
                "avg_importance": 0,
                "memory_types": {},
                "most_accessed": None,
                "least_accessed": None,
            }

        memory_types = {}

        total_importance = 0

        for memory in memories:

            total_importance += memory.importance

            memory_types[memory.memory_type] = (
                memory_types.get(
                    memory.memory_type,
                    0,
                )
                + 1
            )

        avg_importance = round(
            total_importance / len(memories),
            2,
        )

        most_accessed = max(
            memories,
            key=lambda m: m.access_count,
        )

        least_accessed = min(
            memories,
            key=lambda m: m.access_count,
        )

        return {
            "total_memories": len(memories),
            "avg_importance": avg_importance,
            "memory_types": memory_types,
            "most_accessed": {
                "id": most_accessed.id,
                "memory": most_accessed.memory,
                "access_count": most_accessed.access_count,
            },
            "least_accessed": {
                "id": least_accessed.id,
                "memory": least_accessed.memory,
                "access_count": least_accessed.access_count,
            },
        }

    @staticmethod
    def boost_memories(
        db: Session,
        access_threshold: int = 10,
    ):

        memories = (
            db.query(Memory)
            .filter(
                Memory.access_count >= access_threshold,
                Memory.importance < 10,
            )
            .all()
        )

        updated = 0

        for memory in memories:

            memory.importance += 1
            memory.access_count = 0
            memory.updated_at = datetime.utcnow()

            updated += 1

        db.commit()

        return updated

    @staticmethod
    def get_importance_distribution(
        db: Session,
        session_id: str,
    ):

        memories = (
            db.query(Memory)
            .filter(
                Memory.session_id == session_id,
            )
            .all()
        )

        distribution = {}

        for memory in memories:

            importance = memory.importance

            distribution[importance] = (
                distribution.get(
                    importance,
                    0,
                )
                + 1
            )

        return distribution

    @staticmethod
    def get_memory_timeline(
        db: Session,
        session_id: str,
    ):

        memories = (
            db.query(Memory)
            .filter(
                Memory.session_id == session_id,
            )
            .all()
        )

        timeline = defaultdict(int)

        for memory in memories:

            day = (
                memory.created_at
                .date()
                .isoformat()
            )

            timeline[day] += 1

        return dict(
            sorted(
                timeline.items()
            )
        )

    @staticmethod
    def get_memory_health(
        db: Session,
        session_id: str,
    ):

        memories = (
            db.query(Memory)
            .filter(
                Memory.session_id == session_id,
            )
            .all()
        )

        total = len(memories)

        if total == 0:

            return {
                "health_score": 0,
                "active": 0,
                "stale": 0,
                "never_used": 0,
            }

        active = 0
        stale = 0
        never_used = 0

        threshold = datetime.utcnow() - timedelta(days=30)

        for memory in memories:

            if (memory.access_count or 0) == 0:

                never_used += 1

            if (
                memory.last_accessed
                and memory.last_accessed >= threshold
            ):

                active += 1

            elif (
                memory.last_accessed
                and memory.last_accessed < threshold
            ):

                stale += 1

        score = (
            (active * 0.7)
            + ((total - never_used) * 0.3)
        )

        health_score = round(
            min(score / total, 1.0) * 100,
            1,
        )

        return {
            "health_score": health_score,
            "active": active,
            "stale": stale,
            "never_used": never_used,
        }

    @staticmethod
    def increment_access_count(
        db,
        memory_id: int,
    ):

        memory = MemoryRepository.get_memory_by_id(
            db=db,
            memory_id=memory_id,
        )

        if memory is None:
            return

        memory.access_count += 1

        db.commit()

        db.refresh(memory)

        return memory