--> (AI Personal OS)

An AI-powered personal memory system that lets you capture, search, and reflect on everything that matters to you. Built with **FastAPI**, **Streamlit**, **PostgreSQL**, **Qdrant**, and **OpenAI Embeddings**, it combines structured storage with semantic search and AI-driven reflection to act as a second brain for your facts, preferences, goals, and projects.

---

Features

| Feature | Description |
|
| Memory CRUD | Create, read, update, and delete memories through a clean REST API |
| Semantic Search | Find relevant memories by meaning, not just keywords, powered by Qdrant vector search |
| AI Reflection Engine | Generates AI-driven reflections and insights from your stored memories |
| Dashboard Analytics | Visual overview of memory health, types, and importance |
| Memory Timeline | Track how your memory base grows over time |
| Importance Tracking | Prioritize memories with a 1–10 importance scale |
| Export Memories | Download your entire memory base as a CSV file |
| PostgreSQL Storage | Reliable, structured persistence for all memory data |
| FastAPI REST APIs | Fast, typed, and well-documented backend endpoints |
| Streamlit Dashboard | Interactive frontend for exploring and managing memories |

---

Tech Stack

- Language: Python
- Backend: FastAPI
- Frontend: Streamlit
- Database: PostgreSQL
- Vector Store:** Qdrant
- Embeddings:** OpenAI Embeddings
- ORM: SQLAlchemy
- Visualization: Plotly



Project Structure

```text
app/          # Core backend application (API routes, services, repositories, models)
frontend/     # Streamlit dashboard and UI pages
docs/         # Project documentation
tests/        # Test suite
```



 Getting Started

Start the Backend API

```bash
uvicorn main:app --reload
```

### 2. Launch the Dashboard

```bash
streamlit run frontend/pages/dashboard.py
```

The API will be available at `http://127.0.0.1:8000` and the Streamlit dashboard will open automatically in your browser.



Author

Arnav Shah