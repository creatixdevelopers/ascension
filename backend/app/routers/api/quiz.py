from fastapi import APIRouter, Request
from app.models import User, Quiz, Response
from app.services.auth import requires
from app.services.db import dbDep
from app.schemas.quiz import QuizSubmissionSchema, ResponseIdSchema, ResponseReadSchema
from app.schemas.data_table import DataTableSchema, DataTableResponseSchema
from app.services.exceptions import BadRequest, NotFound
from sqlalchemy import select, func, or_
from app.config import settings
import json

router = APIRouter(prefix="/quiz", tags=["quiz"])
QUIZ_ID = settings.QUIZ_ID


@router.get("/response/{response_id}/")
@requires(["response.read"])
async def get_quiz_response(request: Request, response_id: str, db: dbDep):
    response = Response.uget(db, uid=response_id)
    if response:
        questions_path = str(settings._static_dir / "data" / QUIZ_ID / "questions.json")
        with open(questions_path, "r", encoding="utf-8") as f:
            questions = json.load(f)

        res = {}
        for pillar, pillar_data in questions.items():
            res[pillar] = []
            for i, question in enumerate(pillar_data.get("questions", [])):
                res[pillar].append(
                    {
                        "question": question.get("en"),
                        "response": response.data.get(pillar, {}).get(str(i), 0),
                    }
                )

        return ResponseReadSchema(
            uid=response.uid, user=response.user, created=response.created, data=res
        )
    raise NotFound


@router.put("/response/")
@requires(["response.create"])
async def put_quiz_response(request: Request, data: QuizSubmissionSchema, db: dbDep):
    quiz = Quiz.uget(db, uid=data.quiz_id)
    user = User.uget(db, uid=request.state.sub)
    if quiz and user:
        Response.create(
            db,
            quiz_id=quiz.id,
            user_id=user.id,
            data=data.responses,
        )
        db.commit()
        return {"message": "Submission successful"}
    raise BadRequest


@router.post(
    "/response/data-table/",
    response_model=DataTableResponseSchema[ResponseIdSchema],
)
@requires(["response.read.all"])
async def _datatable(request: Request, data: DataTableSchema, db: dbDep):
    query = (
        select(Response)
        .join(Response.user)
        .join(Response.quiz)
        .where(Quiz.uid == QUIZ_ID)
    )
    total = db.execute(select(func.count()).select_from(query.subquery())).scalar_one()

    if data.search:
        query = query.filter(
            or_(
                User.name.like(f"%{data.search}%"),
                User.email.like(f"%{data.search}%"),
            )
        )

    column_mapper = {
        "name": User.name,
        "email": User.email,
        "created": User.created,
    }
    order_by = []
    for order_data in data.order:
        if column := column_mapper.get(order_data["id"]):
            order_by.append(column.desc() if order_data["desc"] else column)
    query = query.order_by(*order_by) if order_by else query.order_by(User.id.desc())

    results: list[User] = (
        db.execute(query.offset(data.skip).limit(data.limit)).scalars().all()
    )
    res = [
        ResponseIdSchema.model_validate(result, from_attributes=True)
        for result in results
    ]
    return DataTableResponseSchema[ResponseIdSchema](
        data=res,
        filtered=len(results),
        total=total,
    )
