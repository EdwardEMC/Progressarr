from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.auth.dependencies import get_current_user
from app.auth.service import AuthService
from app.auth.session import create_session_token
from app.config import settings
from app.database import async_session
from app.db_models import User, ServiceConfig
from app.services.client_factory import create_jellyfin_client, create_seerr_client
from app.services.jellyfin_service import JellyfinService
from app.services.seerr_service import SeerrService


router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
)


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool
    seerr_user_id: int | None


class LoginResponse(BaseModel):
    user: UserResponse


@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    payload: LoginRequest,
    response: Response,
) -> LoginResponse:
    async with async_session() as session:
        result = await session.execute(
            select(ServiceConfig).limit(1)
        )

        config = result.scalar_one_or_none()

        if config is None:
            raise HTTPException(
                status_code=500,
                detail="Progressarr configuration has not been initialized.",
            )

        jellyfin_client = create_jellyfin_client(config)
        jellyfin = JellyfinService(jellyfin=jellyfin_client)

        seerr_client = create_seerr_client(config)
        seerr = SeerrService(seerr=seerr_client)

        service = AuthService(
            session,
            jellyfin,
            seerr,
        )

        user = await service.authenticate(
            username=payload.username,
            password=payload.password,
        )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password.",
        )

    token = create_session_token(user.id)

    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.session_expiry_hours * 60 * 60,
    )

    return LoginResponse(
        user=UserResponse(
            id=user.id,
            username=user.username,
            is_admin=user.is_admin,
            seerr_user_id=user.seerr_user_id,
        )
    )


@router.post("/logout")
async def logout(
    response: Response,
) -> dict[str, str]:
    response.delete_cookie(
        key=settings.session_cookie_name,
    )

    return {
        "message": "Logged out successfully.",
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        is_admin=user.is_admin,
        seerr_user_id=user.seerr_user_id,
    )