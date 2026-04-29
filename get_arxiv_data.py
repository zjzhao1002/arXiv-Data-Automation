import arxiv
import pandas as pd
import os
import ollama
import json
import pymupdf

def category_checker(category: str):
    all_categories = {
        "cs.AI": "Artificial Intelligence",
        "cs.AR": "Hardware Architecture",
        "cs.CC": "Computational Complexity",
        "cs.CE": "Computational Engineering, Finance, and Science",
        "cs.CG": "Computational Geometry",
        "cs.CL": "Computation and Language",
        "cs.CR": "Cryptography and Security",
        "cs.CV": "Computer Vision and Pattern Recognition",
        "cs.CY": "Computers and Society",
        "cs.DB": "Databases",
        "cs.DC": "Distributed, Parallel, and Cluster Computing",
        "cs.DL": "Digital Libraries",
        "cs.DM": "Discrete Mathematics",
        "cs.DS": "Data Structures and Algorithms",
        "cs.ET": "Emerging Technologies",
        "cs.FL": "Formal Languages and Automata Theory",
        "cs.GL": "General Literature",
        "cs.GR": "Graphics",
        "cs.GT": "Computer Science and Game Theory",
        "cs.HC": "Human-Computer Interaction",
        "cs.IR": "Information Retrieval",
        "cs.IT": "Information Theory",
        "cs.LG": "Machine Learning",
        "cs.LO": "Logic in Computer Science",
        "cs.MA": "Multiagent Systems",
        "cs.MM": "Multimedia",
        "cs.MS": "Mathematical Software",
        "cs.NA": "Numerical Analysis",
        "cs.NE": "Neural and Evolutionary Computing",
        "cs.NI": "Networking and Internet Architecture",
        "cs.OH": "Other Computer Science",
        "cs.OS": "Operating Systems",
        "cs.PF": "Performance",
        "cs.PL": "Programming Languages",
        "cs.RO": "Robotics",
        "cs.SC": "Symbolic Computation",
        "cs.SD": "Sound",
        "cs.SE": "Software Engineering",
        "cs.SI": "Social and Information Networks",
        "cs.SY": "Systems and Control",
        "econ.EM": "Econometrics",
        "econ.GN": "General Economics",
        "econ.TH": "Theoretical Economics",
        "eess.AS": "Audio and Speech Processing",
        "eess.IV": "Image and Video Processing",
        "eess.SP": "Signal Processing",
        "eess.SY": "Systems and Control",
        "math.AC": "Commutative Algebra",
        "math.AG": "Algebraic Geometry",
        "math.AP": "Analysis of PDEs",
        "math.AT": "Algebraic Topology",
        "math.CA": "Classical Analysis and ODEs",
        "math.CO": "Combinatorics",
        "math.CT": "Category Theory",
        "math.CV": "Complex Variables",
        "math.DG": "Differential Geometry",
        "math.DS": "Dynamical Systems",
        "math.FA": "Functional Analysis",
        "math.GM": "General Mathematics",
        "math.GN": "General Topology",
        "math.GR": "Group Theory",
        "math.GT": "Geometric Topology",
        "math.HO": "History and Overview",
        "math.IT": "Information Theory",
        "math.KT": "K-Theory and Homology",
        "math.LO": "Logic",
        "math.MG": "Metric Geometry",
        "math.MP": "Mathematical Physics",
        "math.NA": "Numerical Analysis",
        "math.NT": "Number Theory",
        "math.OA": "Operator Algebras",
        "math.OC": "Optimization and Control",
        "math.PR": "Probability",
        "math.QA": "Quantum Algebra",
        "math.RA": "Rings and Algebras",
        "math.RT": "Representation Theory",
        "math.SG": "Symplectic Geometry",
        "math.SP": "Spectral Theory",
        "math.ST": "Statistics Theory",
        "astro-ph.CO": "Cosmology and Nongalactic Astrophysics",
        "astro-ph.EP": "Earth and Planetary Astrophysics",
        "astro-ph.GA": "Astrophysics of Galaxies",
        "astro-ph.HE": "High Energy Astrophysical Phenomena",
        "astro-ph.IM": "Instrumentation and Methods for Astrophysics",
        "astro-ph.SR": "Solar and Stellar Astrophysics",
        "cond-mat.dis-nn": "Disordered Systems and Neural Networks",
        "cond-mat.mes-hall": "Mesoscale and Nanoscale Physics",
        "cond-mat.mtrl-sci": "Materials Science",
        "cond-mat.other": "Other Condensed Matter",
        "cond-mat.quant-gas": "Quantum Gases",
        "cond-mat.soft": "Soft Condensed Matter",
        "cond-mat.stat-mech": "Statistical Mechanics",
        "cond-mat.str-el": "Strongly Correlated Electrons",
        "cond-mat.supr-con": "Superconductivity",
        "gr-qc": "General Relativity and Quantum Cosmology",
        "hep-ex": "High Energy Physics - Experiment",
        "hep-lat": "High Energy Physics - Lattice",
        "hep-ph": "High Energy Physics - Phenomenology",
        "hep-th": "High Energy Physics - Theory",
        "math-ph": "Mathematical Physics",
        "nlin.AO": "Adaptation and Self-Organizing Systems",
        "nlin.CD": "Chaotic Dynamics",
        "nlin.CG": "Cellular Automata and Lattice Gases",
        "nlin.PS": "Pattern Formation and Solitons",
        "nlin.SI": "Exactly Solvable and Integrable Systems",
        "nucl-ex": "Nuclear Experiment",
        "nucl-th": "Nuclear Theory",
        "physics.acc-ph": "Accelerator Physics",
        "physics.ao-ph": "Atmospheric and Oceanic Physics",
        "physics.app-ph": "Applied Physics",
        "physics.atm-clus": "Atomic and Molecular Clusters",
        "physics.atom-ph": "Atomic Physics",
        "physics.bio-ph": "Biological Physics",
        "physics.chem-ph": "Chemical Physics",
        "physics.class-ph": "Classical Physics",
        "physics.comp-ph": "Computational Physics",
        "physics.data-an": "Data Analysis, Statistics and Probability",
        "physics.ed-ph": "Physics Education",
        "physics.flu-dyn": "Fluid Dynamics",
        "physics.gen-ph": "General Physics",
        "physics.geo-ph": "Geophysics",
        "physics.hist-ph": "History and Philosophy of Physics",
        "physics.ins-det": "Instrumentation and Detectors",
        "physics.med-ph": "Medical Physics",
        "physics.optics": "Optics",
        "physics.plasm-ph": "Plasma Physics",
        "physics.pop-ph": "Popular Physics",
        "physics.soc-ph": "Physics and Society",
        "physics.space-ph": "Space Physics",
        "quant-ph": "Quantum Physics",
        "q-bio.BM": "Biomolecules",
        "q-bio.CB": "Cell Behavior",
        "q-bio.GN": "Genomics",
        "q-bio.MN": "Molecular Networks",
        "q-bio.NC": "Neurons and Cognition",
        "q-bio.OT": "Other Quantitative Biology",
        "q-bio.PE": "Populations and Evolution",
        "q-bio.QM": "Quantitative Methods",
        "q-bio.SC": "Subcellular Processes",
        "q-bio.TO": "Tissues and Organs",
        "q-fin.CP": "Computational Finance",
        "q-fin.EC": "Economics",
        "q-fin.GN": "General Finance",
        "q-fin.MF": "Mathematical Finance",
        "q-fin.PM": "Portfolio Management",
        "q-fin.PR": "Pricing of Securities",
        "q-fin.RM": "Risk Management",
        "q-fin.ST": "Statistical Finance",
        "q-fin.TR": "Trading and Market Microstructure",
        "stat.AP": "Applications",
        "stat.CO": "Computation",
        "stat.ME": "Methodology",
        "stat.ML": "Machine Learning",
        "stat.OT": "Other Statistics",
        "stat.TH": "Statistics Theory"
    }
    if category not in all_categories.keys():
        raise ValueError(f"Invalid category: {category}. Please choose from the following categories: {', '.join(all_categories.keys())}")
    return all_categories[category]

