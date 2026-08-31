import httpx

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from app.clients.radarr import RadarrClient
from app.clients.sonarr import SonarrClient
from app.models import Download
from app.services.download_service import DownloadService
from app.services.artwork_service import ArtworkService

BASE_DIR = Path(__file__).resolve().parent.parent
ARTWORK_CACHE_DIR = BASE_DIR / "data" / "artwork"

app = FastAPI(
    title="Progressarr",
    version="0.1.0",
)


radarr = RadarrClient()
sonarr = SonarrClient()
artwork = ArtworkService(
    cache_dir=ARTWORK_CACHE_DIR
)

download_service = DownloadService(
    radarr=radarr,
    sonarr=sonarr,
    artwork=artwork,
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


@app.get(
    "/api/artwork/{source}/{image_type}/{item_id}"
)
async def get_artwork(
    source: str,
    image_type: str,
    item_id: int,
):
    if source not in {"radarr", "sonarr"}:
        raise HTTPException(
            status_code=404,
            detail="Unknown artwork source",
        )

    if image_type not in {"poster", "fanart"}:
        raise HTTPException(
            status_code=404,
            detail="Unknown artwork type",
        )

    cache_path = (
        ARTWORK_CACHE_DIR
        / source
        / str(item_id)
        / f"{image_type}.jpg"
    )

    # Cache hit
    if cache_path.exists():
        return FileResponse(
            cache_path,
            media_type="image/jpeg",
            headers={
                "Cache-Control": "public, max-age=86400",
            },
        )

    # Cache miss
    try:
        if source == "radarr":
            item = await radarr.get_movie(item_id)
            client = radarr
        else:
            item = await sonarr.get_series(item_id)
            client = sonarr

        image = next(
            (
                image
                for image in item.get("images", [])
                if image.get("coverType") == image_type
            ),
            None,
        )

        if not image:
            raise HTTPException(
                status_code=404,
                detail="Artwork not found",
            )

        image_url = image.get("url")

        if not image_url:
            raise HTTPException(
                status_code=404,
                detail="Artwork URL not found",
            )

        image_data = await client.get_image(image_url)

        cache_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        cache_path.write_bytes(image_data)

        return FileResponse(
            cache_path,
            media_type="image/jpeg",
            headers={
                "Cache-Control": "public, max-age=86400",
            },
        )

    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve artwork",
        ) from exc