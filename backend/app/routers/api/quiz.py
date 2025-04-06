from fastapi import APIRouter, Request
from app.models import User, Quiz, Response
from app.services.auth import requires
from app.services.db import dbDep
from app.schemas.quiz import QuizSubmissionSchema
from app.services.exceptions import BadRequest

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.put("/response")
@requires(["response.create"])
async def put_quiz_response(request: Request, data: QuizSubmissionSchema, db: dbDep):
    quiz = Quiz.uget(db, uid=data.quiz_id)
    user = User.uget(db, uid=request.state.sub)
    if quiz and user:
        existing_response = Response.get_by(
            db, first=True, quiz_id=quiz.id, user_id=user.id
        )
        if existing_response:
            existing_response.delete()
        Response.create(
            db,
            quiz_id=quiz.id,
            user_id=user.id,
            data=data.responses,
        )
        db.commit()
        return {"message": "Submission successful"}
    raise BadRequest
