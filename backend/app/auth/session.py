from itsdangerous import BadSignature, URLSafeSerializer

from app.config import settings


serializer = URLSafeSerializer(
    settings.session_secret,
)


def create_session_token(
    user_id: int,
) -> str:
    return serializer.dumps(
        {
            "user_id": user_id,
        }
    )


def get_user_id_from_token(
    token: str,
) -> int | None:
    try:
        data = serializer.loads(token)
    except BadSignature:
        return None

    user_id = data.get("user_id")

    if not isinstance(user_id, int):
        return None

    return user_id