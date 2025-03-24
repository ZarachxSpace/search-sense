import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import AsyncSession
from database.postgres import get_db  # PostgreSQL Integration
from models.user_queries import get_all_queries  # Fetch stored queries
from database.elastic_search import QueryDatabase  # Import but don't instantiate here

class FAISSIndex:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize FAISS index and Sentence Transformer model."""
        self.model = SentenceTransformer(model_name)

        # Try to use GPU acceleration if available
        self.use_gpu = faiss.get_num_gpus() > 0
        if self.use_gpu:
            self.index = faiss.index_cpu_to_gpu(
                faiss.StandardGpuResources(), 0, faiss.IndexFlatL2(384)
            )
        else:
            self.index = faiss.IndexFlatL2(384)  # Default CPU-based FAISS

        self.query_map = {}  # Map FAISS indices to queries

    async def load_queries(self, db: AsyncSession):
        """Load queries from PostgreSQL and Elasticsearch into FAISS."""
        elastic = QueryDatabase()  # Lazy instantiation here
        stored_queries = elastic.search_all_queries()  # From Elasticsearch
        pg_queries = await get_all_queries(db)         # From PostgreSQL

        combined_queries = list(set(stored_queries + [q.query for q in pg_queries]))
        self.add_queries(combined_queries)

    def add_queries(self, queries):
        """Add queries to FAISS index."""
        if not queries:
            return

        embeddings = self.model.encode(queries)
        embeddings = np.array(embeddings).astype("float32")

        start_idx = len(self.query_map)
        self.index.add(embeddings)

        for i, query in enumerate(queries):
            self.query_map[start_idx + i] = query  # Store query ID mapping

    def search_similar_queries(self, query, top_k=5):
        """Retrieve similar queries using FAISS."""
        if self.index.ntotal == 0:
            return []  # Return empty if FAISS index is not populated

        query_embedding = self.model.encode([query]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)

        return [self.query_map[idx] for idx in indices[0] if idx in self.query_map]

# Initialize FAISS but defer DB loading
faiss_index = FAISSIndex()