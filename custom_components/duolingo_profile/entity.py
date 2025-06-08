"""Base entity for Duolingo Profile integration."""

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from .const import DOMAIN
from .coordinator import DuolingoCoordinator


class DuolingoEntity(CoordinatorEntity[DuolingoCoordinator]):
    """Base entity for Duolingo Profile sensors and binary sensors."""

    def __init__(
        self, coordinator: DuolingoCoordinator, sensor_type: str, profile_name: str
    ) -> None:
        """Initialize the Duolingo entity."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._profile_name = profile_name
        self._slug_name = slugify(profile_name)
        self._attr_unique_id = f"{coordinator.user_id}_{sensor_type}"
        self._attr_entity_registry_object_id = (
            f"{DOMAIN}_{self._slug_name}_{sensor_type}"
        )
        self._attr_entity_id = f"{DOMAIN}_{self._slug_name}_{sensor_type}"
        self._attr_name = sensor_type.replace("_", " ").title()
        self._attr_device_info: DeviceInfo = {
            "identifiers": {(DOMAIN, coordinator.user_id)},
            "name": profile_name,
            "manufacturer": "Duolingo",
            "model": f"User Profile for {coordinator.user_id}",
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return self._attr_device_info

    @property
    def available(self) -> bool:
        """Return availability based on the coordinator."""
        return self.coordinator.last_update_success
