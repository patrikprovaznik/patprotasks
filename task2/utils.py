import logging
import os
from logging import Logger


def get_logger(logs_fold: str, log_path: str, log_name: str, log_level: str) -> Logger:
    set_log_level = {'logging.DEBUG': logging.DEBUG,
                     'logging.INFO': logging.INFO,
                     'logging.WARNING': logging.WARNING,
                     'logging.ERROR': logging.ERROR,
                     }.get(log_level, logging.ERROR)
    logger = logging.getLogger(log_name)
    logger.setLevel(level=set_log_level)

    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s -  %(module)s - %(levelname)s - %(message)s')
    os.makedirs(logs_fold, exist_ok=True)
    fh = logging.FileHandler(f"{log_path}", mode="w")
    fh.setFormatter(formatter)
    fh.setLevel(level=set_log_level)

    logger.addHandler(fh)
    return logger
