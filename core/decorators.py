"""This module provides helper decorators."""

import asyncio


def aioshield(func):
    """Protect an awaitable object from being cancelled."""
    async def wrapper(*args, **kwargs):
        return await asyncio.shield(func(*args, **kwargs))
    return wrapper


def aiowait(timeout):
    """Wait for the awaitable to complete with a timeout."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            return asyncio.wait_for(func(*args, **kwargs), timeout)
        return wrapper
    return decorator
