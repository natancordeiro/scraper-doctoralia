from typing import List

def extract_specialties(specializations_text: str) -> str:
    """Extrai especialidades a partir do texto encontrado na tag data-test-id."""
    if not specializations_text:
        return []
    specialties = [specialty.strip() for specialty in specializations_text.split(",") if specialty.strip()]
    return ", ".join(specialties) if specialties else ""