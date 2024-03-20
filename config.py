import logging

CACHE_DAY = 30

LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILENAME = 'your_log_file.log'

logging.basicConfig(filename=LOG_FILENAME, level=LOG_LEVEL, format=LOG_FORMAT)
