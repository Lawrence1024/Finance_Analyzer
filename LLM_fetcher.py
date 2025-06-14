from transformers import T5ForQuestionAnswering, T5Tokenizer

# Directory to save the model
MODEL_DIR = 'data/models/t5-small'

# Create the directory if it doesn't exist
import os
os.makedirs(MODEL_DIR, exist_ok=True)

# Function to download and save the model and tokenizer
def download_and_save_model():
    print(f"Downloading the model and tokenizer from Hugging Face to {MODEL_DIR}...")
    
    # Download model and tokenizer
    model = T5ForQuestionAnswering.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')

    # Save the model and tokenizer locally
    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

    print(f"Model downloaded and saved locally in {MODEL_DIR}.")

# Call the function to download and save the model
download_and_save_model()
