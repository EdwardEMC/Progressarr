from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ServiceConfig(Base):
    __tablename__ = "service_config"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    radarr_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    radarr_api_key: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    sonarr_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    sonarr_api_key: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    jellyfin_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    jellyfin_api_key: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    is_admin: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
