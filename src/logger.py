import logging
import os

class FlushFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()

def get_logger(name: str, log_file: str) -> logging.Logger:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_PATH  = os.path.join(BASE_DIR, f'../logs/{log_file}')
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = FlushFileHandler(LOG_PATH, encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s :: %(message)s'
        ))
        logger.addHandler(handler)

    return logger