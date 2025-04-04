import asyncio
from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI

from config import HOST, PORT
from db import get_ch_tables
from db.db import bind_topic_to_ch
from utils import connect_routers
import routers

sentry_sdk.init(
    dsn="https://442d577c31a358efd9a706063c10eb82@o4509033998909440.ingest.de.sentry.io/4509034251944016",
    send_default_pii=True,
)


@asynccontextmanager
async def at_startup(app: FastAPI):
    tasks = [get_ch_tables(), bind_topic_to_ch()]
    await asyncio.gather(*tasks)
    yield

app = FastAPI(root_path='/events_database', docs_url='/docs', title='Чтение событий',
              description='Сервис для чтения событий из БД',
              swagger_ui_parameters={"docExpansion": "none", "defaultModelsExpandDepth": -1}, lifespan=at_startup)

connect_routers(app, routers)

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=False, workers=3)
