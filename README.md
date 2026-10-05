# AI Personal OS

A memory-augmented conversational AI platform. It remembers who you are across sessions using a multi-layered memory system, hybrid retrieval, and automatic reflection.

Stack: Python · FastAPI · OpenAI API (Responses + Embeddings) · PostgreSQL · Redis · Qdrant · Streamlit · Docker Compose

No PyTorch or local ML models: embeddings come from the OpenAI API, so the Docker image stays small.

## Features

- Conversational backend: session-based chat with persistent history in PostgreSQL, structured error handling and logging.
- Multi-layered memory: persistent, semantic, episodic and reflective memories, plus decay, boost, forgetting and consolidation.
- Hybrid retrieval: semantic search in Qdrant combined with episodic, reflective and always-on persistent memories, scored by a custom **Memory Ranker.
- Context Optimizer: deduplicates and compresses memories under a token budget before they are injected into the LLM prompt.
- Reflection Generator: synthesizes higher-level insights from episodic memories for long-term personalization.
- Conversation summarization: trigger-based rolling summaries to keep long chats coherent.
- Redis: embedding cache and per-user rate limiting.
- Optional API key auth via the `X-API-Key` header.

## Architecture

```
User message
   |
   v
Hybrid Retrieval (Qdrant vectors + PostgreSQL metadata)
   |
   v
Memory Ranker -> Context Optimizer -> LLM (OpenAI Responses API)
   |
   v
Reply to user
   |
   v  (background tasks)
Fact extraction -> Episode store -> Reflection Generator -> Summarizer
```

Embeddings and a small payload (`user_id`, `kind`) live in Qdrant. The memory text and metadata (importance, strength, access count, timestamps) live in PostgreSQL. Both are linked by the same memory ID.

### Memory ranking

Each candidate memory is scored as:

| Component | Weight |
|---|---|
| Vector similarity | 0.50 |
| Recency (14-day half-life) | 0.15 |
| Importance x strength | 0.25 |
| Memory kind (persistent > reflection > semantic > episodic) | 0.10 |

### Memory lifecycle

- **Boost:** a memory gains strength when it is retrieved and used, or when the same fact is seen again.
- **Decay:** strength decays exponentially over time; important memories decay more slowly. Runs hourly.
- **Forgetting:** weak, low-importance, non-persistent memories are archived and removed from Qdrant.
- **Consolidation:** old episodic memories are merged into durable semantic facts.

## Services (Docker Compose)

| Service | Image | Purpose |
|---|---|---|
| `api` | built from `Dockerfile` | FastAPI backend |
| `ui` | same image as `api` | Streamlit chat UI |
| `postgres` | `postgres:16-alpine` | History and memory metadata |
| `redis` | `redis:7-alpine` | Cache and rate limiting |
| `qdrant` | `qdrant/qdrant:v1.12.0` | Vector store |

All services have health checks and dependency-aware startup (`depends_on: service_healthy`).

## Quick start

Requirements: Docker with Docker Compose, and an OpenAI API key.

```bash
git clone https://github.com/arnavshah038-jpg/AI-Personal-OS.git
cd AI-Personal-OS
cp .env.example .env        # set OPENAI_API_KEY and POSTGRES_PASSWORD
docker compose up -d --build
```

- Chat UI: http://localhost:8501
- Swagger / OpenAPI docs: http://localhost:8000/docs
- PostgreSQL is exposed on `127.0.0.1:5433` to avoid clashing with a local Postgres.

Stop: `docker compose down`
Full cleanup (containers, volumes, images): `docker compose down -v --rmi local`

## Configuration

Set these in `.env`:

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key (required) |
| `POSTGRES_PASSWORD` | Database password (use letters and numbers only) |
| `APP_API_KEY` | If set, every API call needs an `X-API-Key` header. **Set this on any public deployment.** |
| `CHAT_MODEL` | Chat model, default `gpt-4o-mini` |

## API

| Method | Endpoint | Description |
|---|---|---|
| POST | `/chat` | Send a message; returns the reply and the memories used |
| GET | `/sessions/{id}/history` | Full message history of a session |
| GET | `/memories` | List a user's active memories |
| POST | `/maintenance/run` | Run decay, forgetting, consolidation and reflection |
| GET | `/health` | Health check |

Example:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "s1", "message": "My name is Arnav and I love FastAPI", "user_id": "default"}'
```

Start a new `session_id` and ask "What is my name?" to see long-term memory working across sessions.

## Tests

The ranker and optimizer are pure functions, so tests need no services:

```bash
python -m venv .venv && source .venv/bin/activate
pip install pytest
pytest
```

## Project structure

```
app/
  main.py         FastAPI app and endpoints
  config.py       settings
  db.py, models.py   PostgreSQL via SQLAlchemy
  vector.py       Qdrant client
  embeddings.py   OpenAI embeddings with Redis cache
  llm.py          OpenAI Responses API wrapper with retries
  store.py        memory writes and fact extraction
  retrieval.py    hybrid retrieval
  ranker.py       Memory Ranker
  optimizer.py    Context Optimizer
  lifecycle.py    decay, boost, forgetting, consolidation
  reflection.py   Reflection Generator
  summarizer.py   conversation summarization
  cache.py        Redis cache and rate limiting
ui/streamlit_app.py
tests/
```

## Deployment

See [DEPLOY_AWS.md](DEPLOY_AWS.md) for deploying to an AWS EC2 instance with Docker Compose.