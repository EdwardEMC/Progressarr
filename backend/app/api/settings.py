import httpx
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.auth.dependencies import get_current_user
from app.database import async_session
from app.db_models import User
from app.services.config_service import ConfigService

router = APIRouter(
    prefix="/api/settings",
    tags=["settings"],
)


class ServiceSettings(BaseModel):
    url: str | None = None
    configured: bool = False


class SettingsResponse(BaseModel):
    radarr: ServiceSettings
    sonarr: ServiceSettings
    jellyfin: ServiceSettings
    seerr: ServiceSettings


class RadarrSettingsUpdate(BaseModel):
    url: str = Field(min_length=1)
    api_key: str | None = None


class SonarrSettingsUpdate(BaseModel):
    url: str = Field(min_length=1)
    api_key: str | None = None


class SeerrSettingsUpdate(BaseModel):
    url: str = Field(min_length=1)
    api_key: str | None = None


class JellyfinSettingsUpdate(BaseModel):
    url: str = Field(min_length=1)
    api_key: str | None = None


class SettingsUpdate(BaseModel):
    radarr: RadarrSettingsUpdate | None = None
    sonarr: SonarrSettingsUpdate | None = None
    jellyfin: JellyfinSettingsUpdate | None = None
    seerr: SeerrSettingsUpdate | None = None


class ConnectionTestRequest(BaseModel):
    url: str = Field(min_length=1)
    api_key: str = Field(min_length=1)


class ConnectionTestResponse(BaseModel):
    success: bool
    message: str


@router.get("", response_model=SettingsResponse)
async def get_settings(
    user: User = Depends(get_current_user),
) -> SettingsResponse:
    async with async_session() as session:
        service = ConfigService(session)
        config = await service.get_config()

    return SettingsResponse(
        radarr=ServiceSettings(
            url=config.radarr_url,
            configured=bool(config.radarr_url and config.radarr_api_key),
        ),
        sonarr=ServiceSettings(
            url=config.sonarr_url,
            configured=bool(config.sonarr_url and config.sonarr_api_key),
        ),
        seerr=ServiceSettings(
            url=config.seerr_url,
            configured=bool(config.seerr_url and config.seerr_api_key),
        ),
        jellyfin=ServiceSettings(
            url=config.jellyfin_url,
            configured=bool(config.jellyfin_url and config.jellyfin_api_key),
        ),
    )


@router.put("")
async def update_settings(
    payload: SettingsUpdate,
    user: User = Depends(get_current_user),
) -> SettingsResponse:
    async with async_session() as session:
        service = ConfigService(session)

        kwargs = {}

        if payload.radarr is not None:
            kwargs["radarr_url"] = payload.radarr.url

            if payload.radarr.api_key is not None:
                kwargs["radarr_api_key"] = payload.radarr.api_key

        if payload.sonarr is not None:
            kwargs["sonarr_url"] = payload.sonarr.url

            if payload.sonarr.api_key is not None:
                kwargs["sonarr_api_key"] = payload.sonarr.api_key

        if payload.seerr is not None:
            kwargs["seerr_url"] = payload.seerr.url

            if payload.seerr.api_key is not None:
                kwargs["seerr_api_key"] = payload.seerr.api_key

        if payload.jellyfin is not None:
            kwargs["jellyfin_url"] = payload.jellyfin.url

            if payload.jellyfin.api_key is not None:
                kwargs["jellyfin_api_key"] = payload.jellyfin.api_key

        await service.update_config(**kwargs)

        config = await service.get_config()

    return SettingsResponse(
        radarr=ServiceSettings(
            url=config.radarr_url,
            configured=bool(config.radarr_url and config.radarr_api_key),
        ),
        sonarr=ServiceSettings(
            url=config.sonarr_url,
            configured=bool(config.sonarr_url and config.sonarr_api_key),
        ),
        seerr=ServiceSettings(
            url=config.seerr_url,
            configured=bool(config.seerr_url and config.seerr_api_key),
        ),
        jellyfin=ServiceSettings(
            url=config.jellyfin_url,
            configured=bool(config.jellyfin_url and config.jellyfin_api_key),
        ),
    )


@router.post(
    "/radarr/test",
    response_model=ConnectionTestResponse,
)
async def test_radarr(
    payload: ConnectionTestRequest,
    user: User = Depends(get_current_user),
) -> ConnectionTestResponse:
    return await _test_connection(
        url=payload.url,
        api_key=payload.api_key,
        service="Radarr",
    )


