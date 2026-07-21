--> Persistent AI Memory Assistant

A production-ready AI assistant with long-term memory powered by FastAPI, OpenAI, PostgreSQL, Qdrant, and Docker.

The assistant remembers important information across conversations, retrieves memories using semantic search, consolidates duplicate memories, generates long-term reflections, and automatically manages memory importance over time.



# Features

--> Long-Term Memory

- Persistent memory storage
- Semantic memory retrieval
- Memory importance scoring
- Memory confidence scoring
- Automatic memory consolidation
- Memory forgetting
- Memory decay
- Memory boost
- Reflection memory
- Episodic memory
- Context optimization

---

--> AI Capabilities

- OpenAI Responses API
- Semantic Search
- Memory Ranking
- Hybrid Retrieval
- Reflection Generation
- Context Optimization



--> 🗄 Database

- PostgreSQL
- Qdrant Vector Database



--> Backend

- FastAPI
- SQLAlchemy
- Docker
- REST APIs

---

--> Architecture

```
                User
                  │
                  ▼
            FastAPI Backend
                  │
        ┌─────────┴──────────┐
        ▼                    ▼
  Memory Engine         OpenAI API
        │
        ▼
 ┌──────────────┐
 │ PostgreSQL   │
 └──────────────┘
        │
        ▼
 ┌──────────────┐
 │ Qdrant       │
 └──────────────┘




--> Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Backend | FastAPI |
| AI | OpenAI Responses API |
| Vector DB | Qdrant |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Frontend | Streamlit |
| Container | Docker |
| Embeddings | OpenAI Embeddings |



--> Project Structure


app/
    agents/
    api/
    consolidation/
    core/
    database/
    memory/
    repositories/
    services/
    utils/

frontend/

docs/

tests/




--> Memory Engine

The project includes:

- Semantic Retrieval
- Memory Ranking
- Confidence Scoring
- Memory Consolidation
- Reflection Generation
- Episodic Memory
- Memory Forgetting
- Memory Boost
- Memory Decay
- Context Optimization

---

# 🐳 Docker

Start the complete application:

```bash
docker compose up --build
```



--> Backend

```bash
uvicorn main:app --reload
```

---

--> Frontend

```bash
streamlit run frontend/dashboard.py
```

---

--> API

--> Chat

```
POST /chat
```

---

--> Memories

```
GET /memories
```

---

--> Reflection

```
GET /reflections
```

---

--> Current Version

**v1.0**

Current capabilities:

- Persistent Long-Term Memory
- Semantic Search
- Reflection Memory
- Episodic Memory
- Memory Consolidation
- Docker Deployment

---

--> Future Roadmap

- Planner Agent
- Tool Calling
- LangGraph Integration
- Gmail Integration
- Calendar Integration
- GitHub Integration
- Browser Tools
- Multi-Agent Workflows

---

--> Author

**Arnav Shah**

AI / LLM Engineer

---

--> License

MIT License