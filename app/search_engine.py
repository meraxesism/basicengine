# app/search_engine.py

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
INDEX_FILE = "data/embeddings/faiss.index"
METADATA_FILE = "data/embeddings/metadata.json"
MODEL_NAME = "all-MiniLM-L6-v2"

# Load model once
model = SentenceTransformer(MODEL_NAME)

# Load index + metadata
index = faiss.read_index(INDEX_FILE)
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

def search_query(query, top_k=1):
    # Embed the user query
    query_embedding = model.encode([query], convert_to_numpy=True)
    
    # Search similar vectors
    distances, indices = index.search(query_embedding, top_k)

    # Return top results
    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            results.append(metadata[idx])
    
    return results[0] if results else {"text": "No relevant result found."}
