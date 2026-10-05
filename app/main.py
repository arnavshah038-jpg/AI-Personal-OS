import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from . import cache, lifecycle, vector
from .config import settings
from .db import Base, SessionLocal, engine, get_db
from .llm import respond
from .models import ChatSession, Memory, Message, Summary
from .optimizer import optimize
from .reflection import generate_reflections, should_reflect
from .retrieval import retrieve
from .store import extract_and_store_facts, store_episode
from .summarizer import maybe_summarize

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("aipos")

SYSTEM = ("You are a personal AI assistant with long-term memory. Use the memory block naturally "
          "when relevant; never claim to remember things not listed there.")


def maintenance_once():
    with SessionLocal() as db:
        d, f = lifecycle.decay_all(db), lifecycle.forget(db)
        log.info("maintenance: decayed=%s forgotten=%s", d, f)
        return {"decayed": d, "forgotten": f}


async def _maintenance_loop():
    while True:
        await asyncio.sleep(3600)
        try:
            await asyncio.to_thread(maintenance_once)
        except Exception:
            log.exception("maintenance failed")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    vector.ensure_collection()
    task = asyncio.create_task(_maintenance_loop())
    yield
    task.cancel()


app = FastAPI(title="AI Personal OS", version="1.0", lifespan=lifespan)


@app.exception_handler(Exception)
async def on_error(request: Request, exc: Exception):
    log.exception("unhandled error on %s", request.url.path)
    return JSONResponse({"error": "internal_error", "detail": str(exc)[:200]}, status_code=500)


def auth(x_api_key: str = Header(default="")):
    if settings.app_api_key and x_api_key != settings.app_api_key:
        raise HTTPException(401, "invalid api key")


class ChatIn(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    message: str = Field(min_length=1, max_length=4000)
    user_id: str = "default"


class ChatOut(BaseModel):
    reply: str
    memories_used: list[dict]


@app.get("/health")
def health():
    return {"status": "ok"}


def post_chat(session_id: str, user_id: str, user_msg: str, reply: str):
    """Background: memory writes, reflection, summary (user ko wait nahi karna padta)."""
    try:
        with SessionLocal() as db:
            extract_and_store_facts(db, user_id, user_msg)
            store_episode(db, user_id, user_msg, reply)
            if should_reflect(db, user_id, settings.reflect_every):
                generate_reflections(db, user_id)
            maybe_summarize(db, session_id)
    except Exception:
        log.exception("post_chat failed")


@app.post("/chat", response_model=ChatOut, dependencies=[Depends(auth)])
def chat(body: ChatIn, bg: BackgroundTasks, db: Session = Depends(get_db)):
    if cache.hit_rate_limit(body.user_id):
        raise HTTPException(429, "too many requests")
    if not db.get(ChatSession, body.session_id):
        db.add(ChatSession(id=body.session_id, user_id=body.user_id))
        db.commit()
    db.add(Message(session_id=body.session_id, role="user", content=body.message))
    db.commit()

    try:
        ranked = retrieve(db, body.user_id, body.message)
    except Exception:
        log.exception("retrieval failed, continuing without memory")
        ranked = []
    block, used = optimize(ranked, settings.context_token_budget)

    summary = db.get(Summary, body.session_id)
    history = (db.query(Message).filter(Message.session_id == body.session_id)
               .order_by(Message.id.desc()).limit(10).all())[::-1]
    instructions = SYSTEM
    if summary:
        instructions += f"\n\nConversation summary so far:\n{summary.text}"
    if block:
        instructions += f"\n\nMemory:\n{block}"

    try:
        reply = respond(instructions, [{"role": m.role, "content": m.content} for m in history])
    except Exception as e:
        log.exception("llm failed")
        raise HTTPException(502, f"LLM error: {str(e)[:150]}")

    db.add(Message(session_id=body.session_id, role="assistant", content=reply))
    db.commit()
    for c in used:  # jo memory kaam aayi, usse boost
        if (m := db.get(Memory, c.id)):
            lifecycle.boost(db, m, 0.1)
    bg.add_task(post_chat, body.session_id, body.user_id, body.message, reply)
    return ChatOut(reply=reply, memories_used=[{"kind": c.kind, "content": c.content, "score": round(c.score, 3)} for c in used])


@app.get("/sessions/{session_id}/history", dependencies=[Depends(auth)])
def history(session_id: str, db: Session = Depends(get_db)):
    rows = db.query(Message).filter(Message.session_id == session_id).order_by(Message.id).all()
    return [{"role": m.role, "content": m.content, "at": m.created_at} for m in rows]


@app.get("/memories", dependencies=[Depends(auth)])
def memories(user_id: str = "default", db: Session = Depends(get_db)):
    rows = (db.query(Memory).filter(Memory.user_id == user_id, Memory.archived.is_(False))
            .order_by(Memory.importance.desc(), Memory.created_at.desc()).limit(100).all())
    return [{"id": m.id, "kind": m.kind, "content": m.content, "importance": m.importance,
             "strength": round(m.strength, 3), "accessed": m.access_count} for m in rows]


@app.post("/maintenance/run", dependencies=[Depends(auth)])
def run_maintenance(user_id: str = "default", db: Session = Depends(get_db)):
    out = maintenance_once()
    out["consolidated"] = lifecycle.consolidate(db, user_id)
    out["reflections"] = generate_reflections(db, user_id)
    return out
