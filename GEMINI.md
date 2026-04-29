# arXiv Data Automation

This project is a Python-based automation tool designed to fetch research paper metadata from arXiv, extract keywords and contact information using an LLM, download PDFs, and synchronize the results with a Google Sheet.

## Project Overview

- **Purpose**: Automates the process of tracking new research papers on arXiv. It fetches data for specific categories, uses Llama 3.2 (via Ollama) to summarize/extract keywords and extract contact information (emails and affiliations) from downloaded PDFs, and uploads the compiled data to a Google Sheet for easy tracking and sharing.
- **Main Technologies**:
  - **Python 3.13**: The core programming language.
  - **arxiv**: Library for interacting with the arXiv API and downloading PDFs.
  - **Ollama (Llama 3.2)**: Used for intelligent keyword extraction from titles and abstracts, and contact information extraction from PDFs.
  - **PyMuPDF**: Used for extracting text from PDF files to enable contact information extraction.
  - **pandas**: Used for data manipulation and intermediate CSV storage.
  - **gspread**: For interacting with the Google Sheets API.
  - **Google Sheets API**: The destination for the processed data.

## Architecture & Key Files

### Core Scripts
- `main.py`: The entry point of the application. It defines the categories (`hep-ph`, `hep-ex` by default) and the date range (last 7 days), then orchestrates the fetching and sheet update process.
- `get_arxiv_data.py`: Contains logic to query the arXiv API, download PDF files to a date-stamped directory, and use `ollama` to generate 5 keywords and extract contact info for each paper. It includes a `category_checker` to validate categories and integrated model verification to ensure the Ollama model is available.
- `update_google_sheet.py`: Handles authentication with Google APIs using a service account and updates a specific spreadsheet with the new data.

### Configuration & Data
- `user_input.json`: Configures the target Google Sheet ID, the intermediate CSV filename, and the path to the Google credentials file.
- `credentials.json`: (User-provided) Google Service Account credentials for API access.
- `arxiv_data.csv`: Intermediate CSV file where fetched data is stored before being uploaded to Google Sheets.
- `pdf_[START_DATE]_to_[END_DATE]/`: Local directory created automatically to store downloaded research papers.

## Building and Running

### Prerequisites
1.  **Python 3.13+**: Ensure Python is installed and the virtual environment is activated (`source bin/activate`).
2.  **Ollama**: Install [Ollama](https://ollama.ai/) and pull the required model:
    ```bash
    ollama pull llama3.2
    ```
3.  **Google Cloud Setup**:
    - Enable the **Google Sheets API** and **Google Drive API** in the Google Cloud Console.
    - Create a **Service Account** and download the JSON key as `credentials.json`.
    - Share your target Google Sheet with the Service Account's email address (with Editor permissions).

### Execution
Run the main script to fetch data, download PDFs, and update the sheet:
```bash
python main.py
```

## Development Conventions

- **Modular Design**: Logic is separated into fetching, processing, and uploading modules.
- **Automated Downloads**: PDF files are automatically retrieved and organized into folders named by date range.
- **LLM Integration**: Keyword and contact information extraction are performed locally using Ollama, ensuring data privacy and no API costs.
- **Data Persistence**: Data is first saved to a local CSV (`arxiv_data.csv`) before being pushed to Google Sheets, providing a local backup.
- **Categorization and Validation**: The tool supports a wide range of arXiv categories. The `category_checker` in `get_arxiv_data.py` ensures that only valid categories are processed and provides human-readable names for logging.
- **Model Verification and Auto-Pull**: The tool automatically checks for the required Ollama model before processing. If the model is missing, it prompts the user to pull it automatically.
