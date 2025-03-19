import logging
import os

from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('HOST') or '127.0.0.1'
PORT = int(os.getenv('PORT') or 3041)

LOG_FORMAT = '[%(levelname) -3s %(asctime)s] %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# KAFKA_HOST1 = os.getenv('KAFKA_HOST1') or '192.168.1.6'
# KAFKA_PORT1 = int(os.getenv('KAFKA_PORT1') or 9094)
# KAFKA_BOOTSTRAP_SERVERS1 = [f'{KAFKA_HOST1}:{KAFKA_PORT1}']

KAFKA_HOST = os.getenv('KAFKA_HOST') or 'kafka-0'
KAFKA_PORT = int(os.getenv('KAFKA_PORT') or 9092)
KAFKA_BOOTSTRAP_SERVERS = [f'{KAFKA_HOST}:{KAFKA_PORT}']

KAFKA_CH_CONSUMER_COMMON_CONFIG = (
    """
    kafka_thread_per_consumer = 0,
    kafka_num_consumers = 1, 
    date_time_input_format='best_effort'
    """
)

CH_HOST = os.getenv('CH_HOST') or '192.168.1.6'
CH_TCP_PORT = int(os.getenv('CH_PORT') or 9000)
CH_HTTP_PORT = int(os.getenv('CH_HTTP_PORT') or 8123)
CH_USER = os.getenv('CH_USER')
CH_PWD = os.getenv('CH_PWD')
CH_NAME = os.getenv('CH_NAME')
CH_DSN = f'clickhouse+asynch://{CH_USER}:{CH_PWD}@{CH_HOST}:{CH_TCP_PORT}/{CH_NAME}'

CH_SHARDED_DB_NAME = os.getenv('CH_SHARDED') or 'shard'
CH_KAFKA_DB_NAME = os.getenv('CH_KAFKA') or 'kafka'
