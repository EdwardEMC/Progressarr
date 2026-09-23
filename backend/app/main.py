import httpx
import os

from collections.abc import AsyncIterator
from datetime import datetime
from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select
from typing import Literal

from app.api.auth import router as auth_router
from app.api.requests import router as requests_router
from app.api.settings import router as settings_router
from app.api.setup import router as setup_router
from app.auth.context import AuthContext
from app.auth.dependencies import get_current_auth
from app.auth.session import initialize_session_serializer
from app.database import async_session, init_database
from app.db_models import ServiceConfig
from app.models import Download, RecentImportFilters, RecentImportResponse
from app.services.artwork_service import ArtworkService
from app.services.client_factory import (
    create_jellyfin_client,
    create_radarr_client,
    create_seerr_client,
    create_sonarr_client,
)
from app.services.config_bootstrap import bootstrap_app_config, bootstrap_config
from app.services.download_service import DownloadService
from app.services.jellyfin_service import JellyfinService
from app.services.request_service import RequestService
from app.services.seerr_service import SeerrService

BASE_DIR = Path(__file__).resolve().parent.parent
ARTWORK_CACHE_DIR = BASE_DIR / "data" / "artwork"
FRONTEND_DIST_DIR = BASE_DIR / "frontend" / "dist"


async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await init_database()

    async with async_session() as session:
        await bootstrap_config(session)

        session_secret = await bootstrap_app_config(session)

    initialize_session_serializer(session_secret)

    yield


APP_VERSION = os.getenv(
    "APP_VERSION",
    "0.1.0",
)

app = FastAPI(
    title="Progressarr",
    version=APP_VERSION,
    lifespan=lifespan,
)

app.include_router(requests_router)
app.include_router(auth_router)
app.include_router(settings_router)
app.include_router(setup_router)


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
async def get_downloads(
    auth: AuthContext = Depends(get_current_auth)
) -> list[Download]:
    try:
        config = await get_service_config()

        radarr = create_radarr_client(config)
        sonarr = create_sonarr_client(config)

        seerr_client = create_seerr_client(config)
        seerr = SeerrService(seerr=seerr_client)

        request_service = RequestService(
            seerr=seerr,
        )

        download_service = DownloadService(
            radarr=radarr,
            sonarr=sonarr,
            artwork=artwork,
            requests=request_service,
        )

        return await download_service.get_downloads(
            seerr_user_id=auth.user.seerr_user_id if auth.user else None, 
            is_admin=auth.is_admin,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve download data: {exc}",
        ) from exc


@app.get(
    "/api/downloads/recent",
    response_model=RecentImportResponse,
)
async def get_recent_downloads(
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    media_type: Literal["movie", "episode"] | None = None,
    source: Literal["radarr", "sonarr"] | None = None,
    quality: str | None = None,
    season: int | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    sort: Literal[
        "imported_at",
        "title",
        "size",
        "quality",
    ] = "imported_at",
    sort_direction: Literal["asc", "desc"] = "desc",
    auth: AuthContext = Depends(get_current_auth),
) -> RecentImportResponse:
    try:
        filters = RecentImportFilters(
            search=search,
            media_type=media_type,
            source=source,
            quality=quality,
            season=season,
            from_date=from_date,
            to_date=to_date,
            sort=sort,
            sort_direction=sort_direction,
        )
                
        config = await get_service_config()

        radarr = create_radarr_client(config)
        sonarr = create_sonarr_client(config)
        seerr_client = create_seerr_client(config)

        seerr = SeerrService(seerr=seerr_client)
        request_service = RequestService(seerr=seerr)

        download_service = DownloadService(
            radarr=radarr,
            sonarr=sonarr,
            artwork=artwork,
            requests=request_service,
        )

        return await download_service.get_recent_imports(
            seerr_user_id=auth.user.seerr_user_id
            if auth.user
            else None,
            is_admin=auth.is_admin,
            page=page,
            page_size=page_size,
            filters=filters
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve recent downloads: {exc}",
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


@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    file_path = FRONTEND_DIST_DIR / full_path

    if file_path.is_file():
        return FileResponse(file_path)

    return FileResponse(FRONTEND_DIST_DIR / "index.html")
