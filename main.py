import json
from src.scraper import DoctorScraper
from utils.setup_logger import logger

def main():

    # Carregar as cidades e URLs do arquivo JSON
    try:
        with open("data/filtros.json", "r", encoding="utf-8") as file:
            filtros = json.load(file)
    except FileNotFoundError:
        logger.error("Arquivo filtros.json não encontrado.")
        exit(1)

    # Processar cidade específica ou todas as cidades
    logger.info("Processando dados.")
    for nome, url in filtros.items():

        # Extrai as informações
        scraper = DoctorScraper(base_url=url, nome=nome)
        data = scraper.scrape()

         # Salvar os dados da cidade em um arquivo JSON
        try:
            with open(f"data/{nome.replace(' ', '_')}.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logger.info(f"Raspagem dos dados: {nome} concluída e dados salvos em data/{nome.replace(' ', '_')}.json.")
        except Exception as e:
            logger.error(f"Erro ao salvar os dados do {nome}: {e}")

if __name__ == "__main__":
    main()
