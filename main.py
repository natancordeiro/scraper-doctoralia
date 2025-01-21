# main.py
import json
from src.scraper import DoctorScraper
from utils.setup_logger import setup_logger

logger = setup_logger("main")

if __name__ == "__main__":
    # Carregar as cidades e URLs do arquivo JSON
    try:
        with open("data/cities.json", "r", encoding="utf-8") as file:
            cities = json.load(file)
    except FileNotFoundError:
        logger.error("Arquivo cities.json não encontrado.")
        exit(1)
    
    all_data = []
    for city, url in cities.items():
        scraper = DoctorScraper(base_url=url, city=city)
        city_data = scraper.scrape()
        all_data.extend(city_data)

    # Salvar os dados em um arquivo JSON
    try:
        with open("data/output.json", "w", encoding="utf-8") as file:
            json.dump(all_data, file, ensure_ascii=False, indent=4)
        logger.info("Raspagem concluída e dados salvos em data/output.json.")
    except Exception as e:
        logger.error(f"Erro ao salvar os dados: {e}")

# utils/http_client.py
import httpx
from utils.setup_logger import setup_logger

logger = setup_logger("http_client")

def get_http_client() -> httpx.Client:
    """Cria e retorna uma instância de cliente HTTPX configurado."""
    try:
        client = httpx.Client(timeout=30)
        logger.info("Cliente HTTP criado com sucesso.")
        return client
    except Exception as e:
        logger.error(f"Erro ao criar cliente HTTP: {e}")
        raise