from app.clients.radarr import RadarrClient
from app.clients.sonarr import SonarrClient
from app.db_models import ServiceConfig


def create_radarr_client(
    config: ServiceConfig,
) -> RadarrClient:
    if not config.radarr_url:
        raise RuntimeError("Radarr is not configured.")

    if not config.radarr_api_key:
        raise RuntimeError("Radarr API key is not configured.")

    return RadarrClient(
        base_url=config.radarr_url,
        api_key=config.radarr_api_key,
    )


def create_sonarr_client(
    config: ServiceConfig,
) -> SonarrClient:
    if not config.sonarr_url:
        raise RuntimeError("Sonarr is not configured.")

    if not config.sonarr_api_key:
        raise RuntimeError("Sonarr API key is not configured.")

    return SonarrClient(
        base_url=config.sonarr_url,
        api_key=config.sonarr_api_key,
    )
