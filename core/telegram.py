"""This module provides functionality for async functionality with telegram."""

import os

from .http import HTTPRequest


class TelegramBot(HTTPRequest):
    """Class that provides async interactions with telegram bot."""

    def __init__(self, timeout=60):
        """Initialize client session for async telegram bot interactions."""
        super().__init__(timeout)
        token = os.environ["TELEGRAM_BOT_TOKEN"]

        self.token = token
        self.api = f"https://api.telegram.org/bot{token}"

    async def send_message(self, chat_id, text, **kwargs):
        """
        Send message to user by chat_id. Can be provided extra options
        such as: silent notifications, change parse mode, etc.
        """
        endpoint = f"{self.api}/sendMessage"
        params = {"chat_id": chat_id, "text": text, **kwargs}

        return await self.get(endpoint, params=params)
