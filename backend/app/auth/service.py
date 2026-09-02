from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.password import (
    hash_password,
    verify_password,
)
from app.db_models import User


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def get_user_by_username(
        self,
        username: str,
    ) -> User | None:
        result = await self.session.execute(
            select(User).where(
                User.username == username
            )
        )

        return result.scalar_one_or_none()

    async def create_user(
        self,
        username: str,
        password: str,
        *,
        is_admin: bool = True,
    ) -> User:
        user = User(
            username=username,
            password_hash=hash_password(password),
            is_admin=is_admin,
        )

        self.session.add(user)

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def authenticate(
        self,
        username: str,
        password: str,
    ) -> User | None:
        user = await self.get_user_by_username(
            username
        )

        if user is None:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        return user

    async def has_users(self) -> bool:
        result = await self.session.execute(
            select(User.id).limit(1)
        )

        return result.scalar_one_or_none() is not None
