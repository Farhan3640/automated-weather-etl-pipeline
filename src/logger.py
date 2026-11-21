
import logging
from pathlib import Path
from datetime import datetime


def get_logger():

    log_directory = Path("logs")
    log_directory.mkdir(exist_ok=True)

    log_file = log_directory / (
        f"etl_{datetime.now().strftime('%Y%m%d')}.log"
    )

    logger = logging.getLogger("weather_etl")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(
            log_file, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


logger = get_logger()
