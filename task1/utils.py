
import logging


def get_logger(log_path, log_level):
    logger = logging.getLogger(__name__)
    logger.setLevel(level=log_level)

    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt="%Y-%m-%d_%H-%M-%S")
    fh = logging.FileHandler(f"{log_path}", mode="w")
    fh.setFormatter(formatter)
    fh.setLevel(level=logging.INFO)

    logger.addHandler(fh)
    return logger


logger = get_logger("/home/patrik/Documents/patprotasks/task1/logger.log", logging.INFO)

logger.info(f'jeba')
