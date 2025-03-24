import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("faiss_index/index.faiss")

with open("faiss_index/id_to_text.pkl", "rb") as f:
    id_to_text = pickle.load(f)

query = "ai tools for productivity"
embedding = model.encode([query])

D, I = index.search(np.array(embedding), 5)

print("Similar queries:")
for idx in I[0]:
    print("•", id_to_text[idx])