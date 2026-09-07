from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy import select

from app.auth.session import get_session_data
from app.config import settings
from app.database import async_session
from app.db_models import User


async def get_current_user(
    progressarr_session: str | None = Cookie(
        default=None,
        alias=settings.session_cookie_name,
    ),
) -> User:
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

    if session_data.get("auth_type") != "jellyfin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session type.",
        )

    user_id = session_data.get("user_id")

    if not isinstance(user_id, int):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session.",
        )

    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))

        user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists.",
        )

    return user


async def require_admin(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required.",
        )

    return user


async def require_local_admin(
    progressarr_session: str | None = Cookie(
        default=None,
        alias=settings.session_cookie_name,
    ),
) -> None:
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

    if session_data.get("auth_type") != "local_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Local administrator access required.",
        )
