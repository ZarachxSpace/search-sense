from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

es_host = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
print("Using host:", es_host)

es = Elasticsearch([es_host])
print("Ping:", es.ping())