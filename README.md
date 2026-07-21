# 🧠 AI Personal OS

> **Production-ready AI Personal Assistant with Persistent Long-Term Memory, Semantic Retrieval, Reflection Engine, Multi-Agent Planning, and Retrieval-Augmented Generation (RAG).**

AI Personal OS is an intelligent memory-centric AI assistant that continuously learns from conversations, stores important information, retrieves relevant memories using semantic search, consolidates duplicate memories, generates long-term reflections, and optimizes context for future interactions.

Designed as a production-ready AI operating system, it combines **FastAPI**, **OpenAI**, **PostgreSQL**, **Redis**, **Qdrant**, and **Docker** into a scalable architecture.

---

# ✨ Features

## 🧠 Persistent Memory System

- Persistent Long-Term Memory
- Semantic Memory Retrieval
- Hybrid Memory Ranking
- Memory Importance Scoring
- Memory Confidence Scoring
- Context Optimization
- Automatic Memory Consolidation
- Reflection Memory
- Episodic Memory
- Memory Forgetting
- Memory Decay
- Memory Boost

---

## 🤖 AI Capabilities

- OpenAI Responses API
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Hybrid Retrieval Pipeline
- Reflection Generation
- Intelligent Context Optimization
- Planner Agent
- Confidence-Based Memory Retrieval

---

## 🗄 Databases

- PostgreSQL
- Redis
- Qdrant Vector Database

---

## ⚙ Backend

- FastAPI
- SQLAlchemy
- REST APIs
- Docker
- Docker Compose

---

# 🏗 System Architecture

```
                           User
                             │
                             ▼
                  Streamlit Dashboard
                             │
                             ▼
                      FastAPI Backend
                             │
               ┌─────────────┴──────────────┐
               ▼                            ▼
         Planner Agent                 OpenAI API
               │
               ▼
         Chat Service
               │
               ▼
        Memory Engine
               │
   ┌───────────┼────────────┐
   ▼           ▼            ▼
Redis      PostgreSQL     Qdrant
(Session)   Metadata      Vector DB
```

---

# 🛠 Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Backend | FastAPI |
| AI | OpenAI Responses API |
| Memory | RAG |
| Vector Database | Qdrant |
| Database | PostgreSQL |
| Cache | Redis |
| ORM | SQLAlchemy |
| Frontend | Streamlit |
| Containerization | Docker |
| Embeddings | OpenAI Embeddings |

---

# 📂 Project Structure

```
app/
├── agents/
├── api/
├── consolidation/
├── core/
├── database/
├── exceptions/
├── memory/
├── middleware/
├── models/
├── rag/
├── reflection/
├── repositories/
├── schemas/
├── services/
├── tools/
└── utils/

frontend/
docs/
scripts/
tests/
```

---

# 🧠 Memory Engine

The memory system provides:

- Persistent Long-Term Memory
- Semantic Retrieval
- Hybrid Memory Ranking
- Confidence Scoring
- Reflection Generation
- Episodic Memory
- Memory Consolidation
- Memory Forgetting
- Memory Decay
- Memory Boost
- Context Optimization

---

# 🚀 Quick Start

## Clone Repository

```bash
git clone https://github.com/arnavshah038-jpg/AI-Personal-OS.git
cd AI-Personal-OS
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🐳 Docker

Start the complete application:

```bash
docker compose up --build
```

---

# ▶ Run Backend

```bash
uvicorn main:app --reload
```

---

# 🎨 Run Frontend

```bash
streamlit run frontend/dashboard.py
```

---

# 📡 REST API

## Chat

```http
POST /chat
```

## Memories

```http
GET /memories
```

## Reflections

```http
GET /reflections
```

---

# 📌 Current Version

## v1.0

### Implemented

- ✅ Persistent Long-Term Memory
- ✅ Semantic Retrieval
- ✅ Reflection Memory
- ✅ Episodic Memory
- ✅ Memory Consolidation
- ✅ Memory Confidence Scoring
- ✅ Context Optimization
- ✅ Docker Deployment

---

# 🗺 Roadmap

## v1.1

- Planner Agent Improvements
- Tool Calling

## v1.2

- LangGraph Integration
- Multi-Agent Workflows

## v2.0

- Gmail Integration
- Calendar Integration
- GitHub Integration
- Browser Tools
- Autonomous AI Workflows

---

# 👨‍💻 Author

**Arnav Shah**

AI / LLM Engineer

GitHub:
https://github.com/arnavshah038-jpg

---

# 📄 License

This project is licensed under the MIT License.