import asyncio
import json
import time

import redis
from config import settings

from fastapi import WebSocket

from .constants import (
    POOL_MAX_CONNECTIONS,
    SUBSCRIBER_CONNECTION_TIMEOUT,
    SUBSCRIBER_RETRY_DELAY,
)


class RedisSubscriber:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=getattr(settings, "REDIS_DB", 0),
            password=getattr(settings, "REDIS_PASSWORD", None),
            max_connections=POOL_MAX_CONNECTIONS,
        )
        self.redis = redis.StrictRedis.from_pool(self.pool)

    async def listen(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel := settings.REDIS_CHANNEL)

        while True:
            try:
                message = pubsub.get_message(
                    ignore_subscribe_messages=True,
                    timeout=SUBSCRIBER_CONNECTION_TIMEOUT,
                )
                if message:
                    data = json.loads(message["data"])
                    await self.websocket.send_text(
                        f"{data['sender']}: {data['message']}"
                    )
            except redis.ConnectionError:
                print("Redis connection lost. Retrying...")
                while True:
                    try:
                        self.redis = redis.StrictRedis(connection_pool=self.pool)
                        pubsub = self.redis.pubsub()
                        pubsub.subscribe(channel)
                        print("Reconnected to Redis.")
                        break
                    except redis.ConnectionError:
                        time.sleep(SUBSCRIBER_RETRY_DELAY)

            except asyncio.CancelledError:
                break

            await asyncio.sleep(SUBSCRIBER_CONNECTION_TIMEOUT)
