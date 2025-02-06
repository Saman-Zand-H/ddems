import asyncio
from typing import List

from fastapi import WebSocket
from src.infrastructure.pubsub import RedisPublisher, RedisSubscriber


class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.redis_publisher = RedisPublisher()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

        redis_subscriber = RedisSubscriber(websocket)
        asyncio.create_task(redis_subscriber.listen())

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await websocket.close()

    async def send_message(self, message: str, sender: str):
        self.redis_publisher.publish_message(message, sender)

    async def broadcast_message(self, message: str, sender: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(f"{sender}: {message}")
            except Exception:
                pass
