import os
import requests
from database.faiss_store import faiss_index
from database.elastic_search import QueryDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from models.user_queries import get_recent_queries

query_db = None

def get_query_db():
    global query_db
    if query_db is None:
        query_db = QueryDatabase()
    return query_db

async def fetch_faiss_queries(query, top_n=5):
    return faiss_index.search_similar_queries(query, top_n)

async def fetch_elastic_queries(query, top_n=5):
    db = get_query_db()
    return db.search_similar_queries(query, top_n)

async def fetch_postgres_queries(user_id: int, db: AsyncSession, top_n=5):
    queries = await get_recent_queries(db, user_id, top_n)
    return [q.query for q in queries] if queries else []

def fetch_google_results(query, num_results=5):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

    if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
        print("Missing Google API credentials in environment variables.")
        return []

    search_url = (
        f"https://www.googleapis.com/customsearch/v1?"
        f"q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
    )
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        if "items" in data:
            return [
                item["title"]
                for item in data["items"][:num_results]
            ]
    except Exception as e:
        print(f"Google API Error: {e}")
    return []

def fetch_duckduckgo_results(query, num_results=5):
    search_url = f"https://api.duckduckgo.com/?q={query}&format=json"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        if "RelatedTopics" in data:
            return [
                item.get("Text", "")
                for item in data["RelatedTopics"][:num_results]
            ]
    except Exception as e:
        print(f"DuckDuckGo API Error: {e}")
    return []