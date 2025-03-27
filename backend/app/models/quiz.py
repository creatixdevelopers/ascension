from typing import Optional

from sqlalchemy import JSON, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils import generate_uid
from .user import User

from .base import Base, CreatedMixin, LastUpdatedMixin, ModelMixin


class Quiz(Base, ModelMixin, CreatedMixin, LastUpdatedMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[str] = mapped_column(
        String(17), unique=True, index=True, default=generate_uid
    )

    responses: Mapped[list["Response"]] = relationship(back_populates="quiz")


class Response(Base, ModelMixin, CreatedMixin, LastUpdatedMixin):
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    data: Mapped[Optional[dict]] = mapped_column(JSON)

    quiz: Mapped[Quiz] = relationship("Quiz", back_populates="responses")
    user: Mapped[User] = relationship("User", back_populates="responses")
