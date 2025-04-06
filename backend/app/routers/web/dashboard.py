from fastapi import APIRouter, Request
from sqlalchemy import and_, or_, select
from starlette.responses import RedirectResponse

from app.models import Payment, Quiz, Response, User
from app.services.auth import web_requires
from app.services.db import dbDep
from app.utils import current_datetime

from . import templates

router = APIRouter(tags=["auth"])

QUIZ_ID = "zWPa15oNvBxkEfulAqRQZOL"


@router.get("/404/")
async def get_404(request: Request):
    return templates.TemplateResponse("404.jinja", {"request": request})


@router.get("/home/")
@web_requires([])
async def get_home(request: Request, db: dbDep):
    # Check if a valid payment exists
    now = current_datetime()
    query = (
        select(Payment)
        .join(Payment.user)
        .where(
            and_(
                User.uid == request.state.sub,
                or_(Payment.valid_until.is_(None), Payment.valid_until > now),
            )
        )
    )
    payment = db.execute(query).scalars().first()
    if payment:
        return RedirectResponse("/quiz/")

    return templates.TemplateResponse("home.jinja", {"request": request})


@router.get("/payment-callback/")
async def get_payment_callback(request: Request, db: dbDep):
    return templates.TemplateResponse("base.jinja", {"request": request})


@router.get("/quiz/")
@web_requires([])
async def get_quiz(request: Request, db: dbDep):
    # Check if the user has already taken the quiz
    query = (
        select(Response)
        .join(Response.quiz)
        .join(Response.user)
        .where(and_(Quiz.uid == QUIZ_ID, User.uid == request.state.sub))
    )
    response = db.execute(query).scalars().first()
    if response:
        return RedirectResponse("/feedback/")
    return templates.TemplateResponse(
        "quiz.jinja", {"request": request, "quiz_id": QUIZ_ID}
    )


@router.get("/feedback/")
@web_requires([])
async def get_feedback(request: Request, db: dbDep):
    quiz = Quiz.uget(db=db, uid=QUIZ_ID)
    user = User.uget(db=db, uid=request.state.sub)
    response = Response.get_by(db=db, first=True, quiz_id=quiz.id, user_id=user.id)
    return templates.TemplateResponse(
        "feedback.jinja",
        {"request": request, "quiz_id": QUIZ_ID, "results": response.data},
    )
