import json
import os
import re
from bs4 import BeautifulSoup
from pathlib import Path
from uuid import uuid4

# Config
INPUT_DIR = 'data/filings_html'
OUTPUT_DIR = 'data/cleaned_filings'  # Each chunk will be saved here
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Helper to clean and chunk text
def clean_text(text):
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\u00a0', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text, chunk_size=100):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i+chunk_size])

def extract_year_and_form(filename):
    year_match = re.search(r'20\d{2}', filename)
    form_type = '10-K' if '10k' in filename.lower() else '10-Q' if '10q' in filename.lower() else 'UNKNOWN'
    return (year_match.group(0) if year_match else 'UNKNOWN', form_type)

def process_file(html_path):
    filename = os.path.basename(html_path)
    year, form_type = extract_year_and_form(filename)

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    body = soup.find('body')
    if not body:
        return

    text = clean_text(body.get_text())

    sections = {
        "balance_sheet": ['balance sheet', 'assets', 'liabilities'],
        "income_statement": ['income statement', 'revenue', 'net income'],
        "cash_flow": ['cash flow', 'operating activities'],
        "management_discussion": ["management's discussion", 'analysis', 'strategic']
    }

    chunks_to_save = []

    for section_name, keywords in sections.items():
        if any(kw.lower() in text.lower() for kw in keywords):
            section_chunks = list(chunk_text(text))
            for chunk in section_chunks:
                chunks_to_save.append({
                    "id": str(uuid4()),
                    "file": filename,
                    "year": year,
                    "form": form_type,
                    "section": section_name,
                    "text": chunk
                })

    for chunk in chunks_to_save:
        chunk_file = os.path.join(OUTPUT_DIR, f"{chunk['id']}.json")
        with open(chunk_file, 'w') as f:
            json.dump(chunk, f)

# Main loop
for file in os.listdir(INPUT_DIR):
    if file.endswith(".htm") or file.endswith(".html"):
        process_file(os.path.join(INPUT_DIR, file))
