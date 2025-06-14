import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import GPTJForCausalLM, GPT2Tokenizer
import os
import torch

# Directories
INDEX_DIR = 'data/faiss_index'  # Directory where the FAISS index is stored
MODEL_DIR = 'data/models/gpt-j-6B'  # Directory where the GPT-J model is saved
CLEANED_FILES_DIR = 'data/cleaned_filings'  # Directory where cleaned document files are stored
FILENAMES_MAPPING_FILE = 'data/faiss_index/filenames_mapping.json'  # File storing filenames mapping
TOP_K = 5  # Number of documents to retrieve

# Load the pre-trained Sentence-Transformer model for query embedding
model = GPTJForCausalLM.from_pretrained(MODEL_DIR)  # Load GPT-J model
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_DIR)  # Load GPT-2 tokenizer for GPT-J

# Load Sentence-Transformer for query encoding
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to load the FAISS index
def load_faiss_index():
    index_path = os.path.join(INDEX_DIR, "embeddings_index.faiss")
    return faiss.read_index(index_path)

# Function to load filenames mapping
def load_filenames_mapping():
    with open(FILENAMES_MAPPING_FILE, 'r') as f:
        filenames = json.load(f)
    return filenames

# Function to generate the query embedding using Sentence-Transformers
def generate_query_embedding(query):
    # Use Sentence-Transformer to generate embedding for the query
    query_embedding = sentence_model.encode([query])  # Encodes the query into a vector
    return np.array(query_embedding)  # Ensure it's a numpy array

# Function to query the FAISS index
def query_faiss_index(query, top_k=TOP_K):
    query_embedding = generate_query_embedding(query)

    # Load the FAISS index
    index = load_faiss_index()

    # Perform the search (find the top k most similar embeddings)
    distances, indices = index.search(query_embedding, top_k)
    return indices[0], distances[0]

# Function to retrieve relevant documents based on the indices
def retrieve_documents(indices):
    # Load the filenames mapping to link indices to actual files
    filenames = load_filenames_mapping()  # Load the list of filenames
    documents = []
    
    # Map the indices to the filenames and read the content
    for idx in indices:
        file_name = "cleaned_" + filenames[idx] + ".json"  # Retrieve the corresponding filename
        with open("output.txt", 'a') as f:
            f.write(f"selected file {file_name} \n")
        file_path = os.path.join(CLEANED_FILES_DIR, file_name)  # Get the full path of the file
        
        with open(file_path, 'r') as f:
            documents.append(f.read())  # Read the document content
    
    return documents

# Function to split long documents into smaller chunks
def chunk_documents(documents, chunk_size=2000):
    """
    Split documents into smaller chunks to fit within the model's token limit.
    """
    chunks = []
    
    for doc in documents:
        doc_tokens = tokenizer.encode(doc)
        for i in range(0, len(doc_tokens), chunk_size):
            chunk = doc_tokens[i:i + chunk_size]
            chunks.append(tokenizer.decode(chunk, skip_special_tokens=True))
    
    return chunks

# Function to generate a response using GPT-J based on chunked documents
def generate_response(query, retrieved_documents):
    # Combine the query with the retrieved documents and chunk them
    combined_prompt = f"Query: {query}\n\nDocuments:\n" + "\n\n".join(retrieved_documents) + "\n\nResponse:"

    # Chunk the combined prompt if it's too long
    chunks = chunk_documents([combined_prompt])

    # Generate a response for each chunk and combine the results
    responses = []
    for chunk in chunks:
        inputs = tokenizer.encode(chunk, return_tensors="pt")
        attention_mask = torch.ones(inputs.shape, device=inputs.device)  # Create attention mask
        
        # Generate the response from GPT-J for each chunk
        outputs = model.generate(inputs, attention_mask=attention_mask, max_length=2048, num_return_sequences=1, no_repeat_ngram_size=2)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # responses.append(generated_text)
        # print(generated_text)
        with open("output.txt", 'a') as f:
            f.write(f"{generated_text} \n\n")
        print(generated_text)

    # Combine the responses from all chunks
    # return "\n".join(responses)


# Example usage
query = "What was the revenue in 2019 for the company?"
indices, distances = query_faiss_index(query)

# Retrieve the most relevant documents based on indices
retrieved_documents = retrieve_documents(indices)

# Generate the response using the query and the retrieved documents
response = generate_response(query, retrieved_documents)

# Output the generated response
# print("Generated Response:", response)
