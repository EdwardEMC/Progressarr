from app.services.seerr_service import SeerrService


class RequestService:
    def __init__(
        self,
        seerr: SeerrService,
    ) -> None:
        self.seerr = seerr

    async def get_user_requests(
        self,
        seerr_user_id: int,
    ) -> list[dict]:
        return await self.seerr.get_requests_by_user(
            seerr_user_id
        )

    async def get_requested_media(
        self,
        seerr_user_id: int,
    ) -> list[dict]:
        requests = await self.get_user_requests(
            seerr_user_id
        )

        media = []

        for request in requests:
            request_media = request.get("media")

            if not request_media:
                continue

            media_type = request_media.get("mediaType")
            external_service_id = request_media.get(
                "externalServiceId"
            )

            if media_type not in {"movie", "tv"}:
                continue

            if external_service_id is None:
                continue

            media.append(
                {
                    "request_id": request.get("id"),
                    "media_type": media_type,
                    "service_item_id": external_service_id,
                    "requested_by": request.get("requestedBy"),
                    "seasons": request_media.get(
                        "seasons",
                        [],
                    ),
                }
            )

        return media

    async def get_requester_for_media(
        self,
        seerr_user_id: int,
        media_type: str,
        service_item_id: int,
        season: int | None = None,
    ) -> dict | None:
        media = await self.get_requested_media(
            seerr_user_id
        )

        for request in media:
            if request["media_type"] != media_type:
                continue

            if request["service_item_id"] != service_item_id:
                continue

            # Movies don't have seasons.
            if media_type == "movie":
                return request

            # TV requests need to match the requested season.
            requested_seasons = request.get("seasons", [])

            for requested_season in requested_seasons:
                if requested_season.get("seasonNumber") == season:
                    return request

        return None

    async def get_requested_media_lookup(
        self,
        seerr_user_id: int,
    ) -> dict[tuple[str, int, int | None], dict]:
        media = await self.get_requested_media(
            seerr_user_id
        )

        return self._build_requested_media_lookup(
            media
        )

    async def get_all_requested_media_lookup(
        self,
    ) -> dict[tuple[str, int, int | None], dict]:
        requests = await self.seerr.get_requests()

        media = []

        for request in requests:
            request_media = request.get("media")

            if not request_media:
                continue

            media_type = request_media.get("mediaType")
            service_item_id = request_media.get(
                "externalServiceId"
            )

            if media_type not in {"movie", "tv"}:
                continue

            if service_item_id is None:
                continue

            media.append(
                {
                    "media_type": media_type,
                    "service_item_id": service_item_id,
                    "requested_by": request.get(
                        "requestedBy"
                    ),
                    "seasons": request.get(
                        "seasons",
                        [],
                    ),
                }
            )

        return self._build_requested_media_lookup(
            media
        )

    def _build_requested_media_lookup(
        self,
        media: list[dict],
    ) -> dict[tuple[str, int, int | None], dict]:
        lookup = {}

        for item in media:
            media_type = item["media_type"]
            service_item_id = item["service_item_id"]

            requester = item.get("requested_by") or {}

            requester_data = {
                "id": requester.get("id"),
                "username": requester.get("displayName"),
            }

            if media_type == "movie":
                lookup[
                    (
                        media_type,
                        service_item_id,
                        None,
                    )
                ] = requester_data

                continue

            for season in item.get("seasons", []):
                season_number = season.get("seasonNumber")

                lookup[
                    (
                        media_type,
                        service_item_id,
                        season_number,
                    )
                ] = requester_data

        return lookup