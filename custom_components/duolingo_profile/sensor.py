from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTime

from .const import DOMAIN
from .coordinator import DuolingoCoordinator
from .entity import DuolingoEntity


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Duolingo Profile sensors for a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        DuolingoSensor(coordinator, entry.data.get("name"), "streak"),
        DuolingoSensor(coordinator, entry.data.get("name"), "total_xp"),
        DuolingoSensor(coordinator, entry.data.get("name"), "crowns"),
    ]

    async_add_entities(sensors)


class DuolingoSensor(DuolingoEntity, SensorEntity):
    """Sensor for Duolingo profile statistics."""

    def __init__(
        self, coordinator: DuolingoCoordinator, profile_name: str, sensor_type: str
    ) -> None:
        """Initialize the Duolingo sensor."""
        super().__init__(coordinator, sensor_type, profile_name)
        self._attr_icon = self._get_icon()
        self._attr_native_unit_of_measurement = self._get_unit()

    def _get_icon(self) -> str:
        return {
            "streak": "mdi:fire",
            "total_xp": "mdi:star-circle",
            "crowns": "mdi:crown",
        }.get(self._sensor_type, "mdi:help-circle")

    def _get_unit(self) -> str | None:
        return {
            "streak": UnitOfTime.DAYS,
            "total_xp": "XP",
            "crowns": None,
        }.get(self._sensor_type)

    @property
    def native_value(self) -> int | None:
        """Return the sensor state."""
        data = self.coordinator.data
        course = data.get("courses", [{}])[0]
        return {
            "streak": data.get("streak"),
            "total_xp": data.get("totalXp"),
            "crowns": course.get("crowns"),
        }.get(self._sensor_type)
