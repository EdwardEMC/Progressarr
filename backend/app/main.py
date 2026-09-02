import httpx

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from sqlalchemy import select

from app.api.auth import router as auth_router
from app.api.settings import router as settings_router
from app.database import async_session, init_database
from app.db_models import ServiceConfig
from app.models import Download
from app.services.artwork_service import ArtworkService
from app.services.client_factory import (
    create_jellyfin_client,
    create_radarr_client,
    create_sonarr_client,
)
from app.services.config_bootstap import bootstrap_config
from app.services.download_service import DownloadService
from app.services.jellyfin_service import JellyfinService

BASE_DIR = Path(__file__).resolve().parent.parent
ARTWORK_CACHE_DIR = BASE_DIR / "data" / "artwork"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()

    async with async_session() as session:
        await bootstrap_config(session)

    yield


app = FastAPI(
    title="Progressarr",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(settings_router)
app.include_router(auth_router)


artwork = ArtworkService(
    cache_dir=ARTWORK_CACHE_DIR,
)


async def get_service_config() -> ServiceConfig:
    async with async_session() as session:
        result = await session.execute(select(ServiceConfig).limit(1))

        config = result.scalar_one_or_none()

        if config is None:
            raise RuntimeError("Progressarr configuration has not been initialized.")

        return config


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
    }


@app.get("/api/jellyfin/system")
async def get_jellyfin_system() -> dict:
    try:
        config = await get_service_config()

        jellyfin = create_jellyfin_client(config)

        service = JellyfinService(
            jellyfin=jellyfin,
        )

        return await service.get_system_info()

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve Jellyfin system info: {exc}",
        ) from exc


@app.get("/api/downloads", response_model=list[Download])
async def get_downloads() -> list[Download]:
    try:
        config = await get_service_config()

        radarr = create_radarr_client(config)
        sonarr = create_sonarr_client(config)

        download_service = DownloadService(
            radarr=radarr,
            sonarr=sonarr,
            artwork=artwork,
        )

        return await download_service.get_downloads()

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve download data: {exc}",
        ) from exc


@app.get("/api/artwork/{source}/{image_type}/{item_id}")
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

    cache_path = ARTWORK_CACHE_DIR / source / str(item_id) / f"{image_type}.jpg"

    if cache_path.exists():
        return FileResponse(
            cache_path,
            media_type="image/jpeg",
            headers={
                "Cache-Control": "public, max-age=86400",
            },
        )

    try:
        config = await get_service_config()

        if source == "radarr":
            client = create_radarr_client(config)
            item = await client.get_movie(item_id)
        else:
            client = create_sonarr_client(config)
            item = await client.get_series(item_id)

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
