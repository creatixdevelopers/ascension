from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from app.config import settings

templates = Jinja2Templates(directory=settings.templates_dir)
web_router = APIRouter()

from .auth import router as auth_router
from .dashboard import router as dashboard_router

for router in [auth_router, dashboard_router]:
    web_router.include_router(router)