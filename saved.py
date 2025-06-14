from transformers import pipeline

# Load the T5 model for question answering
qa_pipeline = pipeline("question-answering", model="t5-small")

# Define the context and question

# Define the path to the JSON file
file_path = "data/cleaned_filings/cleaned_0000766792_000143774920006524_cvv20191231_10k.json"

# Open and read the content as plain text
with open(file_path, 'r', encoding='utf-8') as file:
    text_content = file.read()

question = "What was the revenue in 2019?"

# Get the answer
result = qa_pipeline(question=question, context=text_content)
print(f"Answer: {result['answer']}")