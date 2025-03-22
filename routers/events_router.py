import json

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from db.db import ch_select_query, get_fields
from db.models import TABLES
from consumer.consumer import EventsConsumer

router = APIRouter(prefix='/events', tags=['Events'])


@router.get('/playback')
async def get_playback_events(parameters: str = '{}'):
    """Получение событий проигрывателя"""
    return JSONResponse(content=await ch_select_query(TABLES['playback_events'], json.loads(parameters)))


@router.get('/playback/stream')
async def get_playback_events_stream(request: Request):
    """Получение событий проигрывателя из очереди"""
    return StreamingResponse(EventsConsumer('playback_events', request).get_events_stream(),
                             media_type='text/html; charset=utf-8')


@router.get('/playback/fields')
async def get_playback_events_fields():
    """Получение полей событий проигрывателя"""
    return JSONResponse(content=get_fields(TABLES['playback_events']))


@router.get('/playlist')
async def get_playlist_events(parameters: str = '{}'):
    """Получение событий плейлистов"""
    return JSONResponse(content=await ch_select_query(TABLES['playlist_events'], json.loads(parameters)))


@router.get('/playlist/stream')
async def get_playlist_events_stream(request: Request):
    """Получение событий плейлистов из очереди"""
    return StreamingResponse(EventsConsumer('playlist_events', request).get_events_stream(), media_type='text/html')


@router.get('/playlist/fields')
async def get_playlist_events_fields():
    """Получение полей событий плейлистов"""
    return JSONResponse(content=get_fields(TABLES['playlist_events']))


@router.get('/user')
async def get_user_account_events(parameters: str = '{}'):
    """Получение событий аккаунта пользователя"""
    return JSONResponse(content=await ch_select_query(TABLES['user_account_events'], json.loads(parameters)))


@router.get('/user/stream')
async def get_user_account_events_stream(request: Request):
    """Получение событий аккаунта пользователя из очереди"""
    return StreamingResponse(EventsConsumer('user_account_events', request).get_events_stream(), media_type='text/html')


@router.get('/user/fields')
async def get_user_account_events_fields():
    """Получение полей событий аккаунта пользователя"""
    return JSONResponse(content=get_fields(TABLES['user_account_events']))
