from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy import select

from app.auth.context import AuthContext
from app.auth.session import get_session_data
from app.config import settings
from app.database import async_session
from app.db_models import User


async def get_current_auth(
    progressarr_session: str | None = Cookie(
        default=None,
        alias=settings.session_cookie_name,
    ),
) -> AuthContext:
    if not progressarr_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    session_data = get_session_data(progressarr_session)

    if session_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session.",
        )

    auth_type = session_data.get("auth_type")

    if auth_type == "local_admin":
        return AuthContext(
            auth_type="local_admin",
        )

    if auth_type == "jellyfin":
        user_id = session_data.get("user_id")

        if not isinstance(user_id, int):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session.",
            )

        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )

            user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User no longer exists.",
            )

        return AuthContext(
            auth_type="jellyfin",
            user=user,
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid session type.",
    )


async def get_current_user(
    auth: AuthContext = Depends(get_current_auth),
) -> User:
    if not auth.is_jellyfin or auth.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Jellyfin user authentication required.",
        )

    return auth.user


async def require_admin(
    auth: AuthContext = Depends(get_current_auth),
) -> AuthContext:
    if not auth.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required.",
        )

    return auth


async def require_local_admin(
    auth: AuthContext = Depends(get_current_auth),
) -> AuthContext:
    if not auth.is_local_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Local administrator access required.",
        )

    return auth