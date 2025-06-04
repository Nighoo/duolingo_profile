"""Tests for the Duolingo Profile API client."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import aiohttp
import pytest

from custom_components.duolingo_profile.api import (
    DEFAULT_TIMEOUT,
    DuolingoError,
    UserNotFound,
    async_get_profile,
)


class DummyResponse:
    """Dummy response for testing HTTP client behavior."""

    def __init__(self, status: int, data: dict):
        self.status = status
        self._data = data

    def raise_for_status(self) -> None:
        if self.status != 200:
            from aiohttp import ClientResponseError

            raise ClientResponseError(None, None, status=self.status)

    async def json(self) -> dict:
        return self._data


@pytest.mark.asyncio
async def test_async_get_profile_success(monkeypatch):
    dummy_data = {
        "username": "user",
        "streak": 5,
        "totalXp": 100,
        "courses": [],
        "streakData": {},
    }

    # Simulate successful HTTP response from session.get
    async def dummy_get(self, url: str):
        return DummyResponse(200, dummy_data)

    monkeypatch.setattr(aiohttp.ClientSession, "get", dummy_get)

    session = aiohttp.ClientSession()
    result = await async_get_profile(session, "user_id", timeout=DEFAULT_TIMEOUT)
    assert result == dummy_data
    await session.close()


@pytest.mark.asyncio
async def test_async_get_profile_not_found(monkeypatch):
    # Simulate 404 returned by API
    async def dummy_get(self, url: str):
        return DummyResponse(404, {})

    monkeypatch.setattr(aiohttp.ClientSession, "get", dummy_get)

    session = aiohttp.ClientSession()
    with pytest.raises(UserNotFound):
        await async_get_profile(session, "missing", timeout=DEFAULT_TIMEOUT)
    await session.close()


@pytest.mark.asyncio
async def test_async_get_profile_error(monkeypatch):
    # Simulate connection error by raising DuolingoError
    async def dummy_get(self, url: str):
        raise DuolingoError("fail")

    monkeypatch.setattr(aiohttp.ClientSession, "get", dummy_get)

    session = aiohttp.ClientSession()
    with pytest.raises(DuolingoError):
        await async_get_profile(session, "user_id", timeout=DEFAULT_TIMEOUT)
    await session.close()
