import os
import logging
from dataclasses import dataclass

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@dataclass
class LinkedInConfig:
    email: str
    password: str
    search_term: str
    max_connections_per_page: int = 9
    timeout: int = 10
    max_pages: int = 100

def main():
    config = LinkedInConfig(
        email=os.getenv("LINKEDIN_EMAIL"),
        password=os.getenv("LINKEDIN_PASSWORD"),
        search_term="full stack"
    )
    logger.info(f"Configuração carregada: {config}")

if __name__ == "__main__":
    main()
