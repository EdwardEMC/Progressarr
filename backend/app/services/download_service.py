import asyncio
from datetime import datetime

import httpx

from app.clients.radarr import RadarrClient
from app.clients.sonarr import SonarrClient
from app.models import Download, DownloadStatus, RecentImport, RecentImportFilters, RecentImportResponse
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

    async def get_recent_imports(
        self,
        seerr_user_id: int | None = None,
        is_admin: bool = False,
        page: int = 1,
        page_size: int = 20,
        filters: RecentImportFilters | None = None,
    ) -> RecentImportResponse:
        page = max(page, 1)
        page_size = min(max(page_size, 1), 100)

        if filters is None:
            filters = RecentImportFilters()

        required_count = page * page_size + 1

        history_page = 1
        history_page_size = 100

        filtered_imports: list[RecentImport] = []

        # Only query the services that can actually contain
        # the requested media type.
        radarr_has_more = filters.media_type != "episode"
        sonarr_has_more = filters.media_type != "movie"

        can_stop_early = (
            filters.sort == "imported_at"
            and filters.sort_direction == "desc"
        )

        requested_media = None

        if not is_admin and seerr_user_id is not None:
            requested_media = (
                await self.requests.get_requested_media_lookup(
                    seerr_user_id,
                )
            )

        while radarr_has_more or sonarr_has_more:
            requests = []

            if radarr_has_more:
                requests.append(
                    self.radarr.get_history(
                        page=history_page,
                        page_size=history_page_size,
                    )
                )

            if sonarr_has_more:
                requests.append(
                    self.sonarr.get_history(
                        page=history_page,
                        page_size=history_page_size,
                    )
                )

            results = await asyncio.gather(*requests)

            result_index = 0

            batch_imports: list[RecentImport] = []

            # --------------------------------------------------
            # Radarr
            # --------------------------------------------------

            if radarr_has_more:
                radarr_history = results[result_index]
                result_index += 1

                records = radarr_history.get("records", [])

                total_records = radarr_history.get(
                    "totalRecords"
                )

                if total_records is not None:
                    radarr_has_more = (
                        history_page * history_page_size
                        < total_records
                    )
                else:
                    radarr_has_more = (
                        len(records) >= history_page_size
                    )

                batch_imports.extend(
                    await self._process_radarr_history(
                        radarr_history,
                        filters,
                    )
                )

            # --------------------------------------------------
            # Sonarr
            # --------------------------------------------------

            if sonarr_has_more:
                sonarr_history = results[result_index]
                result_index += 1

                records = sonarr_history.get("records", [])

                total_records = sonarr_history.get(
                    "totalRecords"
                )

                if total_records is not None:
                    sonarr_has_more = (
                        history_page * history_page_size
                        < total_records
                    )
                else:
                    sonarr_has_more = (
                        len(records) >= history_page_size
                    )

                batch_imports.extend(
                    await self._process_sonarr_history(
                        sonarr_history,
                        filters,
                    )
                )

            # --------------------------------------------------
            # Permissions
            # --------------------------------------------------

            if is_admin:
                permitted_imports = batch_imports

            elif requested_media is None:
                permitted_imports = []

            else:
                permitted_imports = []

                for item in batch_imports:
                    if item.service_item_id is None:
                        continue

                    if item.media_type == "movie":
                        request_key = (
                            "movie",
                            item.service_item_id,
                            None,
                        )
                    else:
                        request_key = (
                            "tv",
                            item.service_item_id,
                            item.season,
                        )

                    if request_key in requested_media:
                        permitted_imports.append(item)

            # --------------------------------------------------
            # Filters
            # --------------------------------------------------

            filtered_batch = self._filter_recent_imports(
                permitted_imports,
                filters,
            )

            filtered_imports.extend(filtered_batch)

            history_page += 1

            # For newest-first sorting we can stop as soon as
            # we have enough matching results.
            if (
                can_stop_early
                and len(filtered_imports) >= required_count
            ):
                break

        # ------------------------------------------------------
        # Sorting
        # ------------------------------------------------------

        sort_reverse = filters.sort_direction == "desc"

        sort_keys = {
            "imported_at": lambda item: item.imported_at,
            "title": lambda item: item.title.lower(),
            "size": lambda item: item.size or 0,
            "quality": lambda item: (
                item.quality or ""
            ).lower(),
        }

        filtered_imports.sort(
            key=sort_keys[filters.sort],
            reverse=sort_reverse,
        )

        # ------------------------------------------------------
        # Pagination
        # ------------------------------------------------------

        start = (page - 1) * page_size
        end = start + page_size

        items = filtered_imports[start:end]

        return RecentImportResponse(
            items=items,
            page=page,
            page_size=page_size,
            has_more=end < len(filtered_imports),
        )

    async def _process_radarr_history(
        self,
        history: dict,
        filters: RecentImportFilters,
    ) -> list[RecentImport]:
        tasks = [
            self._process_radarr_history_item(item, filters)
            for item in history.get("records", [])
        ]

        results = await asyncio.gather(*tasks)

        return [
            item
            for item in results
            if item is not None
        ]

    async def _process_radarr_history_item(
        self,
        item: dict,
        filters: RecentImportFilters,
    ) -> RecentImport | None:
        if not self._matches_raw_history_filters(item, filters):
            return None

        movie_id = item.get("movieId")

        if movie_id is None:
            return None

        title = item.get("sourceTitle", "Unknown")
        artwork = None

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

        quality = None
        quality_data = item.get("quality", {})

        if isinstance(quality_data, dict):
            quality = (
                quality_data
                .get("quality", {})
                .get("name")
            )

        size = item.get("data", {}).get("size")

        try:
            size = int(size) if size is not None else None
        except (TypeError, ValueError):
            size = None

        imported_at = item.get("date")

        if not imported_at:
            return None

        return RecentImport(
            id=f"radarr-{item.get('id')}",
            media_type="movie",
            service_item_id=movie_id,
            title=title,
            release=item.get("sourceTitle"),
            artwork=artwork,
            quality=quality,
            size=size,
            imported_at=imported_at,
            source="radarr",
        )


    async def _process_sonarr_history(
        self,
        history: dict,
        filters: RecentImportFilters,
    ) -> list[RecentImport]:
        tasks = [
            self._process_sonarr_history_item(item, filters)
            for item in history.get("records", [])
        ]

        results = await asyncio.gather(*tasks)

        return [
            item
            for item in results
            if item is not None
        ]

    
    async def _process_sonarr_history_item(
        self,
        item: dict,
        filters: RecentImportFilters,
    ) -> RecentImport | None:
        if not self._matches_raw_history_filters(item, filters):
            return None

        series_id = item.get("seriesId")
        episode_id = item.get("episodeId")

        if series_id is None:
            return None

        title = item.get("sourceTitle", "Unknown")
        artwork = None

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

        season = None
        episode = None

        if episode_id is not None:
            try:
                episode_data = await self.sonarr.get_episode(
                    episode_id
                )

                season = episode_data.get("seasonNumber")
                episode = episode_data.get("episodeNumber")

            except httpx.HTTPError:
                pass

        quality = None
        quality_data = item.get("quality", {})

        if isinstance(quality_data, dict):
            quality = (
                quality_data
                .get("quality", {})
                .get("name")
            )

        size = item.get("data", {}).get("size")

        try:
            size = int(size) if size is not None else None
        except (TypeError, ValueError):
            size = None

        imported_at = item.get("date")

        if not imported_at:
            return None

        return RecentImport(
            id=f"sonarr-{item.get('id')}",
            media_type="episode",
            service_item_id=series_id,
            title=title,
            release=item.get("sourceTitle"),
            artwork=artwork,
            season=season,
            episode=episode,
            quality=quality,
            size=size,
            imported_at=imported_at,
            source="sonarr",
        )

    def _filter_recent_imports(
        self,
        imports: list[RecentImport],
        filters: RecentImportFilters,
    ) -> list[RecentImport]:
        filtered = imports

        if filters.search:
            search = filters.search.strip().lower()

            filtered = [
                item
                for item in filtered
                if search in item.title.lower()
                or (
                    item.release is not None
                    and search in item.release.lower()
                )
            ]

        if filters.media_type:
            filtered = [
                item
                for item in filtered
                if item.media_type == filters.media_type
            ]

        if filters.source:
            filtered = [
                item
                for item in filtered
                if item.source == filters.source
            ]

        if filters.quality:
            quality = filters.quality.strip().lower()

            filtered = [
                item
                for item in filtered
                if item.quality is not None
                and item.quality.lower() == quality
            ]

        if filters.season is not None:
            filtered = [
                item
                for item in filtered
                if item.season == filters.season
            ]

        if filters.from_date is not None:
            filtered = [
                item
                for item in filtered
                if self._parse_import_date(
                    item.imported_at
                ) >= filters.from_date
            ]

        if filters.to_date is not None:
            filtered = [
                item
                for item in filtered
                if self._parse_import_date(
                    item.imported_at
                ) <= filters.to_date
            ]

        return filtered

    def _parse_import_date(self, value: str) -> datetime:
        return datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

    def _matches_raw_history_filters(
        self,
        item: dict,
        filters: RecentImportFilters,
    ) -> bool:
        if item.get("eventType") != "downloadFolderImported":
            return False

        # Quality
        if filters.quality:
            quality_data = item.get("quality", {})
            quality = None

            if isinstance(quality_data, dict):
                quality = (
                    quality_data
                    .get("quality", {})
                    .get("name")
                )

            if (
                quality is None
                or filters.quality.lower() not in quality.lower()
            ):
                return False

        # Import date
        imported_at = item.get("date")

        if not imported_at:
            return False

        try:
            imported_at_dt = self._parse_import_date(imported_at)
        except ValueError:
            return False

        if (
            filters.from_date is not None
            and imported_at_dt < filters.from_date
        ):
            return False

        if (
            filters.to_date is not None
            and imported_at_dt > filters.to_date
        ):
            return False

        return True
    
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
