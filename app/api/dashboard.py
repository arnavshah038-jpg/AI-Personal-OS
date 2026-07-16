from fastapi import APIRouter

from app.database.session import SessionLocal
from app.repositories.memory_repository import MemoryRepository

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/health")
def dashboard_health():

    return {
        "status": "ok",
        "message": "Dashboard API Working",
    }


@router.get("/memories")
def get_memories():

    db = SessionLocal()

    try:

        memories = MemoryRepository.get_memories(
            db=db,
            session_id="arnav",
        )

        return [
            {
                "id": memory.id,
                "memory": memory.memory,
                "memory_type": memory.memory_type,
                "importance": memory.importance,
                "access_count": memory.access_count,
                "last_accessed": memory.last_accessed,
                "created_at": memory.created_at,
            }
            for memory in memories
        ]

    finally:

        db.close()


@router.get("/stats")
def get_dashboard_stats():

    db = SessionLocal()

    try:

        return MemoryRepository.get_memory_stats(
            db=db,
            session_id="arnav",
        )

    finally:

        db.close()


@router.get("/top-memories")
def get_top_memories():

    db = SessionLocal()

    try:

        memories = MemoryRepository.get_memories(
            db=db,
            session_id="arnav",
        )

        memories = sorted(
            memories,
            key=lambda memory: memory.access_count or 0,
            reverse=True,
        )[:10]

        return [
            {
                "memory": memory.memory,
                "access_count": memory.access_count or 0,
                "importance": memory.importance,
            }
            for memory in memories
        ]

    finally:

        db.close()


@router.get("/importance-distribution")
def get_importance_distribution():

    db = SessionLocal()

    try:

        return MemoryRepository.get_importance_distribution(
            db=db,
            session_id="arnav",
        )

    finally:

        db.close()


@router.get("/memory-timeline")
def get_memory_timeline():

    db = SessionLocal()

    try:

        return MemoryRepository.get_memory_timeline(
            db=db,
            session_id="arnav",
        )

    finally:

        db.close()


@router.get("/memory-health")
def get_memory_health():

    db = SessionLocal()

    try:

        return MemoryRepository.get_memory_health(
            db=db,
            session_id="arnav",
        )

    finally:

        db.close()