from transformers import pipeline
import textwrap

# Load free extractive QA model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Read text content
with open("data/cleaned_filings/cleaned_0000766792_000143774920006524_cvv20191231_10k.json", 'r', encoding='utf-8') as file:
    text_content = file.read()

# Split into manageable chunks
chunks = textwrap.wrap(text_content, width=1000)

# Define your question
question = "Focus on revenue. What was the revenue in 2019?"

# Run QA over chunks
best_answer = {"score": 0.0, "answer": None}
for chunk in chunks:
    try:
        result = qa_pipeline(question=question, context=chunk)
        if result['score'] > best_answer['score']:
            best_answer = result
    except Exception as e:
        continue

print(f"Answer: {best_answer['answer']}")
