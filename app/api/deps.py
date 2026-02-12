from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import TOKEN_TYPE_ACCESS, decode_token, validate_token_type
from app.db.session import get_db
from app.models.user import User

security = HTTPBearer(auto_error=False)


def _unauthorized(detail: str = "No autenticado") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user_from_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized("Token no proporcionado o invalido")

    try:
        token_payload = decode_token(credentials.credentials)
        validate_token_type(token_payload, TOKEN_TYPE_ACCESS)
        user_id = int(token_payload.sub)
    except (ValueError, TypeError):
        raise _unauthorized("Access token invalido o expirado")

    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise _unauthorized("Usuario no encontrado")

    return user


def require_roles(*allowed_roles: str) -> Callable[[User], User]:
    allowed_set = set(allowed_roles)

    def role_dependency(current_user: User = Depends(get_current_user_from_access_token)) -> User:
        if current_user.role not in allowed_set:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para esta accion",
            )
        return current_user

    return role_dependency
