from sentence_transformers import SentenceTransformer
from database.elastic_search import QueryDatabase

class QueryExpander:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize the Query Expander using SentenceTransformer for embeddings and ElasticSearch."""
        self.model = SentenceTransformer(model_name)
        self.db = QueryDatabase()  # ElasticSearch Connection
        
        # Fetch stored queries dynamically from ElasticSearch
        self.query_database = self.db.search_all_queries()

    def expand_query(self, query, num_return_seq=3):
        """
        Expands the input query by retrieving similar queries from ElasticSearch.
        
        :param query: The original search query (string).
        :param num_return_seq: Number of expanded queries to return.
        
        :return: List of semantically similar queries.
        """
        expanded_queries = self.db.search_similar_queries(query, num_return_seq)
        return expanded_queries


if __name__ == "__main__":
    query_expander = QueryExpander()
    query = "best programming laptops 2024"
    print("Original Query:", query)
    print("Expanded Queries:", query_expander.expand_query(query))