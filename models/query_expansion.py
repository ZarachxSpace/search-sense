from sentence_transformers import SentenceTransformer
from database.elastic_search import QueryDatabase
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from search_engines.fetch_queries import fetch_google_suggestions, fetch_duckduckgo_suggestions

class QueryExpander:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize the Query Expander using SentenceTransformer for embeddings and ElasticSearch."""
        self.model = SentenceTransformer(model_name)
        self.db = QueryDatabase()  # ElasticSearch Connection
        
        # Fetch stored queries dynamically from ElasticSearch
        self.query_database = self.db.search_all_queries()

    def filter_duplicate_queries(self, query_list, model):
        """Remove duplicate queries using semantic similarity."""
        embeddings = model.encode(query_list)
        similarity_matrix = cosine_similarity(embeddings)

        unique_queries = []
        for i, query in enumerate(query_list):
            if all(similarity_matrix[i][j] < 0.85 for j in range(i)):  # Threshold for similarity
                unique_queries.append(query)

        return unique_queries

    def expand_query(self, query, num_return_seq=5):
        """Retrieve diverse expanded queries from ElasticSearch and search engine data."""
        similar_queries = self.db.search_similar_queries(query, num_return_seq)
        google_queries = fetch_google_suggestions(query)
        duckduckgo_queries = fetch_duckduckgo_suggestions(query)

        all_queries = list(set(similar_queries + google_queries + duckduckgo_queries))  # Remove duplicates
        filtered_queries = self.filter_duplicate_queries(all_queries, self.model)  # Ensure diverse expansions

        return filtered_queries[:num_return_seq]  # Return only the top N expansions
    
    


if __name__ == "__main__":
    query_expander = QueryExpander()
    query = "best programming laptops 2024"
    print("Original Query:", query)
    print("Expanded Queries:", query_expander.expand_query(query))