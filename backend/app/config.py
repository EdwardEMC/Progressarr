from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    radarr_url: str | None = None
    radarr_api_key: str | None = None

    sonarr_url: str | None = None
    sonarr_api_key: str | None = None

    seerr_url: str | None = None
    seerr_api_key: str | None = None

    jellyfin_url: str | None = None
    jellyfin_api_key: str | None = None

    session_secret: str | None = None
    session_cookie_name: str = "progressarr_session"
    session_expiry_hours: int = 24

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
    )


settings = Settings()
