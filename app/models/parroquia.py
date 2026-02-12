from decimal import Decimal

from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Parroquia(Base):
    __tablename__ = "parroquias"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    cuota_mensual: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    datos_bancarios: Mapped[str | None] = mapped_column(Text, nullable=True)
