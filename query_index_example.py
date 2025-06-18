import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
INDEX_PATH = 'data/faiss_index_chunked/sec_chunked_index.faiss'
META_PATH = 'data/faiss_index_chunked/chunk_metadata.json'

# Load index and metadata
index = faiss.read_index(INDEX_PATH)
with open(META_PATH, 'r') as f:
    metadata = json.load(f)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def search(query, top_k=5):
    query_embedding = model.encode(query).astype('float32')
    scores, indices = index.search(np.array([query_embedding]), top_k)

    print(f"\nTop {top_k} results for query: '{query}'\n")
    for rank, idx in enumerate(indices[0]):
        meta = metadata[idx]
        print(f"[{rank+1}] {meta['file']} | {meta['form']} {meta['year']} | {meta['section']}")
        print(f"     → {meta['text'][:200]}...\n")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python sec_query_retriever.py 'Your question here'")
    else:
        search(' '.join(sys.argv[1:]))