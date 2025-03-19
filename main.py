import asyncio

import uvicorn
from fastapi import FastAPI

from config import HOST, PORT
from db import get_ch_tables
from db.db import bind_topic_to_ch
from utils import connect_routers
import routers

app = FastAPI(root_path='/events_database', docs_url='/docs', title='Чтение событий',
              description='Сервис для чтения событий из БД',
              swagger_ui_parameters={"docExpansion": "none", "defaultModelsExpandDepth": -1})

connect_routers(app, routers)


def start_uvicorn(loop):
    config = uvicorn.Config(app, host=HOST, port=PORT, workers=3, loop=loop)
    server = uvicorn.Server(config)
    loop.run_until_complete(server.serve())


def load_tables(loop):
    loop.create_task(get_ch_tables())


def bind_topics(loop):
    loop.create_task(bind_topic_to_ch())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bind_topics(loop)
    load_tables(loop)
    start_uvicorn(loop)
