from elasticsearch import Elasticsearch
from datetime import datetime

class QueryDatabase:
    def __init__(self, host="http://localhost:9200"):
        """Initialize connection to ElasticSearch"""
        self.es = Elasticsearch(hosts=[host])

    def store_query(self, query: str):
        """Store a new query in ElasticSearch with a timestamp"""
        doc = {
            "query": query,
            "timestamp": datetime.utcnow()
        }
        self.es.index(index="queries", document=doc)

    def search_similar_queries(self, query: str, top_n: int = 5):
        """Retrieve similar queries using full-text search"""
        body = {
            "query": {
                "match": {
                    "query": query
                }
            }
        }
        response = self.es.search(index="queries", body=body, size=top_n)
        return [hit["_source"]["query"] for hit in response["hits"]["hits"]]
    
    def search_all_queries(self):
        """Retrieve all stored queries from ElasticSearch."""
        body = {
            "query": {
                "match_all": {}  # Fetch everything in the index
            }
        }
        response = self.es.search(index="queries", body=body, size=1000)  # Adjust size if needed
        return [hit["_source"]["query"] for hit in response["hits"]["hits"]]
