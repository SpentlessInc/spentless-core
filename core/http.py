"""This module provides functionality for async http interactions."""

from urllib.parse import urlencode

import aiohttp

from core.decorators import aiowait


class HTTPRequest:
    """Class that provides http basic async requests."""

    def __init__(self, timeout=60):
        """Initialize client session for async http requests."""
        timeout = aiohttp.ClientTimeout(total=timeout)
        self._session = aiohttp.ClientSession(timeout=timeout)

    @aiowait(timeout=10)
    async def close(self):
        """Release gracefully all acquired resources."""
        await self._session.close()

    async def get(self, url, headers=None, params=""):
        """Return response from async get http request in json format."""
        url = f"{url}?{urlencode(params)}"
        async with self._session.get(url, headers=headers) as response:
            return await response.json(), response.status

    async def post(self, url, headers=None, body=None):
        """Return response from async post http request in json format."""
        async with self._session.post(url, headers=headers, json=body) as response:
            return await response.json(), response.status

    async def delete(self, url, headers=None):
        """Return response from async delete http request in json format."""
        async with self._session.delete(url, headers=headers) as response:
            return await response.json(), response.status

    async def put(self, url, headers=None, body=None):
        """Return response from async put http request in json format."""
        async with self._session.delete(url, headers=headers, json=body) as response:
            return await response.json(), response.status
