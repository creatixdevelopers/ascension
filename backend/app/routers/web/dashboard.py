from fastapi import APIRouter, Request
from . import templates

router = APIRouter(tags=["auth"])

@router.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.jinja", {"request": request})

@router.get("/quiz")
async def quiz(request: Request):
    return templates.TemplateResponse("quiz.jinja", {"request": request})

@router.get("feedback")
async def feedback(request: Request):
    return templates.TemplateResponse("feedback.jinja", {"request": request})
