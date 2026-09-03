import httpx


class SeerrClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-Api-Key": api_key,
        }

    async def get_user_by_jellyfin_id(
        self,
        jellyfin_user_id: str,
    ) -> dict | None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/api/v1/user/jellyfin/{jellyfin_user_id}",
                headers=self.headers,
            )

            if response.status_code == 404:
                return None

            response.raise_for_status()

            return response.json()

    async def get_requests(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/api/v1/request",
                headers=self.headers,
            )

            response.raise_for_status()

            data = response.json()

            return data.get("results", [])

    async def get_requests_by_user(
        self,
        user_id: int,
    ) -> list[dict]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/api/v1/user/{user_id}/requests",
                headers=self.headers,
            )

            response.raise_for_status()

            data = response.json()

            return data.get("results", [])