from sqlalchemy import Table

from db import metadata, engine
from utils import get_topics

TABLES = {}


async def get_ch_tables():
    for topic in get_topics():
        try:
            async with engine.begin() as conn:
                tbl = await conn.run_sync(lambda conn: Table(topic, metadata, autoload_with=conn))
                TABLES[topic] = tbl
        except Exception:
            pass
