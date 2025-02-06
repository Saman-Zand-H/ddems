from typing import Any

import redis
from config import settings

from .constants import POOL_MAX_CONNECTIONS


class RedisPublisher:
    def __init__(self):
        self.pool = redis.ConnectionPool(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=getattr(settings, "REDIS_DB", 0),
            password=getattr(settings, "REDIS_PASSWORD", None),
            max_connections=POOL_MAX_CONNECTIONS,
        )
        self.redis = redis.StrictRedis.from_pool(self.pool)

    def publish_message(self, message: Any):
        self.redis.publish(settings.REDIS_CHANNEL, message)
