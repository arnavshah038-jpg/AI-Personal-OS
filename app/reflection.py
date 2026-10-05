"""Reflection Generator: episodic memories -> higher-level insights."""
from sqlalchemy.orm import Session
from .llm import json_call
from .models import Memory
from .store import remember


def generate_reflections(db: Session, user_id: str, n: int = 12) -> int:
    rows = (db.query(Memory).filter(Memory.user_id == user_id, Memory.kind == "episodic",
                                    Memory.archived.is_(False))
            .order_by(Memory.created_at.desc()).limit(n).all())
    if len(rows) < 4:
        return 0
    out = json_call('From these interaction notes infer 1-3 higher-level insights about the user\'s '
                    'goals, style or recurring needs. JSON: {"insights": ["..."]}',
                    "\n".join(f"- {m.content}" for m in rows))
    count = 0
    for i in out.get("insights", []):
        if isinstance(i, str) and remember(db, user_id, "reflection", i, importance=0.8):
            count += 1
    return count


def should_reflect(db: Session, user_id: str, every: int) -> bool:
    total = db.query(Memory).filter(Memory.user_id == user_id, Memory.kind == "episodic").count()
    return total > 0 and total % every == 0
