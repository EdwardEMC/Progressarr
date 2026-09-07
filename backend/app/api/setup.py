from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.auth.session import create_admin_session_token
from app.config import settings
from app.database import async_session
from app.db_models import AppConfig, ServiceConfig
from app.services.connection_test_service import test_jellyfin_connection
from app.services.password_service import hash_password

router = APIRouter(
    prefix="/api/setup",
    tags=["setup"],
)


class SetupRequest(BaseModel):
    jellyfin_url: str = Field(min_length=1)
    jellyfin_api_key: str = Field(min_length=1)
    admin_password: str = Field(min_length=8)


@router.get("/status")
async def get_setup_status() -> dict[str, bool]:
    async with async_session() as session:
        result = await session.execute(select(AppConfig).limit(1))

        config = result.scalar_one_or_none()

    return {
        "setup_required": (config is None or not config.setup_complete),
    }


@router.post("")
async def setup(
    payload: SetupRequest,
    response: Response,
) -> dict[str, str]:
    async with async_session() as session:
        result = await session.execute(select(AppConfig).limit(1))

        app_config = result.scalar_one_or_none()

        if app_config is None:
            raise HTTPException(
                status_code=500,
                detail="Application configuration has not been initialized.",
            )

        if app_config.setup_complete:
            raise HTTPException(
                status_code=403,
                detail="Progressarr setup has already been completed.",
            )

        service_config_result = await session.execute(select(ServiceConfig).limit(1))

        service_config = service_config_result.scalar_one_or_none()

        if service_config is None:
            service_config = ServiceConfig()
            session.add(service_config)

        try:
            result = await test_jellyfin_connection(
                url=payload.jellyfin_url,
                api_key=payload.jellyfin_api_key,
            )
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail="Unable to connect to Jellyfin.",
            ) from exc

        if not result.success:
            raise HTTPException(
                status_code=400,
                detail=result.message,
            )

        service_config.jellyfin_url = payload.jellyfin_url
        service_config.jellyfin_api_key = payload.jellyfin_api_key

        app_config.admin_password_hash = hash_password(
            payload.admin_password,
        )

        app_config.setup_complete = True

        await session.commit()

    token = create_admin_session_token()

    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.session_expiry_hours * 60 * 60,
    )

    return {
        "message": "Progressarr setup completed successfully.",
    }
