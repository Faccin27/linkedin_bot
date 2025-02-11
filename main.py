import os
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Alterado para DEBUG para mais detalhes
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    logger.debug("Iniciando projeto LinkedIn Automation")

if __name__ == "__main__":
    main()
