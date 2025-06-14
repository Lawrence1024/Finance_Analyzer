import os
import json
import requests
from tqdm import tqdm
from pathlib import Path
from bs4 import BeautifulSoup

# CONFIGURATION
SUBMISSIONS_DIR = 'data/submissions_data'
SAVE_DIR = 'data/filings_html'
ALLOWED_FORMS = {'10-K', '10-Q'}
MAX_TOTAL_BYTES = 1 * 1024 ** 3  # 5 GB limit

print(f"MAX_TOTAL_BYTES is {MAX_TOTAL_BYTES}")

# Make save directory
Path(SAVE_DIR).mkdir(exist_ok=True)

# Function to get the URL of a filing based on CIK, accession number, and filename
def get_filing_url(cik, accession_number, filename):
    cik = str(cik).lstrip("0")
    acc_no_nodash = accession_number.replace("-", "")
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_no_nodash}/{filename}"

# Download filing document from URL
def download_file(url, save_path):
    try:
        response = requests.get(url, headers={'User-Agent': 'lawrence92@berkeley.edu'}, timeout=15)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return len(response.content)
        return 0
    except:
        return 0

# Track total downloaded size and count
total_downloaded = 0
downloaded_files = 0

# Iterate through all submission files in the `submissions_data` directory
submission_files = list(Path(SUBMISSIONS_DIR).glob("*.json"))

for submission_file in tqdm(submission_files, desc="Parsing submission files"):
    with open(submission_file) as f:
        data = json.load(f)
    
    cik = data.get("cik", "")
    filings = data.get("filings", {}).get("recent", {})
    count = len(filings.get("accessionNumber", []))

    for i in range(count):
        form = filings.get("form", [])[i]
        if form not in ALLOWED_FORMS:
            continue

        acc_no = filings.get("accessionNumber", [])[i]
        filename = filings.get("primaryDocument", [])[i]

        url = get_filing_url(cik, acc_no, filename)
        
        if total_downloaded > MAX_TOTAL_BYTES:
            print(f"\nReached ~5GB limit at {total_downloaded / (1024**3):.2f} GB.")
            exit()

        save_filename = f"{cik}_{acc_no.replace('-', '')}_{filename}".replace("/", "_")
        save_path = os.path.join(SAVE_DIR, save_filename)
        
        if not os.path.exists(save_path):
            downloaded_size = download_file(url, save_path)
            if downloaded_size > 0:
                total_downloaded += downloaded_size
                downloaded_files += 1

print(f"\nDone! Downloaded {downloaded_files} filings, total {total_downloaded / (1024**3):.2f} GB.")
