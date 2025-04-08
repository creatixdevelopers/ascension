from datetime import datetime

from pydantic import BaseModel
from typing import Dict

from app.schemas.user import UserIdSchema


class QuizSubmissionSchema(BaseModel):
    quiz_id: str
    responses: Dict[str, Dict[str, int]]


class QuizReadSchema(BaseModel):
    uid: str
    name: str
    description: str
    created: datetime
    last_updated: datetime


class ResponseIdSchema(BaseModel):
    uid: str
    user: UserIdSchema
    created: datetime


class ResponseReadSchema(ResponseIdSchema):
    data: dict
