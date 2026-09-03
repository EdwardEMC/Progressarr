from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_models import ServiceConfig


class ConfigService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_config(self) -> ServiceConfig:
        result = await self.session.execute(select(ServiceConfig).limit(1))

        config = result.scalar_one_or_none()

        if config is None:
            config = ServiceConfig()
            self.session.add(config)
            await self.session.commit()
            await self.session.refresh(config)

        return config

    async def update_config(
        self,
        *,
        radarr_url: str | None = None,
        radarr_api_key: str | None = None,
        sonarr_url: str | None = None,
        sonarr_api_key: str | None = None,
        seerr_url: str | None = None,
        seerr_api_key: str | None = None,
        jellyfin_url: str | None = None,
        jellyfin_api_key: str | None = None,
    ) -> ServiceConfig:
        config = await self.get_config()

        if radarr_url is not None:
            config.radarr_url = radarr_url

        if radarr_api_key is not None:
            config.radarr_api_key = radarr_api_key

        if sonarr_url is not None:
            config.sonarr_url = sonarr_url

        if sonarr_api_key is not None:
            config.sonarr_api_key = sonarr_api_key

        if seerr_url is not None:
            config.seerr_url = seerr_url

        if seerr_api_key is not None:
            config.seerr_api_key = seerr_api_key

        if jellyfin_url is not None:
            config.jellyfin_url = jellyfin_url

        if jellyfin_api_key is not None:
            config.jellyfin_api_key = jellyfin_api_key

        await self.session.commit()
        await self.session.refresh(config)

        return config
