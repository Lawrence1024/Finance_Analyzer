import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Directory for the FAISS index
INDEX_DIR = 'data/faiss_index'  # Directory where the FAISS index is stored
QUERY_MODEL = 'all-MiniLM-L6-v2'  # Pre-trained model for query embedding

# Load the pre-trained Sentence-BERT model for generating query embeddings
model = SentenceTransformer(QUERY_MODEL)

# Function to load the FAISS index
def load_faiss_index():
    index_path = f"{INDEX_DIR}/embeddings_index.faiss"
    return faiss.read_index(index_path)

# Function to query the FAISS index
def query_faiss_index(query, top_k=5):
    # Generate the query embedding
    query_embedding = model.encode([query])

    # Load the FAISS index
    index = load_faiss_index()

    # Perform the search (find the top k most similar embeddings)
    distances, indices = index.search(np.array(query_embedding), top_k)

    # Get the most similar files based on the search
    return indices[0], distances[0]

# Example usage
query = "What are the key financial metrics for the company in 2019?"
indices, distances = query_faiss_index(query)

# Output the results
print("Top-k most similar documents based on the query:")
for idx, distance in zip(indices, distances):
    print(f"Document index: {idx}, Similarity Distance: {distance}")
