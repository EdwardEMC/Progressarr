from fastapi import Cookie, Depends, HTTPException, status

from sqlalchemy import select

from app.auth.session import get_user_id_from_token
from app.database import async_session
from app.db_models import User
from app.config import settings


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

    user_id = get_user_id_from_token(
        progressarr_session
    )

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session.",
        )

    async with async_session() as session:
        result = await session.execute(
            select(User).where(
                User.id == user_id
            )
        )

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