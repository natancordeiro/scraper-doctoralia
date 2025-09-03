import json
from openpyxl import Workbook
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
        scraper = DoctorScraper(base_url=url, city=nome)
        data = scraper.scrape()

        # Verifica se há dados antes de salvar
        if data:
            try:
                # Criar um novo arquivo Excel
                wb = Workbook()
                ws = wb.active
                ws.title = nome

                # Adicionar cabeçalhos (chaves do primeiro item)
                headers = list(data[0].keys()) if data else []
                ws.append(headers)

                # Adicionar os dados ao arquivo Excel
                for item in data:
                    ws.append(list(item.values()))

                # Definir caminho do arquivo
                caminho_arquivo = f"data/{nome.replace(' ', '_')}.xlsx"
                wb.save(caminho_arquivo)

                logger.info(f"Raspagem dos dados: {nome} concluída e dados salvos em {caminho_arquivo}.")
            except Exception as e:
                logger.error(f"Erro ao salvar os dados do {nome}: {e}")
        else:
            logger.warning(f"Nenhum dado encontrado para {nome}.")

if __name__ == "__main__":
    main()
