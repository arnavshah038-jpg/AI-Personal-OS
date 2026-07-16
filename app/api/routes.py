from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.memory_repository import MemoryRepository
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.forget import ForgetRequest, ForgetResponse
from app.services.chat_service import chat
from app.services.forget_service import forget

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "AI Personal OS is Running 🚀"
    }


# ---------------- CHAT ----------------

@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat_api(
    request: Request,
    body: ChatRequest,
):

    answer = chat(
        request=request,
        session_id=body.session_id,
        message=body.message,
    )

    return ChatResponse(
        response=answer,
    )


# ---------------- FORGET ----------------

@router.post(
    "/forget",
    response_model=ForgetResponse,
)
def forget_api(
    body: ForgetRequest,
):

    return forget(
        session_id=body.session_id,
        message=body.message,
    )


# ---------------- MEMORY TEST ----------------

@router.post("/memory/test")
def save_memory_test(
    db: Session = Depends(get_db),
):

    memory = MemoryRepository.save_memory(
        db=db,
        session_id="arnav",
        memory="My name is Arnav",
        importance=10,
    )

    return {
        "message": "Memory saved successfully!",
        "id": memory.id,
    }