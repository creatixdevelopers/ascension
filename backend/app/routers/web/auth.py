from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from . import templates
from app.services.auth import web_requires

router = APIRouter(tags=["auth"])


@router.get("/login")
@web_requires([], optional=True)
async def login(request: Request):
    if getattr(request.state, "sub", None):
        return RedirectResponse("/home")
    return templates.TemplateResponse("login.jinja", {"request": request})


@router.get("/signup")
@web_requires([], optional=True)
async def signup(request: Request):
    if getattr(request.state, "sub", None):
        return RedirectResponse("/home")
    return templates.TemplateResponse("signup.jinja", {"request": request})


@router.get("/forgot-password")
@web_requires([], optional=True)
async def forgot_password(request: Request):
    if getattr(request.state, "sub", None):
        return RedirectResponse("/home")
    return templates.TemplateResponse("forgot_password.jinja", {"request": request})


@router.get("/reset-password")
@web_requires([], optional=True)
async def reset_password(request: Request):
    if getattr(request.state, "sub", None):
        return RedirectResponse("/home")
    return templates.TemplateResponse("reset_password.jinja", {"request": request})
