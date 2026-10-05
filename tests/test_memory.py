from datetime import datetime, timedelta, timezone
from app.ranker import Candidate, rank
from app.optimizer import optimize, est_tokens

NOW = datetime.now(timezone.utc)


def mk(id, kind, text, sim, imp=0.5, age=0):
    return Candidate(id, kind, text, imp, 1.0, NOW - timedelta(days=age), sim)


def test_similarity_dominates():
    r = rank([mk("a", "episodic", "x", 0.2), mk("b", "episodic", "y", 0.9)], NOW)
    assert r[0].id == "b"


def test_recent_beats_old_when_equal():
    r = rank([mk("old", "semantic", "x", 0.5, age=60), mk("new", "semantic", "y", 0.5, age=0)], NOW)
    assert r[0].id == "new"


def test_optimizer_dedupes_and_respects_budget():
    ranked = rank([
        mk("1", "persistent", "User likes python and fastapi a lot", 0.9),
        mk("2", "semantic", "User likes python and fastapi a lot!", 0.8),
        mk("3", "episodic", "word " * 400, 0.7),
    ], NOW)
    block, chosen = optimize(ranked, budget=50)
    assert [c.id for c in chosen] == ["1"]
    assert est_tokens(block) <= 50
    assert "Known facts" in block
