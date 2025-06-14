import requests
import zipfile
import io
import os

def download_and_extract_zip(url, extract_to='data/'):
    # Create output directory
    os.makedirs(extract_to, exist_ok=True)
    
    # SEC requires a valid user-agent
    headers = {
        'User-Agent': 'lawrence92@berkeley.edu'
    }
    
    print(f"Downloading from {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Download failed! HTTP {response.status_code}")
    
    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extraction completed: {extract_to}")
    except zipfile.BadZipFile:
        raise Exception("File is not a valid zip file. Check the URL and headers.")

# Run this with correct SEC bulk data URL
download_and_extract_zip(
    'https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip',
    'data/xbrl_data'
)

download_and_extract_zip(
    'https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip',
    'data/submissions_data'
)
