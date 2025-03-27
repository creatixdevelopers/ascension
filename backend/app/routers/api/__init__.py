from fastapi import APIRouter

from .auth import router as auth_router
from .user import router as user_router

api_router = APIRouter(prefix="/api")

for router in [auth_router, user_router]:
    api_router.include_router(router)
