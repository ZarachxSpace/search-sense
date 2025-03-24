from elasticsearch import Elasticsearch, ConnectionError
from datetime import datetime
import os
import time
from sqlalchemy.orm import Session
from database.models import UserPreferences

class QueryDatabase:
    def __init__(self):
        """Initialize connection to ElasticSearch & PostgreSQL with retries"""
        self.ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
        self.es = None
        self.connect_to_es()
        self.create_documents_index()  # Ensure the index exists

    def connect_to_es(self):
        """Retry connecting to Elasticsearch"""
        max_retries = 5
        retry_delay = 5  # seconds

        for attempt in range(max_retries):
            try:
                self.es = Elasticsearch(self.ELASTICSEARCH_HOST)
                if self.es.ping():
                    print(f"Connected to Elasticsearch at {self.ELASTICSEARCH_HOST}")
                    return
            except ConnectionError:
                print(f"Elasticsearch not available. Retrying ({attempt + 1}/{max_retries})...")
                time.sleep(retry_delay)

        raise ConnectionError(f"Failed to connect to Elasticsearch at {self.ELASTICSEARCH_HOST}")

    def store_query(self, query: str, db: Session):
        """Store a new query in Elasticsearch and PostgreSQL"""
        doc = {
            "query": query,
            "timestamp": datetime.utcnow()
        }

        try:
            self.es.index(index="queries", document=doc)
        except Exception as e:
            print(f"Error storing query in Elasticsearch: {e}")

        try:
            db.execute("INSERT INTO queries (query, timestamp) VALUES (:query, :timestamp)", doc)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error storing query in PostgreSQL: {e}")

    def search_similar_queries(self, query: str, top_n: int = 5):
        try:
            body = {
                "query": {
                    "match": {
                        "query": {
                            "query": query,
                            "fuzziness": "AUTO"
                        }
                    }
                },
                "sort": [{"timestamp": {"order": "desc"}}]
            }
            response = self.es.search(index="queries", body=body, size=top_n)
            return [hit["_source"]["query"] for hit in response["hits"]["hits"]]
        except Exception as e:
            print(f"Elasticsearch Error: {e}")
            return []

    def search_all_queries(self):
        try:
            body = {"query": {"match_all": {}}}
            response = self.es.search(index="queries", body=body, size=1000)
            return [hit["_source"]["query"] for hit in response["hits"]["hits"]]
        except Exception as e:
            print(f"Elasticsearch Error: {e}")
            return []

    def search_documents(self, query: str, top_n: int = 10):
        try:
            body = {
                "query": {
                    "match": {
                        "content": query
                    }
                }
            }
            response = self.es.search(index="documents", body=body, size=top_n)
            return [
                {
                    "title": hit["_source"].get("title", "No Title"),
                    "content": hit["_source"].get("content", "No Content"),
                    "score": hit.get("_score", 0)
                }
                for hit in response["hits"]["hits"]
            ]
        except Exception as e:
            print(f"Elasticsearch Error: {e}")
            return []

    def get_user_preferences(self, user_id: str, db: Session):
        try:
            preferences = db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
            return preferences.preferred_keywords if preferences else []
        except Exception as e:
            print(f"PostgreSQL Error: {e}")
            return []

    def create_documents_index(self):
        try:
            if not self.es.indices.exists(index="documents"):
                body = {
                    "mappings": {
                        "properties": {
                            "title": {"type": "text"},
                            "content": {"type": "text"},
                            "timestamp": {"type": "date"}
                        }
                    }
                }
                self.es.indices.create(index="documents", body=body)
                print("Created 'documents' index")
        except Exception as e:
            print(f"Error creating 'documents' index: {e}")
