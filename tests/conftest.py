"""Pytest configuration and stubs for Home Assistant modules."""

import sys
import types

# Stub async_timeout for API client
async_timeout_mod = types.ModuleType("async_timeout")


class TimeoutError(Exception):
    pass


async_timeout_mod.TimeoutError = TimeoutError


def timeout(sec):
    class DummyContext:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

    return DummyContext()


async_timeout_mod.timeout = timeout
sys.modules["async_timeout"] = async_timeout_mod
# Stub aiohttp_retry for API client
sys.modules["aiohttp_retry"] = types.ModuleType("aiohttp_retry")
setattr(sys.modules["aiohttp_retry"], "RetryClient", object)
setattr(sys.modules["aiohttp_retry"], "ExponentialRetry", object)

# Stub homeassistant core
ha = types.ModuleType("homeassistant")
sys.modules["homeassistant"] = ha

ha_core = types.ModuleType("homeassistant.core")
ha_core.HomeAssistant = object
sys.modules["homeassistant.core"] = ha_core

# Stub update coordinator
ha_helpers = types.ModuleType("homeassistant.helpers")
sys.modules["homeassistant.helpers"] = ha_helpers

ha_uc = types.ModuleType("homeassistant.helpers.update_coordinator")


class DataUpdateCoordinator:
    def __init__(self, hass, logger, name, update_method, update_interval):
        self.hass = hass

    @classmethod
    def __class_getitem__(cls, item):
        return cls


ha_uc.DataUpdateCoordinator = DataUpdateCoordinator
ha_uc.UpdateFailed = Exception
sys.modules["homeassistant.helpers.update_coordinator"] = ha_uc

# Stub aiohttp_client helper
ha_aiohttp = types.ModuleType("homeassistant.helpers.aiohttp_client")


def async_get_clientsession(*args, **kwargs):
    return None


ha_aiohttp.async_get_clientsession = async_get_clientsession
sys.modules["homeassistant.helpers.aiohttp_client"] = ha_aiohttp

# Stub config entries base classes
ha_ce = types.ModuleType("homeassistant.config_entries")


# ConfigFlow and ConfigEntry
class ConfigFlow:
    pass


class ConfigEntry:
    pass


ha_ce.ConfigFlow = ConfigFlow
ha_ce.ConfigEntry = ConfigEntry
sys.modules["homeassistant.config_entries"] = ha_ce

# Stub update_coordinator TYPE imports
# Stub data entry flow result type
ha_def = types.ModuleType("homeassistant.data_entry_flow")
ha_def.FlowResult = object
sys.modules["homeassistant.data_entry_flow"] = ha_def
# Stub config_validation module
ha_cv = types.ModuleType("homeassistant.helpers.config_validation")
ha_cv.string = str
ha_cv.empty_config_schema = lambda: None
ha_cv.platform_only_config_schema = lambda: None
ha_cv.config_entry_only_config_schema = lambda domain=None: None
sys.modules["homeassistant.helpers.config_validation"] = ha_cv
# Stub typing helpers
ha_typing = types.ModuleType("homeassistant.helpers.typing")
ha_typing.ConfigType = dict
sys.modules["homeassistant.helpers.typing"] = ha_typing
# Stub core constants and Platform
ha_const = types.ModuleType("homeassistant.const")
ha_const.Platform = types.SimpleNamespace(
    SENSOR="sensor", BINARY_SENSOR="binary_sensor"
)
sys.modules["homeassistant.const"] = ha_const
