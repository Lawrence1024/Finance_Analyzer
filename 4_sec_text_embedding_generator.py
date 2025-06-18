import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Directories
CLEANED_DIR = 'data/cleaned_filings'
EMBEDDINGS_DIR = 'data/embeddings_chunked'
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Collect all chunk files
chunks = []
for fname in os.listdir(CLEANED_DIR):
    if fname.endswith('.json'):
        path = os.path.join(CLEANED_DIR, fname)
        with open(path, 'r') as f:
            data = json.load(f)
            chunks.append(data)

# Generate and save embeddings
for chunk in tqdm(chunks, desc="Generating embeddings"):
    text = chunk['text']
    embedding = model.encode(text)
    
    out_path = os.path.join(EMBEDDINGS_DIR, f"{chunk['id']}.json")
    with open(out_path, 'w') as f:
        json.dump({
            'id': chunk['id'],
            'file': chunk['file'],
            'year': chunk['year'],
            'form': chunk['form'],
            'section': chunk['section'],
            'text': chunk['text'],
            'embedding': embedding.tolist()
        }, f)