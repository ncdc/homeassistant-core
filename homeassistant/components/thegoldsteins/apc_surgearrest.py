"""APC SurgeArrest."""

import logging

from homeassistant.exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)


class Client:
    """APC SurgeArrest API."""

    def __init__(self) -> None:
        """Initialize."""
        self._app_id = "schneider-5w-id"
        self._app_secret = "schneider-4p5If6sO_QS9F0mQLJmOoCxswng"
        self._access_token = None
        self._refresh_token = None

    async def login(self, web_session, username: str, password: str) -> bool:
        """Test if we can authenticate with the host."""
        url = "https://user-field.aylanetworks.com/users/sign_in.json"
        data = {
            "user": {
                "email": username,
                "application": {"app_id": self._app_id, "app_secret": self._app_secret},
                "password": password,
            }
        }
        response = await web_session.post(url, json=data, timeout=5.0)
        body = await response.json()

        # {"access_token":"","refresh_token":"","expires_in":86400,"role":"EndUser","role_tags":[]}%

        if response.status != 200:
            _LOGGER.error("Login failed with error: %s", body["error"])
            raise InvalidAuth

        self._access_token = body["access_token"]

        return True

    async def list_devices(self, web_session) -> None:
        """List devices."""


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
