"""Memory writes: persistent / semantic / episodic / reflection."""
from uuid import uuid4
from sqlalchemy.orm import Session
from . import vector
from .embeddings import embed
from .lifecycle import boost
from .llm import json_call
from .models import Memory

EXTRACT_PROMPT = (
    "Extract durable facts about the USER from this message (name, job, preferences, goals, "
    "relationships, habits). Skip small talk. "
    'JSON: {"facts": [{"text": "...", "importance": 0.0-1.0}]}. Empty list if none.'
)


def remember(db: Session, user_id: str, kind: str, content: str, importance: float = 0.5) -> Memory | None:
    content = content.strip()
    if not content:
        return None
    vec = embed(content)
    if kind in ("persistent", "semantic"):  # duplicate fact ko dobara mat likho, boost karo
        hits = vector.search(vec, user_id, limit=1)
        if hits and hits[0].score > 0.93 and (m := db.get(Memory, str(hits[0].id))) and not m.archived:
            boost(db, m)
            return m
    m = Memory(id=str(uuid4()), user_id=user_id, kind=kind, content=content, importance=importance)
    db.add(m)
    db.commit()
    vector.upsert(m.id, vec, {"user_id": user_id, "kind": kind})
    return m


def extract_and_store_facts(db: Session, user_id: str, user_message: str) -> int:
    out = json_call(EXTRACT_PROMPT, user_message)
    n = 0
    for f in out.get("facts", []):
        if isinstance(f, dict) and f.get("text"):
            imp = float(f.get("importance", 0.6))
            remember(db, user_id, "persistent" if imp >= 0.8 else "semantic", f["text"], imp)
            n += 1
    return n


def store_episode(db: Session, user_id: str, user_msg: str, reply: str):
    summary = f"User said: {user_msg[:200]} | Assistant replied: {reply[:200]}"
    remember(db, user_id, "episodic", summary, importance=0.3)
