# arXiv-Data-Automation 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-Llama3.2-orange.svg)](https://ollama.ai/)

A Python-based automation tool that streamlines research paper tracking by fetching data from arXiv, downloading PDFs, performing local AI-driven keyword extraction, and synchronizing everything to Google Sheets.

## ✨ Features

- **Automated Retrieval**: Fetches the latest research papers from arXiv for specified categories (e.g., `hep-ph`, `hep-ex`).
- **PDF Downloader**: Automatically downloads and organizes research papers in PDF format into date-stamped local directories.
- **Local AI Analysis**: Uses **Ollama (Llama 3.2)** to analyze abstracts and extract relevant keywords, as well as extract contact information (emails and affiliations) directly from PDFs, without sending data to external cloud LLM APIs.
- **Google Sheets Sync**: Automatically updates a Google Spreadsheet with new paper metadata (Title, Authors, arXiv URL, PDF link, AI-generated keywords, and extracted contact info).
- **CSV Export**: Maintains a local `arxiv_data.csv` for data persistence and offline use.

## 🛠️ Prerequisites

1. **Python 3.13+**: Ensure you have a modern Python version installed.
2. **Ollama**: Install [Ollama](https://ollama.ai/) and download the Llama 3.2 model:
   ```bash
   ollama pull llama3.2
   ```
3. **Google Cloud Credentials**:
   - Enable the Google Sheets and Google Drive APIs.
   - Create a Service Account and download the JSON key as `credentials.json`.
   - Share your target Google Sheet with the service account's email (Editor access).

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/arXiv-Data-Automation.git
   cd arXiv-Data-Automation
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv .
   source bin/activate  # On Windows: Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: Ensure you have `arxiv`, `pandas`, `gspread`, `ollama`, and `google-auth` installed.)*

## ⚙️ Configuration

Update `user_input.json` with your specific details:

```json
{
    "sheet_id": "YOUR_GOOGLE_SHEET_ID_HERE", 
    "csv_file": "arxiv_data.csv",
    "credentials_file": "credentials.json"
}
```

## 📖 Usage

Simply run the main script to trigger the automation:

```bash
python main.py
```

The script will:
1. Fetch papers from the last 7 days for the configured categories.
2. **Download all related PDFs to a local directory.**
3. Verify the Ollama model (and prompt to pull if missing).
4. Generate keywords and extract contact info using Llama 3.2.
5. Save data to `arxiv_data.csv`.
6. Create/Update a worksheet in your Google Sheet named `Data_[StartDate]_to_[EndDate]`.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