@router.post(
    "/sonarr/test",
    response_model=ConnectionTestResponse,
)
async def test_sonarr(
    payload: ConnectionTestRequest,
    user: User = Depends(get_current_user),
) -> ConnectionTestResponse:
    return await _test_connection(
        url=payload.url,
        api_key=payload.api_key,
        service="Sonarr",
    )


async def _test_connection(
    *,
    url: str,
    api_key: str,
    service: str,
) -> ConnectionTestResponse:
    base_url = url.rstrip("/")

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
        ) as client:
            response = await client.get(
                f"{base_url}/api/v3/system/status",
                headers={
                    "X-Api-Key": api_key,
                },
            )

            if response.status_code == 401:
                return ConnectionTestResponse(
                    success=False,
                    message=f"{service} rejected the API key.",
                )

            response.raise_for_status()

            return ConnectionTestResponse(
                success=True,
                message=f"Successfully connected to {service}.",
            )

    except httpx.ConnectError:
        return ConnectionTestResponse(
            success=False,
            message=f"Unable to connect to {service}.",
        )

    except httpx.TimeoutException:
        return ConnectionTestResponse(
            success=False,
            message=f"{service} connection timed out.",
        )

    except httpx.HTTPStatusError as exc:
        return ConnectionTestResponse(
            success=False,
            message=(f"{service} returned HTTP {exc.response.status_code}."),
        )

    except httpx.HTTPError:
        return ConnectionTestResponse(
            success=False,
            message=f"Unable to communicate with {service}.",
        )


@router.post(
    "/seerr/test",
    response_model=ConnectionTestResponse,
)
async def test_seerr(
    payload: ConnectionTestRequest,
    user: User = Depends(get_current_user),
) -> ConnectionTestResponse:
    return await _test_seerr_connection(
        url=payload.url,
        api_key=payload.api_key,
    )


async def _test_seerr_connection(
    *,
    url: str,
    api_key: str,
) -> ConnectionTestResponse:
    base_url = url.rstrip("/")

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
        ) as client:
            response = await client.get(
                f"{base_url}/api/v1/status",
                headers={
                    "X-Api-Key": api_key,
                },
            )

            if response.status_code in {401, 403}:
                return ConnectionTestResponse(
                    success=False,
                    message="Seerr rejected the API key.",
                )

            response.raise_for_status()

            return ConnectionTestResponse(
                success=True,
                message="Successfully connected to Seerr.",
            )

    except httpx.ConnectError:
        return ConnectionTestResponse(
            success=False,
            message="Unable to connect to Seerr.",
        )

    except httpx.TimeoutException:
        return ConnectionTestResponse(
            success=False,
            message="Seerr connection timed out.",
        )

    except httpx.HTTPStatusError as exc:
        return ConnectionTestResponse(
            success=False,
            message=f"Seerr returned HTTP {exc.response.status_code}.",
        )

    except httpx.HTTPError:
        return ConnectionTestResponse(
            success=False,
            message="Unable to communicate with Seerr.",
        )


@router.post(
    "/jellyfin/test",
    response_model=ConnectionTestResponse,
)
async def test_jellyfin(
    payload: ConnectionTestRequest,
    user: User = Depends(get_current_user),
) -> ConnectionTestResponse:
    return await _test_jellyfin_connection(
        url=payload.url,
        api_key=payload.api_key,
    )


async def _test_jellyfin_connection(
    *,
    url: str,
    api_key: str,
) -> ConnectionTestResponse:
    base_url = url.rstrip("/")

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
        ) as client:
            response = await client.get(
                f"{base_url}/System/Info",
                headers={
                    "X-Emby-Token": api_key,
                },
            )

            if response.status_code in {401, 403}:
                return ConnectionTestResponse(
                    success=False,
                    message="Jellyfin rejected the API key.",
                )

            response.raise_for_status()

            return ConnectionTestResponse(
                success=True,
                message="Successfully connected to Jellyfin.",
            )

    except httpx.ConnectError:
        return ConnectionTestResponse(
            success=False,
            message="Unable to connect to Jellyfin.",
        )

    except httpx.TimeoutException:
        return ConnectionTestResponse(
            success=False,
            message="Jellyfin connection timed out.",
        )

    except httpx.HTTPStatusError as exc:
        return ConnectionTestResponse(
            success=False,
            message=(f"Jellyfin returned HTTP {exc.response.status_code}."),
        )

    except httpx.HTTPError:
        return ConnectionTestResponse(
            success=False,
            message="Unable to communicate with Jellyfin.",
        )
