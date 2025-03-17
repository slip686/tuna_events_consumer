from aiochclient import ChClient
from aiohttp import ClientSession
from clickhouse_sqlalchemy import Table
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import MetaData

from config import CH_DSN, CH_HOST, CH_KAFKA_DB_NAME, CH_SHARDED_DB_NAME, KAFKA_HOST, KAFKA_PORT, \
    KAFKA_CH_CONSUMER_COMMON_CONFIG, CH_HTTP_PORT
from utils import get_topics

engine = create_async_engine(CH_DSN, pool_pre_ping=True, )
metadata = MetaData()


async def ch_select_query(tbl_obj: Table, params: dict):
    async with ClientSession() as session:
        fields = ', '.join(params.get('fields', '*'))
        filters = add_object_filters(params, tbl_obj)
        filters_string = ''
        if filters:
            if len(filters) > 1:
                filters_string = 'WHERE ' + filters[0] + ' AND ' + ' AND '.join(filters[1:])
            else:
                filters_string = 'WHERE ' + filters[0]
        query = f"""
        SELECT {fields} FROM {tbl_obj.name} {filters_string} FORMAT JSONEachRow
        """
        client = ChClient(session, url=f"http://{CH_HOST}:{CH_HTTP_PORT}")
        rows = await client.fetch(query)
        return rows


async def bind_topic_to_ch():
    async with ClientSession() as session:
        client = ChClient(session, url=f"http://{CH_HOST}:{CH_HTTP_PORT}")
        for t in get_topics():
            await client.execute(f"CREATE DATABASE IF NOT EXISTS {CH_KAFKA_DB_NAME}")
            await client.execute(f"""
            CREATE TABLE IF NOT EXISTS {CH_KAFKA_DB_NAME}.{t}_queue 
            AS {CH_SHARDED_DB_NAME}.{t}
            ENGINE = Kafka('{KAFKA_HOST}:{KAFKA_PORT}', '{t}', '{t}_ch_consumer','JSONEachRow') 
            SETTINGS {KAFKA_CH_CONSUMER_COMMON_CONFIG};
            """)
            await client.execute(f"""
            CREATE MATERIALIZED VIEW IF NOT EXISTS {CH_KAFKA_DB_NAME}.{t}_mv TO {CH_SHARDED_DB_NAME}.{t} 
            AS SELECT * FROM {CH_KAFKA_DB_NAME}.{t}_queue;
            """)


def get_fields(table):
    fields = table.columns
    res = {}
    for field in fields:
        data = {'alias': {'ru': field.comment}, 'type': str(field.type)}
        res.update({field.description: data})
    return res


def get_fields_for_filters(fields):
    res = {}
    for field in fields:
        if str(field.type) in ['Int64', 'UInt64', 'Int32', 'UInt32', 'Int16', 'UInt16', 'Int8', 'UInt8', 'Int128']:
            field_type = 'num'
        elif str(field.type) == 'Bool':
            field_type = 'bool'
        else:
            field_type = 'str'
        res.update({field.description: field_type})
    return res


def add_object_filters(args, tbl_obj):
    res = []
    if not args:
        return res
    table_fields = get_fields_for_filters(tbl_obj.columns)
    if 'attribute' in args:
        for attr in args['attribute']:
            if attr['field'] in table_fields:
                field = attr['field']
                if attr['op'] == '==':
                    op = '='
                elif attr['op'] in ['<', '<=', '>', '>=', '!=', 'ilike', 'like', 'in', 'not in', 'between']:
                    if attr['value'] is None and attr['op'] == '!=':
                        op = 'IS NOT'
                    else:
                        op = attr['op']
                else:
                    continue
                if (table_fields[attr['field']] == 'num' or table_fields[attr['field']] == 'bool') and op != 'between':
                    value = attr['value']
                elif op == 'between':
                    value = f"""{' AND '.join([f"'{i}'" for i in attr['value']])}"""
                elif op == "IS NOT":
                    value = 'NULL'
                elif table_fields[attr['field']] == 'str':
                    if type(attr['value']) == list:
                        value = '(' + ",".join([f"'{i}'" for i in attr['value']]) + ')'
                    else:
                        if op == 'ilike' or op == 'like':
                            op = 'ilike'
                            value = f"'%{attr['value']}%'"
                        else:
                            value = f"'{attr['value']}'"
                else:
                    value = attr['value']
                res.append(f"{f'{tbl_obj.name}.'}{field} {op} {value}")
    return res
