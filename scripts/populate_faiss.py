import os
from sentence_transformers import SentenceTransformer
import faiss
from database.elastic_search import QueryDatabase
from dotenv import load_dotenv
import numpy as np
import pickle

load_dotenv()

MODEL_NAME = os.getenv("FAISS_MODEL_NAME", "all-MiniLM-L6-v2")
INDEX_PATH = "faiss_index/index.faiss"
MAPPING_PATH = "faiss_index/id_to_text.pkl"

# Step 1: Load model
model = SentenceTransformer(MODEL_NAME)

# Step 2: Fetch queries from Elasticsearch
query_db = QueryDatabase()
queries = query_db.search_all_queries()

if not queries:
    print("No queries found in ElasticSearch.")
    exit()

# Step 3: Embed queries
print("🔄 Encoding queries...")
embeddings = model.encode(queries, show_progress_bar=True)

# Step 4: Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Step 5: Save index and mapping
os.makedirs("faiss_index", exist_ok=True)
faiss.write_index(index, INDEX_PATH)

with open(MAPPING_PATH, "wb") as f:
    pickle.dump(queries, f)

print(f"FAISS index built and saved with {len(queries)} entries.")