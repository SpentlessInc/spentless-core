"""This module provides functionality for redis interactions."""

import os
import json
import pickle

import aioredis

from core.decorators import aioshield, aiowait


class PoolManager:
    """Class that provides redis executions via pool manager."""

    def __init__(self):
        """Initialize connections pool manager from env configs."""
        self.pool = None

        host = os.environ["REDIS_HOST"]
        port = os.environ["REDIS_PORT"]
        self.address = (host, port)

        self.password = os.environ.get("REDIS_PASSWORD")
        self.timeout = os.environ.get("REDIS_TIMEOUT")
        self.connection_min_size = os.environ.get("REDIS_CONNECTION_MIN_SIZE", 1)
        self.connection_max_size = os.environ.get("REDIS_CONNECTION_MAX_SIZE", 5)

    @classmethod
    async def create(cls):
        """Create and initialize pool manager for redis connections."""
        instance = cls()
        instance.pool = await aioredis.create_pool(
            address=instance.address,
            password=instance.password,
            minsize=instance.connection_min_size,
            maxsize=instance.connection_max_size,
            create_connection_timeout=instance.timeout
        )

        return instance

    @aiowait(timeout=10)
    async def close(self):
        """Close gracefully all connections in the pool with a timeout."""
        self.pool.close()
        await self.pool.wait_closed()

    async def get(self, key, deserialize=False, default=None):
        """
        Get the value of a key and deserialize it if required.
        Return default value if key does not exist.
        """
        with await self.pool as con:
            value = await con.execute("get", key)
            if value is not None and deserialize:
                return pickle.loads(value)

            return value if value is not None else default

    @aioshield
    async def set(self, key, value, expire=None):
        """Set key to hold the string value with expire time if provided."""
        with await self.pool as con:
            if not expire:
                return await con.execute("set", key, value)

            return await con.execute("set", key, value, "ex", expire)

    async def dump(self, key, value, expire=None):
        """Set key to hold the serialized value with expire time if provided."""
        return await self.set(key, pickle.dumps(value), expire)

    @aioshield
    async def remove(self, *keys):
        """Removes the specified keys. A key is ignored if it does not exist."""
        with await self.pool as con:
            return await con.execute("del", *keys)

    @aioshield
    async def publish(self, channel, message):
        """Publish message to provided channel."""
        message = json.dumps(message)
        with await self.pool as con:
            return await con.execute("publish", channel, message)
