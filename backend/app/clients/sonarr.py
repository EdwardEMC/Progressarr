import httpx


class SonarrClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-Api-Key": api_key,
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

    async def get_series(
        self,
        series_id: int,
    ) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/api/v3/series/{series_id}",
                headers=self.headers,
            )

            response.raise_for_status()

            return response.json()

    async def get_episode(
        self,
        episode_id: int,
    ) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/api/v3/episode/{episode_id}",
                headers=self.headers,
            )

            response.raise_for_status()

            return response.json()

    async def get_image(
        self,
        image_url: str,
    ) -> bytes:
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
        ) as client:
            if "mediacover" in image_url.lower():
                parts = image_url.lower().split("mediacover")
                image_url = f"/api/v3/mediacover{parts[1]}"

            full_url = f"{self.base_url.rstrip('/')}/{image_url.lstrip('/')}"

            response = await client.get(
                full_url,
                headers={
                    **self.headers,
                    "Accept": "image/*",
                },
            )

            if "login" in str(response.url):
                raise httpx.HTTPError(
                    "Sonarr rejected authentication and redirected to login."
                )

            response.raise_for_status()

            return response.content
