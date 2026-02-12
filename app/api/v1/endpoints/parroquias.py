from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models.parroquia import Parroquia
from app.models.user import User
from app.schemas.parroquia import (
    ParroquiaCreateRequest,
    ParroquiaDetailResponse,
    ParroquiaListItemResponse,
    ParroquiaUpdateRequest,
)

router = APIRouter(prefix="/parroquias", tags=["parroquias"])


@router.get("", response_model=list[ParroquiaListItemResponse])
def list_parroquias(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=25, ge=1, le=100),
    _: User = Depends(require_roles("admin", "contador")),
    db: Session = Depends(get_db),
) -> list[Parroquia]:
    offset = (page - 1) * size
    stmt = select(Parroquia).order_by(Parroquia.id).offset(offset).limit(size)
    return list(db.scalars(stmt).all())


@router.get("/{parroquia_id}", response_model=ParroquiaDetailResponse)
def get_parroquia_detail(
    parroquia_id: int,
    _: User = Depends(require_roles("admin", "contador")),
    db: Session = Depends(get_db),
) -> Parroquia:
    parroquia = db.scalar(select(Parroquia).where(Parroquia.id == parroquia_id))
    if parroquia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parroquia no encontrada")
    return parroquia


@router.post("", response_model=ParroquiaDetailResponse, status_code=status.HTTP_201_CREATED)
def create_parroquia(
    payload: ParroquiaCreateRequest,
    _: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> Parroquia:
    existing = db.scalar(
        select(Parroquia).where(func.lower(Parroquia.nombre) == payload.nombre.strip().lower())
    )
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una parroquia con ese nombre",
        )

    parroquia = Parroquia(
        nombre=payload.nombre.strip(),
        cuota_mensual=payload.cuota_mensual,
        datos_bancarios=payload.datos_bancarios,
    )
    db.add(parroquia)
    db.commit()
    db.refresh(parroquia)
    return parroquia


@router.patch("/{parroquia_id}", response_model=ParroquiaDetailResponse)
def update_parroquia(
    parroquia_id: int,
    payload: ParroquiaUpdateRequest,
    _: User = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> Parroquia:
    parroquia = db.scalar(select(Parroquia).where(Parroquia.id == parroquia_id))
    if parroquia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parroquia no encontrada")

    update_data = payload.model_dump(exclude_unset=True)
    if "nombre" in update_data and update_data["nombre"] is not None:
        normalized_nombre = update_data["nombre"].strip()
        existing = db.scalar(
            select(Parroquia).where(
                func.lower(Parroquia.nombre) == normalized_nombre.lower(),
                Parroquia.id != parroquia_id,
            )
        )
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una parroquia con ese nombre",
            )
        update_data["nombre"] = normalized_nombre

    for field, value in update_data.items():
        setattr(parroquia, field, value)

    db.add(parroquia)
    db.commit()
    db.refresh(parroquia)
    return parroquia
