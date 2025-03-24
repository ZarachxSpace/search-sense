from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import QueryLogs
from datetime import datetime

async def store_user_query(db: AsyncSession, user_id: int, query: str):
    """Store user search queries into PostgreSQL"""
    try:
        new_query = QueryLogs(user_id=user_id, query=query, timestamp=datetime.utcnow())
        db.add(new_query)
        await db.commit()
        return new_query
    except Exception as e:
        await db.rollback()  # Rollback if an error occurs
        print(f"Error storing user query: {e}")
        return None

async def get_recent_queries(db: AsyncSession, user_id: int, limit: int = 10):
    """Retrieve a user's most recent search queries"""
    try:
        result = await db.execute(
            select(QueryLogs)
            .filter(QueryLogs.user_id == user_id)
            .order_by(QueryLogs.timestamp.desc())
            .limit(limit)
        )
        return result.scalars().all()
    except Exception as e:
        print(f"Error retrieving recent queries: {e}")
        return []

async def get_all_queries(db: AsyncSession):
    """Retrieve all stored queries from PostgreSQL."""
    try:
        result = await db.execute(select(QueryLogs).order_by(QueryLogs.timestamp.desc()))
        return result.scalars().all()
    except Exception as e:
        print(f"Error retrieving all queries: {e}")
        return []