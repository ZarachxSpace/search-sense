from fastapi import FastAPI, Query, Depends, HTTPException
from models.query_expansion import QueryExpander
from database.elastic_search import QueryDatabase
from search_engines.fetch_queries import fetch_google_results, fetch_duckduckgo_results
from sqlalchemy.ext.asyncio import AsyncSession
from database.postgres import get_db
from database import crud
from database.models import User

app = FastAPI()

query_expander = None

def get_query_expander():
    global query_expander
    if query_expander is None:
        query_expander = QueryExpander()
    return query_expander

@app.get("/")
async def home():
    return {"message": "Search-sense API is running!"}

@app.get("/expand_query")
async def expand_query(query: str, num_return_seq: int = 5, user_id: int = None, db: AsyncSession = Depends(get_db)):
    results = await get_query_expander().expand_query(query=query, user_id=user_id, num_return_seq=num_return_seq, db=db)
    return results

@app.get("/search_results/")
async def search_results(query: str, num_results: int = 5):
    google_results = fetch_google_results(query, num_results)
    duckduckgo_results = fetch_duckduckgo_results(query, num_results)
    return {
        "query": query,
        "google_results": google_results,
        "duckduckgo_results": duckduckgo_results
    }

@app.get("/db_test/")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute("SELECT 1")
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/users/")
async def create_user(username: str, email: str, db: AsyncSession = Depends(get_db)):
    existing_user = await crud.get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = await crud.create_user(db, username, email)
    return {"message": "User created successfully!", "user": new_user}

@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/")
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/{user_id}/preferences/")
async def store_user_preferences(user_id: int, preferences: dict, db: AsyncSession = Depends(get_db)):
    updated_prefs = await crud.store_user_preferences(db, user_id, preferences)
    return {"message": "User preferences updated!", "preferences": updated_prefs}

@app.get("/users/{user_id}/preferences/")
async def get_user_preferences(user_id: int, db: AsyncSession = Depends(get_db)):
    preferences = await crud.get_user_preferences(db, user_id)
    return {"user_id": user_id, "preferences": preferences}
