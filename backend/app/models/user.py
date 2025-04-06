from datetime import datetime
from typing import List

from passlib.context import CryptContext
from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils import generate_uid

from .base import Base, CreatedMixin, LastUpdatedMixin, ModelMixin
from .role import Role

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base, ModelMixin, CreatedMixin, LastUpdatedMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    uid: Mapped[str] = mapped_column(
        String(17), unique=True, index=True, default=generate_uid
    )
    email: Mapped[str] = mapped_column(String(128), unique=True)
    name: Mapped[str] = mapped_column(String(128))
    phone: Mapped[str] = mapped_column(String(16))
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))

    role: Mapped[Role] = relationship("Role", back_populates="users")
    payments: Mapped[list["Payment"]] = relationship(back_populates="user")
    responses: Mapped[list["Response"]] = relationship(back_populates="user")

    @property
    def password(self) -> Exception:
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = password_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return password_context.verify(password, self.password_hash)

    @hybrid_property
    def role_name(self) -> str:
        return self.role.name

    @hybrid_property
    def scopes(self) -> List[str]:
        return [p.name for p in self.role.permissions]


class Payment(Base, ModelMixin, CreatedMixin):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True, index=True
    )
    payment_id: Mapped[int] = mapped_column(String, primary_key=True)
    type: Mapped[str] = mapped_column(String(16), nullable=False)
    data: Mapped[dict] = mapped_column(JSON, nullable=True)
    valid_until: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped[User] = relationship("User", back_populates="payments")
