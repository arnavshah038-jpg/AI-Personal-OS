from pydantic import BaseModel


class MemoryDecision(BaseModel):
    action: str
    memory_id: int | None = None
    new_memory: str | None = None