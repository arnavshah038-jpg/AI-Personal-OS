import csv
import io

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.database.session import SessionLocal
from app.memory.vector_store import VectorStore
from app.reflection.reflection_service import ReflectionService
from app.repositories.memory_repository import MemoryRepository
from app.repositories.reflection_repository import ReflectionRepository
from app.schemas.memory import (
    MemoryDashboardResponse,
    MemoryResponse,
)
from app.services.memory_service import MemoryService

router = APIRouter(
    prefix="/memories",
    tags=["Memory Dashboard"],
)


# -------------------------------------------------------
# Request Model
# -------------------------------------------------------

class MemoryCreateRequest(BaseModel):

    session_id: str
    memory: str
    memory_type: str
    importance: int = 5


# -------------------------------------------------------
# Memory Dashboard
# -------------------------------------------------------

@router.get(
    "/dashboard",
    response_model=MemoryDashboardResponse,
)
def memory_dashboard(
    session_id: str,
):

    return MemoryService.get_dashboard(
        session_id=session_id,
    )


# -------------------------------------------------------
# Create Memory
# -------------------------------------------------------

@router.post("/")
def create_memory(
    request: MemoryCreateRequest,
):

    db = SessionLocal()

    try:

        memory = MemoryRepository.save_memory(
            db=db,
            session_id=request.session_id,
            memory=request.memory,
            importance=request.importance,
            memory_type=request.memory_type,
        )

        return {
            "message": "Memory created successfully.",
            "id": memory.id,
        }

    finally:

        db.close()


# -------------------------------------------------------
# Update Memory
# -------------------------------------------------------

@router.put("/{memory_id}")
def update_memory(
    memory_id: int,
    request: MemoryCreateRequest,
):

    db = SessionLocal()

    try:

        memory = MemoryRepository.get_memory_by_id(
            db=db,
            memory_id=memory_id,
        )

        if memory is None:

            raise HTTPException(
                status_code=404,
                detail="Memory not found.",
            )

        updated_memory = MemoryRepository.update_memory(
            db=db,
            memory_id=memory_id,
            memory=request.memory,
            memory_type=request.memory_type,
            importance=request.importance,
        )

        # Update vector in Qdrant
        VectorStore.update_memory(
            memory_id=updated_memory.id,
            session_id=updated_memory.session_id,
            memory=updated_memory.memory,
            memory_type=updated_memory.memory_type,
            importance=updated_memory.importance,
        )

        return {
            "message": "Memory updated successfully.",
            "id": updated_memory.id,
        }

    finally:

        db.close()


# -------------------------------------------------------
# Get All Memories
# -------------------------------------------------------

@router.get(
    "/",
    response_model=list[MemoryResponse],
)
def get_memories(
    session_id: str,
):

    db = SessionLocal()

    try:

        memories = MemoryRepository.get_memories(
            db=db,
            session_id=session_id,
        )

        return memories

    finally:

        db.close()


# -------------------------------------------------------
# Semantic Memory Search
# -------------------------------------------------------

@router.get("/search")
def search_memories(
    session_id: str,
    query: str,
    limit: int = 5,
):

    db = SessionLocal()

    try:

        memories = VectorStore.search_memories(
            session_id=session_id,
            query=query,
            limit=limit,
        )

        for memory in memories:

            MemoryRepository.increment_access_count(
                db=db,
                memory_id=memory["memory_id"],
            )

        return memories

    finally:

        db.close()


# -------------------------------------------------------
# Export Memories (CSV)
# -------------------------------------------------------

@router.get("/export")
def export_memories(
    session_id: str,
):

    db = SessionLocal()

    try:

        memories = MemoryRepository.get_memories(
            db=db,
            session_id=session_id,
        )

        output = io.StringIO()

        writer = csv.writer(output)

        writer.writerow(
            [
                "ID",
                "Memory",
                "Type",
                "Importance",
                "Access Count",
                "Created At",
            ]
        )

        for memory in memories:

            writer.writerow(
                [
                    memory.id,
                    memory.memory,
                    memory.memory_type,
                    memory.importance,
                    memory.access_count,
                    memory.created_at,
                ]
            )

        output.seek(0)

        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition":
                "attachment; filename=memories.csv"
            },
        )

    finally:

        db.close()


# -------------------------------------------------------
# AI Reflection
# -------------------------------------------------------

@router.get("/reflection")
def generate_reflection():

    reflection = ReflectionService.generate_reflection()

    return {
        "reflection": reflection,
    }


# -------------------------------------------------------
# Reflection History
# -------------------------------------------------------

@router.get("/reflections")
def get_reflections():

    db = SessionLocal()

    try:

        reflections = (
            ReflectionRepository.get_recent_reflections(
                db=db,
                session_id="arnav",
                limit=20,
            )
        )

        return [
            {
                "id": reflection.id,
                "reflection": reflection.reflection,
                "importance": reflection.importance,
                "created_at": reflection.created_at,
            }
            for reflection in reflections
        ]

    finally:

        db.close()


# -------------------------------------------------------
# Get Memory By ID
# -------------------------------------------------------

@router.get(
    "/{memory_id}",
    response_model=MemoryResponse,
)
def get_memory(
    memory_id: int,
):

    db = SessionLocal()

    try:

        memory = MemoryRepository.get_memory_by_id(
            db=db,
            memory_id=memory_id,
        )

        if memory is None:

            raise HTTPException(
                status_code=404,
                detail="Memory not found.",
            )

        return memory

    finally:

        db.close()


# -------------------------------------------------------
# Delete Memory
# -------------------------------------------------------

@router.delete(
    "/{memory_id}",
)
def delete_memory(
    memory_id: int,
):

    db = SessionLocal()

    try:

        memory = MemoryRepository.get_memory_by_id(
            db=db,
            memory_id=memory_id,
        )

        if memory is None:

            raise HTTPException(
                status_code=404,
                detail="Memory not found.",
            )

        VectorStore.delete_memory(
            memory_id=memory.id,
        )

        MemoryRepository.delete_memory_by_id(
            db=db,
            memory_id=memory.id,
        )

        return {
            "message": "Memory deleted successfully."
        }

    finally:

        db.close()