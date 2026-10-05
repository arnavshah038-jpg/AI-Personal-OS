"""Hybrid retrieval: semantic (vector) + episodic + reflection + always-on persistent facts."""
from sqlalchemy.orm import Session
from .embeddings import embed
from . import vector
from .models import Memory
from .ranker import Candidate, rank


def _cand(m: Memory, sim: float) -> Candidate:
    return Candidate(m.id, m.kind, m.content, m.importance, m.strength, m.created_at, sim)


def retrieve(db: Session, user_id: str, query: str, k: int = 20) -> list[Candidate]:
    sims = {str(h.id): h.score for h in vector.search(embed(query), user_id, limit=k)}
    rows = db.query(Memory).filter(Memory.id.in_(sims), Memory.archived.is_(False)).all() if sims else []
    cands = {m.id: _cand(m, sims[m.id]) for m in rows}
    persistent = (db.query(Memory).filter(Memory.user_id == user_id, Memory.kind == "persistent",
                                          Memory.archived.is_(False))
                  .order_by(Memory.importance.desc()).limit(5).all())
    for m in persistent:
        cands.setdefault(m.id, _cand(m, 0.3))
    return rank(list(cands.values()))
