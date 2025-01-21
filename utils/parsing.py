from typing import List

def extract_specialties(specializations_text: str) -> List[str]:
    """Extrai especialidades a partir do texto encontrado na tag data-test-id."""
    if not specializations_text:
        return []
    return [specialty.strip() for specialty in specializations_text.split(",")]