import asyncio

from kafka import KafkaConsumer, KafkaAdminClient
from fastapi import Request

from config import logger, KAFKA_BOOTSTRAP_SERVERS, KAFKA_CONSUMER_COMMON_CONFIG


class EventsConsumer:

    def __init__(self, topic, request: Request):
        self.topic = topic
        self.group_id = f'{self.topic}_temp_consumer_{id(self)}'
        self.consumer = self._get_consumer()
        self.request = request

    def _get_consumer(self) -> KafkaConsumer:
        consumer = KafkaConsumer(self.topic, group_id=self.group_id, **KAFKA_CONSUMER_COMMON_CONFIG)
        return consumer

    async def get_events_stream(self):
        asyncio.get_running_loop().create_task(self._background_cleanup())
        logger.info(f'Group {self.group_id} consumer stream started')
        while True:
            messages = await asyncio.to_thread(self.consumer.poll, 0.1, None, True)
            if messages:
                for _, records in messages.items():
                    for record in records:
                        yield record.value
            await asyncio.sleep(1)

    async def _background_cleanup(self):
        while True:
            if await self.request.is_disconnected():
                self.consumer.close()
                self._remove_group()
                logger.info(f'Temp {self.topic} consumer closed. Group {self.group_id} was removed')
                break
            await asyncio.sleep(1)

    def _remove_group(self):
        admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, client_id='admin')
        admin_client.delete_consumer_groups([self.group_id])
        admin_client.close()
