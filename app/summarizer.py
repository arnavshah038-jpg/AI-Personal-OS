"""Trigger-based conversation summarization."""
from sqlalchemy import func
from sqlalchemy.orm import Session
from .config import settings
from .llm import respond
from .models import Message, Summary


def maybe_summarize(db: Session, session_id: str):
    n = db.query(func.count(Message.id)).filter(Message.session_id == session_id).scalar()
    if n == 0 or n % settings.summarize_every:
        return
    msgs = (db.query(Message).filter(Message.session_id == session_id)
            .order_by(Message.id.desc()).limit(settings.summarize_every).all())[::-1]
    prev = db.get(Summary, session_id)
    transcript = "\n".join(f"{m.role}: {m.content}" for m in msgs)
    text = respond("Update the running summary of this conversation in under 120 words. Keep facts, decisions, open questions.",
                   [{"role": "user", "content": f"Previous summary:\n{prev.text if prev else '(none)'}\n\nNew messages:\n{transcript}"}])
    if prev:
        prev.text = text
    else:
        db.add(Summary(session_id=session_id, text=text))
    db.commit()
