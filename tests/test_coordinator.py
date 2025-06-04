"""Tests for the Duolingo Profile DataUpdateCoordinator."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from types import SimpleNamespace

import pytest

from custom_components.duolingo_profile.api import DuolingoError
from custom_components.duolingo_profile.coordinator import (
    DuolingoCoordinator,
    UpdateFailed,
)


class DummyHass:
    """Minimal HomeAssistant stub for coordinator."""

    def __init__(self):
        import asyncio

        self.loop = asyncio.get_event_loop()
        self.helpers = SimpleNamespace(
            aiohttp_client=SimpleNamespace(
                async_get_clientsession=lambda *args, **kwargs: None
            )
        )


@pytest.mark.asyncio
async def test_update_data_success(monkeypatch):
    dummy_data = {
        "username": "user",
        "streak": 1,
        "totalXp": 10,
        "courses": [],
        "streakData": {},
    }

    async def mock_get_profile(session, user_id):
        return dummy_data

    monkeypatch.setattr(
        "custom_components.duolingo_profile.coordinator.async_get_profile",
        mock_get_profile,
    )

    hass = DummyHass()
    coordinator = DuolingoCoordinator(hass, "user_id", "Profile", 300)
    result = await coordinator._async_update_data()
    assert result == dummy_data


@pytest.mark.asyncio
async def test_update_data_failure(monkeypatch):
    async def mock_get_profile(session, user_id):
        raise DuolingoError("failure")

    monkeypatch.setattr(
        "custom_components.duolingo_profile.coordinator.async_get_profile",
        mock_get_profile,
    )

    hass = DummyHass()
    coordinator = DuolingoCoordinator(hass, "user_id", "Profile", 300)
    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()
