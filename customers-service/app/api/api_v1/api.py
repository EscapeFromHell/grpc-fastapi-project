from app.api.api_v1.endpoints import router
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(router, prefix="/customers", tags=["customers"])
