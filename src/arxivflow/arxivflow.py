import arxiv
import pandas as pd
import pymupdf
import os
import datetime
import sqlite3
import gspread
from .ollama_functions import OllamaFunctions

class arXivFlow:
    def __init__(self, 
                 categories: str | list[str], 
                 start_date: str | datetime.datetime = datetime.datetime.now() - datetime.timedelta(days=7), 
                 end_date: str | datetime.datetime = datetime.datetime.now(), 
                 max_results: int | None = 100, 
                 ollama_model: str | None = None
                 ):
        self.categories = categories if isinstance(categories, list) else [categories]
        self.start_date = start_date
        self.end_date = end_date
        self.max_results = int(max_results / len(self.categories)) if max_results else None
        self.ollama_model = ollama_model
        self.dfs = []

    def _get_date_string(self, date: datetime.datetime | str) -> str:
        if isinstance(date, str):
            return date+"000000"
        return date.strftime("%Y%m%d000000")

    def _category_checker(self, category: str) -> str:
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
    
    def set_pdfs_path(self, path: str) -> None:
        self.pdfs_path = path
        if not os.path.exists(self.pdfs_path):
            os.makedirs(self.pdfs_path)
    
    def _get_pdfs_path(self) -> str:
        if hasattr(self, 'pdfs_path') and self.pdfs_path:
            return self.pdfs_path
        else:
            start_date = self._get_date_string(self.start_date)
            end_date = self._get_date_string(self.end_date)
            current_dir = os.getcwd()
            pdf_dir = os.path.join(current_dir, f"pdf_{start_date[:8]}_to_{end_date[:8]}")
            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)
            return pdf_dir
    
    def get_arxiv_data(self, download_pdfs: bool = False) -> pd.DataFrame:
        start_date = self._get_date_string(self.start_date)
        end_date = self._get_date_string(self.end_date)
        for category in self.categories:
            df = self._get_category_data(category, start_date, end_date, download_pdfs)
            self.dfs.append(df)
        merged_df = pd.concat(self.dfs, ignore_index=True)
        return merged_df

    def _get_category_data(self, category: str, start_date: str, end_date: str, download_pdfs: bool = False) -> pd.DataFrame:
        if self._category_checker(category):
            print(f"Retrieving data for category {category} ({self._category_checker(category)}) from {start_date[:8]} to {end_date[:8]}...")

        client = arxiv.Client()
        query = f"cat:{category} AND submittedDate:[{start_date} TO {end_date}]"

        search = arxiv.Search(
            query=query,
            max_results=self.max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate, 
        )

        results = client.results(search)

        data = []

        if self.ollama_model is not None:
            ollama_functions = OllamaFunctions(model_name=self.ollama_model)

        for result in results:
            # Download PDF
            if download_pdfs:
                try:
                    pdf_dir = self._get_pdfs_path()
                    result.download_pdf(dirpath=pdf_dir, filename=f"{result.get_short_id()}.pdf")
                    print(f"Downloaded PDF for {result.get_short_id()}")
                    if self.ollama_model is not None:
                        doc = pymupdf.open(f"{pdf_dir}/{result.get_short_id()}.pdf")
                        page = doc[0]
                        text = page.get_text()
                        contact_info = ollama_functions.extract_contact_ollama(text) # type: ignore
                        print(f"Extracted Contact Information for {result.get_short_id()}.")
                        doc.close()
                    else:
                        contact_info = {"emails": [], "affiliations": []}
                except Exception as e:
                    print(f"Failed to download PDF for {result.get_short_id()}: {e}")
                    contact_info = {"emails": [], "affiliations": []}
            else:
                contact_info = {"emails": [], "affiliations": []}

            entry = {
                "arXiv ID": result.get_short_id(), 
                "Title": result.title, 
                "Authors": ", ".join([author.name for author in result.authors]),
                "arXiv URL": result.entry_id, 
                "PDF URL": result.pdf_url,
                "Published Date/Updated Date": result.published.strftime("%Y-%m-%d") if result.published == result.updated else result.updated.strftime("%Y-%m-%d"), 
                "Categories": ", ".join(result.categories),
                "Abstract": result.summary.replace("\n", " ").strip(),
            }

            if download_pdfs:
                emails = contact_info.get("emails", [])
                affiliations = contact_info.get("affiliations", [])
                print(affiliations)
                entry["Emails"] = ", ".join(emails) if emails else ""
                entry["Affiliations"] = "; ".join(affiliations) if affiliations else ""

            data.append(entry)

        df = pd.DataFrame(data)
        if df.empty:
            print(f"No results found for category {category} between {start_date[:8]} and {end_date[:8]}.")
            return df
        
        if self.ollama_model is not None:
            df['Keywords'] = df.apply(lambda row: ollama_functions.extract_keywords_ollama(row['Title'], row['Abstract']), axis=1)
            df["Keywords"] = df["Keywords"].apply(lambda x: ", ".join(x) if isinstance(x, list) else "")
        return df
    
    def save_to_csv(self, filename: str | None = None) -> None:
        merged_df = pd.concat(self.dfs, ignore_index=True)
        if filename is None:
            start_date = self._get_date_string(self.start_date)
            end_date = self._get_date_string(self.end_date)
            filename = f"arxiv_data_{start_date[:8]}_to_{end_date[:8]}.csv"
        merged_df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def save_to_json(self, filename: str | None = None) -> None:
        merged_df = pd.concat(self.dfs, ignore_index=True)
        if filename is None:
            start_date = self._get_date_string(self.start_date)
            end_date = self._get_date_string(self.end_date)
            filename = f"arxiv_data_{start_date[:8]}_to_{end_date[:8]}.json"
        merged_df.to_json(filename, orient='records', lines=True)
        print(f"Data saved to {filename}")

    def save_to_excel(self, filename: str | None = None) -> None:
        merged_df = pd.concat(self.dfs, ignore_index=True)
        if filename is None:
            start_date = self._get_date_string(self.start_date)
            end_date = self._get_date_string(self.end_date)
            filename = f"arxiv_data_{start_date[:8]}_to_{end_date[:8]}.xlsx"
        merged_df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")

    def save_to_sqlite(self, filename: str | None = None, table_name: str = "arxiv_data") -> None:
        merged_df = pd.concat(self.dfs, ignore_index=True)
        if filename is None:
            start_date = self._get_date_string(self.start_date)
            end_date = self._get_date_string(self.end_date)
            filename = f"arxiv_data_{start_date[:8]}_to_{end_date[:8]}.db"
        conn = sqlite3.connect(filename)
        merged_df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        print(f"Data saved to {filename} in table {table_name}")

    def save_to_google_sheet(self, sheet_id: str, credentials_file: str, sheet_name: str | None = None) -> None:
        merged_df = pd.concat(self.dfs, ignore_index=True)
        merged_df = merged_df.fillna('')  # Replace NaN with empty string for better compatibility with Google Sheets
        data = [merged_df.columns.values.tolist()] + merged_df.values.tolist()  # Convert DataFrame to list of lists
        if sheet_name is None:
            start_date = self._get_date_string(self.start_date)
            end_date = self._get_date_string(self.end_date)
            sheet_name = f"Data_{start_date[:8]}_to_{end_date[:8]}"
        try:
            gc = gspread.service_account(filename=credentials_file)
            workbook = gc.open_by_key(sheet_id)
            worksheets = workbook.worksheets()
            worksheet_titles = [ws.title for ws in worksheets]
            if sheet_name in worksheet_titles:
                worksheet = workbook.worksheet(sheet_name)
            else:
                worksheet = workbook.add_worksheet(title=sheet_name, rows=len(data), cols=len(data[0]) if data else 0)
            worksheet.clear()  # Clear existing content
            worksheet.update('A1', data)  # type: ignore # Update with new data starting from cell A1
            print("Google Sheet updated successfully.")
        except Exception as e:
            print(f"Error loading Google Sheets credentials: {e}")
            return