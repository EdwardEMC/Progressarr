from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field

from app.auth.dependencies import get_current_user
from app.auth.service import AuthService
from app.auth.session import create_session_token
from app.config import settings
from app.database import async_session
from app.db_models import User


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
        service = AuthService(session)

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

class SetupRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=8)


@router.post(
    "/setup",
    response_model=UserResponse,
)
async def setup(
    payload: SetupRequest,
) -> UserResponse:
    async with async_session() as session:
        service = AuthService(session)

        if await service.has_users():
            raise HTTPException(
                status_code=409,
                detail="A user already exists.",
            )

        user = await service.create_user(
            username=payload.username,
            password=payload.password,
            is_admin=True,
        )

    return UserResponse(
        id=user.id,
        username=user.username,
        is_admin=user.is_admin,
    )


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
    )