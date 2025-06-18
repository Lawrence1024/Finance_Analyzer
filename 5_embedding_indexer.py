import os
import json
import faiss
import numpy as np
from tqdm import tqdm

# Config paths
EMBEDDING_DIR = 'data/embeddings_chunked'
INDEX_DIR = 'data/faiss_index_chunked'
os.makedirs(INDEX_DIR, exist_ok=True)

# Load embeddings and metadata
embeddings = []
metadata = []

for fname in tqdm(os.listdir(EMBEDDING_DIR), desc="Loading embeddings"):
    if fname.endswith(".json"):
        path = os.path.join(EMBEDDING_DIR, fname)
        with open(path, 'r') as f:
            data = json.load(f)
            embeddings.append(np.array(data['embedding'], dtype='float32'))
            metadata.append({
                "id": data['id'],
                "file": data['file'],
                "year": data['year'],
                "form": data['form'],
                "section": data['section'],
                "text": data['text']
            })

embedding_matrix = np.stack(embeddings)

# Build FAISS index
dim = embedding_matrix.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embedding_matrix)

# Save index and metadata
faiss.write_index(index, os.path.join(INDEX_DIR, "sec_chunked_index.faiss"))
with open(os.path.join(INDEX_DIR, "chunk_metadata.json"), 'w') as f:
    json.dump(metadata, f)

print("✅ FAISS index and metadata saved.")