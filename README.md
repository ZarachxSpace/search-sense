# SearchSense

SearchSense is a project that enhances search relevance through intelligent query expansion and semantic re-ranking of results. It is built as a backend service using FastAPI, FAISS, and ElasticSearch, and integrates external sources like Google and DuckDuckGo to deliver improved search outcomes.

---

## Features

- **Query Expansion** using:
  - **FAISS** (with SentenceTransformers)
  - **ElasticSearch** fuzzy matching
  - **External APIs** like Google and DuckDuckGo
- **Re-ranking** of results based on semantic similarity
- **Dynamic FAISS updates** on each new query
- **Asynchronous FastAPI** architecture for high performance

---

## Tech Stack

- **Python 3.9+**
- **FastAPI** — Web framework for APIs
- **FAISS** — Vector similarity search
- **SentenceTransformers** — Embedding generation
- **ElasticSearch** — Keyword indexing and fuzzy matching
- **Docker** — ElasticSearch local deployment
- **Uvicorn** — ASGI server

Optional integrations:
- **Google Custom Search API**
- **DuckDuckGo Instant Answer API**
- **PostgreSQL** (optional)

---

## Getting Started

### Prerequisites

- Python 3.9+
- Docker (for ElasticSearch)
- `pip` for Python packages

### Installation

```bash
git clone https://github.com/yourusername/searchsense.git
cd searchsense
pip install -r requirements.txt
```

To run ElasticSearch locally using Docker:

```bash
docker-compose up -d
```

To start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

---

## Project Structure

```
searchsense/
│
├── app/
│   ├── api/                # FastAPI endpoints
│   ├── core/               # Configurations and utilities
│   ├── models/             # Pydantic models
│   ├── services/           # Logic for expansion and re-ranking
│   ├── search/             # ElasticSearch and FAISS integration
│   └── main.py             # FastAPI app entry point
│
├── database/
│   ├── elastic_search.py   # ElasticSearch logic
│   ├── faiss_index.py      # FAISS indexing and updates
│
├── scripts/                # Setup or helper scripts
├── requirements.txt
└── docker-compose.yml
```

---

## Future Improvements

- Add user preference-based personalization layer
- Integrate FAISS persistence layer
- Expand to additional search APIs

---

## License

This project is licensed under the MIT License.
