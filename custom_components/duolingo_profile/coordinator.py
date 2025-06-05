"""Duolingo Coordinator for periodic profile data updates."""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import DuolingoError, async_get_profile
from .models import ProfileData

_LOGGER = logging.getLogger(__name__)


class DuolingoCoordinator(DataUpdateCoordinator[ProfileData]):
    """Coordinator to fetch Duolingo profile data periodically."""

    def __init__(
        self,
        hass: HomeAssistant,
        user_id: str,
        profile_name: str | None,
        update_interval: int,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"Duolingo Data for {profile_name or user_id}",
            update_method=self._async_update_data,
            update_interval=timedelta(seconds=update_interval),
        )
        self.user_id = user_id
        self.profile_name = profile_name

    async def _async_update_data(self) -> ProfileData:
        """Fetch data from the Duolingo API."""
        session = async_get_clientsession(self.hass)
        try:
            return await async_get_profile(session, self.user_id)
        except DuolingoError as err:
            raise UpdateFailed(f"Error fetching Duolingo data: {err}") from err
