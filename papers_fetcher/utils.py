import re
from typing import Tuple

def is_non_academic(affiliation: str) -> bool:
    academic_keywords = [
        "university", "college", "institute", "school",
        "hospital", "research", "center", "faculty", "department"
    ]
    return not any(word in affiliation.lower() for word in academic_keywords)

def extract_email_and_company(affil: str) -> Tuple[str, str]:
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", affil)
    company_match = re.search(r"([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)", affil)
    email = email_match.group(0) if email_match else ""
    company = company_match.group(0) if company_match else ""
    return email, company