def ollama_model_checker(model_name: str) -> bool:
    available_models = ollama.list()
    model_names = [model['model'] for model in available_models.models]
    if f"{model_name}:latest" in model_names:
        return True
    else:
        print(f"Model '{model_name}' is not available in Ollama. Available models are: {', '.join(model_names)}")
        return False

def ollama_pull_model(model_name: str):
    ollama.pull(model_name)
    print(f"Model '{model_name}' pulled successfully.")

def extract_keywords_ollama(title: str, abstract: str, model_name: str = "llama3.2") -> list:
    
    if not ollama_model_checker(model_name):
        print(f"Do you want to pull the model '{model_name}' from the Ollama registry? (yes/no)")
        user_input = input().strip().lower()
        if user_input == 'yes':
            ollama_pull_model(model_name)
        else:
            print("Model pull cancelled by user.")
            return []

    print(f"Extracting keywords using {model_name} for title: {title}")
    prompt = f"""
    Extract 5 keywords from the following title and abstract:\n\n
    Title: {title}\n\n
    Abstract: {abstract}\n\n
    Respond in JSON format: {{\"keywords\": [\"kw1\", \"kw2\", ...]}}
    """
    response = ollama.chat(
        model=model_name, 
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

def extract_contact_ollama(text: str, model_name: str = "llama3.2") -> dict:
    if not ollama_model_checker(model_name):
        print(f"Do you want to pull the model '{model_name}' from the Ollama registry? (yes/no)")
        user_input = input().strip().lower()
        if user_input == 'yes':
            ollama_pull_model(model_name)
        else:
            print("Model pull cancelled by user.")
            return {"emails": [], "affiliations": []}

    prompt = f"""
    Extract the emails and affiliations from the following text:\n\n
    {text}\n\n
    Return the contact information in a JSON format: {{\"emails\": [], \"affiliations\": []}}. 
    Don't add any keys to the JSON object. Don't guess if you don't see any contact information in the text.
    """
    response = ollama.chat(model=model_name, format="json", messages=[{"role": "user", "content": prompt}])
    raw_content = response['message']['content']
    try:
        content_json = json.loads(raw_content)
        return content_json
    except json.JSONDecodeError:
        print(f"Error decoding JSON from Ollama response: {raw_content}")
        return {"emails": [], "affiliations": []}

def get_arxiv_data(category: str, start_date: str, end_date: str):
    if category_checker(category):
        print(f"Retrieving data for category {category} ({category_checker(category)}) from {start_date} to {end_date}...")

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
            contact_info = extract_contact_ollama(text, "llama3.2")  # type: ignore
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
    
    df['Keywords'] = df.apply(lambda row: extract_keywords_ollama(row['Title'], row['Abstract'], "llama3.2"), axis=1)
    return df
