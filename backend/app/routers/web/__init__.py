from fastapi import APIRouter
from .auth import router as auth_router
from .dashboard import router as dashboard_router


web_router = APIRouter()

for router in [auth_router, dashboard_router]:
    web_router.include_router(router)
