from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ParroquiaListItemResponse(BaseModel):
    id: int
    nombre: str
    cuota_mensual: Decimal

    model_config = ConfigDict(from_attributes=True)


class ParroquiaDetailResponse(BaseModel):
    id: int
    nombre: str
    cuota_mensual: Decimal
    datos_bancarios: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ParroquiaCreateRequest(BaseModel):
    nombre: str = Field(min_length=1, max_length=255)
    cuota_mensual: Decimal = Field(ge=0)
    datos_bancarios: str | None = None


class ParroquiaUpdateRequest(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=255)
    cuota_mensual: Decimal | None = Field(default=None, ge=0)
    datos_bancarios: str | None = None
