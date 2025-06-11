import os
import json
import requests
from tqdm import tqdm
from pathlib import Path

# CONFIGURATION
SUBMISSIONS_DIR = 'data/submissions_data'
SAVE_DIR = 'data/filings_html'
ALLOWED_FORMS = {'10-K', '10-Q'}
MAX_TOTAL_BYTES = 5 * 1024 ** 3  # 20 GB

# Make save dir
Path(SAVE_DIR).mkdir(exist_ok=True)

def get_filing_url(cik, accession_number, filename):
    cik = str(cik).lstrip("0")
    acc_no_nodash = accession_number.replace("-", "")
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc_no_nodash}/{filename}"

def estimate_file_size(url):
    try:
        response = requests.head(url, timeout=10)
        size = int(response.headers.get("Content-Length", 0))
        return size
    except:
        return 0

def download_file(url, save_path):
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            return len(response.content)
        return 0
    except:
        return 0

# Track total downloaded size
total_downloaded = 0
downloaded_files = 0

# Iterate all submission files
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
        est_size = estimate_file_size(url)
        
        if total_downloaded + est_size > MAX_TOTAL_BYTES:
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
