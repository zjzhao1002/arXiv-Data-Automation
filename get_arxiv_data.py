import arxiv
import pandas as pd
import os
import ollama
import json

def extract_keywords_ollama(title: str, abstract: str):
    model = "llama3.2"
    print(f"Extracting keywords using {model} for title: {title}")
    prompt = f"Extract 5 keywords from the following title and abstract:\n\nTitle: {title}\n\nAbstract: {abstract}\n\nRespond in JSON format: {{\"keywords\": [\"kw1\", \"kw2\", ...]}}"
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
            result.download_pdf(dirpath=pdf_dir)
            print(f"Downloaded PDF for {result.get_short_id()}")
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
            "Abstract": result.summary.replace("\n", " ").strip()
        })

    df = pd.DataFrame(data)
    df['Keywords'] = df.apply(lambda row: extract_keywords_ollama(row['Title'], row['Abstract']), axis=1)
    return df
