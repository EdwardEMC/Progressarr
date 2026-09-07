from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_models import AppConfig
from app.services.password_service import verify_password


class LocalAuthService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def authenticate(
        self,
        password: str,
    ) -> bool:
        result = await self.session.execute(select(AppConfig).limit(1))

        config = result.scalar_one_or_none()

        if config is None:
            return False

        if config.admin_password_hash is None:
            return False

        return verify_password(
            password,
            config.admin_password_hash,
        )
