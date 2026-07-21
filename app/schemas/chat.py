from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):

    session_id: str
    message: str



class MemorySource(BaseModel):

    memory: str
    type: str
    score: float
    confidence: float
    importance: int
    reason: str



class ChatResponse(BaseModel):

    response: str
    sources: Optional[List[MemorySource]] = []