from database.elastic_search import QueryDatabase
from search_engines.fetch_queries import fetch_google_suggestions, fetch_duckduckgo_suggestions

class QueryUpdater:
    def __init__(self):
        """Initialize connection to ElasticSearch"""
        self.db = QueryDatabase()

    def update_query_database(self, query: str):
        """Fetch new related queries and store them dynamically."""
        google_queries = fetch_google_suggestions(query)
        duckduckgo_queries = fetch_duckduckgo_suggestions(query)
        all_queries = set(google_queries + duckduckgo_queries)  # Merge & remove duplicates

        for suggestion in all_queries:
            self.db.store_query(suggestion)

        return list(all_queries)  # Return new queries for debugging
    

if __name__ == "__main__":
    query_updater = QueryUpdater()
    query = "best programming laptops 2024"
    new_queries = query_updater.update_query_database(query)
    print("New Queries Fetched & Stored:", new_queries)