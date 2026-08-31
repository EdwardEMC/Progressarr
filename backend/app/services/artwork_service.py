from pathlib import Path

from app.models import Artwork


class ArtworkService:
    def __init__(
        self,
        cache_dir: Path,
    ) -> None:
        self.cache_dir = cache_dir

    def get_artwork(
        self,
        source: str,
        item_id: int,
        images: list[dict],
    ) -> Artwork:
        image_types = {
            image.get("coverType")
            for image in images
        }

        poster_url = None
        backdrop_url = None

        if "poster" in image_types:
            poster_url = (
                f"/api/artwork/"
                f"{source}/poster/{item_id}"
            )

        if "fanart" in image_types:
            backdrop_url = (
                f"/api/artwork/"
                f"{source}/fanart/{item_id}"
            )

        return Artwork(
            poster_url=poster_url,
            backdrop_url=backdrop_url,
        )

    def get_cache_path(
        self,
        source: str,
        item_id: int,
        image_type: str,
    ) -> Path:
        return (
            self.cache_dir
            / source
            / str(item_id)
            / f"{image_type}.jpg"
        )