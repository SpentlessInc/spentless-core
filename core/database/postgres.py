"""This module provides functionality for postgres interactions."""

import os
import asyncpg

from core.decorators import aioshield, aiowait


class PoolManager:
    """Class that provides postgres executions via pool manager."""

    def __init__(self):
        """Initialize connections pool manager from env configs."""
        self.pool = None

        self.host = os.environ.get("POSTGRES_HOST")
        self.port = os.environ.get("POSTGRES_PORT")

        self.user = os.environ["POSTGRES_USER"]
        self.password = os.environ["POSTGRES_PASSWORD"]
        self.database = os.environ["POSTGRES_DB"]

        self.connection_min_size = os.environ.get("POSTGRES_CONNECTION_MIN_SIZE", 10)
        self.connection_max_size = os.environ.get("POSTGRES_CONNECTION_MAX_SIZE", 10)

    @classmethod
    async def create(cls):
        """Create and initialize pool manager for postgres connections."""
        instance = cls()
        instance.pool = await asyncpg.create_pool(
            host=instance.host,
            port=instance.port,
            database=instance.database,
            user=instance.user,
            password=instance.password,
            min_size=instance.connection_min_size,
            max_size=instance.connection_max_size
        )

        return instance

    @classmethod
    async def create_connection(cls):
        """Return initialized connection to postgres."""
        instance = cls()
        conn = await asyncpg.connect(
            host=instance.host,
            port=instance.port,
            database=instance.database,
            user=instance.user,
            password=instance.password
        )

        return conn

    @aiowait(timeout=10)
    async def close(self):
        """
        Close gracefully all connections in the pool with a timeout.
        Errors raised will cause immediate pool termination.
        """
        await self.pool.close()

    @aioshield
    async def execute(self, query, *query_args, timeout=5.0):
        """Execute an SQL command (or commands)."""
        async with self.pool.acquire() as con:
            return await con.execute(query, *query_args, timeout=timeout)

    @aioshield
    async def executemany(self, query, *query_args):
        """Execute an SQL command for all provided arguments."""
        async with self.pool.acquire() as con:
            return await con.executemany(query, *query_args)

    async def fetch(self, query, *query_args, timeout=5.0):
        """Run a query and return the results as a list."""
        async with self.pool.acquire() as con:
            return await con.fetch(query, *query_args, timeout=timeout)

    async def fetchone(self, query, *query_args, timeout=5.0):
        """Run a query and return the first row."""
        async with self.pool.acquire() as con:
            return await con.fetchrow(query, *query_args, timeout=timeout)
