import httpx
from bs4 import BeautifulSoup
from utils.setup_logger import setup_logger

# Configurando o logger
logger = setup_logger("scraper", "scraper.log")

class DoctorScraper:
    def __init__(self, base_url: str, city: str):
        self.base_url = base_url
        self.city = city
        self.client = httpx.Client()
        logger.info(f"Scraper inicializado para {city}.")

    def get_last_page(self, url: str) -> int:
        """Obtém o número da última página a partir da paginação."""
        try:
            response = self.client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            last_page_tags = soup.select("a.page-link:not([aria-label='next'])")
            if last_page_tags:
                last_page = int(last_page_tags[-1].text.strip())
                logger.info(f"Última página encontrada: {last_page}")
                return last_page
            else:
                logger.warning("Não foi possível encontrar a última página.")
                return 1
        except Exception as e:
            logger.error(f"Erro ao obter última página: {e}")
            return 1

    def scrape_page(self, url: str) -> list:
        """Raspa os dados de uma única página."""
        try:
            response = self.client.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            doctors = []
            for item in soup.select("#search-content ul > li"):
                try:
                    link_tag = item.select_one("a")
                    name_tag = item.select_one("span[itemprop='name']")
                    reviews_tag = item.select_one("span.opinion-numeral")

                    link_to_profile = link_tag["href"] if link_tag else None
                    professional = name_tag.text.strip() if name_tag else None
                    reviews = (
                        int(reviews_tag.text.strip().split()[0]) if reviews_tag else 0
                    )
                    doctors.append({
                        "professional": professional,
                        "link_to_profile": link_to_profile,
                        "reviews": reviews,
                        "city": self.city,
                    })
                except Exception as e:
                    logger.error(f"Erro ao processar dados de um médico: {e}")
            logger.info(f"{len(doctors)} médicos encontrados na página.")
            return doctors
        except Exception as e:
            logger.error(f"Erro ao raspar página: {e}")
            return []

    def scrape(self) -> list:
        """Orquestra o processo de raspagem para todas as páginas."""
        
        logger.info(f"Iniciando raspagem para a cidade: {self.city}")
        all_doctors = []
        last_page = self.get_last_page(self.base_url)

        for page in range(1, last_page + 1):
            logger.info(f"Raspando página {page}/{last_page}...")
            page_url = f"{self.base_url}&page={page}"
            doctors = self.scrape_page(page_url)
            all_doctors.extend(doctors)

        logger.info(f"Raspagem concluída para {self.city}. Total de médicos: {len(all_doctors)}")
        return all_doctors
