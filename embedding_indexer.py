import faiss
import json
import numpy as np
import os

# Directories
EMBEDDINGS_DIR = 'data/embeddings'  # Folder where embeddings are stored
INDEX_DIR = 'data/faiss_index'      # Folder to store the FAISS index
os.makedirs(INDEX_DIR, exist_ok=True)

# Function to load embeddings from the JSON files
def load_embeddings():
    embeddings = []
    filenames = []
    
    # Load all embeddings from the JSON files
    for filename in os.listdir(EMBEDDINGS_DIR):
        if filename.endswith('_embedding.json'):
            file_path = os.path.join(EMBEDDINGS_DIR, filename)
            with open(file_path, 'r') as f:
                embedding = json.load(f)
            
            embeddings.append(np.array(embedding))  # Convert to numpy array
            filenames.append(filename.replace('.htm_embedding.json', ''))  # Store the original file name
    return np.array(embeddings), filenames

# Function to create and save a FAISS index
def create_faiss_index(embeddings):
    # Initialize a FAISS index
    dim = embeddings.shape[1]  # Get the dimensionality of the embeddings
    index = faiss.IndexFlatL2(dim)  # Use L2 distance for measuring similarity (you can also use cosine similarity)
    
    # Add embeddings to the index
    index.add(embeddings)
    
    return index

# Function to save the FAISS index and filenames mapping
def save_faiss_index(index, filenames, index_file, filename_mapping_file):
    faiss.write_index(index, index_file)  # Save the index to disk
    with open(filename_mapping_file, 'w') as f:
        json.dump(filenames, f)  # Save the filenames to disk
    print(f"FAISS index and filename mapping saved to {index_file} and {filename_mapping_file}")

# Main process
def index_embeddings():
    # Step 1: Load embeddings from the saved JSON files
    embeddings, filenames = load_embeddings()
    
    # Step 2: Create the FAISS index
    faiss_index = create_faiss_index(embeddings)
    
    # Step 3: Save the FAISS index and filenames mapping
    index_file = os.path.join(INDEX_DIR, "embeddings_index.faiss")
    filename_mapping_file = os.path.join(INDEX_DIR, "filenames_mapping.json")
    save_faiss_index(faiss_index, filenames, index_file, filename_mapping_file)

# Run the indexing process
index_embeddings()
