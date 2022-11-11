import logging
import os


def get_logger(log_path, log_name, log_level):
    log_level_info = {'logging.DEBUG': logging.DEBUG,
                      'logging.INFO': logging.INFO,
                      'logging.WARNING': logging.WARNING,
                      'logging.ERROR': logging.ERROR,
                      }
    set_log_level = log_level_info.get(log_level, logging.ERROR)
    logger = logging.getLogger(log_name)
    logger.setLevel(level=set_log_level)

    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logs_folder = 'logs/'
    os.makedirs(logs_folder, exist_ok=True)
    fh = logging.FileHandler(f"{log_path}", mode="w")
    fh.setFormatter(formatter)
    fh.setLevel(level=set_log_level)

    logger.addHandler(fh)
    return logger
