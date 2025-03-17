import logging
import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST') or '127.0.0.1'
PORT = int(os.getenv('PORT') or 3040)

LOG_FORMAT = '[%(levelname) -3s %(asctime)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

KAFKA_HOST = os.getenv('KAFKA_HOST') or '192.168.1.6'
KAFKA_PORT = int(os.getenv('KAFKA_PORT') or 9094)
KAFKA_BOOTSTRAP_SERVERS = [f'{KAFKA_HOST}:{KAFKA_PORT}']

KAFKA_CONSUMER_COMMON_CONFIG = {'bootstrap_servers': KAFKA_BOOTSTRAP_SERVERS,
                                'retries': 5,
                                'batch_size': 100,
                                'linger_ms': 50}

CH_HOST = os.getenv('CH_HOST') or '192.168.1.6'
CH_PORT = int(os.getenv('CH_PORT') or 8123)
