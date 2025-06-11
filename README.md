# 🚀 My Awesome Project

Welcome to **My Awesome Project**! This README will guide you through setting up the project on your local machine.

<!-- ---

## 📦 Prerequisites

Before you begin, make sure you have the following installed:

- [Git](https://git-scm.com/)
- [Python 3.10+](https://www.python.org/) (or your project's language/runtime)
- [Docker](https://www.docker.com/) *(optional)*
- Code editor (e.g., VSCode)

--- -->

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/my-awesome-project.git
cd my-awesome-project
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download data

```bash
python3 data_grbber.py # or visit https://www.sec.gov/search-filings/edgar-application-programming-interfaces
```
This should create two folders (submissions_data and xbrl_data). Detailed explination on the two folders can be found here. 

<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>


## 📁 EDGAR Bulk Data Folders Overview

After unzipping the SEC bulk data ZIP files, you'll get two main folders:

---

### 📁 `xbrl_data/` (from `companyfacts.zip`)

This folder contains:
- **One JSON file per company** (by CIK)
- Each file includes **financial statement data** extracted from 10-Ks, 10-Qs, etc.
- Data is structured by accounting concepts like:
  - `NetIncomeLoss`
  - `Revenues`
  - `Assets`
  - `EarningsPerShareDiluted`
- This is the **main source of numerical financial data** to train machine learning models.

> 🧾 “What did each company report?” (Actual financial numbers, by quarter/year)

---

### 📁 `submissions_data/` (from `submissions.zip`)

This folder contains:
- **Filing metadata** for each company (also by CIK)
- Each file lists filings with:
  - Filing date
  - Form type (`10-K`, `10-Q`, etc.)
  - Accession numbers (used to build URLs to documents)

> 📅 “When did the company file, and what documents?”

---

### 🧠 Summary

| Folder              | What's Inside?                      | Use Case                              |
|--------------------|--------------------------------------|----------------------------------------|
| `xbrl_data/`        | Financial numbers (XBRL facts)       | Train ML models on actual financials   |
| `submissions_data/` | Filing metadata (filing history)     | Track timing, link to raw filings      |


<!-- ### 4. Configure Environment Variables

Copy the sample `.env` file and modify it with your settings:

```bash
cp .env.example .env
```

Edit the `.env` file:

```ini
API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
DEBUG=True
```

### 5. Run the Application

```bash
python main.py
```

Or using Docker:

```bash
docker compose up --build
```

---

## ✅ Test the Setup

To verify everything is working:

1. Open your browser and go to: `http://localhost:8000`
2. Ensure no errors appear in the terminal
3. Optionally, run tests:

```bash
pytest
```

---

## 💡 Tips

- Use `black` and `flake8` to format and lint your code.
- Run `deactivate` to exit the virtual environment when done.

---

## 📬 Need Help?

If you encounter issues, open an [issue](https://github.com/your-username/my-awesome-project/issues) or contact the maintainer. -->
