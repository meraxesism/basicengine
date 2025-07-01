import json
import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = "data/chunks.json"
INDEX_FILE = "data/embeddings/faiss.index"
MODEL_NAME = "all-MiniLM-L6-v2"  # Fast + accurate

def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def build_faiss_index():
    print("🔍 Loading text chunks...")
    chunks = load_chunks()
    texts = [chunk["text"] for chunk in chunks]

    print("🧠 Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("📐 Generating embeddings...")
    embeddings = model.encode(texts, convert_to_numpy=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)

    print(f"✅ Saved FAISS index with {len(embeddings)} vectors.")

    # Also save chunks alongside index
    with open("data/embeddings/metadata.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    return index
