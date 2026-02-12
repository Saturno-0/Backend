from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Importa modelos para que SQLAlchemy registre metadata.
from app.models.parroquia import Parroquia  # noqa: E402,F401
from app.models.user import User  # noqa: E402,F401
