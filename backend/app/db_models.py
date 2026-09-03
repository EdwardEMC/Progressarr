from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AppConfig(Base):
    __tablename__ = "app_config"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    session_secret: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )


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

    seerr_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    seerr_api_key: Mapped[str | None] = mapped_column(
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

    jellyfin_user_id: Mapped[str | None] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )

    seerr_user_id: Mapped[int | None] = mapped_column(
        nullable=True,
        unique=True,
        index=True,
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
