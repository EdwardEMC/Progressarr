import asyncio

import httpx

from app.clients.radarr import RadarrClient
from app.clients.sonarr import SonarrClient
from app.models import Download, DownloadStatus
from app.services.artwork_service import ArtworkService
from app.services.request_service import RequestService


class DownloadService:
    def __init__(
        self,
        radarr: RadarrClient,
        sonarr: SonarrClient,
        artwork: ArtworkService,
        requests: RequestService,
    ) -> None:
        self.radarr = radarr
        self.sonarr = sonarr
        self.artwork = artwork
        self.requests = requests

    async def get_downloads(
        self,
        seerr_user_id: int | None = None,
        is_admin: bool = False,
    ) -> list[Download]:
        radarr_queue, sonarr_queue = await asyncio.gather(
            self.radarr.get_queue(),
            self.sonarr.get_queue(),
        )

        downloads = []

        downloads.extend(await self._process_radarr_queue(radarr_queue))

        downloads.extend(await self._process_sonarr_queue(sonarr_queue))

        if is_admin:
            requested_media = await self.requests.get_all_requested_media_lookup()

            for download in downloads:
                key = (
                    "movie" if download.media_type == "movie" else "tv",
                    download.service_item_id,
                    download.season,
                )

                requester = requested_media.get(key)

                if requester is not None:
                    download.requested_by_id = requester.get("id")
                    download.requested_by_username = requester.get("username")

        elif seerr_user_id is not None:
            requested_media = await self.requests.get_requested_media_lookup(
                seerr_user_id
            )

            filtered_downloads = []

            for download in downloads:
                key = (
                    "movie" if download.media_type == "movie" else "tv",
                    download.service_item_id,
                    download.season,
                )

                requester = requested_media.get(key)

                if requester is None:
                    continue

                download.requested_by_id = requester.get("id")
                download.requested_by_username = requester.get("username")

                filtered_downloads.append(download)

            downloads = filtered_downloads

        return downloads

    async def _process_radarr_queue(
        self,
        queue: dict,
    ) -> list[Download]:
        downloads = []

        for item in queue.get("records", []):
            size = item.get("size", 0)
            size_remaining = item.get("sizeleft", 0)

            movie_id = item.get("movieId")

            title = item.get("title", "Unknown")

            artwork = None

            if movie_id:
                try:
                    movie = await self.radarr.get_movie(movie_id)
                    title = movie.get("title", title)

                    artwork = self.artwork.get_artwork(
                        source="radarr",
                        item_id=movie_id,
                        images=movie.get("images", []),
                    )
                except httpx.HTTPError:
                    pass
            else:
                artwork = None

            downloads.append(
                Download(
                    id=f"radarr-{item['id']}",
                    media_type="movie",
                    service_item_id=movie_id,
                    title=title,
                    release=item.get("releaseTitle"),
                    artwork=artwork,
                    status=self._get_status(item),
                    progress=self._calculate_progress(
                        size,
                        size_remaining,
                    ),
                    size=size,
                    size_remaining=size_remaining,
                    time_left=item.get("timeleft"),
                    estimated_completion_time=item.get("estimatedCompletionTime"),
                    download_client=item.get("downloadClient"),
                    protocol=item.get("protocol"),
                    indexer=item.get("indexer"),
                    error_message=item.get("errorMessage"),
                )
            )

        return downloads

    async def _process_sonarr_queue(
        self,
        queue: dict,
    ) -> list[Download]:
        downloads = []

        for item in queue.get("records", []):
            size = item.get("size", 0)
            size_remaining = item.get("sizeleft", 0)

            series_id = item.get("seriesId")
            episode_id = item.get("episodeId")

            title = item.get("title", "Unknown")
            season = item.get("seasonNumber")
            episode = None

            artwork = None

            if series_id:
                try:
                    series = await self.sonarr.get_series(series_id)
                    title = series.get("title", title)

                    artwork = self.artwork.get_artwork(
                        source="sonarr",
                        item_id=series_id,
                        images=series.get("images", []),
                    )
                except httpx.HTTPError:
                    pass
            else:
                artwork = None

            if episode_id:
                try:
                    episode_data = await self.sonarr.get_episode(episode_id)
                    episode = episode_data.get("episodeNumber")
                except httpx.HTTPError:
                    pass

            downloads.append(
                Download(
                    id=f"sonarr-{item['id']}",
                    media_type="episode",
                    service_item_id=series_id,
                    title=title,
                    release=item.get("title"),
                    artwork=artwork,
                    season=season,
                    episode=episode,
                    status=self._get_status(item),
                    progress=self._calculate_progress(
                        size,
                        size_remaining,
                    ),
                    size=size,
                    size_remaining=size_remaining,
                    time_left=item.get("timeleft"),
                    estimated_completion_time=item.get("estimatedCompletionTime"),
                    download_client=item.get("downloadClient"),
                    protocol=item.get("protocol"),
                    indexer=item.get("indexer"),
                    error_message=item.get("errorMessage"),
                )
            )

        return downloads

    @staticmethod
    def _calculate_progress(
        size: int,
        size_remaining: int,
    ) -> float:
        if size <= 0:
            return 0.0

        downloaded = size - size_remaining

        return round(
            max(
                0.0,
                min(
                    100.0,
                    downloaded / size * 100,
                ),
            ),
            2,
        )

    @staticmethod
    def _get_status(item: dict) -> DownloadStatus:
        tracked_state = item.get("trackedDownloadState")
        status = item.get("status")

        if tracked_state == "importPending":
            return DownloadStatus.IMPORT_PENDING

        if tracked_state == "importBlocked":
            return DownloadStatus.FAILED

        if status == "completed":
            return DownloadStatus.COMPLETED

        if status in {"downloading", "queued"}:
            return DownloadStatus.DOWNLOADING

        return DownloadStatus.UNKNOWN
