from datetime import datetime
from enum import Enum
from typing import Literal
from pydantic import BaseModel


class DownloadStatus(str, Enum):
    DOWNLOADING = "downloading"
    IMPORT_PENDING = "import_pending"
    FAILED = "failed"
    COMPLETED = "completed"
    UNKNOWN = "unknown"


class Artwork(BaseModel):
    poster_url: str | None = None
    backdrop_url: str | None = None


class Download(BaseModel):
    id: str
    media_type: str

    # Radarr movie ID or Sonarr series ID
    service_item_id: int | None = None

    requested_by_id: int | None = None
    requested_by_username: str | None = None

    title: str
    release: str | None = None

    artwork: Artwork | None = None

    season: int | None = None
    episode: int | None = None

    status: DownloadStatus
    progress: float

    size: int
    size_remaining: int

    time_left: str | None = None
    estimated_completion_time: str | None = None

    download_client: str | None = None
    protocol: str | None = None
    indexer: str | None = None

    error_message: str | None = None


class RecentImport(BaseModel):
    id: str

    media_type: str
    service_item_id: int | None = None

    title: str

    release: str | None = None

    artwork: Artwork | None = None

    season: int | None = None
    episode: int | None = None

    quality: str | None = None

    size: int | None = None

    imported_at: str

    source: str


class RecentImportResponse(BaseModel):
    items: list[RecentImport]
    page: int
    page_size: int
    has_more: bool


class RecentImportFilters(BaseModel):
    search: str | None = None
    media_type: Literal["movie", "episode"] | None = None
    source: Literal["radarr", "sonarr"] | None = None
    quality: str | None = None
    season: int | None = None
    from_date: datetime | None = None
    to_date: datetime | None = None
    sort: Literal["imported_at", "title", "size", "quality"] = "imported_at"
    sort_direction: Literal["asc", "desc"] = "desc"