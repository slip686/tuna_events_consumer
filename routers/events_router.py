import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from db.db import ch_select_query, get_fields
from db.models import TABLES

router = APIRouter(prefix='/events', tags=['Events'])


@router.get('/playback')
async def get_playback_events(parameters: str = '{}'):
    """Получение событий проигрывателя"""
    return JSONResponse(content=await ch_select_query(TABLES['playback_events'], json.loads(parameters)))


@router.get('/playback/fields')
async def get_playback_events_fields():
    """Получение полей событий проигрывателя"""
    return JSONResponse(content=get_fields(TABLES['playback_events']))


@router.get('/playlist')
async def get_playlist_events(parameters: str = '{}'):
    """Получение событий плейлистов"""
    return JSONResponse(content=await ch_select_query(TABLES['playlist_events'], json.loads(parameters)))


@router.get('/playlist/fields')
async def get_playlist_events_fields():
    """Получение полей событий плейлистов"""
    return JSONResponse(content=get_fields(TABLES['playlist_events']))


@router.get('/user')
async def get_user_account_events(parameters: str = '{}'):
    """Получение событий аккаунта пользователя"""
    return JSONResponse(content=await ch_select_query(TABLES['playlist_events'], json.loads(parameters)))


@router.get('/user/fields')
async def get_user_account_events_fields():
    """Получение полей событий аккаунта пользователя"""
    return JSONResponse(content=get_fields(TABLES['playlist_events']))
