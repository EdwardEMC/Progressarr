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


def create_session_token(
    user_id: int,
) -> str:
    return get_serializer().dumps(
        {
            "user_id": user_id,
        }
    )


def get_user_id_from_token(
    token: str,
) -> int | None:
    try:
        data = get_serializer().loads(token)
    except BadSignature:
        return None

    user_id = data.get("user_id")

    if not isinstance(user_id, int):
        return None

    return user_id
