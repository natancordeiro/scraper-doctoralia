import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str = "app.log", level: int = logging.INFO) -> logging.Logger:
    """Configura e retorna um logger com nível de log e arquivo de saída."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Configura o formato do log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Configura o manipulador de arquivo com rotação
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setFormatter(formatter)

    # Adiciona o manipulador ao logger
    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger
