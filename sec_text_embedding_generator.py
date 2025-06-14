import json
from sentence_transformers import SentenceTransformer
import os

# Define the directory for the cleaned files and where to store embeddings
CLEANED_DATA_DIR = 'data/cleaned_filings'  # Folder where your cleaned files are saved
EMBEDDINGS_DIR = 'data/embeddings'         # Folder to save the embeddings
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

# Load the pre-trained Sentence-BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to load the cleaned JSON files
def load_cleaned_data():
    files = []
    for filename in os.listdir(CLEANED_DATA_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(CLEANED_DATA_DIR, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)
            files.append(data)
    return files

# Function to generate embeddings for the financial data sections
def generate_embeddings(cleaned_data):
    embeddings = {}
    
    for entry in cleaned_data:
        file_name = entry["file"]
        financial_data = entry["financial_data"]
        
        # Combine all relevant sections into a single string
        combined_text = "\n".join([
            financial_data.get("balance_sheet", ""),
            financial_data.get("income_statement", ""),
            financial_data.get("cash_flow", ""),
            financial_data.get("management_discussion", "")
        ])
        
        # Generate the embedding for this combined text
        embedding = model.encode(combined_text)
        embeddings[file_name] = embedding

    return embeddings

# Save the embeddings to disk
def save_embeddings(embeddings):
    for file_name, embedding in embeddings.items():
        embedding_path = os.path.join(EMBEDDINGS_DIR, f"{file_name}_embedding.json")
        with open(embedding_path, 'w') as f:
            json.dump(embedding.tolist(), f)  # Save as a list for easy loading
        print(f"Saved embedding for {file_name}")

# Main process
cleaned_data = load_cleaned_data()
embeddings = generate_embeddings(cleaned_data)
save_embeddings(embeddings)
