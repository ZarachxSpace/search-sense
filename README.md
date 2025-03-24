# SearchSense

This is a project that enhances search relevance through intelligent query expansion and semantic re-ranking of results. It is built as a backend service using FastAPI, FAISS, and ElasticSearch, and integrates external sources like Google and DuckDuckGo to deliver improved search outcomes.

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

## Project Structure

```
├── README.md
├── api
│   └── main.py
├── database
│   ├── crud.py
│   ├── elastic_search.py
│   ├── faiss_store.py
│   ├── models.py
│   └── postgres.py
├── docker-compose.yaml
├── models
│   ├── query_expansion.py
│   └── user_queries.py
├── requirements.txt
├── scripts
│   ├── populate_faiss.py
│   └── update_queries.py
├── search_engines
│   └── fetch_queries.py
└── tests
    ├── test_es.py
    ├── test_faiss.py
    └── testing_queries.py
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ZarachxSpace/searchsense.git
cd searchsense
```

### 2. Set Environment Variables

Create a `.env` file in the root directory and set the required environment variables.
Refer to .env.example for more details. 

### 3. Install Dependencies

It's recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 4. Run ElasticSearch Locally

```bash
docker-compose up -d
```

### 5. Run the API

```bash
uvicorn api.main:app --reload
```

---

## API Endpoints

- `GET /expand_query?query=...`  
  Expand a user query using FAISS + ElasticSearch + public APIs.

- `GET /search_results?query=...`  
  Retrieve search results from Google + DuckDuckGo.

- `POST /users/`  
  Create a user (PostgreSQL only, optional).

---

## FAISS Index

The FAISS index is dynamically updated every time a new query is inserted.  
No static data is required, making it portable and reproducible without relying on PostgreSQL.

---

## Notes

- **PostgreSQL** integration is optional. If not available, query history will only persist in ElasticSearch.
- **Google Custom Search API** requires your own API key and engine ID.
- **DuckDuckGo** has limited metadata but works without authentication.

---

## Optional Integrations

- **Google Custom Search API**
- **DuckDuckGo Instant Answer API**
- **PostgreSQL** (optional)

---

## License

This project is licensed under the MIT License.
Feel free to fork and improve the project.

---

## Contributors
**Zarach** – [GitHub Profile](https://github.com/ZarachxSpace)

---

## Support
For any issues, open a GitHub **issue** or contact via **email**.

