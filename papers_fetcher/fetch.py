from typing import List, Dict
from Bio import Entrez
import time
from papers_fetcher.utils import is_non_academic, extract_email_and_company

# ✅ Define the paper structure
class PubMedPaper:
    def __init__(
        self,
        pmid: str,
        title: str,
        date: str,
        non_academic_authors: List[str],
        companies: List[str],
        email: str
    ):
        self.pmid = pmid
        self.title = title
        self.date = date
        self.non_academic_authors = non_academic_authors
        self.companies = companies
        self.email = email

    def to_dict(self) -> Dict:
        return {
            "PubmedID": self.pmid,
            "Title": self.title,
            "Publication Date": self.date,
            "Non-academicAuthor(s)": "; ".join(self.non_academic_authors),
            "CompanyAffiliation(s)": "; ".join(self.companies),
            "Corresponding Author Email": self.email
        }

# ✅ Define the function
def fetch_papers(query: str, max_results: int = 10, debug: bool = False) -> List[PubMedPaper]:
    Entrez.email = "your_email@example.com"  # Change to your real email
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    ids = record["IdList"]
    time.sleep(0.3)

    if debug:
        print(f"Found {len(ids)} papers: {ids}")

    results = []
    handle = Entrez.efetch(db="pubmed", id=','.join(ids), rettype="medline", retmode="text")
    from Bio import Medline
    records = Medline.parse(handle)

    for rec in records:
        pmid = rec.get("PMID", "")
        title = rec.get("TI", "")
        date = rec.get("DP", "")
        affils = rec.get("AD", [])

        if isinstance(affils, str):
            affils = [affils]

        non_acads = []
        companies = []
        email = ""

        for affil in affils:
            if is_non_academic(affil):
                name, comp = extract_email_and_company(affil)
                if name:
                    non_acads.append(name)
                if comp:
                    companies.append(comp)
                if "@" in affil:
                    email = affil.split()[-1]

        if non_acads:
            results.append(PubMedPaper(pmid, title, date, non_acads, companies, email))

    return results
