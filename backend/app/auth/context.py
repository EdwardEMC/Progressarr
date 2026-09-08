from dataclasses import dataclass
from typing import Literal

from app.db_models import User


AuthType = Literal["jellyfin", "local_admin"]

@dataclass
class AuthContext:
    auth_type: AuthType
    user: User | None = None

    @property
    def is_local_admin(self) -> bool:
        return self.auth_type == "local_admin"

    @property
    def is_jellyfin(self) -> bool:
        return self.auth_type == "jellyfin"

    @property
    def is_admin(self) -> bool:
        if self.is_local_admin:
            return True

        return self.user is not None and self.user.is_admin
