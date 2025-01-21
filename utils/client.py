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