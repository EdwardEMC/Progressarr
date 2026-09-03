from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_models import User
from app.services.jellyfin_service import JellyfinService
from app.services.seerr_service import SeerrService


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        jellyfin: JellyfinService | None = None,
        seerr: SeerrService | None = None,
    ) -> None:
        self.session = session
        self.jellyfin = jellyfin
        self.seerr = seerr
        

    async def get_user_by_jellyfin_id(
        self,
        jellyfin_user_id: str,
    ) -> User | None:
        result = await self.session.execute(
            select(User).where(
                User.jellyfin_user_id == jellyfin_user_id
            )
        )

        return result.scalar_one_or_none()


    async def get_user_by_seerr_id(
        self,
        seerr_user_id: int,
    ) -> User | None:
        result = await self.session.execute(
            select(User).where(
                User.seerr_user_id == seerr_user_id
            )
        )
        return result.scalar_one_or_none()


    async def authenticate(
        self,
        username: str,
        password: str,
    ) -> User | None:
        if self.jellyfin is None:
            raise RuntimeError(
                "Jellyfin authentication is not configured."
            )

        try:
            result = await self.jellyfin.authenticate_user(
                username=username,
                password=password,
            )
        except Exception:
            return None

        jellyfin_user = result.get("User")

        if not jellyfin_user:
            return None

        jellyfin_user_id = jellyfin_user.get("Id")

        if not jellyfin_user_id:
            return None

        seerr_user_id = None

        if self.seerr is not None:
            try:
                seerr_user = await self.seerr.get_user_by_jellyfin_id(
                    jellyfin_user_id
                )

                if seerr_user is not None:
                    seerr_user_id = seerr_user.get("id")

            except Exception:
                # Seerr being unavailable or unconfigured should not prevent Jellyfin login.
                pass

        user = await self.get_user_by_jellyfin_id(
            jellyfin_user_id
        )

        is_admin = bool(
            jellyfin_user.get("Policy", {}).get(
                "IsAdministrator",
                False,
            )
        )

        if user is None:
            user = User(
                username=username,
                jellyfin_user_id=jellyfin_user_id,
                seerr_user_id=seerr_user_id,
                is_admin=is_admin,
            )

            self.session.add(user)

        else:
            user.jellyfin_user_id = jellyfin_user_id
            user.seerr_user_id = seerr_user_id
            user.is_admin = is_admin

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def has_users(self) -> bool:
        result = await self.session.execute(
            select(User.id).limit(1)
        )

        return result.scalar_one_or_none() is not None
