import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# Paths
INDEX_PATH = 'data/faiss_index_chunked/sec_chunked_index.faiss'
META_PATH = 'data/faiss_index_chunked/chunk_metadata.json'

# Load FAISS index and metadata
index = faiss.read_index(INDEX_PATH)
with open(META_PATH, 'r') as f:
    metadata = json.load(f)

# Load sentence embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Load local LLM (change to a smaller model if needed)
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="auto", device_map="auto")
llm = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)

def query_sec_qa_local(question, top_k=5):
    # Step 1: Embed query and search
    query_vec = embedder.encode(question).astype('float32')
    scores, indices = index.search(np.array([query_vec]), top_k)

    # Step 2: Build context from top chunks
    context = "\n\n".join([metadata[i]['text'] for i in indices[0]])

    # Step 3: Construct prompt for generation
    prompt = f"""
        You are a financial assistant. Use the context below to answer the question truthfully and concisely.

        Context:
        {context}

        Question:
        {question}

        Answer:
    """

    # Step 4: Run local model
    print("\n📥 Prompt Sent to LLM:\n", prompt[:300], "...\n")  # show preview
    result = llm(prompt)[0]['generated_text']

    # Step 5: Print only answer part (remove echoed prompt)
    answer_start = result.lower().find("answer:")
    print("\n📤 Answer:\n")
    print(result[answer_start + 7:].strip())

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python sec_local_llm_chat.py 'Your question here'")
    else:
        query_sec_qa_local(' '.join(sys.argv[1:]))
