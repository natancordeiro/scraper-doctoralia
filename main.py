import os
import json
import logging
import pandas as pd
from src.scraper import DoctorScraper

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

COLUNAS = [
    "Nome", "Local", "estado", "Especialidade",
    "Phone", "Faz teleconsulta", "telefone",
    "site", "rede social", "link"
]

def exportar_para_excel(resultados, caminho_arquivo):
    df = pd.DataFrame(resultados, columns=COLUNAS)
    os.makedirs("export", exist_ok=True)
    df.to_excel(os.path.join("export", caminho_arquivo), index=False)
    logger.info(f"Arquivo Excel salvo em export/{caminho_arquivo}")

def carregar_filtros():
    with open("data/filtros.json", "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    filtros = carregar_filtros()
    for cidade, url in filtros.items():
        logger.info("Iniciando raspagem para a cidade: %s", cidade)
        scraper = DoctorScraper(url, cidade)
        resultados = scraper.scrape()
        flat_resultados = [doc["data"] for doc in resultados if "data" in doc]
        exportar_para_excel(flat_resultados, f"{cidade}.xlsx")
    logger.info("Processo concluído.")

if __name__ == "__main__":
    main()
