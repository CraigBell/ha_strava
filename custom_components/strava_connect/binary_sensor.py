"""Binary sensors for Strava Connect gear flags."""

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_GEAR_BIKES,
    CONF_GEAR_SHOES,
    CONF_STRAVA_CONFIG_UPDATE_EVENT,
    DATA_COORDINATOR,
    DOMAIN,
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Strava gear binary sensors."""
    runtime_data = hass.data.get(DOMAIN, {}).get(config_entry.entry_id, {})
    coordinator = runtime_data.get(DATA_COORDINATOR)
    entries = []

    if coordinator and coordinator.data:
        for gear in coordinator.data.get(CONF_GEAR_SHOES, []):
            entries.extend(
                [
                    StravaGearFlagBinarySensor(
                        config_entry=config_entry,
                        coordinator=coordinator,
                        gear=gear,
                        gear_type="shoe",
                        flag="retired",
                    ),
                    StravaGearFlagBinarySensor(
                        config_entry=config_entry,
                        coordinator=coordinator,
                        gear=gear,
                        gear_type="shoe",
                        flag="primary",
                    ),
                ]
            )
        for gear in coordinator.data.get(CONF_GEAR_BIKES, []):
            entries.append(
                StravaGearFlagBinarySensor(
                    config_entry=config_entry,
                    coordinator=coordinator,
                    gear=gear,
                    gear_type="bike",
                    flag="retired",
                )
            )

    if entries:
        async_add_entities(entries)


class StravaGearFlagBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor exposing a boolean flag about Strava gear."""

    _attr_has_entity_name = True

    def __init__(self, config_entry, coordinator, gear: dict, gear_type: str, flag: str) -> None:
        super().__init__(coordinator)
        self._config_entry_id = config_entry.entry_id
        self._gear_type = gear_type
        self._flag = flag
        gear_id = gear.get("id") or f"{gear_type}_{gear.get('name', 'gear')}"
        self._gear_id = str(gear_id)
        self._initial_name = gear.get("name", "Strava Gear")
        self._attr_unique_id = f"gear_{self._gear_id}_{self._flag}"
        self._attr_name = flag.replace("_", " ").title()

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            self.hass.bus.async_listen(
                CONF_STRAVA_CONFIG_UPDATE_EVENT, self._handle_config_update
            )
        )

    async def _handle_config_update(self, event):  # pylint: disable=unused-argument
        self.async_write_ha_state()

    def _gear_collection_key(self) -> str:
        return CONF_GEAR_SHOES if self._gear_type == "shoe" else CONF_GEAR_BIKES

    def _current_gear(self):
        data = self.coordinator.data or {}
        for gear in data.get(self._gear_collection_key(), []):
            if str(gear.get("id")) == self._gear_id:
                return gear
        return None

    @property
    def available(self) -> bool:
        return self._current_gear() is not None

    @property
    def is_on(self):
        gear = self._current_gear()
        if not gear:
            return None
        return bool(gear.get(self._flag))

    @property
    def device_info(self):
        gear = self._current_gear() or {}
        model_name = gear.get("model_name") or gear.get("name", self._initial_name)
        if gear.get("brand_name") and gear.get("model_name"):
            model = f"{gear['brand_name']} {gear['model_name']}"
        else:
            model = model_name
        return DeviceInfo(
            identifiers={(DOMAIN, self._gear_id)},
            name=gear.get("name", self._initial_name),
            manufacturer="Strava",
            model=model,
        )

    @property
    def extra_state_attributes(self):
        gear = self._current_gear()
        if not gear:
            return {"gear_id": self._gear_id, "gear_type": self._gear_type}
        return {
            "gear_id": self._gear_id,
            "gear_type": self._gear_type,
        }
