import re
import json
import time
import httpx
from httpx import HTTPStatusError, RequestError
from bs4 import BeautifulSoup
from tqdm import tqdm

from utils.setup_logger import logger
from utils.parsing import extract_specialties

class DoctorScraper:
    def __init__(self, base_url: str, nome: str):
        self.base_url = base_url
        self.nome = nome
        self.client = httpx.Client()
        logger.info(f"Scraper inicializado para {nome}.")

    def get_last_page(self, url: str) -> int:
        """Obtém o número da última página a partir da paginação."""
        max_retries = 3

        for attempt in range(1, max_retries + 1):
            try:
                response = self.client.get(url, timeout=10)
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
            except (HTTPStatusError, RequestError) as e:
                logger.warning(f"Tentativa {attempt}/{max_retries} falhou. Erro: {e}")
                if attempt == max_retries:
                    logger.error(f"Erro ao obter última página após {max_retries} tentativas: {e}")
                    return 1
            except Exception as e:
                logger.error(f"Erro inesperado ao obter última página: {e}")
                return 1

    def scrape_page(self, url: str) -> list:
        """Raspa os dados de uma única página."""
        try:
            response = self.client.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            doctors = []
            all_doctors = soup.select("#search-content > ul > li")
            for i, item in enumerate(all_doctors):
                try:
                    link_tag = item.select_one("a")
                    name_tag = item.select_one("span[itemprop='name']")
                    location_tag = item.select_one("span.text-truncate")
                    specialties_tag = item.select_one("span[data-test-id='doctor-specializations']")

                    link_to_profile = link_tag["href"] if link_tag else None
                    professional = name_tag.text.strip() if name_tag else None
                    specialties = extract_specialties(specialties_tag.text.strip() if specialties_tag else "")

                    details = self.get_profile_details(link_to_profile)

                    doctors.append({
                        "Name": professional,
                        "Location": location_tag.text.strip() if location_tag else None,
                        "Specialties": specialties,
                        **details,
                        "URL": link_to_profile
                    })

                except Exception as e:
                    logger.error(f"Erro ao processar dados de um médico: {e}")
            logger.info(f"{len(doctors)} médicos encontrados na página.")
            return doctors
        except Exception as e:
            logger.error(f"Erro ao raspar página: {e}")
            return []
    
    def get_profile_details(self, profile_url: str) -> dict:
        """Obtém informações adicionais do perfil do profissional."""
        try:
            response = self.client.get(profile_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Captura todos os números de telefone e remove duplicatas
            phone_numbers = list({phone.text.strip() for phone in soup.select("a[data-one-tracking-object_type='phone_number'] > b") if phone.text.strip()})

            # Captura todos os sites/emails e remove duplicatas
            websites_emails = list({website.text.strip() for website in soup.select("a[data-patient-app-event-name='dp-doctor-website']") if website.text.strip()})

            # Se houver mais de um item, separa com vírgula. Se não houver, retorna uma string vazia.
            phone_str = phone_numbers[0] if len(phone_numbers) == 1 else ", ".join(phone_numbers) if phone_numbers else ""
            website_str = websites_emails[0] if len(websites_emails) == 1 else ", ".join(websites_emails) if websites_emails else ""

            return {
                "Phone": phone_str,
                "Has Teleconsultation": "Yes" if soup.select_one("i.svg-icon-video-consultation") else "No",
                "Website/Email": website_str,
            }

        except Exception as e:
            logger.error(f"Erro ao obter detalhes do perfil: {e}")
            return {}

    def scrape(self) -> list:
        """Orquestra o processo de raspagem para todas as páginas."""
        
        logger.info(f"Iniciando raspagem para: {self.nome}")
        all_doctors = []
        last_page = self.get_last_page(self.base_url)

        # Processar todas as páginas normalmente
        for page in range(1, last_page + 1):
            logger.info(f"Raspando página {page}/{last_page}...")

            if "page=" in self.base_url:
                page_url = self.base_url.replace("page=1", f"page={page}")
            else:
                connector = "&" if "?" in self.base_url else "?"
                page_url = f"{self.base_url}{connector}page={page}"

            doctors = self.scrape_page(page_url)
            all_doctors.extend(doctors)

        logger.info(f"Raspagem concluída para {self.nome}. Total de médicos: {len(all_doctors)}")
        return all_doctors