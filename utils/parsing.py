import re
from typing import List

def extract_specialties(spans: List[str]) -> List[str]:
    """Extrai especialidades a partir de uma lista de textos de spans."""
    specialties = []
    for text in spans:
        if "RQE" not in text and "CRM" not in text:
            match = re.search(r"-\s(.+?)\sRQE", text)
            if match:
                specialties.append(match.group(1).strip())
    return specialties if specialties else None
