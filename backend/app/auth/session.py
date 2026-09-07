from itsdangerous import BadSignature, URLSafeSerializer

_serializer: URLSafeSerializer | None = None


def initialize_session_serializer(
    session_secret: str,
) -> None:
    global _serializer

    _serializer = URLSafeSerializer(
        session_secret,
    )


def get_serializer() -> URLSafeSerializer:
    if _serializer is None:
        raise RuntimeError(
            "Session serializer has not been initialized.",
        )

    return _serializer


def create_user_session_token(
    user_id: int,
) -> str:
    return get_serializer().dumps(
        {
            "auth_type": "jellyfin",
            "user_id": user_id,
        }
    )


def create_admin_session_token() -> str:
    return get_serializer().dumps(
        {
            "auth_type": "local_admin",
        }
    )


def get_session_data(
    token: str,
) -> dict[str, object] | None:
    try:
        data = get_serializer().loads(token)
    except BadSignature:
        return None

    if not isinstance(data, dict):
        return None

    return data
