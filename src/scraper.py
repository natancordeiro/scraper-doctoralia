import re
import json
import httpx
from httpx import HTTPStatusError, RequestError
from bs4 import BeautifulSoup
from tqdm import tqdm

from utils.setup_logger import logger
from utils.parsing import extract_specialties

class DoctorScraper:
    def __init__(self, base_url: str, city: str):
        self.base_url = base_url
        self.city = city
        self.client = httpx.Client()
        logger.info(f"Scraper inicializado para {city}.")

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

    def get_districts(self, url: str) -> list:
        """Obtém a lista de bairros disponíveis a partir do JSON embutido no HTML."""

        pattern = r"AVAILABLE_FILTERS:\s*(\[.*?\])\s*,\s*ACTIVE_FILTERS"

        try:
            response = self.client.get(url, timeout=10)
            response.raise_for_status()
            match = re.search(pattern, response.text, re.DOTALL)    
            if not match:
                logger.warning("JSON de configuração não encontrado no HTML.")
                return []

            available_filters = json.loads(match.group(1))
            districts_filter = next(
                (f for f in available_filters if f["name"] == "districts"), None
            )
            if not districts_filter:
                logger.warning("Filtro de bairros (districts) não encontrado.")
                return []

            districts = districts_filter.get("items", [])
            logger.info(f"{len(districts)} bairros encontrados.")
            return districts
        except Exception as e:
            logger.error(f"Erro ao obter lista de bairros: {e}")
            return []

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
                    reviews_tag = item.select_one("span.opinion-numeral")
                    span_tags = [span.text.strip() for span in item.select("div.dp-doctor-card + span")]
                    specialties_tag = item.select_one("span[data-test-id='doctor-specializations']")

                    link_to_profile = link_tag["href"] if link_tag else None
                    professional = name_tag.text.strip() if name_tag else None
                    reviews = (
                        int(reviews_tag.text.strip().split()[0]) if reviews_tag else 0
                    )
                    specialties = extract_specialties(specialties_tag.text.strip() if specialties_tag else "")
                    register_id = ' '.join(span_tags)

                    # Busca detalhes do perfil
                    profile_details = self.get_profile_details(link_to_profile, reviews)
                    logger.info(f"Dados do {profile_details['Name']} Extraído com sucesso ({i+1}/{len(all_doctors)})")
                    doctors.append({
                        "professional": professional,
                        "specialties": specialties,
                        "register_id": register_id,
                        "reviews": reviews,
                        "link_to_profile": link_to_profile,
                        "city": self.city,
                        "data": profile_details,
                    })

                except Exception as e:
                    logger.error(f"Erro ao processar dados de um médico: {e}")
            logger.info(f"{len(doctors)} médicos encontrados na página.")
            return doctors
        except Exception as e:
            logger.error(f"Erro ao raspar página: {e}")
            return []
    
    def get_profile_details(self, profile_url: str, reviews_count: int) -> dict:
        """Obtém informações adicionais do perfil do profissional."""
        try:
            response = self.client.get(profile_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            origin_url = profile_url
            name = soup.select_one("div.unified-doctor-header-info__name span[itemprop='name']")
            about = soup.select_one("div.about-description")
            experience_tags = soup.select(".modal-body div.mb-3 ~ div.mb-2")
            insurance_cover = soup.select_one("div[data-id='check-your-insurance-vue'] p.text-muted")
            age_public_range = soup.select_one("div[data-test-id='doctor-address-allowed-patients']")

            # Experiência formatada
            experience = []
            social_links = []
            for tag in experience_tags:
                link_tag = tag.select('a[target="_blank"]')
                if link_tag:
                    experience.append(''.join([tag.text.split()[0], ' ', tag.text.split()[1]]))
                    for link in link_tag:
                        experience.append(f"{link.text.strip()} ({link['href']})")
                        social_links.append({
                            "Social Network": link.text.strip(),
                            "URL": link['href']
                        })
                else:
                    experience.append(tag.text.strip())

            # Serviços médicos
            services = []
            for service in soup.select("div[data-id='services-list-container'] > div"):
                service_name = service.select_one("p[itemprop='availableService']")
                price_tag = service.select_one("div.mr-1")
                price = int(re.search(r"\d+", price_tag.text).group()) if price_tag and re.search(r"\d+", price_tag.text) else None
                services.append({
                    "Service Name": service_name.text.strip() if service_name else None,
                    "Price": price,
                })

            reviews = []
            for review in soup.select("div.opinion.d-block"):
                reviewer_name = review.select_one("span[itemprop='name']")
                review_date = review.select_one("time")
                review_comment = review.select_one("p[itemprop='reviewBody']")
                reviews.append({
                    "Reviewer Name": reviewer_name.text.strip() if reviewer_name else None,
                    "Review Date": review_date.text.strip() if review_date else None,
                    "Review Comment": review_comment.text.strip() if review_comment else None,
                })
            
            if len(reviews) < reviews_count:
                logger.info(f"A procesar {reviews_count} Reviews")
                doctor_id = soup.select_one("div[data-doctor-id]")["data-doctor-id"]
                reviews = self.get_all_reviews(reviews, doctor_id, reviews_count)

            # Obter perguntas e respostas
            link_questions = (
                soup.select_one('a[data-patient-app-event-name="dp-load-more-questions"]')['href']
                if soup.select_one('a[data-patient-app-event-name="dp-load-more-questions"]')
                else None
            )
            health_questions_and_answers = self.get_all_questions(link_questions) if link_questions else []
            return {
                "Origin URL": origin_url,
                "Name": name.text.strip() if name else None,
                "About": about.text.strip() if about else None,
                "Experience": " ".join(experience),
                "Social Links": social_links,
                "Insurance Cover": insurance_cover.text.strip() if insurance_cover else None,
                "AgePublic Range": age_public_range.text.strip() if age_public_range else None,
                "Medical Services": services,
                "Patient Reviews": reviews,
                "Health Questions and Answers": health_questions_and_answers
            }
        except Exception as e:
            logger.error(f"Erro ao obter detalhes do perfil: {e}")
            return {}
        
    def get_all_reviews(self, reviews: list, doctor_id: str, reviews_count: int) -> list:
        """Obtém todas as reviews do profissional a partir do endpoint."""

        try:
            base_url = f"https://www.doctoralia.com.br/ajax/mobile/doctor-opinions/{doctor_id}"
            page = 2

            with tqdm(total=reviews_count, desc=f"Processando Reviews", unit=' Reviews') as pbar:
                pbar.update(len(reviews))
                while True:
                    response = self.client.get(f"{base_url}/{page}", timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    if "html" not in data or "numRows" not in data or "limit" not in data:
                        logger.warning("Resposta inesperada do endpoint de reviews.")
                        break

                    soup = BeautifulSoup(data["html"], "html.parser")
                    review_blocks = soup.select('div[class="opinion d-block"]')

                    for review in review_blocks:
                        reviewer_name = review.select_one("span[itemprop='name']")
                        review_date = review.select_one("time")
                        review_comment = review.select_one("p[itemprop='reviewBody']")
                        reviews.append({
                            "Reviewer Name": reviewer_name.text.strip() if reviewer_name else None,
                            "Review Date": review_date.text.strip() if review_date else None,
                            "Review Comment": review_comment.text.strip() if review_comment else None,
                        })

                    pbar.update(data['limit'])

                    # Verificar se já coletamos todas as reviews
                    if len(reviews) >= reviews_count:
                        break

                    # Incrementa para próxima página
                    page += 1

            logger.info(f"Todas as {len(reviews)} reviews coletadas.")
            return reviews
        except Exception as e:
            logger.error(f"Erro ao obter todas as reviews: {e}")
            return []

    def get_all_questions(self, url: str) -> list:
        """Obtém todas as perguntas e respostas dos médicos."""

        try:
            response = self.client.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            questions_and_answers = []
            question_blocks = soup.select('div[data-id="question-box"]')

            for question_block in question_blocks:
                question = question_block.select_one("p.doctor-question-body").text.strip()
                category = question_block.select_one("div.text-muted a")
                answer_date = question_block.select_one("time").text.strip()
                
                # Pega o texto completo, se tiver, senão pega pelo link
                p_tag = soup.find('p', class_="mb-0", itemprop="text")
                if p_tag:
                    a_tag = p_tag.find('a')
                    if a_tag and 'href' in a_tag.attrs:
                        link_answer = a_tag['href']
                        answer = self.get_full_answer(link_answer)
                    else:
                        answer = p_tag.text.strip()
                else:
                    answer = None

                # Adiciona a resposta ao dicionário de perguntas e respostas
                questions_and_answers.append({
                    "Question Title": question,
                    "Question Category": category.text.strip() if category else None,
                    "Full Question": question,
                    "Answer Date": answer_date,
                    "Answer Text": answer
                })
            
            return questions_and_answers
        
        except Exception as e:
            logger.error(f"Erro ao obter todas as perguntas e respostas: {e}")
            return []

    def get_full_answer(self, link: str) -> str:
        """Obtém a resposta completa do profissional a partir da URL."""

        try:
            response = self.client.get(link, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            answer = soup.select_one("div.doctor-answer-content").text.strip()
            return answer
        except Exception as e:
            logger.error(f"Erro ao obter a resposta completa: {e}")
            return ""

    def scrape(self) -> list:
        """Orquestra o processo de raspagem para todas as páginas."""
        
        logger.info(f"Iniciando raspagem para a cidade: {self.city}")
        all_doctors = []
        last_page = self.get_last_page(self.base_url)

        if last_page > 500:
            logger.info(f"Número de páginas ({last_page}) excede o limite de 500. Aplicando filtro por bairros.")
            districts = self.get_districts(self.base_url)
            if not districts:
                logger.error("Não foi possível obter a lista de bairros. Abortando.")
                return []

            # Dividir os bairros em grupos de 10
            qtde_bairros_processar = 0
            district_batches = [districts[i:i + 10] for i in range(0, len(districts), 10)]
            for batch in district_batches:
                qtde_bairros_processar += len(batch)
                district_ids = "&".join([f"filters[districts][]={d['key']}" for d in batch])
                filtered_url = f"{self.base_url}&{district_ids}"
                logger.info(f"Processando {qtde_bairros_processar}/{len(districts)} bairros > {', '.join(d['name'] for d in batch)}")

                # Raspagem para o filtro atual
                filtered_last_page = self.get_last_page(filtered_url)
                for page in range(1, filtered_last_page + 1):
                    logger.info(f"Raspando página {page}/{filtered_last_page} Filtrando por bairros {qtde_bairros_processar}/{len(districts)}...")
                    page_url = filtered_url.replace("page=1", f"page={page}")
                    doctors = self.scrape_page(page_url)
                    all_doctors.extend(doctors)
        else:
            # Processar todas as páginas normalmente
            for page in range(1, last_page + 1):
                logger.info(f"Raspando página {page}/{last_page}...")
                page_url = self.base_url.replace("page=1", f"page={page}")
                doctors = self.scrape_page(page_url)
                all_doctors.extend(doctors)

        logger.info(f"Raspagem concluída para {self.city}. Total de médicos: {len(all_doctors)}")
        return all_doctors