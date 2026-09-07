import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db_models import AppConfig, ServiceConfig


async def bootstrap_config(
    session: AsyncSession,
) -> None:
    result = await session.execute(select(ServiceConfig).limit(1))

    config = result.scalar_one_or_none()

    if config is None:
        config = ServiceConfig(
            radarr_url=settings.radarr_url,
            radarr_api_key=settings.radarr_api_key,
            sonarr_url=settings.sonarr_url,
            sonarr_api_key=settings.sonarr_api_key,
            seerr_url=settings.seerr_url,
            seerr_api_key=settings.seerr_api_key,
            jellyfin_url=settings.jellyfin_url,
            jellyfin_api_key=settings.jellyfin_api_key,
        )

        session.add(config)

        await session.commit()


async def bootstrap_app_config(
    session: AsyncSession,
) -> str:
    result = await session.execute(select(AppConfig).limit(1))

    config = result.scalar_one_or_none()

    if config is not None:
        return config.session_secret

    if settings.session_secret is not None:
        session_secret = settings.session_secret
    else:
        session_secret = secrets.token_urlsafe(32)

    config = AppConfig(
        session_secret=session_secret,
        setup_complete=False,
    )

    session.add(config)

    await session.commit()

    return session_secret
