from fastapi import APIRouter

from src.routes.v1.analysis import analysis_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(analysis_router)
