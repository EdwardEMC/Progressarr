from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db_models import ServiceConfig


async def bootstrap_config(
    session: AsyncSession,
) -> None:
    result = await session.execute(
        select(ServiceConfig).limit(1)
    )

    config = result.scalar_one_or_none()

    if config is not None:
        return

    config = ServiceConfig(
        radarr_url=settings.radarr_url,
        radarr_api_key=settings.radarr_api_key,
        sonarr_url=settings.sonarr_url,
        sonarr_api_key=settings.sonarr_api_key,
    )

    session.add(config)

    await session.commit()
    