import logging
import os


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/trading_bot.log"),
            logging.StreamHandler(),
        ],
    )


def get_logger(name):
    return logging.getLogger(name)