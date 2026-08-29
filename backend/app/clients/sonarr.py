import httpx

from app.config import settings


class SonarrClient:
    def __init__(self) -> None:
        self.base_url = settings.sonarr_url.rstrip("/")
        self.headers = {
            "X-Api-Key": settings.sonarr_api_key,
        }

    async def get_queue(self) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/api/v3/queue",
                headers=self.headers,
                params={
                    "page": 1,
                    "pageSize": 100,
                },
            )

            response.raise_for_status()

            return response.json()

    async def get_series(self, series_id: int) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/api/v3/series/{series_id}",
                headers=self.headers,
            )

            response.raise_for_status()

            return response.json()

    async def get_episode(self, episode_id: int) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/api/v3/episode/{episode_id}",
                headers=self.headers,
            )

            response.raise_for_status()

            return response.json()
            