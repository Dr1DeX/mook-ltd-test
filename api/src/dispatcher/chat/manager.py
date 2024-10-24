import logging
from asyncio import Lock
from typing import List

from fastapi import WebSocket

from starlette.websockets import WebSocketState


class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.lock = Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            logging.info(f'Connect websocket: {websocket}')
            self.active_connections.append(websocket)
            logging.info(f'Active connections: {len(self.active_connections)}')

    async def disconnect(self, websocket: WebSocket):
        async with self.lock:
            logging.info(f'Disconnect websocket: {websocket}')
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
                logging.info(
                    f'Active connections after disconnect: {len(self.active_connections)}',
                )

    async def broadcast(self, message: dict):
        async with self.lock:
            for connection in self.active_connections:
                if connection.application_state == WebSocketState.CONNECTED:
                    try:
                        logging.info(
                            f'Broadcasting message to websocket client: {message}',
                        )
                        await connection.send_json(message)
                    except Exception as e:
                        logging.error(f"Error broadcasting message: {e}")
                        await self.disconnect(connection)
