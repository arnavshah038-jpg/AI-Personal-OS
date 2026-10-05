"""Decay, boost, forgetting, consolidation."""
import logging
import math
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from . import vector
from .llm import json_call
from .models import Memory, utcnow

log = logging.getLogger("aipos.lifecycle")


def boost(db: Session, m: Memory, amount: float = 0.15):
    m.strength = min(1.0, m.strength + amount)
    m.access_count += 1
    m.last_accessed = m.decayed_at = utcnow()
    db.commit()


def decay_all(db: Session) -> int:
    """Important memories dheere bhoolti hain. Idempotent: sirf last decay se ab tak ka time lagta hai."""
    now = utcnow()
    n = 0
    for m in db.query(Memory).filter(Memory.archived.is_(False)).all():
        days = (now - m.decayed_at).total_seconds() / 86400
        if days <= 0:
            continue
        rate = 0.08 * (1 - 0.8 * m.importance)
        m.strength *= math.exp(-rate * days)
        m.decayed_at = now
        n += 1
    db.commit()
    return n


def forget(db: Session) -> int:
    """Kamzor + kam important memories archive karke vector store se hata do."""
    rows = db.query(Memory).filter(
        Memory.archived.is_(False), Memory.strength < 0.1, Memory.importance < 0.6,
        Memory.kind != "persistent").all()
    for m in rows:
        m.archived = True
    db.commit()
    vector.delete([m.id for m in rows])
    return len(rows)


def consolidate(db: Session, user_id: str, min_batch: int = 10) -> int:
    """Purani episodic memories ko ek semantic memory mein merge karo."""
    from .store import remember  # circular import se bachne ke liye
    rows = (db.query(Memory).filter(Memory.user_id == user_id, Memory.kind == "episodic",
                                    Memory.archived.is_(False))
            .order_by(Memory.created_at).limit(min_batch * 2).all())
    if len(rows) < min_batch:
        return 0
    text = "\n".join(f"- {m.content}" for m in rows)
    out = json_call('Merge these episodic notes into 1-3 durable facts about the user. '
                    'JSON: {"facts": ["..."]}', text)
    facts = [f for f in out.get("facts", []) if isinstance(f, str)]
    if not facts:
        return 0
    for f in facts:
        remember(db, user_id, "semantic", f, importance=0.7)
    for m in rows:
        m.archived = True
    db.commit()
    vector.delete([m.id for m in rows])
    return len(rows)
