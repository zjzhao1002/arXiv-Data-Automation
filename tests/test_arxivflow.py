import os
_parent_dp = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_src_dp = os.path.join(_parent_dp, 'src')
import sys
sys.path.insert(0, _src_dp)

from arxivflow import arxivflow

def test_get_arxiv_data():
    # Initialize the arXivFlow class
    categories = ["cs.AI", "cs.LG"]
    arxiv_flow = arxivflow.arXivFlow(categories=categories, max_results=5, ollama_model="llama3.2")
    
    # Test case 1: Do not download PDFs
    df1 = arxiv_flow.get_arxiv_data(download_pdfs=False)
    assert not df1.empty
    assert "arXiv ID" in df1.columns
    assert "Title" in df1.columns
    assert "Authors" in df1.columns
    assert "Published Date/Updated Date" in df1.columns
    assert "Categories" in df1.columns
    assert "Abstract" in df1.columns

    # Test case 2: Download PDFs and extract contact information
    df2 = arxiv_flow.get_arxiv_data(download_pdfs=True)
    assert not df2.empty
    assert "Emails" in df2.columns
    assert "Affiliations" in df2.columns