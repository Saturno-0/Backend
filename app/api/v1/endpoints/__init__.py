from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.parroquias import router as parroquias_router

__all__ = ["auth_router", "parroquias_router"]
