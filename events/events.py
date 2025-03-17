from kafka import KafkaConsumer

from config import KAFKA_BOOTSTRAP_SERVERS

consumer = KafkaConsumer(
    'playback_events',
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    group_id='echo-messages-to-stdout',
)

for message in consumer:
    print(message.value)
