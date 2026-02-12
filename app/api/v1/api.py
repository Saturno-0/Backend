from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.parroquias import router as parroquias_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(parroquias_router)
