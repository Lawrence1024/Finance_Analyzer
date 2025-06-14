import json
import os
import re
from bs4 import BeautifulSoup

# Define directories for input and output
INPUT_DIR = 'data/filings_html'  # Folder containing your HTML filings
OUTPUT_DIR = 'data/cleaned_filings'  # Folder to save cleaned and structured files
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to clean and preprocess the text (removing unwanted characters)
def clean_text(text):
    # Remove unwanted whitespace and characters
    cleaned_text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with a single space
    cleaned_text = re.sub(r'\u00a0', ' ', cleaned_text)  # Replace Unicode non-breaking space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Replace multiple spaces with a single space
    return cleaned_text.strip()

# Function to extract only the relevant financial figures and summaries
def extract_relevant_financial_data(text, keywords):
    """
    Extracts the key financial data based on provided keywords.
    This method ensures that only relevant sections are captured.
    """
    cleaned_data = clean_text(text)
    
    # Search for relevant sections using the keywords
    relevant_data = []
    for keyword in keywords:
        if keyword.lower() in cleaned_data.lower():
            relevant_data.append(cleaned_data)  # Add to list if the keyword is found
    
    return " ".join(relevant_data)  # Combine all relevant sections into one string

# Function to structure the financial data into separate sections
def structure_financial_data(soup):
    # Initialize empty sections for financial data
    balance_sheet = ""
    income_statement = ""
    cash_flow = ""
    mda = ""

    # Keywords or phrases to detect different sections
    balance_keywords = ['balance sheet', 'consolidated balance sheet', 'assets', 'liabilities']
    income_keywords = ['income statement', 'statement of operations', 'revenue', 'cost of revenue', 'gross profit', 'net income']
    cash_flow_keywords = ['cash flow', 'operating activities', 'net cash', 'capital expenditures']
    mda_keywords = ['management\'s discussion', 'management analysis', 'strategic focus', 'key risks']

    # Extract the body content of the filing
    body_content = soup.find('body')
    
    if body_content:
        text_content = body_content.get_text()

        # Extract and condense financial data
        balance_sheet = extract_relevant_financial_data(text_content, balance_keywords)
        income_statement = extract_relevant_financial_data(text_content, income_keywords)
        cash_flow = extract_relevant_financial_data(text_content, cash_flow_keywords)
        mda = extract_relevant_financial_data(text_content, mda_keywords)

    # Ensure the fields aren't empty; if they are, insert a default placeholder
    if not balance_sheet:
        balance_sheet = "Balance Sheet data not available."
    if not income_statement:
        income_statement = "Income Statement data not available."
    if not cash_flow:
        cash_flow = "Cash Flow data not available."
    if not mda:
        mda = "Management Discussion & Analysis data not available."

    return {
        "balance_sheet": balance_sheet.strip(),
        "income_statement": income_statement.strip(),
        "cash_flow": cash_flow.strip(),
        "management_discussion": mda.strip()
    }

# Function to process the HTML filings and convert them into structured JSON
def process_html_filings():
    for html_file in os.listdir(INPUT_DIR):
        if html_file.endswith('.htm') or html_file.endswith('.html'):
            html_path = os.path.join(INPUT_DIR, html_file)

            # Read the HTML file and parse it
            with open(html_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')

            # Extract and structure the financial data
            structured_data = structure_financial_data(soup)

            # Prepare the cleaned data structure
            cleaned_data = {
                "file": html_file,
                "financial_data": structured_data
            }

            # Save the cleaned data to a new JSON file
            output_filename = f"cleaned_{html_file.replace('.htm', '.json').replace('.html', '.json')}"
            output_path = os.path.join(OUTPUT_DIR, output_filename)
            with open(output_path, 'w') as out_file:
                json.dump(cleaned_data, out_file, indent=4)

            print(f"Processed and saved: {output_filename}")

# Run the processing function
process_html_filings()
