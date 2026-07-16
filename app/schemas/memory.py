from datetime import datetime

from pydantic import BaseModel


# ---------------------------------------
# Single Memory Response
# ---------------------------------------

class MemoryResponse(BaseModel):

    id: int
    session_id: str
    memory: str
    memory_type: str
    importance: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------
# Episode Response
# ---------------------------------------

class EpisodeResponse(BaseModel):

    id: int
    title: str
    description: str
    event_type: str
    importance: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------
# Memory Dashboard Response
# ---------------------------------------

class MemoryDashboardResponse(BaseModel):

    identity: list[str]
    preferences: list[str]
    facts: list[str]
    goals: list[str]
    skills: list[str]
    projects: list[str]
    episodes: list[EpisodeResponse]