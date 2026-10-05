# AI Personal OS

Memory-augmented conversational AI: FastAPI + OpenAI Responses API + Postgres + Redis + Qdrant + Streamlit.
Koi torch / local ML nahi: embeddings OpenAI se aate hain, isliye image ~300 MB aur disk pe ~2 GB total.

## Local chalana (Arch Linux, system pe koi asar nahi)
```bash
cp .env.example .env        # OPENAI_API_KEY aur POSTGRES_PASSWORD bharo
docker compose up -d --build
```
- UI: http://localhost:8501
- API docs (Swagger): http://localhost:8000/docs
- Postgres compose ke andar chalta hai (port 5433), tumhare local postgres se nahi takrata.

Band karna: `docker compose down` | Poora saaf: `docker compose down -v --rmi local`

## Architecture
chat -> hybrid retrieval (Qdrant semantic + episodic + reflection + persistent facts) -> Memory Ranker
-> Context Optimizer (dedupe + token budget) -> LLM -> background: fact extraction, episode store,
reflection generator, conversation summary. Hourly: decay + forgetting. `/maintenance/run`: consolidation.

## Tests
```bash
python -m venv .venv && source .venv/bin/activate && pip install pytest && pytest
```
(ranker/optimizer pure functions hain, bas pytest chahiye.)
