from database.elastic_search import QueryDatabase
from search_engines.fetch_queries import fetch_google_results, fetch_duckduckgo_results
from sqlalchemy.ext.asyncio import AsyncSession
from database.postgres import SessionLocal
import asyncio

class QueryUpdater:
    def __init__(self):
        """Initialize Elasticsearch and PostgreSQL connection."""
        self.db = QueryDatabase()

    async def update_query_database(self, query: str, db: AsyncSession):
        """Fetch new related queries and store them."""
        google_queries = fetch_google_results(query)
        duckduckgo_queries = fetch_duckduckgo_results(query)

        all_queries = set(google_queries + duckduckgo_queries)

        for suggestion in all_queries:
            self.db.store_query(suggestion, db.sync_session)  # 👈 use sync access via .sync_session if needed

        return list(all_queries)


# Dev test only
if __name__ == "__main__":
    from database.postgres import SessionLocal

    async def test():
        async with SessionLocal() as db:
            updater = QueryUpdater()
            new_queries = await updater.update_query_database("quantum computing", db=db)
            print("Fetched and stored:", new_queries)

    asyncio.run(test())