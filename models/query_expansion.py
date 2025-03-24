from sentence_transformers import SentenceTransformer
from search_engines.fetch_queries import (
    get_query_db,
    fetch_google_results,
    fetch_duckduckgo_results
)
from database.faiss_store import faiss_index
from sqlalchemy.ext.asyncio import AsyncSession
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class QueryExpander:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize the Query Expander using SentenceTransformer, ElasticSearch, FAISS."""
        self.model = SentenceTransformer(model_name)
        self.db = get_query_db()
        self.query_database = self.db.search_all_queries()

    def filter_duplicate_queries(self, query_list):
        """Remove semantically similar queries."""
        if not query_list:
            return []

        embeddings = self.model.encode(query_list)
        similarity_matrix = cosine_similarity(embeddings)

        unique_queries = []
        for i, query in enumerate(query_list):
            if all(similarity_matrix[i][j] < 0.85 for j in range(i)):
                unique_queries.append(query)

        return unique_queries

    async def expand_query(self, query, user_id=None, num_return_seq=5, db: AsyncSession = None):
        """Expand a user query using FAISS, ElasticSearch and live suggestions."""
        try:
            faiss_queries = faiss_index.search_similar_queries(query, num_return_seq)
            elastic_queries = self.db.search_similar_queries(query, num_return_seq)
            google_queries = fetch_google_results(query)
            duckduckgo_queries = fetch_duckduckgo_results(query)

            all_queries = list(set(faiss_queries + elastic_queries + google_queries + duckduckgo_queries))
            filtered_queries = self.filter_duplicate_queries(all_queries)
            filtered_queries = [str(q) for q in filtered_queries]

            if db:
                self.db.store_query(query, db.sync_session)

            return {"expanded_queries": filtered_queries[:num_return_seq]}

        except Exception as e:
            print(f"❌ Error expanding query: {e}")
            return {"error": str(e)}

    async def re_rank_results(self, query, search_results, user_id=None, db: AsyncSession = None):
        """Re-rank search results based on semantic similarity and user preferences."""
        query_embedding = self.model.encode([query])
        doc_embeddings = self.model.encode([doc["content"] for doc in search_results])
        similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

        for i, doc in enumerate(search_results):
            doc["semantic_score"] = float(similarities[i])

        if user_id and db:
            user_prefs = self.db.get_user_preferences(user_id, db.sync_session)
            for doc in search_results:
                for keyword in user_prefs:
                    if keyword.lower() in doc["content"].lower():
                        doc["semantic_score"] += 0.2

        return sorted(search_results, key=lambda x: x["score"] + x["semantic_score"], reverse=True)