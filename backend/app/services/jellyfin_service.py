from app.clients.jellyfin import JellyfinClient


class JellyfinService:
    def __init__(
        self,
        jellyfin: JellyfinClient,
    ) -> None:
        self.jellyfin = jellyfin

    async def get_system_info(self) -> dict:
        return await self.jellyfin.get_system_info()
