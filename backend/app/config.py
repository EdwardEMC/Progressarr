from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    radarr_url: str
    radarr_api_key: str

    sonarr_url: str
    sonarr_api_key: str

    seerr_url: str
    seerr_api_key: str

    jellyfin_url: str
    jellyfin_api_key: str

    session_secret: str
    session_cookie_name: str = "progressarr_session"
    session_expiry_hours: int = 24

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        case_sensitive=False,
    )


settings = Settings()