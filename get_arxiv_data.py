import arxiv
import pandas as pd
import os
import ollama
import json
import pymupdf

def extract_keywords_ollama(title: str, abstract: str):
    model = "llama3.2"
    print(f"Extracting keywords using {model} for title: {title}")
    prompt = f"""
    Extract 5 keywords from the following title and abstract:\n\n
    Title: {title}\n\n
    Abstract: {abstract}\n\n
    Respond in JSON format: {{\"keywords\": [\"kw1\", \"kw2\", ...]}}
    """
    response = ollama.chat(
        model=model, 
        format="json",
        messages=[{"role": "user", "content": prompt}])
    raw_content = response['message']['content']
    try:
        content_json = json.loads(raw_content)
        keywords = content_json.get("keywords", [])
    except json.JSONDecodeError:
        print(f"Error decoding JSON from Ollama response: {raw_content}")
        keywords = []
    return keywords

def extract_contact_ollama(text: str) -> dict:
    model = "llama3.2"
    prompt = f"""
    Extract the emails and affiliations from the following text:\n\n
    {text}\n\n
    Return the contact information in a JSON format: {{\"emails\": [], \"affiliations\": []}}. 
    Don't add any keys to the JSON object. Don't guess if you don't see any contact information in the text.
    """
    response = ollama.chat(model=model, format="json", messages=[{"role": "user", "content": prompt}])
    raw_content = response['message']['content']
    try:
        content_json = json.loads(raw_content)
        return content_json
    except json.JSONDecodeError:
        print(f"Error decoding JSON from Ollama response: {raw_content}")
        return {"emails": [], "affiliations": []}

def get_arxiv_data(category: str, start_date: str, end_date: str):
    client = arxiv.Client()
    query = f"cat:{category} AND submittedDate:[{start_date} TO {end_date}]"

    search = arxiv.Search(
        query=query,
        max_results=None,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )

    results = client.results(search)

    data = []
    
    # Create directory for PDFs
    pdf_dir = f"./pdf_{start_date[:8]}_to_{end_date[:8]}"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    for result in results:
        # Download PDF
        try:
            result.download_pdf(dirpath=pdf_dir, filename=f"{result.get_short_id()}.pdf")
            print(f"Downloaded PDF for {result.get_short_id()}")
            doc = pymupdf.open(f"{pdf_dir}/{result.get_short_id()}.pdf")
            page = doc[0]
            text = page.get_text()
            contact_info = extract_contact_ollama(text)  # type: ignore
            print(f"Extracted Contact Information for {result.get_short_id()}:\n{contact_info}")
            doc.close()
        except Exception as e:
            print(f"Failed to download PDF for {result.get_short_id()}: {e}")

        data.append({
            "arXiv ID": result.get_short_id(), 
            "Title": result.title, 
            "Authors": ", ".join([author.name for author in result.authors]),
            "arXiv URL": result.entry_id, 
            "PDF URL": result.pdf_url,
            "Published Date/Updated Date": result.published.strftime("%Y-%m-%d") if result.published != result.updated else result.published.strftime("%Y-%m-%d"), 
            "Categories": ", ".join(result.categories),
            "Abstract": result.summary.replace("\n", " ").strip(),
            "Emails": contact_info.get("emails", []), 
            "Affiliations": contact_info.get("affiliations", []) 
        })

    df = pd.DataFrame(data)
    if df.empty:
        print(f"No results found for category {category} between {start_date} and {end_date}.")
        return df
    
    df['Keywords'] = df.apply(lambda row: extract_keywords_ollama(row['Title'], row['Abstract']), axis=1)
    return df
