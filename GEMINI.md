# arXivFlow

arXivFlow is a Python-based automation tool designed to fetch research paper metadata from arXiv, extract keywords and contact information using local LLMs (Ollama), and synchronize the results with Google Sheets.

## Project Overview

- **Purpose**: Automates the tracking and processing of new research papers. It fetches data for specified arXiv categories, uses Ollama (Llama 3.2) to summarize and extract keywords/contact info from PDFs, and uploads the compiled data to a Google Sheet.
- **Main Technologies**:
  - **Python 3.13**: Core language.
  - **arxiv**: Library for querying the arXiv API.
  - **Ollama (Llama 3.2)**: Local LLM for intelligent extraction.
  - **PyMuPDF**: PDF text extraction for contact information retrieval.
  - **pandas**: Data manipulation and export to CSV, Excel, JSON, and SQLite.
  - **gspread**: Google Sheets API interaction.

## Architecture & Key Files

The project follows a modular structure located in `src/arxivflow/`.

### Core Modules
- `src/arxivflow/arxivflow.py`: Contains the `arXivFlow` class, which orchestrates the entire workflow:
  - Querying arXiv for specific categories and date ranges.
  - Downloading PDFs to the `pdfs/` directory.
  - Processing results and extracting information.
  - Saving data to CSV, JSON, Excel, SQLite, or Google Sheets.
- `src/arxivflow/ollama_functions.py`: Contains the `OllamaFunctions` class for interacting with the local Ollama API to extract keywords and contact details.

### Configuration & Data
- `user_input.json`: Configures the target Google Sheet ID, CSV filename, and credentials path.
- `credentials.json`: (User-provided) Google Service Account credentials.
- `requirements.txt`: Project dependencies.
- `pdfs/`: Local directory where downloaded research papers are stored.

## Building and Running

### Prerequisites
1. **Python 3.13+**: Ensure Python is installed.
2. **Ollama**: Install [Ollama](https://ollama.ai/) and pull the required model:
   ```bash
   ollama pull llama3.2
   ```
3. **Google Cloud Setup**:
   - Enable **Google Sheets** and **Google Drive** APIs.
   - Create a **Service Account** and save the JSON key as `credentials.json`.
   - Share the target Google Sheet with the Service Account email.

### Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv .
   source bin/activate  # On Windows: Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
The `arXivFlow` class can be used as follows:
```python
from arxivflow import arXivFlow
import datetime

# Initialize with categories and optional Ollama model
flow = arXivFlow(
    categories=["cs.AI", "cs.LG"], 
    ollama_model="llama3.2",
    max_results=50,
    start_date=datetime.datetime.now() - datetime.timedelta(days=3)
)

# Optional: Set a custom path for PDF downloads
flow.set_pdfs_path("my_papers")

# Fetch data and optionally download PDFs for contact extraction
df = flow.get_arxiv_data(download_pdfs=True)

# Save to multiple formats
flow.save_to_csv("results.csv")
flow.save_to_json("results.json")
flow.save_to_excel("results.xlsx")
flow.save_to_sqlite("results.db")

# Sync with Google Sheets
flow.save_to_google_sheet(
    sheet_id="YOUR_SHEET_ID", 
    credentials_file="credentials.json"
)
```

## Development Conventions

- **Modular Logic**: All core functionality resides in `src/arxivflow/`.
- **Local AI**: Keyword and contact extraction are performed locally using Ollama to ensure privacy and eliminate API costs. The tool automatically handles model verification and pulling.
- **Data Persistence**: Supports multiple export formats (CSV, JSON, Excel, SQLite) for flexibility.
- **Type Hinting**: The codebase uses Python type hints for better maintainability and clarity.
- **Configurable PDF Handling**: PDFs can be optionally downloaded and stored in custom directories.
