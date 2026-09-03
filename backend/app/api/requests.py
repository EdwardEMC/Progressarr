from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.auth.dependencies import get_current_user
from app.config import settings
from app.database import async_session
from app.db_models import ServiceConfig, User
from app.services.client_factory import create_seerr_client
from app.services.seerr_service import SeerrService
from app.services.request_service import RequestService


router = APIRouter(
    prefix="/api/requests",
    tags=["requests"],
)


@router.get("")
async def get_requests(
    user: User = Depends(get_current_user),
) -> list[dict]:
    if user.seerr_user_id is None:
        return []

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

        seerr_client = create_seerr_client(config)
        seerr = SeerrService(seerr=seerr_client)
        service = RequestService(seerr=seerr)

        return await service.get_user_requests(
            seerr_user_id=user.seerr_user_id
        )