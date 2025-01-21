# main.py
import json
from src.scraper import DoctorScraper
from utils.setup_logger import logger

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
            with open(f"data/{city}.json", "w", encoding="utf-8") as file:
                json.dump(all_data, file, ensure_ascii=False, indent=4)
            logger.info(f"Raspagem da cidade: {city} concluída e dados salvos em data/{city}.json.")
        except Exception as e:
            logger.error(f"Erro ao salvar os dados: {e}")
