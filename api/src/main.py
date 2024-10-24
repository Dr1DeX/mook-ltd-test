import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import socketio

from src.dependency import (
    get_chat_repository,
    get_chat_service,
)
from src.dispatcher.chat.schema import MessageCreateSchema
from src.dispatcher.users.auth.handlers import router as auth_router
from src.dispatcher.users.handlers import router as user_router
from src.infrastructure.database.accessor import AsyncSessionFactory


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

app = FastAPI(title='API LTD Stargazer')


app.include_router(user_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@sio.event
async def connect(sid, environ):
    logging.info(f'Client connected: {sid}')


@sio.event
async def disconnect(sid):
    logging.info(f'Client disconnected: {sid}')


@sio.event
async def message(sid, data):
    chat_repository = await get_chat_repository(
        db_session=AsyncSessionFactory(),
    )
    chat_service = await get_chat_service(
        chat_repository=chat_repository,
    )
    logging.info(f'Received message: {data} from {sid}')
    message_schema = MessageCreateSchema(
        text=data['text'],
        sender_id=data['sender_id'],
    )
    await chat_service.save_message(body=message_schema)
    await sio.emit('message', data)


@sio.on('request_history')
async def handle_history_request(sid):
    chat_repository = await get_chat_repository(
        db_session=AsyncSessionFactory(),
    )
    chat_service = await get_chat_service(
        chat_repository=chat_repository,
    )
    histories = await chat_service.get_all_message()
    history_json = [history.model_dump() for history in histories]
    await sio.emit('chat_history', history_json, room=sid)


app = socketio.ASGIApp(sio, app)
