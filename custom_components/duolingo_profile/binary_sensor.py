"""Platform for Duolingo Profile binary sensors."""

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .coordinator import DuolingoCoordinator
from .entity import DuolingoEntity


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Duolingo Profile binary sensors for a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    profile_name = entry.data.get("name")
    async_add_entities([DuolingoLessonBinarySensor(coordinator, profile_name)])


class DuolingoLessonBinarySensor(DuolingoEntity, BinarySensorEntity):
    """Binary sensor to indicate if a Duolingo lesson was completed today."""

    def __init__(self, coordinator: DuolingoCoordinator, profile_name: str) -> None:
        """Initialize the Duolingo lesson binary sensor."""
        super().__init__(coordinator, "lesson_done_today", profile_name)
        self._attr_icon = "mdi:calendar-check"

    @property
    def is_on(self) -> bool:
        """Return True if a lesson was completed today."""
        data = self.coordinator.data
        if data is None:
            return False
        today = dt_util.now().date().isoformat()
        return (
            data.get("streakData", {}).get("currentStreak", {}).get("endDate") == today
        )
