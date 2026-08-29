from fastapi import FastAPI, HTTPException

from app.clients.radarr import RadarrClient
from app.clients.sonarr import SonarrClient
from app.models import Download
from app.services.download_service import DownloadService


app = FastAPI(
    title="Progressarr",
    version="0.1.0",
)


radarr = RadarrClient()
sonarr = SonarrClient()

download_service = DownloadService(
    radarr=radarr,
    sonarr=sonarr,
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
    }


@app.get("/api/downloads", response_model=list[Download])
async def get_downloads() -> list[Download]:
    try:
        return await download_service.get_downloads()
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve download data: {exc}",
        ) from exc
