from fastapi import APIRouter, Request
from . import templates

router = APIRouter(tags=["auth"])

@router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.jinja", {"request": request})

@router.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.jinja", {"request": request})

@router.get("/forgot-password")
async def forgot_password(request: Request):
    return templates.TemplateResponse("forgot_password.jinja", {"request": request})

@router.get("/reset-password")
async def reset_password(request: Request):
    return templates.TemplateResponse("reset_password.jinja", {"request": request})