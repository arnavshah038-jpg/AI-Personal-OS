"""Context Optimizer: dedupe + token budget + compact prompt block."""
import re
from .ranker import Candidate

ORDER = ["persistent", "reflection", "semantic", "episodic"]
TITLES = {"persistent": "Known facts", "reflection": "Insights", "semantic": "Related knowledge", "episodic": "Past moments"}


def est_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def _words(t: str) -> set[str]:
    return set(re.findall(r"\w+", t.lower()))


def _similar(a: str, b: str, thr: float = 0.7) -> bool:
    wa, wb = _words(a), _words(b)
    return bool(wa and wb) and len(wa & wb) / len(wa | wb) >= thr


def optimize(ranked: list[Candidate], budget: int) -> tuple[str, list[Candidate]]:
    chosen: list[Candidate] = []
    used = 0
    for c in ranked:  # already sorted by score
        if any(_similar(c.content, k.content) for k in chosen):
            continue
        cost = est_tokens(c.content) + 2
        if used + cost > budget:
            continue
        chosen.append(c)
        used += cost
    lines = []
    for kind in ORDER:
        items = [c for c in chosen if c.kind == kind]
        if items:
            lines.append(f"{TITLES[kind]}:")
            lines += [f"- {c.content}" for c in items]
    return "\n".join(lines), chosen
