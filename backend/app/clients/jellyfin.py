import httpx


class JellyfinClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "X-Emby-Token": api_key,
        }

    async def get_system_info(self) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/System/Info",
                headers=self.headers,
            )

            response.raise_for_status()

            return response.json()

    async def authenticate_user(
        self,
        username: str,
        password: str,
    ) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{self.base_url}/Users/AuthenticateByName",
                headers={
                    "X-Emby-Authorization": (
                        'MediaBrowser Client="Progressarr", '
                        'Device="Progressarr", '
                        'DeviceId="progressarr", '
                        'Version="0.1.0"'
                    ),
                    "Content-Type": "application/json",
                },
                json={
                    "Username": username,
                    "Pw": password,
                },
            )

            response.raise_for_status()

            return response.json()
