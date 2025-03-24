from database.faiss_store import faiss_index
from database.elastic_search import QueryDatabase

query_db = QueryDatabase()
queries = query_db.search_all_queries()

if queries:
    print(f"Found {len(queries)} queries in Elasticsearch. Indexing into FAISS...")
    faiss_index.index_queries(queries)
    print("FAISS successfully populated from Elasticsearch.")
else:
    print("No queries found in Elasticsearch.")