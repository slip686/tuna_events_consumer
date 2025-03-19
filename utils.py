import importlib

from fastapi import FastAPI
from kafka import KafkaAdminClient

from config import KAFKA_BOOTSTRAP_SERVERS


def connect_routers(app: FastAPI, routers: __import__):
    for mod in routers.__loader__.get_resource_reader().contents():
        name = mod.split('.py')[0]
        if name not in ['__init__', '__pycache__']:
            cls = getattr(importlib.import_module(f'routers.{name}'), 'router')
            app.include_router(cls)


def get_topics():
    admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, client_id='admin')
    existing_topics = [_ for _ in admin_client.list_topics() if not _.startswith('__')]
    return existing_topics
