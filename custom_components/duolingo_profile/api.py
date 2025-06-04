import asyncio

import aiohttp
import async_timeout

from .models import ProfileData

BASE_URL = "https://www.duolingo.com/2017-06-30/users/{user_id}"
DEFAULT_TIMEOUT = 10


class DuolingoError(Exception):
    """Base exception for Duolingo client errors."""


class UserNotFound(DuolingoError):
    """Raised when Duolingo returns 404 for a given user_id."""


async def async_get_profile(
    session: aiohttp.ClientSession,
    user_id: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> ProfileData:
    """Fetch a Duolingo profile by user_id."""
    url = BASE_URL.format(user_id=user_id)
    try:
        async with async_timeout.timeout(timeout):
            resp = await session.get(url)
            resp.raise_for_status()
            return await resp.json()
    except aiohttp.ClientResponseError as err:
        if err.status == 404:
            raise UserNotFound(user_id) from err
        raise DuolingoError(f"HTTP error fetching profile: {err}") from err
    except (aiohttp.ClientError, asyncio.TimeoutError) as err:
        raise DuolingoError(f"Connection error fetching profile: {err}") from err
