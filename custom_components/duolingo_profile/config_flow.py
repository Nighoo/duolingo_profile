import logging
from typing import Any, cast

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import DuolingoError, UserNotFound, async_get_profile
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER = "user"
STEP_NAME = "name"


class DuolingoConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Duolingo Profile integration."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            user_id = user_input["user_id"]
            session = async_get_clientsession(self.hass)
            try:
                data = await async_get_profile(session, user_id)
            except UserNotFound:
                errors["user_id"] = "user_not_found"
            except DuolingoError:
                errors["base"] = "cannot_connect"
                _LOGGER.error(
                    "Error fetching Duolingo profile %s", user_id, exc_info=True
                )
            else:
                self._user_id = user_id
                self._default_name = data.get("username", f"Duolingo {user_id}")
                return cast(ConfigFlowResult, await self.async_step_name())

        # Show form to input user_id
        return cast(
            ConfigFlowResult,
            self.async_show_form(
                step_id=STEP_USER,
                data_schema=vol.Schema({vol.Required("user_id"): cv.string}),
                errors=errors,
            ),
        )

    async def async_step_name(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            name = user_input["name"]
            # Save both user_id, name, and update_interval
            return cast(
                ConfigFlowResult,
                self.async_create_entry(
                    title=name,
                    data={
                        "user_id": self._user_id,
                        "name": name,
                        "update_interval": user_input["update_interval"],
                    },
                ),
            )

        # Show form to confirm or edit the name, including update_interval
        return cast(
            ConfigFlowResult,
            self.async_show_form(
                step_id=STEP_NAME,
                data_schema=vol.Schema(
                    {
                        vol.Required("name", default=self._default_name): cv.string,
                        vol.Required("update_interval", default=300): vol.All(
                            vol.Coerce(int), vol.Range(min=60, max=86400)
                        ),
                    }
                ),
                errors=errors,
            ),
        )
