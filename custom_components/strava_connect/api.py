"""API helper for Strava Connect."""

from __future__ import annotations

from http import HTTPStatus

from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_entry_oauth2_flow

API_BASE = "https://www.strava.com/api/v3"


class StravaApi:
    """Thin wrapper around the Strava REST API."""

    def __init__(self, session: config_entry_oauth2_flow.OAuth2Session) -> None:
        self._session = session

    async def get_athlete(self) -> dict:
        """Return the authenticated athlete profile."""
        response = await self._session.async_request("GET", f"{API_BASE}/athlete")
        if response.status != HTTPStatus.OK:
            raise HomeAssistantError(
                f"Failed to fetch Strava athlete profile: {response.status} "
                f"{await response.text()}"
            )
        return await response.json()

    async def get_gear(self, gear_id: str) -> dict:
        """Return detailed information about a specific gear item."""
        response = await self._session.async_request(
            "GET", f"{API_BASE}/gear/{gear_id}"
        )
        if response.status != HTTPStatus.OK:
            raise HomeAssistantError(
                f"Failed to fetch Strava gear {gear_id}: {response.status} "
                f"{await response.text()}"
            )
        return await response.json()

    async def set_activity_gear(self, activity_id: int | str, gear_id: str):
        """Assign gear to the provided activity."""
        return await self._session.async_request(
            "PUT",
            f"{API_BASE}/activities/{activity_id}",
            json={"gear_id": gear_id},
        )
