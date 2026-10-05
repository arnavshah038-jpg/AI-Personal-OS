"""Memory Ranker: similarity + recency + importance*strength + kind weight."""
import math
from dataclasses import dataclass
from datetime import datetime, timezone

KIND_WEIGHT = {"persistent": 1.0, "reflection": 0.8, "semantic": 0.7, "episodic": 0.5}
HALF_LIFE_DAYS = 14.0


@dataclass
class Candidate:
    id: str
    kind: str
    content: str
    importance: float
    strength: float
    created_at: datetime
    similarity: float = 0.0
    score: float = 0.0


def score(c: Candidate, now: datetime | None = None) -> float:
    now = now or datetime.now(timezone.utc)
    age_days = max((now - c.created_at).total_seconds() / 86400, 0)
    recency = 0.5 ** (age_days / HALF_LIFE_DAYS)
    return (
        0.50 * c.similarity
        + 0.15 * recency
        + 0.25 * c.importance * c.strength
        + 0.10 * KIND_WEIGHT.get(c.kind, 0.5)
    )


def rank(cands: list[Candidate], now: datetime | None = None) -> list[Candidate]:
    for c in cands:
        c.score = score(c, now)
    return sorted(cands, key=lambda c: c.score, reverse=True)
