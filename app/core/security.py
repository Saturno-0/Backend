from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings
from app.schemas.token import TokenPayload

TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def _create_token(
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    role: str | None = None,
) -> str:
    expire = datetime.now(timezone.utc) + expires_delta

    payload: dict[str, str | int | datetime] = {
        "sub": subject,
        "token_type": token_type,
        "exp": expire,
    }
    if role is not None:
        payload["role"] = role

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(user_id: int, role: str) -> str:
    return _create_token(
        subject=str(user_id),
        token_type=TOKEN_TYPE_ACCESS,
        role=role,
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(user_id: int) -> str:
    return _create_token(
        subject=str(user_id),
        token_type=TOKEN_TYPE_REFRESH,
        expires_delta=timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError as exc:
        raise ValueError("Token invalido o expirado") from exc

    try:
        token_payload = TokenPayload.model_validate(payload)
    except Exception as exc:
        raise ValueError("Payload de token invalido") from exc

    return token_payload


def validate_token_type(payload: TokenPayload, expected_type: str) -> None:
    if payload.token_type != expected_type:
        raise ValueError("Tipo de token invalido")
