from app.clients.seerr import SeerrClient


class SeerrService:
    def __init__(
        self,
        seerr: SeerrClient,
    ) -> None:
        self.seerr = seerr

    async def get_user_by_jellyfin_id(
        self,
        jellyfin_user_id: str,
    ) -> dict | None:
        return await self.seerr.get_user_by_jellyfin_id(jellyfin_user_id)

    async def get_requests(self) -> list[dict]:
        return await self.seerr.get_requests()

    async def get_requests_by_user(
        self,
        user_id: int,
    ) -> list[dict]:
        return await self.seerr.get_requests_by_user(user_id)
