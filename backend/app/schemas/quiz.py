from pydantic import BaseModel
from typing import Dict


class QuizSubmissionSchema(BaseModel):
    quiz_id: str
    responses: Dict[str, Dict[str, int]]
