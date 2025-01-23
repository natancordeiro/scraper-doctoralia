import json
import argparse
from src.scraper import DoctorScraper
from utils.setup_logger import logger


def process_city(city: str, url: str):
    """Processa a raspagem de uma cidade específica."""
    scraper = DoctorScraper(base_url=url, city=city)
    city_data = scraper.scrape()

    # Salvar os dados da cidade em um arquivo JSON
    try:
        with open(f"data/{city.replace(' ', '_')}.json", "w", encoding="utf-8") as file:
            json.dump(city_data, file, ensure_ascii=False, indent=4)
        logger.info(f"Raspagem da cidade: {city} concluída e dados salvos em data/{city.replace(' ', '_')}.json.")
    except Exception as e:
        logger.error(f"Erro ao salvar os dados da cidade {city}: {e}")

    return city_data


def main():
    # Configurar o parser de argumentos
    parser = argparse.ArgumentParser(description="Script para raspagem de dados do Doctoralia.")
    parser.add_argument("cidade", nargs="?", default=None, help="Nome da cidade a ser processada (opcional).")
    parser.add_argument("save_all", nargs="?", default=None, help="Salvar todos os dados em um único JSON (opcional).")

    args = parser.parse_args()

    # Carregar as cidades e URLs do arquivo JSON
    try:
        with open("data/cities.json", "r", encoding="utf-8") as file:
            cities = json.load(file)
    except FileNotFoundError:
        logger.error("Arquivo cities.json não encontrado.")
        exit(1)

    # Processar cidade específica ou todas as cidades
    all_data = []
    if args.cidade:
        cidade = args.cidade
        if cidade in cities:
            logger.info(f"Processando somente a cidade: {cidade}")
            city_data = process_city(cidade, cities[cidade])
            all_data.extend(city_data)
        else:
            logger.error(f"Cidade '{cidade}' não encontrada no arquivo cities.json.")
            exit(1)
    else:
        logger.info("Processando todas as cidades.")
        for city, url in cities.items():
            city_data = process_city(city, url)
            all_data.extend(city_data)
            try:
                with open("data/doctolaria.json", "w", encoding="utf-8") as file:
                    json.dump(all_data, file, ensure_ascii=False, indent=4)
                logger.info("Raspagem concluída para todas as cidades. Dados consolidados salvos em data/doctolaria.json.")
            except Exception as e:
                logger.error(f"Erro ao salvar os dados consolidados: {e}")

    if args.save_all:
        # Salvar os dados consolidados em um único arquivo JSON
        try:
            with open("data/doctolaria.json", "w", encoding="utf-8") as file:
                json.dump(all_data, file, ensure_ascii=False, indent=4)
            logger.info("Raspagem concluída para todas as cidades. Dados consolidados salvos em data/doctolaria.json.")
        except Exception as e:
            logger.error(f"Erro ao salvar os dados consolidados: {e}")

if __name__ == "__main__":
    main()
