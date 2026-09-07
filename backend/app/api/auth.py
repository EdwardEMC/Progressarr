from fastapi import APIRouter, Cookie, HTTPException, Response, status
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.auth.dependencies import get_current_user
from app.auth.session import (
    create_admin_session_token,
    create_user_session_token,
    get_session_data,
)
from app.auth.service import AuthService
from app.config import settings
from app.database import async_session
from app.db_models import ServiceConfig, User
from app.services.client_factory import create_jellyfin_client, create_seerr_client
from app.services.jellyfin_service import JellyfinService
from app.services.local_auth_service import LocalAuthService
from app.services.seerr_service import SeerrService

router = APIRouter(
    prefix="/api/auth",
    tags=["authentication"],
)


class MeResponse(BaseModel):
    auth_type: str
    user: UserResponse | None


class AdminLoginRequest(BaseModel):
    password: str = Field(min_length=1)


class AdminLoginResponse(BaseModel):
    message: str


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
        result = await session.execute(select(ServiceConfig).limit(1))

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

    token = create_user_session_token(user.id)

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
    response_model=MeResponse,
)
async def get_me(
    progressarr_session: str | None = Cookie(
        default=None,
        alias=settings.session_cookie_name,
    ),
) -> MeResponse:
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
        return MeResponse(
            auth_type="local_admin",
            user=None,
        )

    if auth_type == "jellyfin":
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

        return MeResponse(
            auth_type="jellyfin",
            user=UserResponse(
                id=user.id,
                username=user.username,
                is_admin=user.is_admin,
                seerr_user_id=user.seerr_user_id,
            ),
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid session type.",
    )


@router.post(
    "/admin-login",
    response_model=AdminLoginResponse,
)
async def admin_login(
    payload: AdminLoginRequest,
    response: Response,
) -> AdminLoginResponse:
    async with async_session() as session:
        service = LocalAuthService(session)

        authenticated = await service.authenticate(
            password=payload.password,
        )

    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid administrator password.",
        )

    token = create_admin_session_token()

    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.session_expiry_hours * 60 * 60,
    )

    return AdminLoginResponse(
        message="Administrator login successful.",
    )
