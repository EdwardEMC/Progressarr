from enum import Enum

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

