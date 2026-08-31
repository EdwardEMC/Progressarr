import httpx

from app.config import settings


class RadarrClient:
    def __init__(self) -> None:
        self.base_url = settings.radarr_url.rstrip("/")
        self.headers = {
            "X-Api-Key": settings.radarr_api_key,
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

    async def get_movie(self, movie_id: int) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/api/v3/movie/{movie_id}",
                headers=self.headers,
            )

            response.raise_for_status()

            return response.json()

    async def get_image(self, image_url: str) -> bytes:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(
                f"{self.base_url}{image_url}",
                headers=self.headers,
            )

            response.raise_for_status()

            return response.content

    async def get_image(self, image_url: str) -> bytes:
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
        ) as client:
            if "mediacover" in image_url.lower():
                # Reconstruct just the endpoint part securely
                parts = image_url.lower().split("mediacover")
                image_url = f"/api/v3/mediacover{parts[1]}"

            full_url = f"{self.base_url.rstrip('/')}/{image_url.lstrip('/')}"
            
            headers = {
                "X-Api-Key": settings.radarr_api_key,
                "Accept": "image/*"
            }
            
            response = await client.get(
                full_url,
                headers=headers,
            )

            if "login" in str(response.url):
                raise httpx.HTTPError("Radarr rejected authentication and redirected to login.")

            response.raise_for_status()
            return response.content