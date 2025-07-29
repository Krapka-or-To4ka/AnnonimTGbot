import logging
from app.config.config import LEVEL_LOGGING
debug_level = logging.DEBUG
format_log = logging.Formatter("[%(levelname)s] %(name)s: %(message)s - %(asctime)s")
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app/logging/logs.log",encoding='utf-8')
console_handler.setFormatter(format_log)
file_handler.setFormatter(format_log)


def setup_logger(logger:logging.Logger):
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.setLevel(LEVEL_LOGGING)