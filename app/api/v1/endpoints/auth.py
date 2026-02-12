from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH,
    create_access_token,
    create_refresh_token,
    decode_token,
    validate_token_type,
    verify_password,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import LoginResponse, RefreshResponse
from app.schemas.user import UserLoginRequest, UserMeResponse

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


def _unauthorized(detail: str = "Credenciales invalidas") -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def _get_bearer_token(credentials: HTTPAuthorizationCredentials | None) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized("Token no proporcionado o invalido")
    return credentials.credentials


def _get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.scalar(select(User).where(User.id == user_id))


@router.post("/login", response_model=LoginResponse)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    user = db.scalar(select(User).where(User.username == payload.username))

    if user is None:
        raise _unauthorized("Usuario o contrasena incorrectos")

    if not verify_password(payload.password, user.password_hash):
        raise _unauthorized("Usuario o contrasena incorrectos")

    access_token = create_access_token(user_id=user.id, role=user.role)
    refresh_token = create_refresh_token(user_id=user.id)

    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=RefreshResponse)
def refresh_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> RefreshResponse:
    token = _get_bearer_token(credentials)

    try:
        token_payload = decode_token(token)
        validate_token_type(token_payload, TOKEN_TYPE_REFRESH)
        user_id = int(token_payload.sub)
    except (ValueError, TypeError):
        raise _unauthorized("Refresh token invalido o expirado")

    user = _get_user_by_id(db, user_id)
    if user is None:
        raise _unauthorized("Refresh token invalido o expirado")

    access_token = create_access_token(user_id=user.id, role=user.role)
    return RefreshResponse(access_token=access_token)


@router.get("/me", response_model=UserMeResponse)
def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> UserMeResponse:
    token = _get_bearer_token(credentials)

    try:
        token_payload = decode_token(token)
        validate_token_type(token_payload, TOKEN_TYPE_ACCESS)
        user_id = int(token_payload.sub)
    except (ValueError, TypeError):
        raise _unauthorized("Access token invalido o expirado")

    user = _get_user_by_id(db, user_id)
    if user is None:
        raise _unauthorized("Usuario no encontrado")

    return UserMeResponse.model_validate(user)
